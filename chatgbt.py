# # Příklad kódu
# <MainLayout>:
#     orientation: 'vertical'
#     padding: 20
#     spacing: 10
#
#     TextInput:
#         id: title_input
#         hint_text: "Název úkolu"
#
#     TextInput:
#         id: description_input
#         hint_text: "Popis úkolu"
#
#     Button:
#         text: "Vybrat obrázek"
#         on_press: root.open_filechooser()
#
#     Button:
#         text: "Uložit úkol"
#         on_press: root.save_task()
#     Button:
#         text: "Zobrazit seznam úkolů"
#         on_press: root.show_tasks()
#
#     ScrollView:
#         size_hint: (1, None)
#         size: (self.width, 300)
#         GridLayout:
#             id: tasks_container
#             cols: 1
#             size_hint_y: None
#             height: self.minimum_height
#             spacing: 10
#             padding: 10
#
# <FileChooserPopup>:
#     orientation: 'vertical'
#     FileChooserListView:
#         id: filechooser
#         filters: ['*.jpg', '*.jpeg', '*.png']
#         on_selection: root.select(self.selection)
#     Button:
#         text: "Zrušit"
#         size_hint_y: None
#         height: 40
#         on_press: root.cancel()
#
#
#
# import mysql
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.image import Image
#
# from kivy.uix.label import Label
# from kivy.uix.popup import Popup
#
# from kivy.lang import Builder
# from kivymd.app import MDApp
# from kivymd.uix.screen import MDScreen
#
# from config import DB_CONFIG
# from database import create_task
# import shutil
# import os
#
# Builder.load_file('ui.kv')
#
# class MainLayout(BoxLayout):
#     selected_image_path = ""
#
#     def open_filechooser(self):
#         content = FileChooserPopup(select=self.set_image_path, cancel=self.dismiss_popup)
#         self._popup = Popup(title="Vyber obrázek", content=content, size_hint=(0.9, 0.9))
#         self._popup.open()
#
#     def set_image_path(self, selection):
#         if selection:
#             self.selected_image_path = selection[0]
#             print(f"Vybraný obrázek: {self.selected_image_path}")
#         self.dismiss_popup()
#
#     def dismiss_popup(self):
#         self._popup.dismiss()
#
#     def show_tasks(self):
#         # Vyčisti předchozí seznam
#         self.ids.tasks_container.clear_widgets()
#
#         # Připoj se k databázi
#         try:
#             conn = mysql.connector.connect(**DB_CONFIG)
#             cursor = conn.cursor()
#             cursor.execute("SELECT title, description, image_path FROM tasks")
#             tasks = cursor.fetchall()
#             cursor.close()
#             conn.close()
#         except mysql.connector.Error as err:
#             print(f"Chyba při načítání úkolů: {err}")
#             return
#
#         # Zobraz úkoly
#         for title, description, image_path in tasks:
#             task_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=100, spacing=10)
#
#             # Obrázek
#             if image_path and os.path.exists(image_path):
#                 img = Image(source=image_path, size_hint=(None, 1), width=100)
#             else:
#                 img = Image(size_hint=(None, 1), width=100)
#
#             # Popis
#             text_box = BoxLayout(orientation='vertical')
#             text_box.add_widget(Label(text=title, bold=True))
#             text_box.add_widget(Label(text=description))
#
#             task_box.add_widget(img)
#             task_box.add_widget(text_box)
#
#             self.ids.tasks_container.add_widget(task_box)
#
#     def save_task(self):
#         title = self.ids.title_input.text
#         description = self.ids.description_input.text
#         image_path = self.selected_image_path
#
#         if title and description and image_path:
#             if not os.path.exists('images'):
#                 os.makedirs('images')
#             image_filename = os.path.basename(image_path)
#             destination = os.path.join('images', image_filename)
#             shutil.copy(image_path, destination)
#             create_task(title, description, destination)
#             print("Úkol uložen.")
#         else:
#             print("Prosím, vyplňte všechny údaje a vyberte obrázek.")
#
# class FileChooserPopup(BoxLayout):
#     def __init__(self, select, cancel, **kwargs):
#         super().__init__(**kwargs)
#         self.select = select
#         self.cancel = cancel
#
# class MainLayout(MDScreen):
#     pass
#
# class TaskApp(MDApp):
#     def build(self):
#         self.theme_cls.primary_palette = "Blue"
#         self.theme_cls.theme_style = "Light"
#         return Builder.load_file("ui.kv")
#
# if __name__ == '__main__':
#     TaskApp().run()
#
#     < MainLayout @ BoxLayout >:
#     orientation: 'vertical'
#     padding: dp(20)
#     spacing: dp(10)
#
#     MDTopAppBar:
#     title: "Správce úkolů"
#     elevation: 10
#     left_action_items: [["menu", lambda x: app.on_menu_button()]]
#
# MDTextField:
# id: title_input
# hint_text: "Název úkolu"
# mode: "outlined"
# helper_text: "Zadejte název úkolu"
# helper_text_mode: "on_focus"
#
# MDTextField:
# id: description_input
# hint_text: "Popis úkolu"
# mode: "outlined"
# multiline: True
# helper_text: "Zadejte podrobný popis"
# helper_text_mode: "on_focus"
#
# MDRaisedButton:
# text: "Vybrat obrázek"
# icon: "image"
# on_release: root.open_filechooser()
#
# MDRaisedButton:
# text: "Uložit úkol"
# icon: "content-save"
# on_release: root.save_task()
#
# MDRaisedButton:
# text: "Zobrazit seznam úkolů"
# icon: "format-list-bulleted"
# on_release: root.show_tasks()
#
# ScrollView:
# MDList:
# id: tasks_container
#
# < FileChooserPopup @ BoxLayout >:
# orientation: 'vertical'
# FileChooserListView:
# id: filechooser
# filters: ['*.jpg', '*.jpeg', '*.png']
# on_selection: root.select(self.selection)
# MDRaisedButton:
# text: "Zrušit"
# size_hint_y: None
# height: dp(40)
# on_release: root.cancel()

# import requests
#
# response = requests.get("http://192.168.1.10:5000/workers")
# data = response.json()
# print(data)

import mysql.connector

conn = mysql.connector.connect(
    host="192.168.X.X",  # IP adresa PC s databází
    user="remote_user",
    password="tajneheslo",
    database="Projeckt_prace"
)

print("✅ Připojeno k databázi!")