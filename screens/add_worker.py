from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
import requests
from datetime import datetime
import mysql.connector
from kivymd.uix.pickers import MDDatePicker

from config import DB_CONFIG
from local_ip import get_local_ip


class AddWorkerScreen(Screen):
    selected_date_of_birth = None

    def save_worker(self):
        name = self.ids.new_worker_name.text
        date_of_birth_str = self.ids.new_worker_date_of_birth_input.text
        address = self.ids.new_worker_address.text

        if name.strip() and address.strip() and date_of_birth_str.strip():
            try:
                # Převod z textového vstupu na objekt a zpět na správný formát
                parsed_date = datetime.strptime(date_of_birth_str, "%d.%m.%Y").date()
                date_for_mysql = parsed_date.isoformat()  # 'YYYY-MM-DD'

                response = requests.post(
                    f"{get_local_ip()}/workers",
                    json={"name": name, "date_of_birth": date_for_mysql, "address": address}
                )
                if response.status_code == 201:
                    self.show_popup("Úspěch", f"Pracovník '{name}' byl uložen.")
                else:
                    self.show_popup("Chyba", f"Chyba API: {response.text}")
            except Exception as e:
                self.show_popup("Chyba", f"Nelze se připojit k API: {e}")
        else:
            self.show_popup("Neplatná data", "Zadej platné jméno a datum narození.")

        self.ids.new_worker_name.text = ""
        self.ids.new_worker_date_of_birth_input.text = ""
        self.ids.new_worker_address.text = ""

    def show_popup(self, title, message):
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        box.add_widget(Label(text=message))
        popup = Popup(title=title, content=box, size_hint=(0.7, 0.3))
        popup.open()


    def open_date_picker(self):
        picker = MDDatePicker()
        picker.bind(on_save=self.set_date_of_birth)
        picker.open()

    def set_date_of_birth(self, instance, value, date_range):
        self.selected_date_of_birth = value
        self.ids.new_worker_date_of_birth_input.text = value.strftime("%d.%m.%Y")