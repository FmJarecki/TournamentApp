from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from trophy_matches_screen import RankingTable
from db_handler import TournamentDatabase

class TrophyTablesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = TournamentDatabase()
        self.build()

    def generate_results_table(self, teams, headers):
        data = []
        for i in range(len(teams)):
            table_row = [str(0)] * (len(headers[2:]))
            data.append([str(i+1), teams[i]] + table_row)
        return data

    def build(self):
        teams = self.db.get_teams()
        headers = ['Rank' , 'Team', 'MP', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']
        data = self.generate_results_table(teams, headers)
        table = RankingTable(headers=headers, data=data)
        root = ScrollView(size_hint=(1, 1), bar_width=10)
        root.add_widget(table)
        self.add_widget(root)
