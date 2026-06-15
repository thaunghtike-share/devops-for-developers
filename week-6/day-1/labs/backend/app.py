import os
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS

load_dotenv("/app/.env")

app = Flask(__name__)
CORS(app)

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "dbname": os.getenv("POSTGRES_DB", "learn_devops"),
    "user": os.getenv("POSTGRES_USER", "learn_user"),
    "password": os.getenv("POSTGRES_PASSWORD", "learn_password"),
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def init_db():
    for _ in range(30):
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS users (
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(100) NOT NULL,
                            email VARCHAR(150) NOT NULL UNIQUE,
                            role VARCHAR(80) DEFAULT 'Student',
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        );
                    """)
                conn.commit()
            return
        except Exception:
            time.sleep(2)


init_db()


@app.get("/api/health")
def health():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
        db_status = "connected"
    except Exception:
        db_status = "disconnected"

    return jsonify({
        "status": "ok",
        "service": "learn-ecs-backend",
        "port": 8000,
        "database": db_status,
        "db_host": DB_CONFIG["host"]
    })


@app.get("/api/users")
def list_users():
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT id, name, email, role, created_at FROM users ORDER BY created_at DESC;"
            )
            users = cur.fetchall()

    return jsonify({"users": users})


@app.get("/api/stats")
def stats():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM users;")
            total_users = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM users WHERE created_at::date = CURRENT_DATE;")
            today_users = cur.fetchone()[0]

            cur.execute("SELECT COUNT(DISTINCT role) FROM users;")
            total_roles = cur.fetchone()[0]

    return jsonify({
        "total_users": total_users,
        "today_users": today_users,
        "total_roles": total_roles
    })


@app.post("/api/register")
def register():
    data = request.get_json(silent=True) or {}

    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    role = (data.get("role") or "Student").strip()

    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400

    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    INSERT INTO users (name, email, role)
                    VALUES (%s, %s, %s)
                    RETURNING id, name, email, role, created_at;
                    """,
                    (name, email, role),
                )
                user = cur.fetchone()
            conn.commit()

        return jsonify({
            "message": "Registration successful",
            "user": user
        }), 201

    except psycopg2.errors.UniqueViolation:
        return jsonify({"error": "This email is already registered"}), 409
    except Exception as e:
        return jsonify({"error": "Registration failed", "details": str(e)}), 500


@app.delete("/api/users/<int:user_id>")
def delete_user(user_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE id = %s RETURNING id;", (user_id,))
            deleted = cur.fetchone()
        conn.commit()

    if not deleted:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": "User deleted successfully"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
