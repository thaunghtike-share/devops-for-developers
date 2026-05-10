from flask import Flask, jsonify
from flask_cors import CORS
import os
import socket
import time

import mysql.connector
import redis

app = Flask(__name__)
CORS(app)

APP_NAME = os.getenv("APP_NAME", "Docker Compose Demo")

DB_HOST = os.getenv("DB_HOST", "mysql")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "compose_demo")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "apppassword")

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))


def get_mysql_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


def wait_for_mysql():
    for _ in range(20):
        try:
            conn = get_mysql_connection()
            conn.close()
            return True
        except Exception:
            time.sleep(2)
    return False


@app.route("/")
def home():
    return jsonify({
        "message": "Hello from Flask Backend API",
        "app_name": APP_NAME,
        "hostname": socket.gethostname()
    })


@app.route("/health")
def health():
    mysql_status = "connected" if wait_for_mysql() else "not ready"

    try:
        redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        redis_client.ping()
        redis_status = "connected"
    except Exception:
        redis_status = "not ready"

    return jsonify({
        "status": "healthy",
        "service": "backend",
        "mysql": mysql_status,
        "redis": redis_status,
        "database_host": DB_HOST,
        "database_name": DB_NAME,
        "redis_host": REDIS_HOST
    })


@app.route("/visits")
def visits():
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("INSERT INTO visits (message) VALUES (%s)", ("Visit from Flask API",))
    conn.commit()

    cursor.execute("SELECT id, message, created_at FROM visits ORDER BY id DESC LIMIT 5")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    total_visits = redis_client.incr("total_visits")

    return jsonify({
        "app_name": APP_NAME,
        "total_visits_from_redis": total_visits,
        "latest_rows_from_mysql": rows
    })


if __name__ == "__main__":
    wait_for_mysql()
    app.run(host="0.0.0.0", port=5000)
