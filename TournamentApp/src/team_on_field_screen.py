from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen

from config import BRIGHT_IMAGES_PATH, IMAGES_PATH
from icon_button import IconButton

class TeamOnFieldScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout()

        stadium = Image(
            source=f'{IMAGES_PATH}/stadium.png'
        )
        layout.add_widget(stadium)

        player_icon_path = f'{BRIGHT_IMAGES_PATH}/person.png'

        self.players_buttons = [
            IconButton(self.on_player_press, icon_path=player_icon_path, pos_hint={'x': 0.0, 'y': -0.3}, icon_size=(1,1), btn_size=(0.15,0.15)),
            IconButton(self.on_player_press, icon_path=player_icon_path, pos_hint={'x': -0.1, 'y': -0.1}, icon_size=(1,1), btn_size=(0.15,0.15)),
            IconButton(self.on_player_press, icon_path=player_icon_path, pos_hint={'x': 0.1, 'y': -0.1}, icon_size=(1,1), btn_size=(0.15,0.15)),
            IconButton(self.on_player_press, icon_path=player_icon_path, pos_hint={'x': -0.08, 'y': 0.15}, icon_size=(1,1), btn_size=(0.15,0.15)),
            IconButton(self.on_player_press, icon_path=player_icon_path, pos_hint={'x': 0.08, 'y': 0.15}, icon_size=(1,1), btn_size=(0.15,0.15))
        ]

        self.labels = []
        for player_index, player_button in enumerate(self.players_buttons):
            label = Label(
            text=f"[b][color=#434343]Player {player_index}[/color][/b]",
            markup = True,
            pos_hint={'x': player_button.pos_hint['x'], 'y': player_button.pos_hint['y']-(0.0007*player_button.height)}
            )
            self.labels.append(label)

            player_button.bind(size=self.update_font_size)

            layout.add_widget(player_button)
            layout.add_widget(label)

        self.add_widget(layout)

    def update_font_size(self, instance, value):
        for index, label in enumerate(self.players_buttons):
            label.font_size = self.players_buttons[index].width * 0.03

    def on_player_press(self, instance):
        print('player pressed!')


