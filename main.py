
import mysql
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image

from kivy.uix.label import Label
from kivy.uix.popup import Popup

from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

from config import DB_CONFIG
from database import create_task
import shutil
import os

Builder.load_file('ui.kv')

class MainLayout(BoxLayout):
    selected_image_path = ""

    def open_filechooser(self):
        content = FileChooserPopup(select=self.set_image_path, cancel=self.dismiss_popup)
        self._popup = Popup(title="Vyber obrázek", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def set_image_path(self, selection):
        if selection:
            self.selected_image_path = selection[0]
            print(f"Vybraný obrázek: {self.selected_image_path}")
        self.dismiss_popup()

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_tasks(self):
        # Vyčisti předchozí seznam
        self.ids.tasks_container.clear_widgets()

        # Připoj se k databázi
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("SELECT title, description, image_path FROM tasks")
            tasks = cursor.fetchall()
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            print(f"Chyba při načítání úkolů: {err}")
            return

        # Zobraz úkoly
        for title, description, image_path in tasks:
            task_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=100, spacing=10)

            # Obrázek
            if image_path and os.path.exists(image_path):
                img = Image(source=image_path, size_hint=(None, 1), width=100)
            else:
                img = Image(size_hint=(None, 1), width=100)

            # Popis
            text_box = BoxLayout(orientation='vertical')
            text_box.add_widget(Label(text=title, bold=True))
            text_box.add_widget(Label(text=description))

            task_box.add_widget(img)
            task_box.add_widget(text_box)

            self.ids.tasks_container.add_widget(task_box)

    def save_task(self):
        title = self.ids.title_input.text
        description = self.ids.description_input.text
        image_path = self.selected_image_path

        if title and description and image_path:
            if not os.path.exists('images'):
                os.makedirs('images')
            image_filename = os.path.basename(image_path)
            destination = os.path.join('images', image_filename)
            shutil.copy(image_path, destination)
            create_task(title, description, destination)
            print("Úkol uložen.")
        else:
            print("Prosím, vyplňte všechny údaje a vyberte obrázek.")

class FileChooserPopup(BoxLayout):
    def __init__(self, select, cancel, **kwargs):
        super().__init__(**kwargs)
        self.select = select
        self.cancel = cancel

class MainLayout(MDScreen):
    pass

class TaskApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        return Builder.load_file("ui.kv")

if __name__ == '__main__':
    TaskApp().run()