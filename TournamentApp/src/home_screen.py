from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle

from teams_screen import TeamListScreen
from map_screen import MapScreen
from settings_screen import SettingsScreen
from trophy_stage_screen import TropyStageScreen
from icon_button import IconButton
from config import DARK_IMAGES_PATH, BRIGHT_IMAGES_PATH, DARK_THEME_COLOR, BRIGHT_THEME_COLOR, IMAGES_PATH


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.settings = SettingsScreen(name='settings', home_screen=self)

        self.main_layout = BoxLayout(orientation='horizontal')
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(TropyStageScreen(name='trophy'))
        self.screen_manager.add_widget(ProfileView(name='profile'))
        self.screen_manager.add_widget(MapScreen(name='map'))
        self.screen_manager.add_widget(self.settings)
        self.main_layout.add_widget(self.screen_manager)

        with self.canvas.before:
            self.bg_color = Color()
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        main_container = BoxLayout(
            orientation='vertical'
        )

        top_layout = BoxLayout(
            size_hint_y=0.1,
            orientation='horizontal'
        )
        self.settings_button = IconButton(self.on_settings_press, 0.1)
        top_layout.add_widget(self.settings_button)

        top_layout.add_widget(
            Image(
                source=f'{IMAGES_PATH}/title.png'
            )
        )
        top_layout.add_widget(Widget())

        options_layout = BoxLayout(
            size_hint_y=0.1,
            orientation='horizontal'
        )
        self.trophy_button = IconButton(self.on_trophy_press)
        self.teams_button = IconButton(self.on_teams_press)
        self.profile_button = IconButton(self.on_profile_press)
        self.map_button = IconButton(self.on_map_press)
        options_layout.add_widget(self.trophy_button)
        options_layout.add_widget(self.teams_button)
        options_layout.add_widget(self.profile_button)
        options_layout.add_widget(self.map_button)

        main_container.add_widget(top_layout)
        main_container.add_widget(options_layout)
        main_container.add_widget(self.main_layout)

        self.add_widget(main_container)

        self.update_background_color()

    def update_background_color(self):
        if App.get_running_app().is_dark_theme:
            self.bg_color.rgba = DARK_THEME_COLOR
            self.settings_button.update_icon(f'{DARK_IMAGES_PATH}/settings.png')
            self.trophy_button.update_icon(f'{DARK_IMAGES_PATH}/trophy.png')
            self.teams_button.update_icon(f'{DARK_IMAGES_PATH}/teams.png')
            self.profile_button.update_icon(f'{DARK_IMAGES_PATH}/person.png')
            self.map_button.update_icon(f'{DARK_IMAGES_PATH}/map.png')
        else:
            self.bg_color.rgba = BRIGHT_THEME_COLOR
            self.settings_button.update_icon(f'{BRIGHT_IMAGES_PATH}/settings.png')
            self.trophy_button.update_icon(f'{BRIGHT_IMAGES_PATH}/trophy.png')
            self.teams_button.update_icon(f'{BRIGHT_IMAGES_PATH}/teams.png')
            self.profile_button.update_icon(f'{BRIGHT_IMAGES_PATH}/person.png')
            self.map_button.update_icon(f'{BRIGHT_IMAGES_PATH}/map.png')

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def on_trophy_press(self, instance):
        self.screen_manager.current = 'trophy'

    def on_teams_press(self, instance):
        screen_name = 'teams'
        if screen_name in self.screen_manager.screen_names:
            screen_to_remove = self.screen_manager.get_screen(screen_name)
            self.screen_manager.remove_widget(screen_to_remove)

        if 'Player' in self.screen_manager.screen_names:
            screen_to_remove = self.screen_manager.get_screen('Player')
            self.screen_manager.remove_widget(screen_to_remove)

        self.screen_manager.add_widget(TeamListScreen(name=screen_name))
        self.screen_manager.current = 'teams'

    def on_profile_press(self, instance):
        self.screen_manager.current = 'profile'

    def on_map_press(self, instance):
        self.screen_manager.current = 'map'

    def on_settings_press(self, instance):
        self.screen_manager.current = 'settings'




class ProfileView(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Image(
                source=f'{BRIGHT_IMAGES_PATH}/football.png'
            )
        )
