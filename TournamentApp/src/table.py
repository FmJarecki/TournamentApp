from docutils.nodes import title
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from rounded_button import RoundedButton
from kivy.core.window import Window

class Table(BoxLayout):
    def __init__(self, headers, data, title = None, title_font_multiplier = 0.055, rows_font_multiplier = 0.04,headers_sorting = False, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        self.size_hint_y = None
        self.bind(minimum_height=self.setter('height'))
        self.data = data

        self.sort_order = [True] * len(data[0])
        self.title = title
        self.headers = headers
        self.title_font_multiplier = title_font_multiplier
        self.rows_font_multiplier = rows_font_multiplier
        self.headers_sorting = headers_sorting
        self.rows_layout = None
        if self.title:
            self.fill_title()

        if self.headers:
           self.fill_headers()
        self.fill_rows()

    def fill_headers(self):
        screen_width, screen_height = Window.size
        top_padding = screen_height * 0.8 * self.rows_font_multiplier
        if self.title is not None:
            top_padding = 0

        layout = BoxLayout(orientation='horizontal', size_hint_y=None, height = screen_height * 0.1, padding = [0,top_padding,0,0])#, height=50)

        for i, header in enumerate(self.headers):
            if self.headers_sorting:
                button = RoundedButton.create_button(header, lambda btn, col=i: self.sort_by_column(col), False)
            else:
                button = RoundedButton.create_button(header, None, False)
            layout.add_widget(button)
        self.add_widget(layout)

    def fill_rows(self):
        screen_width, screen_height = Window.size
        if self.rows_layout is not None:
            self.remove_widget(self.rows_layout)
        self.rows_layout = BoxLayout(orientation='vertical',size_hint_y = None, spacing = screen_height * 1.25 * self.rows_font_multiplier, padding = [0,screen_height * 0.8 * self.rows_font_multiplier,0,screen_height * 1.25 * self.rows_font_multiplier])
        self.rows_layout.bind(minimum_height=self.rows_layout.setter('height'))
        for row in self.data:
            inner_layout = BoxLayout(orientation='horizontal')
            inner_layout.bind(minimum_height=inner_layout.setter('height'))
            for cell in row:
                inner_layout.add_widget(Label(
                    text=cell,
                    font_size = min(screen_width, screen_height) * self.rows_font_multiplier,
                    text_size = (screen_width, None),
                    halign='center',
                    valign='middle'
                ))
            self.rows_layout.add_widget(inner_layout)
        self.add_widget(self.rows_layout)


    def fill_title(self):
        screen_width, screen_height = Window.size
        title_label = Label(
            text=self.title,
            size_hint_y=None,
            font_size = min(screen_width, screen_height) * self.title_font_multiplier,
            text_size = (screen_width, None),
            bold = True,
            halign='center',
            valign='middle',
            height=screen_height * 0.08
        )
        self.add_widget(title_label)

    def update_table(self):
        self.clear_widgets()
        if self.title:
            self.fill_title()
        if self.headers:
           self.fill_headers()
        self.fill_rows()

    def sort_by_column(self, column_index):
        self.sort_order[column_index] = not self.sort_order[column_index]
        self.data.sort(key=lambda x: x[column_index], reverse = self.sort_order[column_index])
        self.fill_rows()