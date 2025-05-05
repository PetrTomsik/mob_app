projekt/\
│\
├── main.py               # Startovací skript aplikace\
├── models.py             # Datové modely a připojení k MySQL\
├── ui.kv                 # UI rozhraní v Kivy Language\
├── config.py             # Konfigurace DB (host, user, heslo)\
├── database/\
│   └── init.sql          # SQL skript na vytvoření tabulek\
├── images/\
│   └── ...               # Uložené obrázky (lokálně)\
└── utils/\
│   └── image_utils.py    # Práce s obrázky (např. zmenšení, validace)


main.py	Spouští GUI a propojuje části projektu\
models.py	Připojení k databázi, CRUD operace\
ui.kv	Vzhled aplikace v Kivy jazyce (odděleně od logiky)\
config.py	Přihlašovací údaje a název databáze (lepší než psát do models.py)\
database/init.sql	SQL skript pro vytvoření tabulek v MySQL\
images/	Složka, kam se ukládají obrázky uživatelů\
utils/image_utils.py	Pomocné funkce pro práci s obrázky