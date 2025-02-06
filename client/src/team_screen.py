from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.button import Button

from players_layout import PlayersTable
from icon_button import IconButton
from team_on_field_layout import TeamOnFieldLayout
from config import IMAGES_PATH, DARK_COLOR, DARK_IMAGES_PATH, BRIGHT_IMAGES_PATH, BRIGHT_COLOR


class TeamScreen(Screen):
    def __init__(self, team_name: str, **kwargs):
        super().__init__(**kwargs)
        self.team_name = team_name
        self.screen_layout = BoxLayout(orientation='vertical')

        top_layout = BoxLayout(orientation='horizontal', size_hint_y=0.25)
        back_button_icon_path = (f"{DARK_IMAGES_PATH}/back_arrow.png" if App.get_running_app().is_dark_theme
                                  else f"{BRIGHT_IMAGES_PATH}/back_arrow.png")
        back_button = IconButton(
            self.handle_back,
            icon_x_pos=0.3,
            icon_path=back_button_icon_path,
            size_hint_x=0.1
        )
        top_layout.add_widget(back_button)
        team_icon = Image(
            source=f"{IMAGES_PATH}/club_logo.png",
            size_hint_x=0.8
        )
        top_layout.add_widget(team_icon)
        top_layout.add_widget(Widget(size_hint_x=0.1))
        self.screen_layout.add_widget(top_layout)

        options_layout = BoxLayout(
            size_hint_y=0.05,
            orientation='horizontal'
        )
        icons_path: str = DARK_IMAGES_PATH if App.get_running_app().is_dark_theme else BRIGHT_IMAGES_PATH
        self.trophy_button = IconButton(self.on_trophy_press, icon_path=f'{icons_path}/trophy.png')
        self.team_button = IconButton(self.on_team_press, icon_path=f'{icons_path}/team.png')
        self.info_button = IconButton(self.on_info_press, icon_path=f'{icons_path}/info.png')
        options_layout.add_widget(self.trophy_button)
        options_layout.add_widget(self.team_button)
        options_layout.add_widget(self.info_button)
        self.screen_layout.add_widget(options_layout)

        self.bottom_layout = TeamOnFieldLayout(team_name, size_hint_y=0.7)
        self.screen_layout.add_widget(self.bottom_layout)

        self.add_widget(self.screen_layout)

    def on_trophy_press(self, instance):
        if hasattr(self, 'bottom_layout'):
            self.screen_layout.remove_widget(self.bottom_layout)
        self.bottom_layout = TeamOnFieldLayout(self.team_name, size_hint_y=0.7)
        self.screen_layout.add_widget(self.bottom_layout)

    def on_team_press(self, instance):
        if hasattr(self, 'bottom_layout'):
            self.screen_layout.remove_widget(self.bottom_layout)
        self.bottom_layout = PlayersTable(self.team_name, size_hint_y=0.7)
        self.screen_layout.add_widget(self.bottom_layout)
        print('team')

    def on_info_press(self, instance):
        print('info')

    def handle_back(self, instance: Button):
        self.parent.remove_widget(self)
        self.parent.current = 'matches'
