# screens/main_screen.py

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class MainScreen(Screen):
    def _init_(self, **kwargs):
        super()._init_(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        add_worker_btn = Button(text="Přidat pracovníka", size_hint_y=None, height=50)
        add_worker_btn.bind(on_press=self.go_to_add_worker)
        layout.add_widget(add_worker_btn)

        create_task_btn = Button(text="Vytvořit úkol", size_hint_y=None, height=50)
        create_task_btn.bind(on_press=self.go_to_create_task)
        layout.add_widget(create_task_btn)

        self.add_widget(layout)

    def go_to_add_worker(self, instance):
        self.manager.current = "add_worker"

    def go_to_create_task(self, instance):
        self.manager.current = "create_task"