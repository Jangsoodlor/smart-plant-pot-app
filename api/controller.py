import sys
from flask import abort, request
import pymysql
from dbutils.pooled_db import PooledDB
from config import OPENAPI_STUB_DIR, DB_HOST, DB_USER, DB_PASSWD, DB_NAME

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
        cs.execute("""
            SELECT `ts`, `light`, `temperature`, `soil_moisture`
            FROM `plant_sensor`
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
    if (24 % hours) != 0 or hours < 1:
        abort(400, description="Parameter 'hrs' must be positive factors of 24.")
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute(f"""
            SELECT
            DATE_ADD(DATE(`ts`), INTERVAL FLOOR(HOUR(`ts`)/{hours}) * {hours} HOUR) AS ts,
            AVG(light),
            AVG(temperature),
            AVG(soil_moisture)
            FROM plant_sensor
            WHERE `ts` >= NOW() - INTERVAL {days} DAY
            GROUP BY DATE_ADD(DATE(`ts`), INTERVAL FLOOR(HOUR(`ts`)/{hours}) * {hours} HOUR);     
        """)
        result = [models.SensorData(*data) for data in cs.fetchall()]
    return result


def get_latest_weather_data():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT `ts`, `humidity`,`precipitation`, `temperature`, `cloud_cover`
            FROM `open-meteo`
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
    if (24 % hours) != 0 or hours < 1:
        abort(400, description="Parameter 'hrs' must be positive factors of 24.")
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute(f"""
            SELECT
            DATE_ADD(DATE(`ts`), INTERVAL FLOOR(HOUR(`ts`)/{hours}) * {hours} HOUR) AS ts,
            AVG(humidity),
            AVG(precipitation),
            AVG(temperature),
            AVG(cloud_cover)
            FROM `open-meteo`
            WHERE `ts` >= NOW() - INTERVAL {days} DAY
            GROUP BY DATE_ADD(DATE(`ts`), INTERVAL FLOOR(HOUR(`ts`)/{hours}) * {hours} HOUR);     
        """)
        result = [models.WeatherData(*data) for data in cs.fetchall()]
    return result
