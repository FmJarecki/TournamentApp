from kivy.app import App
from kivy.uix.button import Button
from kivy.graphics import RoundedRectangle, Color
from config import DARK_BUTTONS_COLOR, BRIGHT_BUTTONS_COLOR
from kivy.core.window import Window

class RoundedButton(Button):
    def __init__(self, font_size_multiplier = 0.03, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.background_normal = ''
        self.text_size = self.size
        self.halign = 'center'
        self.valign = 'middle'
        self.font_size_multiplier = font_size_multiplier
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
        screen_width, screen_height = Window.size
        self.font_size = min(screen_width, screen_height) * self.font_size_multiplier
        self.text_size = self.size
    @staticmethod
    def create_button(text, clicked_action=lambda text: print(text), active=False, font_size_multiplier = 0.03):
        button = RoundedButton(
            text=text,
            font_size_multiplier = font_size_multiplier,
        )
        if active:
            button = RoundedButton(
                text=f"[b]{text}[/b]",
                markup=True,
                font_size_multiplier = font_size_multiplier
            )
        button.bind(on_press=lambda x, button_text=text: clicked_action(button_text))
        return button