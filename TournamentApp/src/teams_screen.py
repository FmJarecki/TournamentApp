from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import RoundedRectangle, Color
from kivy.uix.widget import Widget

from player_screen import PlayerScreen
from team_on_field_screen import TeamOnFieldScreen
from data_client import get_all_teams
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

class TeamListScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_team = None
        self.build()

    def build(self):
        self.clear_widgets()
        teams = get_all_teams()
        layout = BoxLayout(
            orientation="vertical"
        )
        for team in teams:
            hor_layout = BoxLayout(
            orientation="horizontal",
            size_hint_y = 0.8 / len(teams)
            )
            hor_layout.add_widget(Widget(size_hint_x=0.1))

            team_item = RoundedButton(
                text=team["name"]
            )
            team_item.bind(on_press=lambda x, team_name=team["name"]: self.team_clicked(team_name))
            hor_layout.add_widget(team_item)
            hor_layout.add_widget(Widget(size_hint_x=0.1))
            layout.add_widget(hor_layout)
            layout.add_widget(Widget(
                size_hint_y=0.2 / len(teams)
            ))
            '''
            if self.selected_team == team:
                players = self.db.get_team_players(team)
                for player in players:
                    player_item = Button(
                        text=player,
                        size_hint_y=1/len(players),
                        background_normal='',
                        background_color=(0.25, 0.25, 0.25, 1)
                    )
                    player_item.bind(on_press=lambda x, player_name=player: self.player_clicked(player_name))
                    layout.add_widget(player_item)
            '''
        self.add_widget(layout)

    def team_clicked(self, team_name: str):
        obj = TeamOnFieldScreen(name='Field')
        self.parent.add_widget(obj)
        self.parent.current = obj.name

        #self.selected_team = team_name if self.selected_team != team_name else None
        #self.build()

    def player_clicked(self, player: str):
        player_view = PlayerScreen(player, name='Player')
        self.parent.add_widget(player_view)
        self.parent.current = player_view.name