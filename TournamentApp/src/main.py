import logging
import sys
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from home_screen import HomeScreen
from data_client_setter import generate_fake_data, clear_data
from settings_db import SettingsDB


def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    file_handler = logging.FileHandler('app.log', mode='w', encoding='utf-8')
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


class KVApp(App):
    def __init__(self, is_dark_theme: bool, **kwargs):
        super().__init__(**kwargs)
        App.get_running_app().is_dark_theme = is_dark_theme

    def build(self) -> ScreenManager:
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='HomeScreen'))
        return sm


if __name__ == '__main__':
    setup_logging()
    SettingsDB.initialize_database()

    #clear_data()
    #generate_fake_data(players_per_team=8, total_teams=3)

    app = KVApp(SettingsDB.get_dark_theme_setting())
    app.run()
