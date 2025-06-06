import mysql.connector
from config import DB_CONFIG


def create_database():
    conn = mysql.connector.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        use_pure=DB_CONFIG['use_pure']
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS Projeckt_prace")
    cursor.close()
    conn.close()



def create_table():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(255),
                    description TEXT,
                    image_path VARCHAR(255),
                    assigned_to INT,
                    FOREIGN KEY (assigned_to) REFERENCES workers(id)
                        ON DELETE SET NULL
                        ON UPDATE CASCADE
                )
            """)
    cursor.close()
    conn.close()


def create_workers_table():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS workers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255)
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    create_database()
    # create_table()
    # create_workers_table()
