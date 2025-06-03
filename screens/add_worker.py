import os

from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
import requests
from datetime import datetime

from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.image import Image
import mysql.connector
from kivymd.uix.pickers import MDDatePicker
from kivy.metrics import dp

from config import DB_CONFIG
from local_ip import get_local_ip


class AddWorkerScreen(Screen):
    selected_photo = None
    selected_date_of_birth = None
    menu = None

    def on_kv_post(self, base_widget):
        # Dynamické načtení obrázků z assets/faces/
        photo_dir = "face_photo"
        items = []
        if os.path.exists(photo_dir):
            for filename in os.listdir(photo_dir):
                if filename.lower().endswith((".jpg", ".png", ".jpeg")):
                    items.append({
                        "viewclass": "OneLineListItem",
                        "text": filename,
                        "on_release": lambda x=filename: self.set_photo(x)
                    })

        if not items:
            items.append({
                "viewclass": "OneLineListItem",
                "text": "Žádné obrázky nenalezeny",
                "on_release": lambda: self.dismiss_menu()
            })

        self.menu = MDDropdownMenu(
            caller=self.ids.photo_menu_button,
            items=items,
            width_mult=4,
            max_height=240  # nebo můžeš vynechat
        )

    def open_photo_menu(self):
        if self.menu:
            self.menu.open()

    def dismiss_menu(self):
        if self.menu:
            self.menu.dismiss()

    def set_photo(self, filename):
        self.selected_photo = os.path.join("face_photo", filename)
        self.ids.photo_preview.source = self.selected_photo
        self.menu.dismiss()

    def save_worker(self):
        first_name = self.ids.new_worker_first_name.text.strip()
        last_name = self.ids.new_worker_last_name.text.strip()
        address = self.ids.new_worker_address.text.strip()
        date_str = self.ids.new_worker_date_of_birth_input.text.strip()

        if not (first_name and last_name and address and date_str):
            self.show_popup("Neplatná data", "Vyplň všechna pole.")
            return

        try:
            parsed_date = datetime.strptime(date_str, "%d.%m.%Y").date()
            date_for_mysql = parsed_date.isoformat()
        except ValueError:
            self.show_popup("Chyba", "Datum musí být ve formátu DD.MM.RRRR.")
            return

        data = {
            "first_name": first_name,
            "last_name": last_name,
            "date_of_birth": date_for_mysql,
            "address": address,
        }
        files = {}
        if self.selected_photo:
            try:
                files["photo"] = open(self.selected_photo, "rb")
            except Exception as e:
                self.show_popup("Chyba", f"Nepodařilo se otevřít obrázek: {e}")
                return

        try:
            response = requests.post(f"{get_local_ip()}/workers", data=data, files=files)
            if response.status_code == 201:
                self.show_popup("Úspěch", f"Pracovník '{first_name} {last_name}' byl uložen.")
            else:
                self.show_popup("Chyba API", response.text)
        except Exception as e:
            self.show_popup("Chyba", f"Nepodařilo se připojit k API: {e}")

        self.ids.new_worker_first_name.text = ""
        self.ids.new_worker_last_name.text = ""
        self.ids.new_worker_date_of_birth_input.text = ""
        self.ids.new_worker_address.text = ""
        self.ids.photo_preview.source = ""
        self.selected_photo = None

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