from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
import requests

import mysql.connector
from config import DB_CONFIG
from local_ip import get_local_ip


class AddWorkerScreen(Screen):
    def save_worker(self):
        name = self.ids.new_worker_name.text
        age = self.ids.new_worker_age.text

        if name.strip() and age.isdigit():
            try:
                response = requests.post(
                    f"{get_local_ip()}/workers",
                    json={"name": name, "vek": int(age)}
                )
                if response.status_code == 201:
                    self.show_popup("Úspěch", f"Pracovník '{name}' byl uložen.")
                else:
                    self.show_popup("Chyba", f"Chyba API: {response.text}")
            except Exception as e:
                self.show_popup("Chyba", f"Nelze se připojit k API: {e}")
        else:
            self.show_popup("Neplatná data", "Zadej platné jméno a věk.")

        self.ids.new_worker_name.text = ""
        self.ids.new_worker_age.text = ""

    def show_popup(self, title, message):
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        box.add_widget(Label(text=message))
        popup = Popup(title=title, content=box, size_hint=(0.7, 0.3))
        popup.open()
