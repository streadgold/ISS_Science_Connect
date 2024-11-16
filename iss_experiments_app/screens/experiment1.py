# screens/experiment1.py
from kivy.uix.screenmanager import Screen

class Experiment1Screen(Screen):
    def go_back_to_dashboard(self, *args):
        self.manager.current = 'dashboard'
