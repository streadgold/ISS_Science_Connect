# screens/splash.py
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

class SplashScreen(Screen):
    def on_enter(self):
        # Schedule the transition to the dashboard after 3 seconds
        Clock.schedule_once(self.switch_to_dashboard, 3)

    def switch_to_dashboard(self, dt):
        self.manager.transition.direction = 'left'
        self.manager.current = 'dashboard'
