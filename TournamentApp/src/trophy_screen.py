from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from teams_screen import RoundedButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from trophy_stage_screen import TropyStageScreen

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
        pass
        # headers = ['Rank' , 'Team', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']
        # data = [
        #     [str(1), 'Team A', str(1), str(0), str(0), str(1), str(0), str(1),str(2)],
        #     [str(2), 'Team B', str(0), str(1), str(0), str(1), str(1), str(0),str(1)],
        #     [str(3), 'Team C', str(0), str(0), str(1), str(1), str(4), str(-3),str(0)],
        # ]
        # table = RankingTable(headers=headers, data=data)
        # root = ScrollView(size_hint=(1, 1), bar_width=10)
        # root.add_widget(table)
        # self.add_widget(root)

    def build(self):
        self.clear_widgets()
        layout = BoxLayout(
            orientation="vertical"
        )

        stages = []
        stages.append('Group stage')
        stages.append('Final stage')

        for stage in stages:
            hor_layout = BoxLayout(
            orientation="horizontal",
            size_hint_y = 0.8 / len(stages)
            )
            hor_layout.add_widget(Widget(size_hint_x=0.1))

            stage_btn = self.create_button(stage, self.stage_clicked)

            hor_layout.add_widget(stage_btn)
            hor_layout.add_widget(Widget(size_hint_x=0.1))
            layout.add_widget(hor_layout)
            layout.add_widget(Widget(
                size_hint_y=0.2 / len(stages)
            ))
        self.add_widget(layout)

    def stage_clicked(self, team_name: str):
        obj = StageScreen(name='Stage')
        self.parent.add_widget(obj)
        self.parent.current = obj.name