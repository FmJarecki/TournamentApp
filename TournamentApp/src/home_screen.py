from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle

from settings_screen import SettingsScreen
from icon_button import IconButton
from config import DARK_IMAGES_PATH, BRIGHT_IMAGES_PATH, DARK_THEME_COLOR, BRIGHT_THEME_COLOR, IMAGES_PATH
from matches_screen import MatchesScreen


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.settings = SettingsScreen(name='settings', home_screen=self)

        self.main_layout = BoxLayout(orientation='horizontal')
        self.screen_manager = ScreenManager()

        self.screen_manager.add_widget(MatchesScreen(name='matches'))
        self.screen_manager.add_widget(self.settings)
        self.screen_manager.current = 'matches'

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
        self.settings_button = IconButton(self.on_settings_press, icon_x_pos=0.2)
        top_layout.add_widget(self.settings_button)

        top_layout.add_widget(
            Image(
                source=f'{IMAGES_PATH}/title.png'
            )
        )
        top_layout.add_widget(Widget())

        main_container.add_widget(top_layout)
        main_container.add_widget(self.main_layout)

        self.add_widget(main_container)

        self.update_background_color()

    def update_background_color(self):
        if App.get_running_app().is_dark_theme:
            self.bg_color.rgba = DARK_THEME_COLOR
            self.settings_button.update_icon(f'{DARK_IMAGES_PATH}/settings.png')
        else:
            self.bg_color.rgba = BRIGHT_THEME_COLOR
            self.settings_button.update_icon(f'{BRIGHT_IMAGES_PATH}/settings.png')

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def on_settings_press(self, instance):
        self.screen_manager.current = 'settings'
