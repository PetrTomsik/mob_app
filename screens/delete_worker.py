import requests
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from local_ip import get_local_ip


class DeleteWorkerScreen(Screen):
    def on_pre_enter(self, *args):
        self.load_workers()

    def load_workers(self):
        self.ids.delete_worker_list.clear_widgets()
        try:
            response = requests.get(f"{get_local_ip()}/workers")
            if response.status_code == 200:
                workers = response.json()
                for worker in workers:
                    row = BoxLayout(size_hint_y=None, height=40, spacing=10)
                    label = Label(
                        text=f"{worker['name']} ({worker['date_of_birth']}) – {worker['address']}",
                        size_hint_x=0.8,
                        color=(0, 0, 0, 1)
                    )
                    btn = Button(text="🗑️", size_hint_x=0.2, on_press=lambda inst, wid=worker["id"]: self.delete_worker(wid))
                    row.add_widget(label)
                    row.add_widget(btn)
                    self.ids.delete_worker_list.add_widget(row)
            else:
                self.ids.delete_worker_list.add_widget(Label(text="Chyba při načítání pracovníků"))
        except Exception as e:
            self.ids.delete_worker_list.add_widget(Label(text=f"Chyba připojení: {e}"))

    def delete_worker(self, worker_id):
        try:
            response = requests.delete(f"{get_local_ip()}/workers/{worker_id}")
            if response.status_code == 200:
                self.load_workers()
            else:
                print(f"Chyba při mazání: {response.status_code}")
        except Exception as e:
            print(f"Chyba připojení při mazání: {e}")
