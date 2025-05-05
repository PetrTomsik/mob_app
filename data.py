# from pathlib import Path
#
# import mysql.connector
# from mysql.connector import errorcode
#
# # Získání cesty ke složce, kde se nachází tento skript
# BASE_DIR = Path(__file__).resolve().parent
#
# # Vytvoření cesty k souboru heslo.txt
# heslo_path = BASE_DIR / "heslo.txt"
#
# with open(heslo_path, "r") as file:
#     password = file.read()
#
#
# # Připojení k MySQL serveru (bez specifikace databáze)
# try:
#     cnx = mysql.connector.connect(
#         host='localhost',
#         user='root',
#         password= password,
#         use_pure= True
#     )
#     cursor = cnx.cursor()
#     print("✅ Připojení k MySQL serveru bylo úspěšné.")
# except mysql.connector.Error as err:
#     print(f"❌ Chyba při připojení k MySQL serveru: {err}")
#     exit(1)
#
# # Název databáze
# DB_NAME = 'projekt_prace'
#
# # Pokus o vytvoření databáze
# try:
#     cursor.execute(f"CREATE DATABASE {DB_NAME} DEFAULT CHARACTER SET 'utf8mb4'")
#     print(f"✅ Databáze '{DB_NAME}' byla úspěšně vytvořena.")
# except mysql.connector.Error as err:
#     if err.errno == errorcode.ER_DB_CREATE_EXISTS:
#         print(f"ℹ️ Databáze '{DB_NAME}' již existuje.")
#     else:
#         print(f"❌ Chyba při vytváření databáze: {err}")
#         exit(1)
#
# # Připojení k nově vytvořené databázi
# try:
#     cnx.database = DB_NAME
# except mysql.connector.Error as err:
#     print(f"❌ Chyba při připojení k databázi '{DB_NAME}': {err}")
#     exit(1)
#
# # Definice SQL příkazu pro vytvoření tabulky
# TABLES = {}
# TABLES['tasks'] = (
#     "CREATE TABLE IF NOT EXISTS tasks ("
#     "  id INT AUTO_INCREMENT PRIMARY KEY,"
#     "  title VARCHAR(255) NOT NULL,"
#     "  description TEXT,"
#     "  image_path VARCHAR(255)"
#     ") ENGINE=InnoDB"
# )
#
# # Vytvoření tabulky
# for table_name in TABLES:
#     table_description = TABLES[table_name]
#     try:
#         print(f"➡️ Vytváření tabulky '{table_name}'...")
#         cursor.execute(table_description)
#         print(f"✅ Tabulka '{table_name}' byla úspěšně vytvořena.")
#     except mysql.connector.Error as err:
#         print(f"❌ Chyba při vytváření tabulky '{table_name}': {err}")
#         exit(1)
#
# # Uzavření kurzoru a spojení
# cursor.close()
# cnx.close()
# print("🔚 Spojení s MySQL serverem bylo ukončeno.")