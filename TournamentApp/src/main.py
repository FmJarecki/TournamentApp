from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class MyApp(App):
    def build(self):
        # Stworzenie głównego layoutu w pionie (BoxLayout)
        layout = BoxLayout(orientation='vertical')

        # Stworzenie labelki z domyślnym tekstem
        self.label = Label(text="Hello, Kivy!")
        layout.add_widget(self.label)

        # Stworzenie przycisku
        button = Button(text="Click me!")
        button.bind(on_press=self.on_button_click)
        layout.add_widget(button)

        return layout

    def on_button_click(self, instance):
        # Zmiana tekstu w labelce po kliknięciu na przycisk
        self.label.text = "You clicked the button!"

if __name__ == '__main__':
    MyApp().run()
