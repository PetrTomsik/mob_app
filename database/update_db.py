import mysql.connector
from config import DB_CONFIG


def alter_tasks_table():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # přidej sloupec assigned_to pokud neexistuje
        cursor.execute("""
            ALTER TABLE tasks
            ADD COLUMN assigned_to INT DEFAULT NULL
        """)

        # přidej cizí klíč
        cursor.execute("""
            ALTER TABLE tasks
            ADD CONSTRAINT fk_assigned_to
            FOREIGN KEY (assigned_to) REFERENCES workers(id)
            ON DELETE SET NULL
            ON UPDATE CASCADE
        """)

        conn.commit()
        cursor.close()
        conn.close()
        print("Tabulka tasks byla aktualizována.")
    except mysql.connector.Error as err:
        print(f"Chyba při aktualizaci tabulky: {err}")


#

def alter_tasks_set_not_null():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Získání prvního dostupného ID pracovníka
        cursor.execute("SELECT id FROM workers LIMIT 1;")
        result = cursor.fetchone()
        if not result:
            print("❌ V tabulce 'workers' není žádný záznam. Přidej aspoň jednoho pracovníka.")
            return
        default_worker_id = result[0]

        # Oprava NULL hodnot
        print("🛠️ Opravujeme NULL hodnoty...")
        cursor.execute("UPDATE tasks SET title = '' WHERE title IS NULL;")
        cursor.execute("UPDATE tasks SET description = '' WHERE description IS NULL;")
        cursor.execute("UPDATE tasks SET image_path = '' WHERE image_path IS NULL;")
        cursor.execute("UPDATE tasks SET assigned_to = %s WHERE assigned_to IS NULL;", (default_worker_id,))

        # Změna schématu tabulky na NOT NULL
        print("🔧 Provádíme ALTER TABLE...")
        cursor.execute("ALTER TABLE tasks MODIFY COLUMN title VARCHAR(255) NOT NULL;")
        cursor.execute("ALTER TABLE tasks MODIFY COLUMN description TEXT NOT NULL;")
        cursor.execute("ALTER TABLE tasks MODIFY COLUMN image_path VARCHAR(255) NOT NULL;")
        cursor.execute("ALTER TABLE tasks MODIFY COLUMN assigned_to INT NOT NULL;")

        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Tabulka 'tasks' byla úspěšně upravena na NOT NULL.")

    except mysql.connector.Error as err:
        print(f"❌ Chyba při aktualizaci tabulky: {err}")


def insert_default_workers():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        workers = ['Petr', 'Matěj', 'Taťka', 'Ondra']
        for name in workers:
            cursor.execute("INSERT INTO workers (name) VALUES (%s)", (name,))

        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Výchozí pracovníci byli vloženi do tabulky 'workers'.")

    except mysql.connector.Error as err:
        print(f"❌ Chyba při vkládání pracovníků: {err}")


def assign_all_tasks_to_petr():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Zjisti ID pracovníka s názvem "Petr"
        cursor.execute("SELECT id FROM workers WHERE name = %s", ("Petr",))
        result = cursor.fetchone()

        if not result:
            print("❌ Pracovník 'Petr' nebyl nalezen.")
            return

        petr_id = result[0]

        # Nastav všechny úkoly na tohoto pracovníka
        cursor.execute("UPDATE tasks SET assigned_to = %s", (petr_id,))
        conn.commit()

        cursor.close()
        conn.close()
        print("✅ Všechny úkoly byly přiřazeny Petrovi.")

    except mysql.connector.Error as err:
        print(f"❌ Chyba při přiřazování: {err}")


def delete_workers_by_id_range(start_id=5, end_id=12):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM workers WHERE id BETWEEN %s AND %s", (start_id, end_id))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"✅ Pracovníci s ID od {start_id} do {end_id} byli odstraněni.")
    except mysql.connector.Error as err:
        print(f"❌ Chyba při mazání pracovníků: {err}")


def alter_tables_add_datum_and_vek():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Přidání sloupce 'datum' do tabulky tasks
        try:
            cursor.execute("""
                ALTER TABLE tasks
                ADD COLUMN datum DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            """)
            print("✅ Sloupec 'datum' přidán do 'tasks'.")
        except mysql.connector.Error as e:
            print("ℹ️ Sloupec 'datum' už pravděpodobně existuje:", e)

        # Přidání sloupce 'vek' do tabulky workers
        try:
            cursor.execute("""
                ALTER TABLE workers
                ADD COLUMN vek INT
            """)
            print("✅ Sloupec 'vek' přidán do 'workers'.")
        except mysql.connector.Error as e:
            print("ℹ️ Sloupec 'vek' už pravděpodobně existuje:", e)

        conn.commit()
        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"❌ Chyba při ALTER TABLE: {err}")



if __name__ == "__main__":
    alter_tables_add_datum_and_vek()
    # delete_workers_by_id_range()
    # insert_default_workers()
    # assign_all_tasks_to_petr()
    # alter_tasks_set_not_null()
    # alter_tasks_table()
