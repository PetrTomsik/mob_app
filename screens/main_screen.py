from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.button import Button

import os
import shutil
import requests
import mysql.connector
from config import DB_CONFIG
from screens.filechooser import FileChooserPopup


class MainLayout(BoxLayout):

    selected_image_path = ""
    selected_names = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self._finish_init)
        self._popup = None

    def _finish_init(self, dt):
        self.refresh_worker_checkboxes()

    def open_filechooser(self):
        # Zabrání opakovanému otevírání popupu
        if self._popup and self._popup.parent:
            return
        content = FileChooserPopup(select=self.set_image_path, cancel=self.dismiss_popup)
        self._popup = Popup(title="Vyber obrázek", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def get_worker_id_by_name(self, name):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM workers WHERE name = %s", (name,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result[0] if result else None
        except:
            return None

    def refresh_worker_checkboxes(self):
        # API URL – zadej IP počítače, kde běží Flask server
        api_url = "http://192.168.1.130:5000/workers"

        try:
            response = requests.get(api_url)
            if response.status_code != 200:
                print(f"❌ Chyba API: {response.status_code}")
                return
            workers = response.json()
        except Exception as e:
            print(f"❌ Nepodařilo se připojit k API: {e}")
            return

        self.ids.names_grid.clear_widgets()
        self.selected_names = []

        for worker in workers:
            name = worker["name"]

            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
            checkbox = CheckBox()
            checkbox.assigned_name = name
            checkbox.bind(active=self.on_checkbox_active)

            label = Label(text=name)

            row.add_widget(checkbox)
            row.add_widget(label)
            self.ids.names_grid.add_widget(row)

    def on_checkbox_active(self, checkbox, value):
        parent_box = checkbox.parent

        name = None
        for widget in parent_box.children:
            if isinstance(widget, Label):
                name = widget.text
                break

        # if not name:
        #     return  # pokud není jméno, ignoruj kliknutí

        if value:
            if name not in self.selected_names:
                self.selected_names.append(name)
        else:

            if name in self.selected_names:
                self.selected_names.remove(name)
        print(f"Vybraná jména: {', '.join(self.selected_names)}")

    def set_image_path(self, selection):
        if selection:
            self.selected_image_path = selection[0]
            print(f"Vybraný obrázek: {self.selected_image_path}")
        self.dismiss_popup()

    def dismiss_popup(self):
        if self._popup:
            self._popup.dismiss()
            self._popup = None

    def save_task(self):
        title = self.ids.title_input.text
        description = self.ids.description_input.text
        image_path = self.selected_image_path

        if self.selected_names:
            worker_ids = [self.get_worker_id_by_name(name) for name in self.selected_names if name]
        else:
            worker_ids = None

        if not title or not description or not image_path or not worker_ids:
            print("❗ Vyplň všechna pole a vyber alespoň jedno jméno.")
            return

        # Uložení obrázku
        if not os.path.exists('images'):
            os.makedirs('images')
        image_filename = os.path.basename(image_path)
        destination = os.path.join('images', image_filename)
        shutil.copy(image_path, destination)

        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO tasks (title, description, image_path)
                VALUES (%s, %s, %s)
            """, (title, description, destination))

            task_id = cursor.lastrowid

            for wid in worker_ids:
                cursor.execute("INSERT INTO task_workers (task_id, worker_id) VALUES (%s, %s)", (task_id, wid))

            conn.commit()
            cursor.close()
            conn.close()

            print("✅ Úkol uložen.")
            self.ids.title_input.text = ""
            self.ids.description_input.text = ""
            self.selected_image_path = ""
            self.selected_names = []

        except mysql.connector.Error as err:
            print(f"❌ Chyba při ukládání úkolu: {err}")

    def show_tasks(self):
        self.ids.tasks_container.clear_widgets()
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()

            # Nejprve načteme všechny úkoly
            cursor.execute("""
                       SELECT id, title, description, image_path, datum
                       FROM tasks
                       ORDER BY datum DESC
                   """)
            tasks = cursor.fetchall()

            for task_id, title, description, image_path, datum in tasks:
                # Zjistíme všechna jména pracovníků přiřazených k tomuto úkolu
                cursor.execute("""
                          SELECT w.name FROM workers w
                          JOIN task_workers tw ON w.id = tw.worker_id
                          WHERE tw.task_id = %s
                      """, (task_id,))
                names = [row[0] for row in cursor.fetchall()]
                names_text = ", ".join(names) if names else "Neurčeno"

                # Vykreslení jednoho úkolu
                task_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=120, spacing=10)

                # obrázek (pokud existuje)
                if image_path and os.path.exists(image_path):
                    img = Image(source=image_path, size_hint=(None, 1), width=100)
                else:
                    img = Image(size_hint=(None, 1), width=100)

                # textová část
                text_box = BoxLayout(orientation='vertical')
                text_box.add_widget(Label(text=title, bold=True))
                text_box.add_widget(Label(text=description))
                text_box.add_widget(Label(text=f"Přiřazeno: {names_text}"))
                text_box.add_widget(Label(text=f"Vytvořeno: {datum.strftime('%d.%m.%Y %H:%M')}"))

                task_box.add_widget(img)
                task_box.add_widget(text_box)
                self.ids.tasks_container.add_widget(task_box)

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print(f"❌ Chyba při načítání úkolů: {err}")


class MainScreen(Screen):
    pass