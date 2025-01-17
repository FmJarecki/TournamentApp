from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from ranking_table import RankingTable
from data_client import get_all_teams
from kivy.core.window import Window
class TrophyTablesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build()

    def generate_results_table(self, teams, headers):
        data = []
        for i in range(len(teams)):
            table_row = [str(0)] * (len(headers[2:]))
            data.append([str(i+1), teams[i]] + table_row)
        return data

    def build(self):
        teams = get_all_teams()
        headers = ['Rank' , 'Team', 'MP', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']
        data = self.generate_results_table(teams, headers)
        table = RankingTable(headers=headers, data=data,headers_sorting=True)
        root = ScrollView(size_hint=(1, 1), size=(Window.width, Window.height))#, bar_width=10)
        root.add_widget(table)
        self.add_widget(root)
