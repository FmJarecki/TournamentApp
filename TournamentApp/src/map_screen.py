import webbrowser
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.screen import MDScreen

from config import REPO_DIR

class MapScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build()

    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        button_field = Button(background_normal=f'{REPO_DIR}/data/stadium_google_map.png')
        button_field.bind(on_release=lambda instance: self.open_maps(0.0, 0.0))
        layout.add_widget(button_field)

        button_hotel = Button(background_normal=f'{REPO_DIR}/data/hotel_google_map.png')
        button_hotel.bind(on_release=lambda instance: self.open_maps(0.0, 0.0))
        layout.add_widget(button_hotel)

        self.add_widget(layout)

    @staticmethod
    def open_maps(latitude: float, longitude: float):
        url = f"geo:{latitude},{longitude}?q={latitude},{longitude}(Location)" # for mobile
        url = f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}" # temporary for pc
        webbrowser.open(url)