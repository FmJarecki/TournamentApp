from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

from table import Table
from data_client import get_teams_from_group


class PointsTable(BoxLayout):
    def __init__(self, groups: list[str], **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'
        self.group: str = groups[0]

        transformed_teams = []
        for team in get_teams_from_group(self.group):
            transformed_team = {
                'Name': team.get('name', ''),
                'PTS': team.get('points', 0),
                'GF': team.get('total_goals', 0),
                'GA': team.get('conceded_goals', 0)
            }
            transformed_teams.append(transformed_team)

        table = Table(data=transformed_teams)
        #root = ScrollView(size_hint=(1, 1), size=(Window.width, Window.height))
        #root.add_widget(table)
        self.add_widget(table)
