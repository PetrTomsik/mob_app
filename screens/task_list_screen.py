# screens/task_list_screen.py

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
import requests
import os
from local_ip import get_local_ip


class TaskListScreen(Screen):
    def show_tasks(self):
        self.ids.tasks_container.clear_widgets()

        try:
            response = requests.get(f"{get_local_ip()}/tasks")
            if response.status_code != 200:
                print(f"❌ Chyba API: {response.status_code}")
                return
            tasks = response.json()
        except Exception as e:
            print(f"❌ Nepodařilo se připojit k API: {e}")
            return

        for task in tasks:
            task_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=120, spacing=10)

            image_path = task["image_path"]
            if image_path and os.path.exists(image_path):
                img = Image(source=image_path, size_hint=(None, 1), width=100)
            else:
                img = Image(size_hint=(None, 1), width=100)

            text_box = BoxLayout(orientation='vertical')
            text_box.add_widget(Label(text=task["title"], bold=True, color=(0, 0, 0, 1)))
            text_box.add_widget(Label(text=task["description"], color=(0, 0, 0, 1)))
            text_box.add_widget(Label(text=f"Přiřazeno: {', '.join(task['workers'])}", color=(0, 0, 0, 1)))
            text_box.add_widget(Label(text=f"Vytvořeno: {task['datum']}", color=(0, 0, 0, 1)))

            task_box.add_widget(img)
            task_box.add_widget(text_box)
            self.ids.tasks_container.add_widget(task_box)
