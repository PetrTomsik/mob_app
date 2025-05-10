from kivy.lang import Builder
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.button import Button
import os
import shutil
import mysql.connector
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label

from config import DB_CONFIG

Builder.load_file('ui.kv')


class MainLayout(BoxLayout):
    selected_image_path = ""
    selected_names = []



    def add_name(self, name):
        if name.strip() == "":
            return

        grid = self.ids.names_grid
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)

        checkbox = CheckBox()
        setattr(checkbox, "assigned_name", name)
        checkbox.bind(active=self.on_checkbox_active)

        label = Label(text=name)

        box.add_widget(checkbox)
        box.add_widget(label)
        grid.add_widget(box)

    def open_filechooser(self):
        content = FileChooserPopup(select=self.set_image_path, cancel=self.dismiss_popup)
        self._popup = Popup(title="Vyber obrázek", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def populate_names(self, names_list):
        grid = self.ids.names_grid
        for name in names_list:
            checkbox = CheckBox()
            checkbox.bind(active=self.on_checkbox_active)
            label = Label(text=name)
            grid.add_widget(label)
            grid.add_widget(checkbox)


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
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM workers")
            workers = cursor.fetchall()
            cursor.close()
            conn.close()

            self.ids.names_grid.clear_widgets()
            self.selected_names = []

            for (name,) in workers:
                row = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
                checkbox = CheckBox()
                setattr(checkbox, "assigned_name", name)
                checkbox.bind(active=self.on_checkbox_active)
                label = Label(text=name)
                row.add_widget(checkbox)
                row.add_widget(label)
                self.ids.names_grid.add_widget(row)

        except mysql.connector.Error as err:
            print(f"❌ Chyba při načítání pracovníků: {err}")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.refresh_worker_checkboxes()
        #self.populate_names(["Petr", "Matěj", "Taťka", "Onrda"])

    def on_checkbox_active(self, checkbox, value):
        grid = checkbox.parent.children
        name = None # getattr(checkbox, "assigned_name", None)

        # V GridLayout se widgety ukládají v opačném pořadí, než byly přidány
        for i in range(1, len(grid), 2):
            checkbox = grid[i]

            if checkbox.active:
                label = grid[i - 1]
                name = label.text
                break

        if not name:
            return  # pokud není jméno, ignoruj kliknutí

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
        self._popup.dismiss()

    def save_task(self):
        title = self.ids.title_input.text
        description = self.ids.description_input.text
        image_path = self.selected_image_path

        if self.selected_names:
            worker_id = self.get_worker_id_by_name(self.selected_names[0])
        else:
            worker_id = None

        if not title or not description or not image_path or not worker_id:
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
                   INSERT INTO tasks (title, description, image_path, assigned_to)
                   VALUES (%s, %s, %s, %s)
               """, (title, description, destination, worker_id))
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
            cursor.execute("""
                SELECT t.title, t.description, t.image_path, w.name
                FROM tasks t
                LEFT JOIN workers w ON t.assigned_to = w.id
            """)
            tasks = cursor.fetchall()
            cursor.close()
            conn.close()

            for title, description, image_path, worker_name in tasks:
                task_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=100, spacing=10)
                if image_path and os.path.exists(image_path):
                    img = Image(source=image_path, size_hint=(None, 1), width=100)
                else:
                    img = Image(size_hint=(None, 1), width=100)

                text_box = BoxLayout(orientation='vertical')
                text_box.add_widget(Label(text=title))
                text_box.add_widget(Label(text=description))
                text_box.add_widget(Label(text=f"Přiřazeno: {worker_name or 'Neurčeno'}"))

                task_box.add_widget(img)
                task_box.add_widget(text_box)

                self.ids.tasks_container.add_widget(task_box)

        except mysql.connector.Error as err:
            print(f"❌ Chyba při načítání úkolů: {err}")


class FileChooserPopup(BoxLayout):
    def __init__(self, select, cancel, **kwargs):
        super().__init__(**kwargs)
        self.select = select
        self.cancel = cancel
        self.orientation = 'vertical'
        self.filechooser = FileChooserListView(filters=['*.jpg', '*.jpeg', '*.png'])
        self.filechooser.bind(on_submit=self._file_selected)
        self.add_widget(self.filechooser)
        cancel_button = Button(text="Zrušit", size_hint_y=None, height=40)
        cancel_button.bind(on_press=lambda instance: self.cancel())
        self.add_widget(cancel_button)

    def _file_selected(self, filechooser, selection, touch):
        if selection:
            self.select(selection)


class TaskApp(App):
    def build(self):
        return MainLayout()


if __name__ == '__main__':
    TaskApp().run()
