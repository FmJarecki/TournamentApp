from docutils.nodes import title
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from rounded_button import RoundedButton
from kivy.core.window import Window

class RankingTable(BoxLayout):
    def __init__(self, headers, data, title = None, title_font_multiplier = 0.055, rows_font_multiplier = 0.04, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        self.size_hint_y = None
        self.bind(minimum_height=self.setter('height'))
        self.data = data

        self.cols = 1
        self.sort_order = [True] * len(data[0])
        self.title = title
        self.headers = headers
        self.title_font_multiplier = title_font_multiplier
        self.rows_font_multiplier = rows_font_multiplier

        if self.title:
            self.fill_title()

        if self.headers:
           self.fill_headers()
        self.fill_rows()


        #self.fill_headers()
        # self.sort_by_column(0)

    def fill_headers(self):
        screen_width, screen_height = Window.size
        top_padding = screen_height * 0.8 * self.rows_font_multiplier
        if self.title is not None:
            top_padding = 0

        layout = BoxLayout(orientation='horizontal', size_hint_y=None, height = screen_height * 0.1, padding = [0,top_padding,0,0])#, height=50)
        for i, header in enumerate(self.headers):
            button = RoundedButton.create_button(header, None, False)
            # button = Button(
            #     text=header,
            #     #size_hint_y=1,
            #     #height=50,
            #     size_hint_x=1 / len(self.headers),
            # )
            button.bind(on_release=lambda btn, col=i: self.sort_by_column(col))
            layout.add_widget(button)
        self.add_widget(layout)

    def fill_rows(self):
        screen_width, screen_height = Window.size
        outer_layout = BoxLayout(orientation='vertical',size_hint_y = None, spacing = screen_height * 1.25 * self.rows_font_multiplier, padding = [0,screen_height * 0.8 * self.rows_font_multiplier,0,screen_height * 1.25 * self.rows_font_multiplier])
        outer_layout.bind(minimum_height=outer_layout.setter('height'))



        # title_label.font_size = min(screen_width * multiplier, screen_height * multiplier)
        # title_label.text_size = (screen_width, None)

        for row in self.data:
            inner_layout = BoxLayout(orientation='horizontal')
            inner_layout.bind(minimum_height=inner_layout.setter('height'))
            for cell in row:
                inner_layout.add_widget(Label(
                    text=cell,
                    font_size = min(screen_width, screen_height) * self.rows_font_multiplier,
                    #size_hint_x=1 / len(self.data[0]),
                    #size_hint_y=1,
                    #text_size=(None, None),
                    text_size = (screen_width, None),
                    halign='center',
                    valign='middle'
                ))
            outer_layout.add_widget(inner_layout)
        self.add_widget(outer_layout)


    # @staticmethod
    # def on_size(instance, size):
    #     width, height = size
    #     aspect_ratio = width / height
    #     multiplier = 0.05 if aspect_ratio > 1 else 0.08
    #     instance.font_size = min(width * multiplier, height * multiplier)
    #     #instance.font_size = min(width * 0.25, height * 0.25)
    #     instance.text_size = (width, None)

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
        # Dynamically adjust font size to fit the screen width
        #self.height * 0.4
        #title_label.bind(size=lambda instance, value: setattr(instance, 'font_size', (value * 0.05, value)))
        # title_label.bind(
        #     width=lambda instance, value: setattr(instance, 'font_size', value * 0.05)
        # )

        #title_label.bind(size=self.on_size)
        #self.bind(width=self.update_font_size)
        self.add_widget(title_label)

    # def on_size(self, *args):
    #     print(*args[1])


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
        self.update_table()