import os
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.uix.button import Button

from icon_button import add_icon_button
from config import REPO_DIR


class PlayerScreen(Screen):
    def __init__(self, player_name: str, **kwargs):
        super().__init__(**kwargs)
        self.player_name = player_name
        self.build()

    def build(self):
        layout = BoxLayout(
            orientation="vertical",
        )

        add_icon_button(layout, self.handle_back, f'{REPO_DIR}/data/back_arrow.png', 0.1, 0.1)

        image = AsyncImage(
            source=f'{REPO_DIR}/data/icon.png',
            size_hint=(1, 0.8)
        )
        layout.add_widget(image)
        name_label = Label(
            size_hint=(1, 0.1),
            text=self.player_name,
            halign="center"
        )
        layout.add_widget(name_label)
        self.add_widget(layout)

    def handle_back(self, instance):
        self.parent.remove_widget(self)
        self.parent.current = 'teams'