from config import REPO_DIR

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.image import AsyncImage
from kivymd.uix.button import MDIconButton

import os

class PlayerView(MDScreen):
    def __init__(self, player_name: str, **kwargs):
        super().__init__(**kwargs)
        self.player_name = player_name
        self.build()

    def build(self):
        layout = MDBoxLayout(
            orientation="vertical",
        )

        back_button = MDIconButton(
            icon="arrow-left",
            on_press=self.handle_back,
            pos_hint={'left': 1}
        )
        layout.add_widget(back_button)

        img_path = f'{REPO_DIR}/data/icon.png'
        if os.path.exists(img_path):
            image = AsyncImage(
                source=img_path,
                size_hint=(1, 0.8)
            )
        else:
            image = MDLabel(
                text="👤",
                font_size='48sp',
                halign='center'
            )
        layout.add_widget(image)
        name_label = MDLabel(
            text=self.player_name,
            halign="center"
        )
        layout.add_widget(name_label)
        self.add_widget(layout)

    def handle_back(self, instance):
        self.parent.remove_widget(self)
        self.parent.current = 'teams'