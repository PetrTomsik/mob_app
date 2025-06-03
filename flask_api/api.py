from datetime import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import DB_CONFIG

app = Flask(__name__)
CORS(app)


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


# --- WORKERS ---
@app.route("/workers", methods=["GET"])
def get_workers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, date_of_birth, address FROM workers")
    data = [{"id": row[0], "name": row[1], "date_of_birth": row[2], "address": row[3]} for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(data)


@app.route("/workers", methods=["POST"])
def add_worker():
    data = request.json
    name = data.get("name")
    date_of_birth = data.get("date_of_birth")
    address = data.get("address")

    if not name or not date_of_birth or not address:
        return jsonify({"error": "Neplatná data"}), 400

    try:
        # Ověříme, že datum je ve formátu YYYY-MM-DD
        datetime.strptime(date_of_birth, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Neplatný formát data. Očekává se YYYY-MM-DD"}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO workers (name, date_of_birth, address) VALUES (%s, %s, %s)",
        (name, date_of_birth, address)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"status": "Pracovník uložen"}), 201


# --- TASKS ---
@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, image_path, datum FROM tasks")
    tasks = cursor.fetchall()

    result = []
    for task in tasks:
        task_id, title, desc, img, datum = task

        # najdeme přiřazené pracovníky
        cursor.execute("""
            SELECT w.name FROM workers w
            JOIN task_workers tw ON w.id = tw.worker_id
            WHERE tw.task_id = %s
        """, (task_id,))
        workers = [row[0] for row in cursor.fetchall()]

        result.append({
            "id": task_id,
            "title": title,
            "description": desc,
            "image_path": img,
            "datum": datum.strftime("%Y-%m-%d %H:%M"),
            "workers": workers
        })

    cursor.close()
    conn.close()
    return jsonify(result)


@app.route("/firms", methods=["GET"])
def get_firms():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nazev FROM firms")
    firms = [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(firms)


@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.json
    title = data.get("title")
    description = data.get("description")
    image_path = data.get("image_path")
    worker_ids = data.get("worker_ids", [])
    start_work = data.get("start_work")
    end_work = data.get("end_work")
    firm_id = data.get("firm_id")

    if not title or not description or not image_path or not isinstance(worker_ids, list):
        return jsonify({"error": "Neplatná data"}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
          INSERT INTO tasks (title, description, image_path,start_work,end_work,firm_id)
          VALUES (%s, %s, %s, %s, %s, %s)
      """, (title, description, image_path, start_work, end_work, firm_id))
    task_id = cursor.lastrowid

    for wid in worker_ids:
        cursor.execute("INSERT INTO task_workers (task_id, worker_id) VALUES (%s, %s)", (task_id, wid))

    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"status": "Úkol uložen"}), 201


@app.route("/workers/<int:worker_id>", methods=["DELETE"])
def delete_worker(worker_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Nejprve smažeme vazby ze spojovací tabulky
        cursor.execute("DELETE FROM task_workers WHERE worker_id = %s", (worker_id,))

        # Poté smažeme pracovníka
        cursor.execute("DELETE FROM workers WHERE id = %s", (worker_id,))

        conn.commit()
        return jsonify({"status": "Pracovník smazán"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
