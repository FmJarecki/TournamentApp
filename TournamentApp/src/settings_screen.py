from functools import partial

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.switch import Switch
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button

from matches_screen import MatchesScreen
from settings_db import SettingsDB
from text_manager import TextManager
from icon_button import IconButton
from config import DARK_COLOR, BRIGHT_COLOR, DARK_IMAGES_PATH, BRIGHT_IMAGES_PATH, IMAGES_PATH


class SettingsScreen(Screen):
    def __init__(self, home_screen, **kwargs):
        super().__init__(**kwargs)
        self.home_screen = home_screen

        layout = BoxLayout(
            orientation="vertical",
        )

        back_button_layout = BoxLayout(
            orientation="horizontal",
            size_hint_y=0.1
        )

        back_button_icon_path = (f"{DARK_IMAGES_PATH}/back_arrow.png" if App.get_running_app().is_dark_theme
                                  else f"{BRIGHT_IMAGES_PATH}/back_arrow.png")
        self.back_button = IconButton(
            self.handle_back,
            icon_x_pos=0.2,
            icon_path=back_button_icon_path,
        )

        back_button_layout.add_widget(self.back_button)
        back_button_layout.add_widget(Widget())
        back_button_layout.add_widget(Widget())
        layout.add_widget(back_button_layout)

        theme_layout = BoxLayout(
            orientation="horizontal",
            size_hint_y=0.45
        )

        theme_text = f"[color={DARK_COLOR}]{TextManager.get_text('dark_theme')}[/color]" if App.get_running_app().is_dark_theme\
            else f"[color={BRIGHT_COLOR}]{TextManager.get_text('dark_theme')}[/color]"
        self.theme_label = Label(
            text=theme_text,
            halign="center",
            font_size='20sp',
            markup=True
        )
        theme_layout.add_widget(self.theme_label)

        theme_switch = Switch(active=SettingsDB.get_dark_theme_setting())
        theme_layout.add_widget(theme_switch)
        theme_switch.bind(active=self.on_theme_switch_active)

        layout.add_widget(theme_layout)

        language_layout = BoxLayout(
            orientation="horizontal",
            size_hint_y=0.45
        )
        language_text = f"[color={DARK_COLOR}]{TextManager.get_text('language')}[/color]" if App.get_running_app().is_dark_theme\
            else f"[color={BRIGHT_COLOR}]{TextManager.get_text('language')}[/color]"
        self.language_label = Label(
            text=language_text,
            halign="center",
            font_size='20sp',
            markup=True
        )
        language_layout.add_widget(self.language_label)

        flag_icons = BoxLayout(
            orientation="horizontal",
            size_hint_y=0.45
        )
        en_flag = IconButton(
            partial(self.flag_clicked, "en"),
            icon_path=f"{IMAGES_PATH}/en.png",
            pos_hint={'y': 0.5}
        )
        flag_icons.add_widget(en_flag)

        it_flag = IconButton(
            partial(self.flag_clicked, "it"),
            icon_path=f"{IMAGES_PATH}/it.png",
            pos_hint={'y': 0.5}
        )
        flag_icons.add_widget(it_flag)
        language_layout.add_widget(flag_icons)

        self.add_widget(layout)
        self.add_widget(language_layout)

    def on_theme_switch_active(self, instance, value: bool):
        App.get_running_app().is_dark_theme = value
        self.home_screen.update_background_color()
        self.theme_label.text = f"[color={DARK_COLOR}]{TextManager.get_text('dark_theme')}[/color]" if value \
            else f"[color={BRIGHT_COLOR}]{TextManager.get_text('dark_theme')}[/color]"
        self.language_label.text = f"[color={DARK_COLOR}]{TextManager.get_text('language')}[/color]" if value \
            else f"[color={BRIGHT_COLOR}]{TextManager.get_text('language')}[/color]"
        self.back_button.update_icon(f"{DARK_IMAGES_PATH}/back_arrow.png" if value else f"{BRIGHT_IMAGES_PATH}/back_arrow.png")
        SettingsDB.set_dark_theme_setting(value)

    def flag_clicked(self, value: str, instance: Button):
        TextManager.set_language(value)
        self.theme_label.text = f"[color={DARK_COLOR}]{TextManager.get_text('dark_theme')}[/color]" if value \
            else f"[color={BRIGHT_COLOR}]{TextManager.get_text('dark_theme')}[/color]"
        self.language_label.text = f"[color={DARK_COLOR}]{TextManager.get_text('language')}[/color]" if value \
            else f"[color={BRIGHT_COLOR}]{TextManager.get_text('language')}[/color]"
        SettingsDB.set_language(value)

    def handle_back(self, instance: Button):
        if 'matches' in self.parent.screen_names:
            matches_screen = self.parent.get_screen('matches')
            self.parent.remove_widget(matches_screen)
        self.parent.add_widget(MatchesScreen(name='matches'))
        self.parent.current = 'matches'
