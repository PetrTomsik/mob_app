import os

import requests
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label

from local_ip import get_local_ip  # funkce vracející http://127.0.0.1:8000 nebo jiné
from kivy.clock import Clock


from kivy.properties import ObjectProperty
from kivymd.uix.card import MDCard


class WorkerCard(MDCard):
    name = ObjectProperty(None)
    date_of_birth = ObjectProperty(None)
    address = ObjectProperty(None)
    photo_path = ObjectProperty(None)


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
                    first_name = worker.get('first_name') or 'Neznámý'
                    last_name = worker.get('last_name') or ''
                    address = worker.get('address') or 'Bez adresy'
                    photo = worker.get('photo') or ''

                    dob = worker.get('date_of_birth')
                    if dob:
                        try:
                            # Pokud je datum ve formátu jako: "Thu, 12 Nov 1998 00:00:00 GMT"
                            import datetime
                            parsed = datetime.datetime.strptime(dob, "%a, %d %b %Y %H:%M:%S %Z")
                            formatted_dob = parsed.strftime("%d.%m.%Y")
                        except Exception:
                            formatted_dob = dob  # když neprojde parsování, zobrazí se původní
                    else:
                        formatted_dob = "Neznámé datum"
                    if photo:
                        full_photo_path = os.path.join(os.getcwd(), photo)
                    else:
                        full_photo_path = "assets/worker.png"
                    print("💡 Foto cesta:", full_photo_path, "→ existuje:", os.path.exists(full_photo_path))

                    card = WorkerCard(
                        name=f"{first_name} {last_name}",
                        date_of_birth=formatted_dob,
                        address=address,
                        photo_path=full_photo_path
                    )
                    self.ids.worker_list.add_widget(card)
            else:
                self.ids.worker_list.add_widget(Label(text="Chyba při načítání pracovníků"))
        except Exception as e:
            print(f"Chyba připojení: {e}")
            self.ids.worker_list.add_widget(Label(text=f"Chyba připojení: {e}"))