from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

from team_on_field_screen import TeamOnFieldScreen
from data_client import get_all_teams
from rounded_button import RoundedButton


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

        self.add_widget(layout)

    def team_clicked(self, team_name: str):
        screen_name = 'Field'
        if screen_name in self.parent.screen_names:
            screen_to_remove = self.parent.get_screen(screen_name)
            self.parent.remove_widget(screen_to_remove)
        obj = TeamOnFieldScreen(team_name, name=screen_name)
        self.parent.add_widget(obj)
        self.parent.current = obj.name
