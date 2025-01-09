from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView


class Table(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 9  # Number of columns in the table
        self.size_hint_y = None
        self.bind(minimum_height=self.setter('height'))  # Adjust height dynamically

        # Add table headers
        headers = ['Rank', 'Team', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']
        for header in headers:
            self.add_widget(Label(text=header, bold=True, size_hint_y=None,
                                  height=40, size_hint_x=1/4,halign='center',
                                  valign='middle'))

        # Add rows of data
        for i in range(20):  # Example with 20 rows
            self.add_widget(Label(text=f'Row {i + 1}, Col 1', size_hint_y=None, height=30, size_hint_x=1/4,
                            text_size=(100, None), halign='left', valign='middle',))
            self.add_widget(Label(text=f'Row {i + 1}, Col 2', size_hint_y=None, height=30, size_hint_x=1/4,
                            text_size=(100, None), halign='left', valign='middle',))
            self.add_widget(Label(text=f'Row {i + 1}, Col 3', size_hint_y=None, height=30, size_hint_x=1/4,
                            text_size=(100, None), halign='left', valign='middle',))
            self.add_widget(Label(text=f'Row {i + 1}, Col 4', size_hint_y=None, height=30, size_hint_x=1/4,
                            text_size=(100, None), halign='left', valign='middle',))
            self.add_widget(Label(text=f'Row {i + 1}, Col 5', size_hint_y=None, height=30, size_hint_x=1/4,
                            text_size=(100, None), halign='left', valign='middle',))
            self.add_widget(Label(text=f'Row {i + 1}, Col 6', size_hint_y=None, height=30, size_hint_x=1/4,
                            text_size=(100, None), halign='left', valign='middle',))
            self.add_widget(Label(text=f'Row {i + 1}, Col 7', size_hint_y=None, height=30, size_hint_x=1/4,
                            text_size=(100, None), halign='left', valign='middle',))
            self.add_widget(Label(text=f'Row {i + 1}, Col 8', size_hint_y=None, height=30, size_hint_x=1/4,
                            text_size=(100, None), halign='left', valign='middle',))
            self.add_widget(Label(text=f'Row {i + 1}, Col 9', size_hint_y=None, height=30, size_hint_x=1/4,
                            text_size=(100, None), halign='left', valign='middle',))

class TrophyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build()

    def build(self):
        table = Table()
        root = ScrollView(size_hint=(1, 1), bar_width=10)
        root.add_widget(table)
        self.add_widget(root)  # Attach the ScrollView to the screen
