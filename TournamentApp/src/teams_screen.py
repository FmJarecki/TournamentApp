from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

from db_handler import TournamentDatabase
from player_screen import PlayerScreen
from team_on_field_screen import TeamOnFieldScreen
from rounded_button import RoundedButton




class TeamListScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = TournamentDatabase()
        self.selected_team = None
        self.build()

    def build(self):
        self.clear_widgets()
        teams = self.db.get_teams()
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
                text=team
            )
            team_item.bind(on_press=lambda x, team_name=team: self.team_clicked(team_name))
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