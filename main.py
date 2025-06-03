from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager

# Import všech tříd, které se používají v ui.kv
from screens.main_screen import MainScreen
from screens.worker_screen import WorkerScreen
from screens.add_worker import AddWorkerScreen
from screens.show_worker import ShowWorkerScreen  # ✅ DŮLEŽITÉ
from screens.create_task_screen import CreateTaskScreen
from screens.task_list_screen import TaskListScreen
from screens.delete_worker import DeleteWorkerScreen

from custom_widgets import IconButton
# Nastavení barvy pozadí
Window.clearcolor = (1, 1, 0.8, 1)


class TaskApp(MDApp):
    def build(self):
        Builder.load_file("kv/main_screen.kv")
        Builder.load_file("kv/worker_screen.kv")
        Builder.load_file("kv/task_list_screen.kv")
        Builder.load_file("kv/create_task_screen.kv")
        Builder.load_file("kv/custom_widgets.kv")
        Builder.load_file("kv/header.kv")
        Builder.load_file("kv/base_screen.kv")
        Builder.load_file("kv/main.kv")

        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(TaskListScreen(name="task_list"))
        sm.add_widget(CreateTaskScreen(name="create_task"))

        sm.add_widget(WorkerScreen(name="worker_manager"))
        sm.add_widget(ShowWorkerScreen(name="show_worker"))
        sm.add_widget(AddWorkerScreen(name="add_worker"))
        sm.add_widget(DeleteWorkerScreen(name="delete_worker"))

        sm.bind(current=self.on_screen_change)
        self.title = "Hlavní obrazovka"
        return sm

    def on_screen_change(self, instance, screen_name):
        titles = {
            "main": "Hlavní obrazovka",
            "task_list": "Seznam úkolů",
            "create_task": "Vytvořit úkol",
            "worker_manager": "Správa pracovníků",
            "show_worker": "Seznam pracovníků",
            "add_worker": "Přidat pracovníka",
            "delete_worker": "Smazat pracovníka",
        }
        new_title = titles.get(screen_name, "Moje aplikace")

        # ✅ Změna zde: nastavíme .title na MDApp
        self.title = new_title

        print(f"🔁 Přepnuto na: {screen_name} → {new_title}")

if __name__ == "__main__":
    TaskApp().run()