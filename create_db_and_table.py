# import mysql.connector
#
# from config import DB_CONFIG
#
#
# def get_connection():
#     return mysql.connector.connect(**DB_CONFIG)
#
#
# conn = get_connection()
# cursor = conn.cursor()
#
# # Vytvoření databáze
# cursor.execute("CREATE DATABASE projekt_prace")
#
# # Použití nové databáze
# cursor.execute("USE projekt_prace")
#
# # Vytvoření tabulky
# cursor.execute("""
#     CREATE TABLE tasks (
#         id INT AUTO_INCREMENT PRIMARY KEY,
#         title VARCHAR(255),
#         description TEXT,
#         image_path VARCHAR(255)
#     )
# """)
#
# conn.commit()
# conn.close()