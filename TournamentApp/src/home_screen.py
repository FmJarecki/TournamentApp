from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivy.properties import ObjectProperty
from kivymd.uix.boxlayout import MDBoxLayout

from teams_screen import TeamListScreen

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
    
            MDLabel:
                text: "Choose option."
                halign: "center"
                theme_text_color: "Custom"
                text_color: 0, 0, 0, 1
    '''

    main_container = ObjectProperty()

    def on_settings_press(self):
        print("Settings clicked!")

    def on_search_press(self):
        print("Search clicked!")

    def on_menu_press(self):
        print("Menu clicked!")

    def on_trophy_press(self):
        print("Trophy clicked!")
        self.change_view(TrophyView())

    def on_teams_press(self):
        print("Teams clicked!")
        self.change_view(TeamListScreen())

    def on_profile_press(self):
        print("Profile clicked!")
        self.change_view(ProfileView())

    def on_map_press(self):
        print("Map clicked!")
        self.change_view(MapView())

    def change_view(self, new_view):
        self.main_container.clear_widgets()

        self.main_container.add_widget(new_view)


class TrophyView(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(MDLabel(text="Trophy Screen", halign="center"))


class ProfileView(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(MDLabel(text="Profile Screen", halign="center"))


class MapView(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(MDLabel(text="Map Screen", halign="center"))