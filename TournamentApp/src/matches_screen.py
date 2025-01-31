from datetime import datetime

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.vector import Vector

from points_table import PointsTable
from config import IMAGES_PATH, DARK_COLOR, BRIGHT_COLOR
from map import open_maps
from data_client import get_team, get_time_sorted_matches
from team_screen import TeamScreen


class MatchesScreen(Screen):
    def __init__(self, **kwargs):
        super(MatchesScreen, self).__init__(**kwargs)
        self._matches: list[dict] = get_time_sorted_matches()
        self._match_iter = 0
        self.touch_start_pos = None
        self.touch_start_time = None

        self.layout = BoxLayout(orientation="vertical")
        self.add_widget(self.layout)

        self.update_widgets()

    def update_widgets(self):
        self.layout.clear_widgets()
        match = self._matches[self._match_iter]
        self.layout.add_widget(MatchLayout(match, size_hint=(1, 0.4)))
        groups: list[str] = [get_team(match["teams"][0])["group"], get_team(match["teams"][1])["group"]]
        self.layout.add_widget(PointsTable(groups=groups, size_hint=(1, 0.6)))

    def on_touch_down(self, touch):
        self.touch_start_pos = Vector(touch.x, touch.y)
        self.touch_start_time = datetime.now()
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.touch_start_pos:
            current_pos = Vector(touch.x, touch.y)
            movement = current_pos - self.touch_start_pos

            if movement.x > 50 > abs(movement.y):
                if self._match_iter > 0:
                    self._match_iter -= 1
                    self.update_widgets()
                self.touch_start_pos = None
            elif movement.x < -50 and abs(movement.y) < 50:
                if self._match_iter < len(self._matches) - 1:
                    self._match_iter += 1
                    self.update_widgets()
                self.touch_start_pos = None
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.touch_start_pos:
            current_pos = Vector(touch.x, touch.y)
            movement = current_pos - self.touch_start_pos
            touch_duration = (datetime.now() - self.touch_start_time).total_seconds()

            for child in self.layout.children:
                if isinstance(child, MatchLayout):
                    if child.team_1_icon.collide_point(*touch.pos):
                        team_obj = TeamScreen(self._matches[self._match_iter]['teams'][0], name="team")
                        self.parent.add_widget(team_obj)
                        self.parent.current = team_obj.name
                        print("Kliknieto pierwsza ikone")
                        return True
                    elif child.team_2_icon.collide_point(*touch.pos):
                        print("Kliknieto druga ikone")
                        return True

            if touch_duration < 0.2 and abs(movement.x) < 10 and abs(movement.y) < 10:
                print("Kliknieto w dowolnym miejscu layoutu")

        self.touch_start_pos = None
        return super().on_touch_up(touch)


class MatchLayout(BoxLayout):
    def __init__(self, match: dict, **kwargs):
        super(MatchLayout, self).__init__(**kwargs)

        text_color: str = DARK_COLOR if App.get_running_app().is_dark_theme else BRIGHT_COLOR

        self.orientation = 'vertical'

        date_label = Label(
            text=f"[b][color={text_color}]{match['date']}[/color][/b]",
            markup=True,
            font_size='25sp',
            size_hint=(1, 0.1),
            pos_hint={'y': 0.45}
        )
        self.add_widget(date_label)

        teams_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.6))

        self.team_1_icon = Image(
            source = f"{IMAGES_PATH}/club_logo.png",
            size_hint=(0.45, 1)
        )
        teams_layout.add_widget(self.team_1_icon)

        vs_label = Label(
            text=f"[b][color={text_color}]VS[/color][/b]",
            markup=True,
            font_size='25sp',
            size_hint=(0.1, 0.1),
            pos_hint={'x': 0.45, 'y': 0.45}
        )
        teams_layout.add_widget(vs_label)

        self.team_2_icon = Image(
            source = f"{IMAGES_PATH}/club_logo_2.png",
            size_hint=(0.45, 1)
        )
        teams_layout.add_widget(self.team_2_icon)

        self.add_widget(teams_layout)

        match_date = datetime.strptime(match['date'], "%Y-%m-%d %H:%M")
        now = datetime.now()

        if match_date < now:
            score_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
            team_1_score = Label(
                text=f"[b][color={text_color}]{match['scores'][0]}[/color][/b]",
                markup=True,
                font_size='25sp',
                size_hint=(0.45, 1)
            )
            score_layout.add_widget(team_1_score)

            score_separator = Label(
                text=f"[b][color={text_color}]:[/color][/b]",
                markup=True,
                font_size='25sp',
                size_hint=(0.1, 1)
            )
            score_layout.add_widget(score_separator)

            team_2_score = Label(
                text=f"[b][color={text_color}]{match['scores'][1]}[/color][/b]",
                markup=True,
                font_size='25sp',
                size_hint=(0.45, 1)
            )
            score_layout.add_widget(team_2_score)
            self.add_widget(score_layout)
        else:
            location_label = Label(
                text=f"[b][color={text_color}]{match['stadium']}[/color][/b]",
                markup=True,
                font_size='25sp',
                size_hint=(1, 0.1),
                pos_hint={'y': 0.45}
            )
            self.add_widget(location_label)
