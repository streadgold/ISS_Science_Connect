# screens/experiment2.py
from kivy.uix.screenmanager import Screen

class Experiment2Screen(Screen):
    def go_back_to_dashboard(self, *args):
        self.manager.current = 'dashboard'
