from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import BooleanProperty

from home_screen import HomeScreen
from db_handler import generate_fake_data

class KVApp(App):
    def __init__(self, is_dark_theme: bool, **kwargs):
        super().__init__(**kwargs)
        self.is_dark_theme = BooleanProperty(is_dark_theme)

    def build(self) -> ScreenManager:
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='HomeScreen'))
        return sm

if __name__ == '__main__':
    generate_fake_data()

    app = KVApp(False)
    app.run()
