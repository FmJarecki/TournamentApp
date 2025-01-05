from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.resources import resource_find

from icon_button import add_icon_button
from config import IMAGES_PATH


class PlayerScreen(Screen):
    def __init__(self, player_name: str, **kwargs):
        super().__init__(**kwargs)
        self.player_name = player_name
        self.build()

    def build(self):
        layout = BoxLayout(
            orientation="vertical",
        )

        add_icon_button(layout, self.handle_back, resource_find(f'{IMAGES_PATH}/back_arrow.png'), 0.05, 0.1)

        image = AsyncImage(
            source=resource_find(f'{IMAGES_PATH}/default_player.png'),
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