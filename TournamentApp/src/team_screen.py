from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image

from data_client import get_all_teams
from icon_button import IconButton
from table import Table
from config import IMAGES_PATH, DARK_COLOR, DARK_IMAGES_PATH, BRIGHT_IMAGES_PATH


class TeamScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.team_name = None

    def build(self):
        logo = Image(
            source=f'{IMAGES_PATH}/club_logo.png',
            size_hint=(0.4, 0.4),
            pos_hint={'x': 0.3, 'y': 0.6},
            fit_mode="fill"
        )

        title = Label(
            text=f"[b][color={DARK_COLOR}]{self.team_name}[/color][/b]",
            markup=True,
            size_hint=(0.1, 0.1),
            font_size='40sp',
            pos_hint={'x': 0.45, 'y': 0.5}
        )

        self.add_widget(title)

    def on_enter(self):
        self.build()
