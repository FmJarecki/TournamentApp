from kivy.uix.screenmanager import Screen
from teams_screen import RoundedButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from trophy_matches_screen import TropyMatchesScreen
from trophy_tables_screen import TrophyTablesScreen

class TrophyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build()


    def create_button(self, text, clicked_action = lambda text: print(text)):
        button = RoundedButton(
            text=text
        )
        button.bind(on_press=lambda x, button_text=text: clicked_action(button_text))
        return button

    def build(self):
        self.clear_widgets()
        layout = BoxLayout(
            orientation="vertical"
        )

        buttons = ['Matches', 'Tables']

        for button in buttons:
            hor_layout = BoxLayout(
            orientation="horizontal",
            size_hint_y = 0.8 / len(buttons)
            )
            hor_layout.add_widget(Widget(size_hint_x=0.1))

            btn = self.create_button(button, self.button_clicked)

            hor_layout.add_widget(btn)
            hor_layout.add_widget(Widget(size_hint_x=0.1))
            layout.add_widget(hor_layout)
            layout.add_widget(Widget(
                size_hint_y=0.2 / len(buttons)
            ))
        self.add_widget(layout)

    def button_clicked(self, screen_name: str):
        obj = None
        if screen_name == 'Matches':
            obj = TropyMatchesScreen(name='Matches')
        elif screen_name == 'Tables':
            obj = TrophyTablesScreen(name='Tables')
        if obj:
            self.parent.add_widget(obj)
            self.parent.current = obj.name