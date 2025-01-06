from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.resources import resource_find

from icon_button import IconButton
from config import IMAGES_PATH, DARK_IMAGES_PATH, BRIGHT_IMAGES_PATH


class PlayerScreen(Screen):
    def __init__(self, player_name: str, **kwargs):
        super().__init__(**kwargs)
        self.player_name = player_name
        self.build()

    def build(self):
        layout = BoxLayout(
            orientation="vertical",
        )

        if App.get_running_app().is_dark_theme:
            back_button = IconButton(self.handle_back,
                                     0.05,
                                     0.1,
                                     f'{DARK_IMAGES_PATH}/back_arrow.png')
            text = f"[color=#D9D9D9]{self.player_name}"
        else:
            back_button = IconButton(self.handle_back,
                                     0.05,
                                     0.1,
                                     f'{BRIGHT_IMAGES_PATH}/back_arrow.png')
            text = f"[color=#434343]{self.player_name}"
        layout.add_widget(back_button)
        image = AsyncImage(
            source=resource_find(f'{IMAGES_PATH}/default_player.png')
        )
        layout.add_widget(image)

        name_label = Label(
            size_hint_y=0.1,
            text=text,
            halign="center",
            markup=True
        )
        layout.add_widget(name_label)
        self.add_widget(layout)

    def handle_back(self, instance):
        self.parent.remove_widget(self)
        self.parent.current = 'teams'