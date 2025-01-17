from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen

from player_screen import PlayerScreen
from data_client import get_all_players_from_team
from config import IMAGES_PATH, DARK_COLOR, BRIGHT_COLOR, Position
from icon_button import IconButton


class TeamOnFieldScreen(Screen):
    position_mapping = {
        Position.GK: {'x': 0.35, 'y': 0.08},
        Position.LB: {'x': 0.1, 'y': 0.2},
        Position.RB: {'x': 0.6, 'y': 0.2},
        Position.CB: {'x': 0, 'y': 0},
        Position.LM: {'x': 0.2, 'y': 0.6},
        Position.RM: {'x': 0.5, 'y': 0.6},
        Position.CM: {'x': 0, 'y': 0},
        Position.ST: {'x': 0, 'y': 0},
    }

    def __init__(self, team_name: str, **kwargs):
        super().__init__(**kwargs)

        stadium = Image(
            source=f'{IMAGES_PATH}/stadium.png',
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0},
            allow_stretch=True,
            keep_ratio=False
        )
        self.add_widget(stadium)

        self.title = Label(
            text=f"[b][color=#434343]{team_name}[/color][/b]",
            markup=True,
            size_hint=(0.1, 0.1),
            font_size='40sp',
            pos_hint={'x': 0.45, 'y': 0.85}
        )
        self.add_widget(self.title)

        self.players_buttons = []
        self.labels = []
        player_icon_path = f'{IMAGES_PATH}/shirt_blue.png'

        for player in get_all_players_from_team(team_name):
            if player['is_starting']:
                icon_btn = IconButton(self.on_player_press, size_hint=(0.3, 0.4), icon_path=player_icon_path,
                                 pos_hint=self.position_mapping[player['position']], icon_size = (1.0, 1.0))

                name = Label(
                text=f"[b][color={BRIGHT_COLOR}]{player['name']}[/color][/b]",
                markup = True,
                size_hint=(0.3, 0.4),
                pos_hint={'x': icon_btn.pos_hint['x'], 'y': icon_btn.pos_hint['y']-0.04}
                )

                number = Label(
                text=f"[b][color={DARK_COLOR}]{player['number']}[/color][/b]",
                markup = True,
                size_hint=(0.3, 0.4),
                pos_hint={'x': icon_btn.pos_hint['x'], 'y': icon_btn.pos_hint['y']}
                )

                self.add_widget(icon_btn)
                self.add_widget(name)
                self.add_widget(number)


    def on_player_press(self, player: str):
        player_view = PlayerScreen(player, name='Player')
        self.parent.add_widget(player_view)
        self.parent.current = player_view.name

