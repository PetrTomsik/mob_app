from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty


class IconButton(ButtonBehavior, BoxLayout):
    icon_path = StringProperty()
    button_text = StringProperty()