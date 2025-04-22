import math
import sys
from datetime import datetime

import pandas as pd
import pymysql
from config import (
    DB_HOST,
    DB_NAME,
    DB_PASSWD,
    DB_USER,
    OPENAPI_STUB_DIR,
    PLANT_SENSOR_TABLE,
    WEATHER_TABLE,
)
from dbutils.pooled_db import PooledDB
from flask import abort, request
from model_manager import ModelBuilder, ModelManager

sys.path.append(OPENAPI_STUB_DIR)
from swagger_server import models

pool = PooledDB(
    creator=pymysql,
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWD,
    database=DB_NAME,
    maxconnections=1,
    blocking=True,
)


def get_latest_sensor_data():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute(f"""
            SELECT `ts`, `light`, `temperature`, `soil_moisture`
            FROM `{PLANT_SENSOR_TABLE}`
            ORDER BY ts DESC
            LIMIT 1;
        """)

        result = cs.fetchone()
    return models.SensorData(*result)


def aggregate_sensor_data():
    try:
        days = int(request.args.get("days", 3))
        hours = int(request.args.get("hours", 3))
    except ValueError:
        abort(400, description="'days' and 'hours' must be integers.")
    if hours < 1:
        abort(400, description="Parameter 'hours' must be positive value.")
    if (24 % hours) != 0:
        abort(
            400,
            description="Parameter 'hours' must be positive factors of 24 (24 %\ hours == 0).",
        )
    if days < 1:
        abort(400, description="'days' must a postive integer.")
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute(f"""
            SELECT
            DATE_ADD(DATE(`ts`), INTERVAL FLOOR(HOUR(`ts`)/{hours}) * {hours} HOUR) AS ts,
            AVG(light),
            AVG(temperature),
            AVG(soil_moisture)
            FROM `{PLANT_SENSOR_TABLE}`
            WHERE `ts` > (
                SELECT MAX(`ts`) - INTERVAL {days} DAY FROM `{PLANT_SENSOR_TABLE}`
            )
            GROUP BY DATE_ADD(DATE(`ts`), INTERVAL FLOOR(HOUR(`ts`)/{hours}) * {hours} HOUR);     
        """)
        result = [
            models.SensorData(read_time, light, temperature, soil_moisture)
            for read_time, light, temperature, soil_moisture in cs.fetchall()
        ]
    return result


def get_latest_weather_data():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute(f"""
            SELECT `ts`, `humidity`,`precipitation`, `temperature`, `cloud_cover`
            FROM `{WEATHER_TABLE}`
            ORDER BY `ts` DESC
            LIMIT 1;
        """)
        result = cs.fetchone()
    return models.WeatherData(*result)


def aggregate_weather_data():
    try:
        days = int(request.args.get("days", 3))
        hours = int(request.args.get("hours", 3))
    except ValueError:
        abort(400, description="'days' and 'hours' must be integers.")
    if hours < 1:
        abort(400, description="Parameter 'hours' must be positive value.")
    if (24 % hours) != 0:
        abort(
            400,
            description="Parameter 'hours' must be positive factors of 24 (24 %\ hours == 0).",
        )
    if days < 1:
        abort(400, description="'days' must a postive integer.")

    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute(f"""
            SELECT
            DATE_ADD(DATE(`ts`), INTERVAL FLOOR(HOUR(`ts`)/{hours}) * {hours} HOUR) AS ts,
            AVG(humidity),
            AVG(precipitation),
            AVG(temperature),
            AVG(cloud_cover)
            FROM `{WEATHER_TABLE}`
            WHERE `ts` > (
                SELECT MAX(`ts`) - INTERVAL {days} DAY FROM `{WEATHER_TABLE}`
            )
            GROUP BY DATE_ADD(DATE(`ts`), INTERVAL FLOOR(HOUR(`ts`)/{hours}) * {hours} HOUR);     
        """)
        result = [models.WeatherData(*data) for data in cs.fetchall()]
    return result


def moisture_prediction(moisture):
    if not ModelManager.get_model():
        df = get_moisture_df()
        builder = ModelBuilder()
        builder.add_basic_init(df, "soil_moisture", (2, 0, 1), pd.Timedelta(minutes=15))

        builder.add_exog("temperature", (2, 0, 1), (1, 0, 1, 24)).add_exog(
            "humidity", (2, 0, 1), (1, 0, 1, 24)
        ).build()

    model = ModelManager.get_model()
    latest_time = model.df.index.max()
    number_of_15_min_intervals = math.ceil(
        (((datetime.now() - latest_time).total_seconds() / 60) + (7 * 24 * 60)) / 15
    )

    try:
        prediction, upper, lower = model.fit_model().get_prediction(
            number_of_15_min_intervals
        )
    except ValueError:
        model.main_data = get_moisture_df()
        prediction, upper, lower = model.fit_model().get_prediction(
            number_of_15_min_intervals
        )

    old_data = [
        models.SoilMoisture(index, row["soil_moisture"])
        for index, row in model.df.iterrows()
    ]
    pred_transformed = [
        models.SoilMoisture(ts, value) for ts, value in prediction.items()
    ]
    upper_transformed = [models.SoilMoisture(ts, value) for ts, value in upper.items()]
    lower_transformed = [models.SoilMoisture(ts, value) for ts, value in lower.items()]

    duration = model.get_duration(moisture)
    return models.PredictMoisture(
        duration, old_data, pred_transformed, upper_transformed, lower_transformed
    )


def get_moisture_df():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute(f"""WITH tempTable AS (
                SELECT
                    DATE_ADD(DATE(`ts`), INTERVAL FLOOR(TIME_TO_SEC(TIME(`ts`)) / (15 * 60)) * 15 * 60 SECOND) AS `ts`,
                    AVG(`light`) AS `avg_light`,
                    AVG(`temperature`) AS `avg_temperature`,
                    AVG(`soil_moisture`) AS `avg_soil_moisture`
                FROM `{PLANT_SENSOR_TABLE}`
                GROUP BY DATE_ADD(DATE(`ts`), INTERVAL FLOOR(TIME_TO_SEC(TIME(`ts`)) / (15 * 60)) * 15 * 60 SECOND)
            )

            SELECT 
                t.ts,
                t.avg_light AS light,
                t.avg_temperature AS temperature,
                t.avg_soil_moisture AS soil_moisture,
                w.humidity AS humidity,
                w.temperature AS api_temp,
                w.precipitation,
                w.cloud_cover
            FROM tempTable t
            INNER JOIN `{WEATHER_TABLE}` w ON t.ts = w.ts;
        """)
        columns = [col[0] for col in cs.description]

        data = cs.fetchall()

    df = pd.DataFrame(data, columns=columns)
    df["ts"] = pd.to_datetime(df["ts"])
    df.set_index("ts", inplace=True)
    return df
