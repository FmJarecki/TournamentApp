from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle


from teams_screen import TeamListScreen
from map_screen import MapScreen
from icon_button import add_icon_button
from config import REPO_DIR

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.main_layout = BoxLayout(orientation='horizontal')
        with self.canvas.before:
            Color(*(0.1, 0.1, 0.1, 1))
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(TrophyView(name='trophy'))
        self.screen_manager.add_widget(ProfileView(name='profile'))
        self.screen_manager.add_widget(MapScreen(name='map'))

        self.main_layout.add_widget(self.screen_manager)

        self.build()

    def build(self):
        main_container = BoxLayout(
            orientation='vertical'
        )

        top_layout = BoxLayout(
            size_hint_y=0.1,
            orientation='horizontal'
        )
        add_icon_button(top_layout, self.on_settings_press, f'{REPO_DIR}/data/settings.png', 0.1)
        top_layout.add_widget(
            Label(
                text="Vet Championship",
                bold=True
            )
        )
        top_layout.add_widget(Widget())

        options_layout = BoxLayout(
            size_hint_y=0.1,
            orientation='horizontal'
        )
        add_icon_button(options_layout, self.on_trophy_press, f'{REPO_DIR}/data/trophy.png')
        add_icon_button(options_layout, self.on_teams_press, f'{REPO_DIR}/data/teams.png')
        add_icon_button(options_layout, self.on_profile_press, f'{REPO_DIR}/data/person.png')
        add_icon_button(options_layout, self.on_map_press, f'{REPO_DIR}/data/map.png')

        main_container.add_widget(top_layout)
        main_container.add_widget(options_layout)
        main_container.add_widget(self.main_layout)

        self.add_widget(main_container)

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def on_trophy_press(self, instance):
        self.screen_manager.current = 'trophy'

    def on_teams_press(self, instance):
        screen_name = 'teams'
        if screen_name in self.screen_manager.screen_names:
            screen_to_remove = self.screen_manager.get_screen(screen_name)
            self.screen_manager.remove_widget(screen_to_remove)

        if 'Player' in self.screen_manager.screen_names:
            screen_to_remove = self.screen_manager.get_screen('Player')
            self.screen_manager.remove_widget(screen_to_remove)

        self.screen_manager.add_widget(TeamListScreen(name=screen_name))
        self.screen_manager.current = 'teams'

    def on_profile_press(self, instance):
        self.screen_manager.current = 'profile'

    def on_map_press(self, instance):
        self.screen_manager.current = 'map'

    def on_settings_press(self, instance):
        print("Settings pressed")


class TrophyView(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Trophy Screen", halign='center'))


class ProfileView(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Profile Screen", halign='center'))