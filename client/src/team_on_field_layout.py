from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image

from player_screen import PlayerScreen
from data_client import get_all_players_from_team
from config import IMAGES_PATH, DARK_COLOR, BRIGHT_COLOR, Position
from icon_button import IconButton


class TeamOnFieldLayout(FloatLayout):
    position_mapping = {
        Position.GK: {'x': 0.4, 'y': 0.08},
        Position.LB: {'x': 0.15, 'y': 0.2},
        Position.RB: {'x': 0.65, 'y': 0.2},
        Position.CB: {'x': 0, 'y': 0},
        Position.LM: {'x': 0.2, 'y': 0.6},
        Position.RM: {'x': 0.6, 'y': 0.6},
        Position.CM: {'x': 0, 'y': 0},
        Position.ST: {'x': 0, 'y': 0},
    }

    def __init__(self, team_name: str, **kwargs):
        super().__init__(**kwargs)
        stadium = Image(
            source=f'{IMAGES_PATH}/stadium.png',
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0},

        )
        self.add_widget(stadium)

        self.players_buttons = []
        self.labels = []
        player_icon_path = f'{IMAGES_PATH}/shirt_blue.png'

        for player in get_all_players_from_team(team_name):
            if player['is_starting']:
                def make_callback(player_name: str, player_number: str):
                    return lambda x: self.on_player_press(player_name, player_number)

                icon_btn = IconButton(
                    make_callback(player['name'], player['number']),
                    size_hint=(0.2, 0.2),
                    icon_path=player_icon_path,
                    pos_hint=self.position_mapping[player['position']],
                    icon_size = (0.8, 0.75),
                    icon_y_pos=0.6,
                    icon_fit_mode='fill'
                )

                surname = player['name'].split()
                surname = ' '.join(surname[1:])
                name = Label(
                    text=f"[b][color={DARK_COLOR}]{surname}[/color][/b]",
                    markup = True,
                    font_size='20sp',
                    size_hint=(0.2, 0.2),
                    pos_hint={'x': icon_btn.pos_hint['x'], 'y': icon_btn.pos_hint['y']-0.07}
                )

                number = Label(
                    text=f"[b][color={DARK_COLOR}]{player['number']}[/color][/b]",
                    markup = True,
                    font_size='25sp',
                    size_hint=(0.2, 0.2),
                    pos_hint={'x': icon_btn.pos_hint['x'], 'y': icon_btn.pos_hint['y']+0.01}
                )

                self.add_widget(icon_btn)
                self.add_widget(name)
                self.add_widget(number)

    def on_player_press(self, player: str, number: str):
        player_view = PlayerScreen(player, number, name='Player')
        self.parent.add_widget(player_view)
        self.parent.current = player_view.name
