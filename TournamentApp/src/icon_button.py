from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button

from typing import Callable, Any


class IconButton(FloatLayout):
    def __init__(self,
                 callback: Callable[[Any], None],
                 x_pos: float = 0.5,
                 icon_path: str = '',
                 icon_size = (0.5, 0.5),
                 btn_size = (1.0 ,1.0),
                 **kwargs
                 ):
        super().__init__(**kwargs)
        icon = Image(
            size_hint=icon_size,
            pos_hint={'center_x': x_pos, 'center_y': 0.5}
        )
        icon.source = icon_path if icon_path != '' else icon.source
        self.add_widget(icon)

        button = Button(
            background_color=(1.0, 1.0, 1.0, 0.0),
            size_hint=btn_size,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            on_press=callback
        )
        self.add_widget(button)

    def update_icon(self, icon_path: str):
        for child in self.children:
            if isinstance(child, Image):
                child.source = icon_path
                break
