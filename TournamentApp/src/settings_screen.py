from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.switch import Switch
from kivy.uix.label import Label


class SettingsScreen(Screen):
    def __init__(self, home_screen, **kwargs):
        super().__init__(**kwargs)
        self.home_screen = home_screen

        layout = BoxLayout(
            orientation="vertical",
        )

        theme_layout = BoxLayout(
            orientation="horizontal",
        )

        text = "[color=#D9D9D9]Dark theme[/color]" if App.get_running_app().is_dark_theme\
            else "[color=#434343]Dark theme[/color]"
        self.theme_label = Label(
            text=text,
            halign="center",
            markup=True
        )
        theme_layout.add_widget(self.theme_label)

        theme_switch = Switch(active=True)
        theme_layout.add_widget(theme_switch)
        theme_switch.bind(active=self.on_theme_switch_active)

        layout.add_widget(theme_layout)

        self.add_widget(layout)

    def on_theme_switch_active(self, instance, value):
        App.get_running_app().is_dark_theme = value
        self.home_screen.update_background_color()
        self.theme_label.text = "[color=#D9D9D9]Dark theme[/color]" if value else "[color=#434343]Dark theme[/color]"
