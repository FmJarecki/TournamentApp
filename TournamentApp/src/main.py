from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivy.lang import Builder

from home_screen import HomeScreen
from db_handler import generate_fake_data

class KVApp(MDApp):
    def build(self):
        Builder.load_string(HomeScreen.KV)

        sm = MDScreenManager()
        sm.add_widget(HomeScreen(name='HomeScreen'))
        # sm.add_widget(TeamListScreen(name='TeamListScreen'))
        return sm

if __name__ == '__main__':
    generate_fake_data()
    KVApp().run()
