from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from table import Table
from data_client import get_all_teams, get_all_matches
from kivy.core.window import Window


class TrophyTablesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build()

    def _generate_results_table(self):
        teams = get_all_teams()
        matches = get_all_matches()
        headers = ['Rank' , 'Team', 'MP', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']
        data = []
        if not matches:
            for i, team in enumerate(teams):
                table_row = []
                for header in headers:
                    if header == 'Rank':
                        table_row.append(str(i + 1))
                    elif header == 'Team':
                        table_row.append(team['name'])
                    else:
                        table_row.append(str(0))
                data.append(table_row)
        else:
            teams_stats = []
            for team in teams:
                stats = TrophyTablesScreen._count_team_stats(team, matches)
                teams_stats.append(stats)
            teams_stats.sort(key=lambda x: (x["Pts"], x["GD"], x["GF"]), reverse=True)

            for i, stats in enumerate(teams_stats):
                table_row = []
                for header in headers:
                    if header == 'Rank':
                        table_row.append(str(i + 1))
                    elif header == 'Team':
                        table_row.append(stats['team_name'])
                    elif header == 'MP':
                        table_row.append(str(stats["matches"]))
                    elif header == 'W':
                        table_row.append(str(stats["wins"]))
                    elif header == 'D':
                        table_row.append(str(stats["draws"]))
                    elif header == 'L':
                        table_row.append(str(stats["losses"]))
                    elif header == 'GF':
                        table_row.append(str(stats["GF"]))
                    elif header == 'GA':
                        table_row.append(str(stats["GA"]))
                    elif header == 'GD':
                        table_row.append(str(stats["GD"]))
                    elif header == 'Pts':
                        table_row.append(str(stats["Pts"]))
                data.append(table_row)


        table = Table(headers=headers, data=data, headers_sorting=True)
        root = ScrollView(size_hint=(1, 1), size=(Window.width, Window.height))  # , bar_width=10)
        root.add_widget(table)
        self.add_widget(root)

    @staticmethod
    def _count_team_stats(team, matches: list[dict]) -> dict:
        stats = dict.fromkeys(['matches','wins','losses','draws'], 0)
        stats["team_name"] = team['name']
        stats["GF"] = team['total_goals']
        stats["GA"] = team['conceded_goals']
        stats["GD"] = stats["GF"] - stats["GA"]
        stats["Pts"] = team['points']
        for match in matches:
            if team['name'] in match['teams']:
                stats["matches"] += 1
                team_index = match['teams'].index(team['name'])
                opponent_index = 1 - team_index
                team_score = match['scores'][team_index]
                opponent_score = match['scores'][opponent_index]
                if team_score > opponent_score:
                    stats["wins"] += 1
                elif team_score < opponent_score:
                    stats["losses"] += 1
                else:
                    stats["draws"] += 1
        return stats

    def build(self):
        self._generate_results_table()