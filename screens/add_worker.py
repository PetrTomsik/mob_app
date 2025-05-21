from kivy.uix.screenmanager import Screen
import mysql.connector
from config import DB_CONFIG


class AddWorkerScreen(Screen):
    def save_worker(self):
        name = self.ids.new_worker_name.text
        age = self.ids.new_worker_age.text

        if name.strip() and age.isdigit():
            try:
                conn = mysql.connector.connect(**DB_CONFIG)
                cursor = conn.cursor()
                cursor.execute("INSERT INTO workers (name, vek) VALUES (%s, %s)", (name, int(age)))
                conn.commit()
                cursor.close()
                conn.close()
                print(f"✅ Pracovník '{name}' uložen.")
            except mysql.connector.Error as err:
                print(f"❌ Chyba při ukládání pracovníka: {err}")

        # přepnout zpět a aktualizovat jména
        self.ids.new_worker_name.text = ""
        self.ids.new_worker_age.text = ""
        self.manager.current = "main"

        # najdeme MainLayout a zavoláme jeho refresh
        main_screen = self.manager.get_screen("main")
        main_layout = main_screen.children[0]  # protože MainLayout je přímé dítě MainScreen
        main_layout.refresh_worker_checkboxes()

