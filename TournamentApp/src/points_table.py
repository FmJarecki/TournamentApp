from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, StringProperty

from team_screen import TeamScreen
from rounded_button import RoundedButton
from data_client import get_teams_from_group
from config import DARK_COLOR, BRIGHT_COLOR
from text_manager import TextManager


class ClickableRow(BoxLayout):
    callback = ObjectProperty(None)
    cell_value = StringProperty()

    def __init__(self, cell_value, **kwargs):
        super(ClickableRow, self).__init__(**kwargs)
        self.cell_value = cell_value
        self.orientation = 'horizontal'
        self.size_hint_y = 0.2
        self.is_row = True

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.callback:
                self.callback(self.cell_value)
            return True
        return super(ClickableRow, self).on_touch_down(touch)


class PointsTable(BoxLayout):
    def __init__(self, groups: list[str], **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.group: str = groups[0]
        self.data: list[dict] = []
        for team in get_teams_from_group(self.group):
            transformed_team = {
                'name': team.get('name', ''),
                'pts': team.get('points', 0),
                'gf': team.get('total_goals', 0),
                'ga': team.get('conceded_goals', 0)
            }
            self.data.append(transformed_team)

        self.rows: list[BoxLayout] = []
        self._text_color: str = DARK_COLOR if App.get_running_app().is_dark_theme else BRIGHT_COLOR
        self._sort_order: dict = {}

        self._fill_header()
        self._fill_rows()

    def _fill_header(self):
        layout = BoxLayout(orientation='horizontal', size_hint_y=0.2)
        for index, header in enumerate(self.data[0].keys()):
            x_size: float = 1/(len(self.data)+1) if index !=0 else 2/(len(self.data)+1)
            widget_size_hint_x: float = 0.1 if index != 0 else 0.05
            button_size_hint_x: float = 0.8 if index != 0 else 0.9
            button_layout = BoxLayout(orientation='horizontal', size_hint = (x_size, 1))
            button = RoundedButton(
                text=TextManager.get_text(header),
                on_press=lambda x, data=header: self._sort_by_column(data),
                size_hint_x = button_size_hint_x
            )

            button_layout.add_widget(Widget(size_hint_x = widget_size_hint_x))
            button_layout.add_widget(button)
            button_layout.add_widget(Widget(size_hint_x = widget_size_hint_x))

            layout.add_widget(button_layout)

        self.add_widget(layout)

    def _fill_rows(self):
        self.rows = []
        for row in self.data:
            team_name = list(row.values())[0]
            row_layout = BoxLayout(orientation='horizontal', size_hint_y=0.2)
            row_layout.team_name = team_name
            for index, cell in enumerate(row.values()):
                x_size: float = 1 / (len(row) + 1) if index != 0 else 2 / (len(row) + 1)
                label = Label(
                    text=f"[b][color={self._text_color}]{cell}[/color][/b]",
                    markup=True,
                    font_size='15sp',
                    size_hint_x=x_size
                )
                row_layout.add_widget(label)

            self.rows.append(row_layout)
            self.add_widget(row_layout)

    def _remove_rows(self):
        for row in self.rows:
            self.remove_widget(row)
        self.rows.clear()

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
