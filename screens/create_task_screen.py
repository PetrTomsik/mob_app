# screens/create_task_screen.py
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from datetime import datetime
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.button import Button
from kivy.clock import Clock
import os
import shutil
import requests
from local_ip import get_local_ip


class CreateTaskScreen(Screen):
    selected_image_path = ""
    selected_worker_ids = []
    selected_company_id = None
    companies = []
    start_date = None
    end_date = None
    start_work_datetime = None
    end_work_datetime = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.initialize_data)

    def initialize_data(self, dt):
        self.load_companies()
        self.load_workers()

    def load_companies(self):
        try:
            response = requests.get(f"{get_local_ip()}/firms")
            if response.status_code == 200:
                self.companies = response.json()
                spinner = self.ids.company_spinner
                spinner.values = [company["name"] for company in self.companies]
        except Exception as e:
            print(f"Chyba při načítání firem: {e}")

    def load_workers(self):
        try:
            response = requests.get(f"{get_local_ip()}/workers")
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
            checkbox = CheckBox(
                color=(0, 0, 0, 1),  # pro jistotu, i když barva na checkbox nemá přímý vliv
                background_checkbox_normal='atlas://data/images/defaulttheme/checkbox_off',
                background_checkbox_down='atlas://data/images/defaulttheme/checkbox_on'
                )
            checkbox.assigned_id = worker_id
            checkbox.bind(active=self.on_checkbox_active)

            label = Label(text=name, color=(0, 0, 0, 1))
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
            "start_work": self.start_work_datetime.isoformat() if self.start_work_datetime else None,
            "end_work": self.end_work_datetime.isoformat() if self.end_work_datetime else None,
            "firm_id": self.selected_company_id
             }
        try:
            r = requests.post(f"{get_local_ip()}/tasks", json=payload)
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
        self.ids.start_label.text = "Vybrat začátek"
        self.ids.end_label.text = "Vybrat konec"

    def open_start_date_picker(self):
        picker = MDDatePicker()
        picker.bind(on_save=self.on_start_date_chosen)
        picker.open()

    def on_start_date_chosen(self, instance, value, date_range):
        self.start_date = value
        self.open_start_time_picker()

    def open_start_time_picker(self):
        picker = MDTimePicker()
        picker.bind(time=self.on_start_time_chosen)
        picker.open()

    def on_start_time_chosen(self, instance, time_value):
        self.start_work_datetime = datetime.combine(self.start_date, time_value)
        self.ids.start_label.text = f"Začátek: {self.start_work_datetime.strftime('%d.%m.%Y %H:%M')}"

    def open_end_date_picker(self):
        picker = MDDatePicker()
        picker.bind(on_save=self.on_end_date_chosen)
        picker.open()

    def on_end_date_chosen(self, instance, value, date_range):
        self.end_date = value
        self.open_end_time_picker()

    def open_end_time_picker(self):
        picker = MDTimePicker()
        picker.bind(time=self.on_end_time_chosen)
        picker.open()

    def on_end_time_chosen(self, instance, time_value):
        self.end_work_datetime = datetime.combine(self.end_date, time_value)
        self.ids.end_label.text = f"Konec: {self.end_work_datetime.strftime('%d.%m.%Y %H:%M')}"
