from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from math import log2, ceil
from db_handler import TournamentDatabase
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class RankingTable(GridLayout):
    def __init__(self, headers, data, title = '', **kwargs):
        super().__init__(**kwargs)

        self.size_hint_y = None
        self.bind(minimum_height=self.setter('height'))
        self.data = data

        self.cols = 1
        self.sort_order = [True] * len(data[0])
        self.title = title

        self.fill_title()
        if headers:
            self.headers = headers
            self.fill_headers()
        self.fill_rows()
        #self.sort_by_column(0)

    def fill_headers(self):
        layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        for i, header in enumerate(self.headers):
            button = Button(
                text=header,
                size_hint_y=None,
                height=50,
                size_hint_x=1 / len(self.headers),
            )
            button.bind(on_release=lambda btn, col=i: self.sort_by_column(col))
            layout.add_widget(button)
        self.add_widget(layout)

    def fill_rows(self):
        outer_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=20, padding=[0, 10, 0, 10])
        outer_layout.bind(minimum_height=outer_layout.setter('height'))
        for row in self.data:
            inner_layout = BoxLayout(orientation='horizontal')
            inner_layout.bind(minimum_height=inner_layout.setter('height'))
            for cell in row:
                inner_layout.add_widget(Label(
                    text=cell,
                    size_hint_x=1 / len(self.data[0]),
                    size_hint_y=1,
                    text_size=(None, None),
                    halign='center',
                    valign='middle'
                ))
            outer_layout.add_widget(inner_layout)
        self.add_widget(outer_layout)

    def fill_title(self):
        title_label = Label(
            text=self.title,
            size_hint_y=None,
            height=40,
            font_size=24,
            bold=True,
            halign='center',
            valign='middle'
        )
        self.add_widget(title_label)
    def update_table(self):
        self.clear_widgets()
        self.fill_title()
        self.fill_headers()
        self.fill_rows()

    def sort_by_column(self, column_index):
        self.sort_order[column_index] = not self.sort_order[column_index]
        self.data.sort(key=lambda x: x[column_index], reverse = self.sort_order[column_index])
        self.update_table()


class TrophyMatchesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = TournamentDatabase()
        self.build()

    def build(self):
        self.clear_widgets()
        rounds = self.generate_bracket_robin_round()
        #rounds = self.generate_bracket_eliminations()
        layout = self.generate_trophy_table(rounds, robin_round = True)
        self.add_widget(layout)

    def generate_trophy_table(self,rounds, robin_round = True):

        root = ScrollView(size_hint=(1, 1), bar_width=10)

        container = BoxLayout(orientation='vertical', size_hint_y=None)
        container.bind(minimum_height=container.setter('height'))

        rounds_num = len(rounds) - (1 if not robin_round else 0)

        for i in range(1, rounds_num + 1):
            data_rounds = list(rounds[i-1])
            data_rounds_results = [(team1, str(0), str(0), team2) for team1, team2 in data_rounds]
            table = RankingTable(headers=None, data=data_rounds_results, title=f"Round {i}")
            container.add_widget(table)

        if not robin_round:
            final_round = rounds[-1]
            data = list(final_round)
            table = RankingTable(headers=None, data=data, title=f"Final match")
            container.add_widget(table)
        root.add_widget(container)
        return root


    def generate_bracket_eliminations(self):
        teams = self.db.get_teams()
        num_teams = len(teams)
        next_power_of_two = 2 ** ceil(log2(num_teams))
        num_byes = next_power_of_two - num_teams

        for _ in range(num_byes):
            teams.append('-')

        teams = self.reorder_teams(teams)

        rounds = []
        current_round = [(teams[i], teams[i + 1]) for i in range(0, len(teams), 2)]
        rounds.append(current_round)
        while len(current_round) > 1:
            next_round = []
            for pair in current_round:
                if pair[0] == '-':
                    next_round.append(pair[1])
                elif pair[1] == '-':
                    next_round.append(pair[0])
                else:
                    next_round.append(f"Winner of {pair}")
            current_round = [(next_round[i], next_round[i + 1]) for i in range(0, len(next_round), 2)]
            rounds.append(current_round)
        return rounds

    def generate_bracket_robin_round(self):
        teams = self.db.get_teams()
        num_teams = len(teams)

        rounds = []

        if num_teams % 2 == 1:
            teams.append('-')

        for i in range(num_teams - 1):
            current_round = []
            for j in range(len(teams) // 2):
                team1 = teams[j]
                team2 = teams[len(teams) - 1 - j]
                current_round.append((team1, team2))
            rounds.append(current_round)

            teams = [teams[0]] + [teams[-1]] + teams[1:-1]

        return rounds

    def reorder_teams(self, teams):
        real_teams = [team for team in teams if team != '-']
        byes = [team for team in teams if team == '-']

        reordered = []
        i = 0
        while i < len(real_teams) or i < len(byes):
            if i < len(real_teams):
                reordered.append(real_teams[i])
            if i < len(byes):
                reordered.append(byes[i])
            i += 1
        return reordered


