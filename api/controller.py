import sys
from flask import abort
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


def get_current_moisture():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT ts, soil_moisture
            FROM `plant_sensor`
            ORDER BY ts DESC
            LIMIT 1;
        """)

        result = cs.fetchone()
    return models.RealTimeMoisture(*result)
    