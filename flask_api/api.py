from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "tvoje_heslo",
    "database": "Projeckt_prace"
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


# --- WORKERS ---
@app.route("/workers", methods=["GET"])
def get_workers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, vek FROM workers")
    data = [{"id": row[0], "name": row[1], "vek": row[2]} for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(data)


@app.route("/workers", methods=["POST"])
def add_worker():
    data = request.json
    name = data.get("name")
    vek = data.get("vek")

    if not name or not isinstance(vek, int):
        return jsonify({"error": "Neplatná data"}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO workers (name, vek) VALUES (%s, %s)", (name, vek))
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


@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.json
    title = data.get("title")
    description = data.get("description")
    image_path = data.get("image_path")
    worker_ids = data.get("worker_ids", [])

    if not title or not description or not image_path or not isinstance(worker_ids, list):
        return jsonify({"error": "Neplatná data"}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tasks (title, description, image_path)
        VALUES (%s, %s, %s)
    """, (title, description, image_path))
    task_id = cursor.lastrowid

    for wid in worker_ids:
        cursor.execute("INSERT INTO task_workers (task_id, worker_id) VALUES (%s, %s)", (task_id, wid))

    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"status": "Úkol uložen"}), 201


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
