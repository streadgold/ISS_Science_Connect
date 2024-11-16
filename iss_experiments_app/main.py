from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition, Screen
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.properties import StringProperty, ListProperty, DictProperty
from kivy.metrics import dp
from kivy.clock import Clock
import ctypes
from pathlib import Path
import sys
import platform
from kivy.factory import Factory

# Define the generic ExperimentScreen class
class ExperimentScreen(Screen):
    title = StringProperty("Experiment")
    content = StringProperty("Details about the experiment go here.")
    image_source = StringProperty("assets/images/default.png")  # Default image path

    def go_back_to_dashboard(self, *args):
        print("Navigating back to Dashboard from ExperimentScreen.")
        self.manager.current = 'dashboard'

# Define the SplashScreen
class SplashScreen(Screen):
    def on_enter(self):
        print("SplashScreen entered. Will transition to Dashboard in 2 seconds.")
        # Schedule transition to Dashboard after 2 seconds
        Clock.schedule_once(self.switch_to_dashboard, 2)

    def switch_to_dashboard(self, dt):
        print("Switching from SplashScreen to DashboardScreen.")
        self.manager.current = 'dashboard'

# Define the DashboardScreen
class DashboardScreen(Screen):
    experiments = ListProperty([])        # List to hold experiment data
    button_locations = DictProperty({})   # Dict to map buttons to their locations

    def on_pre_enter(self):
        print("DashboardScreen is setting up experiment buttons.")
        # Clear existing buttons to avoid duplicates
        dashboard_buttons = self.ids.dashboard_buttons
        dashboard_buttons.clear_widgets()
        self.button_locations = {}

        # Iterate over experiments and create circular buttons
        for exp in self.experiments:
            print(f"Adding button for {exp['title']} at location {exp['location']}")
            btn = Factory.CircularButton(
                size=(dp(50), dp(50)),  # Small circular button
                # No text
            )
            btn.bind(on_release=lambda btn, name=exp['name']: self.navigate_to_experiment(name))
            # Add button to the layout first to access its size
            dashboard_buttons.add_widget(btn)
            # Store button and its location
            self.button_locations[btn] = exp['location']

        # Bind the on_resize event to reposition buttons when window size changes
        Window.bind(on_resize=self.on_window_resize)

        # Initial positioning of buttons
        Clock.schedule_once(self.position_all_buttons, 0)

    def navigate_to_experiment(self, name):
        print(f"Navigating to {name} screen.")
        self.manager.current = name

    def position_all_buttons(self, dt):
        for btn, loc in self.button_locations.items():
            self.position_button(btn, loc)

    def on_window_resize(self, window, width, height):
        print("Window resized. Repositioning buttons.")
        self.position_all_buttons(None)

    def position_button(self, button, location):
        """
        Positions the button based on relative (x, y) coordinates.
        location: Tuple of (x, y) where each value is between 0 and 1.
        """
        image_width = Window.width
        image_height = Window.height * 0.8  # Since image size_hint is (1, 0.8) in KV
        x_rel, y_rel = location

        # Calculate absolute positions (in pixels)
        x = x_rel * image_width - (button.width / 2)
        y = y_rel * image_height - (button.height / 2) + (Window.height * 0.2)  # Adjust for image position

        # Set the position in pixels
        button.pos = (x, y)

# Define the QuizScreen
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
    # Define window position variables here
    # (0, 0) represents the top-left corner
    WINDOW_X = 50  # X-coordinate for the window's left edge
    WINDOW_Y = 50  # Y-coordinate for the window's top edge

    def build(self):
        self.title = "ISS Experiments Educational App"
        Window.size = (1000, 800)  # Increased window size for better visibility

        # Set window position based on variables
        self.set_window_position(self.WINDOW_X, self.WINDOW_Y)

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
        # Dynamically add ExperimentScreens below

        # Define experiment data with unique image paths and locations
        experiments = [
            {
                'name': 'experiment1',
                'module':'US LAB',
                'title': 'Experiment 1: Microgravity Effects',
                'content': "Detailed information about Experiment 1 goes here. Explain the objectives, procedures, findings, and significance of the experiment conducted on the ISS.",
                'image': 'assets/images/experiment1.jpg',  # Path to experiment-specific image
                'location': (0.3, 0.5)  # (x, y) relative positions (0 to 1)
            },
            {
                'name': 'experiment2',
                'module':'PMM',
                'title': 'Experiment 2: Fluid Behavior in Space',
                'content': "Detailed information about Experiment 2 goes here. Discuss how fluid dynamics change in microgravity, the methods used to study them, and the implications for space missions.",
                'image': 'assets/images/experiment2.jpg',
                'location': (0.6, 0.4)
            },
            {
                'name': 'experiment3',
                'module':'Columbus',
                'title': 'Experiment 3: Plant Growth in Space',
                'content': "Detailed information about Experiment 3 goes here. Explore how plants adapt to space conditions, the challenges faced, and the benefits for long-term space missions.",
                'image': 'assets/images/experiment3.jpg',
                'location': (0.5, 0.7)
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

    def set_window_position(self, x, y):
        """
        Sets the window's top-left position based on the provided (x, y) coordinates.
        (0, 0) corresponds to the top-left corner of the primary display.
        """
        Window.left = x
        Window.top = y
        print(f"Window position set to ({x}, {y})")

    def on_request_close(self, *args):
        print("Application is closing.")
        self.stop()  # Gracefully stop the Kivy application
        # Removed Window.close() and sys.exit() to prevent forceful termination
        return True  # Indicate that the close request has been handled

    def on_stop(self):
        # Optional: Add any cleanup code here
        print("Application has closed gracefully.")

#    # Optionally, if you still need 'always on top' functionality, uncomment and use with caution
#    def set_always_on_top(self):
#        current_platform = platform.system()
#        if current_platform == "Windows":
#            try:
#                win_infos = Window.get_window_info()
#                for win in win_infos:
#                    if 'winid' in win:
#                        hwnd = win['winid']
#                        # HWND_TOPMOST = -1
#                        # SWP_NOMOVE = 0x0002
#                        # SWP_NOSIZE = 0x0001
#                        ctypes.windll.user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002)
#                        print("Window set to always be on top.")
#                        break
#                else:
#                    print("winid not found in window info. Cannot set window to always be on top.")
#            except Exception as e:
#                print(f"Failed to set window as always on top: {e}")
#        elif current_platform == "Darwin":
#            # macOS specific code can be implemented here
#            print("Always on top feature is not implemented for macOS.")
#        elif current_platform == "Linux":
#            # Linux specific code can be implemented here
#            print("Always on top feature is not implemented for Linux.")
#        else:
#            print(f"Always on top feature is not implemented for {current_platform}.")

if __name__ == '__main__':
    ISSExperimentApp().run()