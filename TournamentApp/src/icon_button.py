from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from typing import Callable, Any


def add_icon_button(layout: BoxLayout, callback: Callable[[Any], None], image_path: str, x_pos: float = 0.5, y_size: float = 1.0):
    button_layout = FloatLayout(size_hint=(1, y_size))
    icon = Image(
        source=image_path,
        size_hint=(0.5, 0.5),
        pos_hint={'center_x': x_pos, 'center_y': 0.5}
    )
    button_layout.add_widget(icon)
    button = Button(
        background_color=(1.0, 1.0, 1.0, 0.0),
        size_hint=(1, 1),
        pos_hint={'center_x': 0.5, 'center_y': 0.5},
        on_press=callback
    )
    button_layout.add_widget(button)
    layout.add_widget(button_layout)
