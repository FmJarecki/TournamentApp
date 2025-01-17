from kivy.uix.screenmanager import Screen
from math import log2, ceil
from data_client import get_all_teams
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from ranking_table import RankingTable
from kivy.core.window import Window

class TrophyMatchesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build()

    def build(self):
        self.clear_widgets()
        rounds = self.generate_bracket_robin_round()
        #rounds = self.generate_bracket_eliminations()
        layout = self.generate_trophy_table(rounds, robin_round = True)
        self.add_widget(layout)

    @staticmethod
    def generate_trophy_table(rounds, robin_round = True):
        rounds_num = len(rounds) - (1 if not robin_round else 0)
        layout = BoxLayout(orientation='vertical', size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        for i in range(1, rounds_num + 1):
            data_rounds = list(rounds[i-1])
            data_rounds_results = [(team1, str(0), str(0), team2) for team1, team2 in data_rounds]
            table = RankingTable(headers=None, data=data_rounds_results, title=f"Round {i}")
            layout.add_widget(table)

        root = ScrollView(size_hint=(1, 1), size=(Window.width, Window.height))
        root.add_widget(layout)
        return root


    def generate_bracket_eliminations(self):
        teams = get_all_teams()
        team_names = [team['name'] for team in teams]
        num_teams = len(team_names)
        next_power_of_two = 2 ** ceil(log2(num_teams))
        num_byes = next_power_of_two - num_teams

        for _ in range(num_byes):
            team_names.append('-')

        team_names = self.reorder_teams(team_names)

        rounds = []
        current_round = [(team_names[i], team_names[i + 1]) for i in range(0, len(team_names), 2)]
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

    @staticmethod
    def generate_bracket_robin_round():
        teams = get_all_teams()
        team_names = [team['name'] for team in teams]
        num_teams = len(team_names)
        rounds = []
        if num_teams % 2 == 1:
            team_names.append('-')

        for i in range(num_teams - 1):
            current_round = []
            for j in range(len(team_names) // 2):
                team1 = team_names[j]
                team2 = team_names[len(team_names) - 1 - j]
                current_round.append((team1, team2))
            rounds.append(current_round)

            team_names = [team_names[0]] + [team_names[-1]] + team_names[1:-1]

        return rounds

    @staticmethod
    def reorder_teams(teams):
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


