from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from home_screen import HomeScreen
from db_handler import generate_fake_data

class KVApp(App):
    def __init__(self, is_dark_theme: bool, **kwargs):
        super().__init__(**kwargs)
        App.get_running_app().is_dark_theme = is_dark_theme

    def build(self) -> ScreenManager:
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='HomeScreen'))
        return sm

if __name__ == '__main__':
    generate_fake_data()

    app = KVApp(True)
    app.run()
