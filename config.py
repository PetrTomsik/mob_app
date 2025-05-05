from pathlib import Path

# Získání cesty ke složce, kde se nachází tento skript
BASE_DIR = Path(__file__).resolve().parent

# Vytvoření cesty k souboru heslo.txt
heslo_path = BASE_DIR / "heslo.txt"

with open(heslo_path, "r") as file:
    password = file.read()

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': password,
    'database': 'projekt_prace',
    'use_pure': True
}