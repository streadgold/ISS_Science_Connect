import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder

kivy.require('2.3.0')
Builder.load_file('main.kv')


class MainScreen(Screen):
    pass


class EFU1_Screen(Screen):
    pass


class EFU2_Screen(Screen):
    pass


class EFU3_Screen(Screen):
    pass


class ISSApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(EFU1_Screen(name="efu1"))
        sm.add_widget(EFU2_Screen(name="efu2"))
        sm.add_widget(EFU3_Screen(name="efu3"))
        return sm


if __name__ == '__main__':
    ISSApp().run()
