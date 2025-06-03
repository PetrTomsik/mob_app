import requests
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from local_ip import get_local_ip  # funkce vracející http://127.0.0.1:8000 nebo jiné
from kivy.clock import Clock


class ShowWorkerScreen(Screen):
    def on_pre_enter(self, *args):
        Clock.schedule_once(lambda dt: self.load_workers(), 0)

    def load_workers(self):
        self.ids.worker_list.clear_widgets()

        try:
            response = requests.get(f"{get_local_ip()}/workers")
            if response.status_code == 200:
                workers = response.json()
                for worker in workers:
                    label = Label(
                        text=f"{worker['first_name']} {worker['last_name']} ({worker['date_of_birth']}) –"
                             f" {worker['address']}",
                        size_hint_y=None,
                        height=30,
                        color=(0, 0, 0, 1),
                    )
                    self.ids.worker_list.add_widget(label)
            else:
                self.ids.worker_list.add_widget(Label(text="Chyba při načítání pracovníků"))
        except Exception as e:
            self.ids.worker_list.add_widget(Label(text=f"Chyba připojení: {e}"))
