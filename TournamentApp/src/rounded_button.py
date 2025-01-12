from kivy.app import App
from kivy.uix.button import Button
from kivy.graphics import RoundedRectangle, Color
from config import DARK_BUTTONS_COLOR, BRIGHT_BUTTONS_COLOR

class RoundedButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.background_normal = ''
        self.text_size = self.size
        self.halign = 'center'
        self.valign = 'middle'
        self.bind(size=self.update_font_size)

    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            if App.get_running_app().is_dark_theme:
                Color(*DARK_BUTTONS_COLOR)
            else:
                Color(*BRIGHT_BUTTONS_COLOR)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[20])

    def update_font_size(self, *args):
        self.font_size = self.height * 0.4
        self.text_size = self.size