from kivy.uix.label import Label
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