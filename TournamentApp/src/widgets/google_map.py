import webbrowser
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class MapApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lat: float = 0.0
        self.lon: float = 0.0

    def build(self):
        layout = BoxLayout()
        button = Button(text="Open in Google Maps")
        button.bind(on_release=self.open_maps)
        layout.add_widget(button)
        return layout

    def set_location(self, latitude: float, longitude: float):
        self.lat = latitude
        self.lon = longitude

    def open_maps(self, instance: Button):
        url = f"geo:{self.lat},{self.lon}?q={self.lat},{self.lon}(Location)" # for mobile
        url = f"https://www.google.com/maps/search/?api=1&query={self.lat},{self.lon}" # temporary for pc
        webbrowser.open(url)