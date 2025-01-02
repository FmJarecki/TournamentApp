from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.screenmanager import MDScreenManager

from teams_screen import TeamListScreen
from map_screen import MapScreen

class HomeScreen(MDScreen):
    KV = '''
<HomeScreen>
    main_container: main_container
           
    MDBoxLayout:
        orientation: 'vertical'
    
        MDBoxLayout:
            orientation: 'horizontal'
            size_hint_y: 0.1
            md_bg_color: 0.4, 0.4, 0.4, 1
    
            MDIconButton:
                icon: "cog"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                on_press: root.on_settings_press()
    
            MDLabel:
                text: "Vet Championship"
                size_hint_x: 1
                halign: "center"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                bold: True
    
            MDIconButton:
                icon: "magnify"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                on_press: root.on_search_press()
    
            MDIconButton:
                icon: "dots-vertical"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                on_press: root.on_menu_press()
    
        MDBoxLayout:
            orientation: 'horizontal'
            size_hint_y: 0.1
            md_bg_color: 0.1, 0.1, 0.1, 1
    
            MDIconButton:
                icon: "trophy"
                theme_text_color: "Custom"
                text_color: 1, 0.6, 0, 1
                size_hint_x: 1
                on_press: root.on_trophy_press()
    
            MDIconButton:
                icon: "account-group"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                size_hint_x: 1
                on_press: root.on_teams_press()
    
            MDIconButton:
                icon: "account"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                size_hint_x: 1
                on_press: root.on_profile_press()
    
            MDIconButton:
                icon: "map-marker"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                size_hint_x: 1
                on_press: root.on_map_press()
    
        MDBoxLayout:
            id: main_container
            md_bg_color: 1, 1, 1, 1
            orientation: 'horizontal'

    '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = MDScreenManager()

        self.screen_manager.add_widget(TrophyView(name='trophy'))
        self.screen_manager.add_widget(ProfileView(name='profile'))
        self.screen_manager.add_widget(MapScreen(name='map'))

        self.main_container.add_widget(self.screen_manager)

    def on_trophy_press(self):
        self.screen_manager.current = 'trophy'

    def on_teams_press(self):
        screen_name = 'teams'
        if screen_name in self.screen_manager.screen_names:
            screen_to_remove = self.screen_manager.get_screen(screen_name)
            self.screen_manager.remove_widget(screen_to_remove)

        if 'Player' in self.screen_manager.screen_names:
            screen_to_remove = self.screen_manager.get_screen('Player')
            self.screen_manager.remove_widget(screen_to_remove)
            
        self.screen_manager.add_widget(TeamListScreen(name=screen_name))
        self.screen_manager.current = 'teams'

    def on_profile_press(self):
        self.screen_manager.current = 'profile'

    def on_map_press(self):
        self.screen_manager.current = 'map'


class TrophyView(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(MDLabel(text="Trophy Screen", halign="center"))


class ProfileView(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(MDLabel(text="Profile Screen", halign="center"))
