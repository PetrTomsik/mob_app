from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
from kivymd.uix.gridlayout import MDGridLayout
from kivy.clock import Clock

class MainScreen(Screen):
    menu_items = ListProperty([
        {"icon": "assets/worker.png", "text": "Pracovníci", "screen": "worker_manager"},
        {"icon": "assets/create_tasks.png", "text": "Vytvořit úkol", "screen": "create_task"},
        {"icon": "assets/show_tasks.png", "text": "Zobrazit úkoly", "screen": "task_list"},
        {"icon": "assets/show_factory.png", "text": "Továrny", "screen": "task_list"},
    ])

    def on_kv_post(self, base_widget):
        self.build_cards()
        # přepočítej i při změně velikosti okna
        self.bind(size=self.on_size)

    def on_size(self, *args):
        self.update_grid_cols()

    def update_grid_cols(self):
        grid = self.ids.get('card_grid')
        if not grid:
            print("⚠️ card_grid nenalezen v self.ids")
            return

        card_width = 170
        available_width = self.width - 40
        new_cols = max(1, int(available_width // card_width))
        grid.cols = new_cols

    def build_cards(self):
        grid = self.ids.card_grid
        grid.clear_widgets()

        for item in self.menu_items:
            card = MDCard(
                size_hint=(None, None),
                size=(150, 150),
                elevation=6,
                ripple_behavior=True,
                on_release=lambda *_ , screen=item["screen"]: setattr(self.manager, "current", screen)
            )
            layout = MDBoxLayout(orientation="vertical", padding=10, spacing=10)
            img = Image(source=item["icon"], size_hint_y=0.6, allow_stretch=True)
            label = MDLabel(text=item["text"], halign="center", theme_text_color="Custom", text_color=(0, 0, 0, 1))
            layout.add_widget(img)
            layout.add_widget(label)
            card.add_widget(layout)
            grid.add_widget(card)

        # počáteční výpočet sloupců
        Clock.schedule_once(lambda dt: self.update_grid_cols())
