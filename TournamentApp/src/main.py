from kivy.app import App
from kivy.uix.screenmanager import ScreenManager


from home_screen import HomeScreen
from db_handler import generate_fake_data

class KVApp(App):
    def build(self):
        #Builder.load_string(HomeScreen.KV)

        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='HomeScreen'))
        # sm.add_widget(TeamListScreen(name='TeamListScreen'))
        return sm

if __name__ == '__main__':
    generate_fake_data()
    KVApp().run()
