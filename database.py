# database.py
import mysql.connector
from config import DB_CONFIG

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def create_task(title, description, image_path):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, description, image_path) VALUES (%s, %s, %s)",
        (title, description, image_path)
    )
    conn.commit()
    conn.close()