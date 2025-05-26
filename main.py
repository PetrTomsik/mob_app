
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from screens.main_screen import MainScreen
from screens.add_worker import AddWorkerScreen
from screens.create_task_screen import CreateTaskScreen
from screens.task_list_screen import TaskListScreen
from kivy.core.window import Window
from custom_widgets import IconButton
Builder.load_file("ui.kv")


Window.clearcolor = (1, 1, 0.8, 1)  # světle žlutá RGBA

class TaskApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(AddWorkerScreen(name="add_worker"))
        sm.add_widget(TaskListScreen(name="task_list"))
        sm.add_widget(CreateTaskScreen(name="create_task"))
        return sm


if __name__ == "__main__":
    TaskApp().run()