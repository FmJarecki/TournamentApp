from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

from rounded_button import RoundedButton
from config import DARK_COLOR, BRIGHT_COLOR


class Table(BoxLayout):
    def __init__(
        self,
        data: list[dict],
        is_header: bool = True,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.orientation: str = 'vertical'
        self.data: list[dict] = data
        self._text_color: str = DARK_COLOR if App.get_running_app().is_dark_theme else BRIGHT_COLOR
        self._sort_order: dict = {}

        if is_header:
           self._fill_header()
        self._fill_rows()

    def _fill_header(self):
        layout = BoxLayout(orientation='horizontal', size_hint_y=0.2)
        for header in self.data[0].keys():
            button_layout = BoxLayout(orientation='horizontal')
            button = RoundedButton(
                text=header,
                on_press=lambda x, data=header: self._sort_by_column(data),
                size_hint_x = 0.8
            )
            button_layout.add_widget(Widget(size_hint_x = 0.1))
            button_layout.add_widget(button)
            button_layout.add_widget(Widget(size_hint_x = 0.1))

            layout.add_widget(button_layout)

        self.add_widget(layout)

    def _fill_rows(self):
        for row in self.data:
            row_layout = BoxLayout(orientation='horizontal', size_hint_y=0.2)
            row_layout.is_row = True
            for cell in row.values():
                label = Label(
                    text=f"[b][color={self._text_color }]{cell}[/color][/b]",
                    markup=True,
                    font_size='15sp',
                )
                row_layout.add_widget(label)
            self.add_widget(row_layout)

    def _remove_rows(self):
        for widget in self.children[:]:
            if hasattr(widget, 'is_row') and widget.is_row:
                self.remove_widget(widget)

    def _sort_by_column(self, header: str):
        if header in self._sort_order:
            self._sort_order[header] = not self._sort_order[header]
        else:
            self._sort_order[header] = True

        if self._sort_order[header]:
            self.data = sorted(self.data, key=lambda x: x[header])
        else:
            self.data = sorted(self.data, key=lambda x: x[header], reverse=True)

        self._remove_rows()
        self._fill_rows()
