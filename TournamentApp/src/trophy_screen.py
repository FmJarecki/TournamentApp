from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from config import BRIGHT_IMAGES_PATH

class TrophyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Image(
                source=f'{BRIGHT_IMAGES_PATH}/football.png'
            )
        )