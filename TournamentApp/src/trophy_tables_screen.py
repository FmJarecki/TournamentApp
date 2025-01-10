from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from trophy_matches_screen import RankingTable

class TrophyTablesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build()


    def build(self):
        headers = ['Rank' , 'Team', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']
        data = [
            [str(1), 'Team A', str(1), str(0), str(0), str(1), str(0), str(1),str(2)],
            [str(2), 'Team B', str(0), str(1), str(0), str(1), str(1), str(0),str(1)],
            [str(3), 'Team C', str(0), str(0), str(1), str(1), str(4), str(-3),str(0)],
        ]
        table = RankingTable(headers=headers, data=data)
        root = ScrollView(size_hint=(1, 1), bar_width=10)
        root.add_widget(table)
        self.add_widget(root)
