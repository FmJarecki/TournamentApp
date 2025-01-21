from kivy.uix.screenmanager import Screen
from data_client import get_all_matches
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from table import Table
from kivy.core.window import Window

class TrophyMatchesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build()

    def build(self):
        self.clear_widgets()
        self._generate_trophy_table()

    def _generate_trophy_table(self):
        matches = get_all_matches()
        rounds_num = max(match['round'] for match in matches)
        layout = BoxLayout(orientation='vertical', size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        for round_num in range(1, rounds_num + 1):
            round_matches = [match for match in matches if match['round'] == round_num]
            data_rounds_results = [
                (match['teams'][0], str(match['scores'][0]), str(match['scores'][1]), match['teams'][1])
                for match in round_matches
            ]
            table = Table(headers=None, data=data_rounds_results, rows_font_multiplier = 0.04, title=f"Round {round_num}")
            layout.add_widget(table)

        root = ScrollView(size_hint=(1, 1), size=(Window.width, Window.height))
        root.add_widget(layout)
        self.add_widget(root)

