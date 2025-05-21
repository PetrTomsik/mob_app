from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.button import Button
from kivy.uix.popup import Popup


class FileChooserPopup(BoxLayout):
    def __init__(self, select, cancel, **kwargs):
        super().__init__(**kwargs)

        self.select = select
        self.cancel = cancel

        # self.filechooser = FileChooserListView(filters=['*.jpg', '*.jpeg', '*.png'])
        # self.filechooser.bind(on_selection=self.file_selected)
        # self.add_widget(self.filechooser)
        #
        # # spodní tlačítko
        # cancel_btn = Button(text="Zrušit", size_hint_y=None, height=40)
        # cancel_btn.bind(on_release=cancel)
        # self.add_widget(cancel_btn)

    def file_selected(self, filechooser, selection, touch):
        if selection:
            self.select(selection)