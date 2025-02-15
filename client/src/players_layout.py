from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView

from config import IMAGES_PATH
from data_client import get_all_players_from_team


class PlayersTable(BoxLayout):
    def __init__(self, team_id: int, **kwargs):
        super(PlayersTable, self).__init__(**kwargs)
        self.players = get_all_players_from_team(team_id)
        self.orientation = "vertical"

        self.scroll_view = ScrollView()

        self.scroll_content = BoxLayout(orientation="vertical", size_hint_y=None)
        self.scroll_content.bind(minimum_height=self.scroll_content.setter('height'))

        self.scroll_content.add_widget(BackgroundColoredLayout((0.2, 0.6, 0.8), "Goalkeepers", size_hint_y=None, height=dp(30)))
        self.add_position_layout("Goalkeeper")
        self.scroll_content.add_widget(BackgroundColoredLayout((0.2, 0.6, 0.8), "Defenders", size_hint_y=None, height=dp(30)))
        self.add_position_layout("Back")
        self.scroll_content.add_widget(BackgroundColoredLayout((0.2, 0.6, 0.8), "Midfielders", size_hint_y=None, height=dp(30)))
        self.add_position_layout("Midfielder")

        self.scroll_view.add_widget(self.scroll_content)
        self.add_widget(self.scroll_view)

    def add_position_layout(self, position: str):
        for player in self.players:
            if player["position"].find(position) != -1:
                layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(60))
                avatar = Image(
                    source=f"{IMAGES_PATH}/default_player.png"
                )
                layout.add_widget(avatar)
                goalkeeper_info_layout = BoxLayout(orientation="vertical")
                goalkeeper_info_layout.add_widget(Label(text=f"{player['number']} {player['name']}"))
                goalkeeper_info_layout.add_widget(Label(text="Birthday: 11.11.2011"))
                layout.add_widget(goalkeeper_info_layout)
                self.scroll_content.add_widget(layout)


class BackgroundColoredLayout(BoxLayout):
    def __init__(self, color: tuple, text: str, **kwargs):
        super(BackgroundColoredLayout, self).__init__(**kwargs)

        with self.canvas.before:
            Color(*color, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect, size=self.update_rect)
        self.add_widget(Label(text=text, font_size=24))

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size