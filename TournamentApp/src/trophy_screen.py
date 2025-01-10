from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

class RankingTable(GridLayout):
    def __init__(self, headers, data, **kwargs):
        super().__init__(**kwargs)

        self.size_hint_y = None
        self.bind(minimum_height=self.setter('height'))
        self.data = data
        self.headers = headers
        self.cols = len(self.headers)
        self.sort_order = [True] * len(self.headers)

        for i, header in enumerate(self.headers):
            button = Button(
                text=header,
                size_hint_y=None,
                height=50,
                size_hint_x=1 / len(self.headers),
            )
            button.bind(on_release=lambda btn, col=i: self.sort_by_column(col))
            self.add_widget(button)

        self.sort_by_column(0)

    def update_table(self):
        self.clear_widgets()

        for i, header in enumerate(self.headers):
            button = Button(
                text=header,
                size_hint_y=None,
                height=50,
                size_hint_x=1 / len(self.headers),
            )
            button.bind(on_release=lambda btn, col = i : self.sort_by_column(col))
            self.add_widget(button)

        for row in self.data:
            for cell in row:
                self.add_widget(Label(
                    text=cell,
                    size_hint_y=None,
                    height=40,
                    size_hint_x=1 / len(self.headers),
                    text_size=(100, None),
                    halign='center',
                    valign='middle'
                ))

    def sort_by_column(self, column_index):
        self.sort_order[column_index] = not self.sort_order[column_index]
        self.data.sort(key=lambda x: x[column_index], reverse = self.sort_order[column_index])
        self.update_table()


class TrophyScreen(Screen):
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
