from db_handler import TournamentDatabase

from kivymd.uix.list import MDListItem, MDListItemHeadlineText
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout

class TeamListScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.db = TournamentDatabase()

        teams = self.db.get_teams()

        layout = MDBoxLayout(
            orientation="vertical",
            spacing=10,
            size_hint=(1, 1),
            md_bg_color=(0.9, 0.9, 0.9, 1),
        )

        for team in teams:
            layout.add_widget(MDListItem(
                MDListItemHeadlineText(
                    text=team,
                ),
                size_hint=(1, None)
                )
            )

        self.add_widget(layout)
