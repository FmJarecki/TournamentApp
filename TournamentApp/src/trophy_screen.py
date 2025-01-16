from kivy.uix.screenmanager import Screen
from rounded_button import RoundedButton
from kivy.uix.boxlayout import BoxLayout
from trophy_matches_screen import TrophyMatchesScreen
from trophy_tables_screen import TrophyTablesScreen

class TrophyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build()

    def build(self):
        self.prepare_screen(TrophyMatchesScreen(name='Matches'))

    def prepare_screen(self,obj):
        self.clear_widgets()
        layout = BoxLayout(
            orientation="vertical",
            size_hint = (1,1)
        )

        button_layout = BoxLayout(
            orientation="horizontal",
            size_hint_y=0.1,
        )

        buttons = ['Matches', 'Tables']
        for button in buttons:
            btn = None
            if obj.name == button:
                btn = RoundedButton.create_button(button, self.button_clicked, active = True)
            else:
                btn = RoundedButton.create_button(button, self.button_clicked, active = False)
            button_layout.add_widget(btn)

        layout.add_widget(button_layout)
        layout.add_widget(obj)
        self.add_widget(layout)


    def button_clicked(self, screen_name: str):
        if screen_name == 'Matches':
            self.prepare_screen(TrophyMatchesScreen(name='Matches'))
        elif screen_name == 'Tables':
            self.prepare_screen(TrophyTablesScreen(name='Tables'))