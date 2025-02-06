from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.image import AsyncImage
from kivy.resources import resource_find

from icon_button import IconButton
from config import IMAGES_PATH, DARK_IMAGES_PATH, BRIGHT_IMAGES_PATH, DARK_COLOR, BRIGHT_COLOR


class PlayerScreen(Screen):
    def __init__(self, player_name: str, number: str, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
        )

        back_button_layout = BoxLayout(
            orientation="horizontal",
            size_hint_y=0.1
        )
        if App.get_running_app().is_dark_theme:
            back_button = IconButton(
                self.handle_back,
                icon_x_pos=0.1,
                icon_path=f'{DARK_IMAGES_PATH}/back_arrow.png',
            )
            text = f"[color={DARK_COLOR}]{player_name}"
        else:
            back_button = IconButton(
                self.handle_back,
                icon_x_pos=0.1,
                icon_path=f'{BRIGHT_IMAGES_PATH}/back_arrow.png',
            )
            text = f"[color={BRIGHT_COLOR}]{player_name}"

        back_button_layout.add_widget(back_button)
        back_button_layout.add_widget(Widget())
        back_button_layout.add_widget(Widget())
        layout.add_widget(back_button_layout)

        image = AsyncImage(
            source=resource_find(f'{IMAGES_PATH}/default_player.png'),
            fit_mode = "fill"
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
