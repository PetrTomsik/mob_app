# screens/create_task_screen.py

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.properties import StringProperty, ListProperty
import os
import shutil
import requests

class CreateTaskScreen(Screen):
    selected_image_path = StringProperty("")
    selected_worker_ids = ListProperty([])
    selected_company_id = None
    companies = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.initialize_data)

    def initialize_data(self, dt):
        self.load_companies()
        self.load_workers()

    def load_companies(self):
        try:
            response = requests.get("http://192.168.1.121:5000/companies")
            if response.status_code == 200:
                self.companies = response.json()
                spinner = self.ids.company_spinner
                spinner.values = [company["name"] for company in self.companies]
        except Exception as e:
            print(f"Chyba při načítání firem: {e}")

    def load_workers(self):
        try:
            response = requests.get("http://192.168.1.121:5000/workers")
            if response.status_code != 200:
                return
            workers = response.json()
        except Exception as e:
            print(f"Chyba při načítání pracovníků: {e}")
            return

        self.ids.names_grid.clear_widgets()
        self.selected_worker_ids.clear()

        for worker in workers:
            worker_id = worker["id"]
            name = worker["name"]

            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
            checkbox = CheckBox()
            checkbox.assigned_id = worker_id
            checkbox.bind(active=self.on_checkbox_active)

            label = Label(text=name)
            row.add_widget(checkbox)
            row.add_widget(label)
            self.ids.names_grid.add_widget(row)

    def on_checkbox_active(self, checkbox, value):
        wid = checkbox.assigned_id
        if value and wid not in self.selected_worker_ids:
            self.selected_worker_ids.append(wid)
        elif not value and wid in self.selected_worker_ids:
            self.selected_worker_ids.remove(wid)

    def on_company_select(self, text):
        for company in self.companies:
            if company["name"] == text:
                self.selected_company_id = company["id"]
                break

    def open_filechooser(self):
        content = FileChooserListView(filters=['*.jpg', '*.jpeg', '*.png'])
        popup = Popup(title="Vyber obrázek", content=content, size_hint=(0.9, 0.9))
        content.bind(on_submit=lambda instance, selection, touch: self.set_image(selection, popup))
        popup.open()

    def set_image(self, selection, popup):
        if selection:
            self.selected_image_path = selection[0]
        popup.dismiss()

    def save_task(self):
        title = self.ids.title_input.text
        description = self.ids.description_input.text
        image_path = self.selected_image_path

        if not title or not description or not self.selected_company_id or not self.selected_worker_ids:
            print("❗ Vyplň všechna pole.")
            return

        image_filename = os.path.basename(image_path)
        new_path = os.path.join("images", image_filename)
        if not os.path.exists("images"):
            os.makedirs("images")
        shutil.copy(image_path, new_path)

        payload = {
            "title": title,
            "description": description,
            "image_path": new_path,
            "worker_ids": self.selected_worker_ids,
            "company_id": self.selected_company_id
        }

        try:
            r = requests.post("http://192.168.1.121:5000/tasks", json=payload)
            if r.status_code == 201:
                print("✅ Úkol uložen.")
                self.reset_form()
            else:
                print(f"❌ Chyba API: {r.status_code}")
        except Exception as e:
            print(f"❌ Chyba při odesílání úkolu: {e}")

    def reset_form(self):
        self.ids.title_input.text = ""
        self.ids.description_input.text = ""
        self.selected_image_path = ""
        self.selected_worker_ids = []
        self.ids.company_spinner.text = "Vyber firmu"
        self.load_workers()
