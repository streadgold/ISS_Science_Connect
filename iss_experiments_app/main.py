from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition, Screen
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.properties import StringProperty, ListProperty
from kivy.metrics import dp
from kivymd.uix.button import MDRaisedButton
from kivy.clock import Clock
from pathlib import Path
import sys
import ctypes
import platform

# Define the generic ExperimentScreen class
class ExperimentScreen(Screen):
    title = StringProperty("Experiment")
    content = StringProperty("Details about the experiment go here.")
    image_source = StringProperty("assets/images/default.png")  # Default image path

    def go_back_to_dashboard(self, *args):
        print("Navigating back to Dashboard from ExperimentScreen.")
        self.manager.current = 'dashboard'

# Define other screens
class SplashScreen(Screen):
    def on_enter(self):
        print("SplashScreen entered. Will transition to Dashboard in 2 seconds.")
        # Schedule transition to Dashboard after 2 seconds
        Clock.schedule_once(self.switch_to_dashboard, 2)

    def switch_to_dashboard(self, dt):
        print("Switching from SplashScreen to DashboardScreen.")
        self.manager.current = 'dashboard'

class DashboardScreen(Screen):
    experiments = ListProperty([])  # List to hold experiment data

    def on_pre_enter(self):
        print("DashboardScreen is setting up experiment buttons.")
        # Clear existing buttons to avoid duplicates
        self.ids.experiment_buttons.clear_widgets()

        # Iterate over experiments and create buttons
        for exp in self.experiments:
            print(f"Adding button for {exp['title']}")
            btn = MDRaisedButton(
                text=exp['title'],
                pos_hint={"center_x": 0.5},
                theme_text_color="Primary",
                md_bg_color=App.get_running_app().theme_cls.primary_color,
                elevation=10,
                font_size=18,
                size_hint_y=None,
                height=dp(50)
            )
            # Use default argument in lambda to capture current experiment name
            btn.bind(on_release=lambda btn, name=exp['name']: self.navigate_to_experiment(name))
            self.ids.experiment_buttons.add_widget(btn)

    def navigate_to_experiment(self, name):
        print(f"Navigating to {name} screen.")
        self.manager.current = name

class QuizScreen(Screen):
    question = StringProperty("Sample Question?")
    options = ListProperty(["Option 1", "Option 2", "Option 3", "Option 4"])

    def go_back_to_dashboard(self, *args):
        print("Navigating back to Dashboard from QuizScreen.")
        self.manager.current = 'dashboard'

    def check_answer(self, selected_option):
        print(f"QuizScreen received selected option: {selected_option}")
        # Example answer checking logic
        correct_answer = "Option 1"  # Replace with actual logic
        if selected_option == correct_answer:
            self.ids.feedback.text = "Correct!"
            self.ids.feedback.theme_text_color = "Primary"
            print("User selected the correct answer.")
        else:
            self.ids.feedback.text = "Incorrect. Try again."
            self.ids.feedback.theme_text_color = "Error"
            print("User selected an incorrect answer.")

# Define the main App class
class ISSExperimentApp(MDApp):
    def build(self):
        self.title = "ISS Experiments Educational App"
        Window.size = (800, 600)  # Set window size

        # Set window to always be on top
        self.set_always_on_top()

        # Set theme
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.accent_palette = "Amber"
        self.theme_cls.theme_style = "Dark"  # Dark theme

        # Load the KV file
        Builder.load_file('myapp.kv')

        # Initialize ScreenManager with a fade transition
        sm = ScreenManager(transition=FadeTransition(duration=1))  # 1-second fade

        # Add static screens to the manager
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        sm.add_widget(QuizScreen(name='quiz'))
        # Add additional static screens here if needed

        # Define experiment data with unique image paths
        experiments = [
            {
                'name': 'experiment1',
                'title': 'Experiment 1: Microgravity Effects',
                'content': "Detailed information about Experiment 1 goes here. Explain the objectives, procedures, findings, and significance of the experiment conducted on the ISS.",
                'image': 'assets/images/experiment1.jpg'  # Path to experiment-specific image
            },
            {
                'name': 'experiment2',
                'title': 'Experiment 2: Fluid Behavior in Space',
                'content': "Detailed information about Experiment 2 goes here. Discuss how fluid dynamics change in microgravity, the methods used to study them, and the implications for space missions.",
                'image': 'assets/images/experiment2.jpg'
            },
            {
                'name': 'experiment3',
                'title': 'Experiment 3: Plant Growth in Space',
                'content': "Detailed information about Experiment 3 goes here. Explore how plants adapt to space conditions, the challenges faced, and the benefits for long-term space missions.",
                'image': 'assets/images/experiment3.jpg'
            },
            # Add more experiments as needed
        ]

        # Define default image path using pathlib
        default_image_path = Path(__file__).parent / 'assets/images/default.png'
        if not default_image_path.exists():
            print(f"Default image not found at {default_image_path}. Ensure `default.png` exists in assets/images/")
            sys.exit(1)  # Exit if default image is missing

        # Dynamically add ExperimentScreens
        for exp in experiments:
            print(f"Adding screen: {exp['name']}")
            # Determine image path
            experiment_image_path = Path(__file__).parent / exp['image']
            if not experiment_image_path.exists():
                print(f"Image for {exp['name']} not found at {experiment_image_path}. Using default image.")
                experiment_image_path = default_image_path
            screen = ExperimentScreen(
                name=exp['name'],
                title=exp['title'],
                content=exp['content'],
                image_source=str(experiment_image_path)
            )
            sm.add_widget(screen)

        # Pass experiment data to DashboardScreen
        dashboard_screen = sm.get_screen('dashboard')
        dashboard_screen.experiments = experiments

        # Start with the splash screen
        sm.current = 'splash'

        # Bind window close event for graceful shutdown
        Window.bind(on_request_close=self.on_request_close)

        return sm

    def set_always_on_top(self):
        current_platform = platform.system()
        if current_platform == "Windows":
            try:
                win_infos = Window.get_window_info()
                for win in win_infos:
                    if 'winid' in win:
                        hwnd = win['winid']
                        # HWND_TOPMOST = -1
                        # SWP_NOMOVE = 0x0002
                        # SWP_NOSIZE = 0x0001
                        ctypes.windll.user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002)
                        print("Window set to always be on top.")
                        break
                else:
                    print("winid not found in window info. Cannot set window to always be on top.")
            except Exception as e:
                print(f"Failed to set window as always on top: {e}")
        elif current_platform == "Darwin":
            # macOS specific code can be implemented here
            print("Always on top feature is not implemented for macOS.")
        elif current_platform == "Linux":
            # Linux specific code can be implemented here
            print("Always on top feature is not implemented for Linux.")
        else:
            print(f"Always on top feature is not implemented for {current_platform}.")

    def on_request_close(self, *args):
       print("Application is closing.")
       self.stop()
       Window.close()
       sys.exit()  # Forcefully terminate the application
       return True  # Indicate that the close request has been handled

    def on_stop(self):
        # Optional: Add any cleanup code here
        print("Application has closed gracefully.")

if __name__ == '__main__':
    ISSExperimentApp().run()