# main.py

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty, ObjectProperty, BooleanProperty
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleview import RecycleView
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from pathlib import Path
from dotenv import load_dotenv
from pathlib import Path
import os
import sqlite3
import requests
from PIL import Image as PILImage  # Import Pillow's Image module
from openai import OpenAI  # Adjust the import based on actual OpenAI client
import time
import openai
import base64
import logging
import threading
from kivy.core.audio import SoundLoader
from kivy.uix.popup import Popup

openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Ensure API key is set

system_prompt = """
You are an expert storyteller and educator specializing in space exploration and modern technology. Your mission is to engage and inspire users of all ages to become interested and involved in space-related activities through thrilling, action-packed narratives.

Guidelines:
1. **Action-Packed Storytelling**:
    - Incorporate dynamic events, high-stakes challenges, and intense scenarios that require quick thinking and decisive actions.
    - Use vivid, descriptive language to depict fast-paced actions, emergencies, and heroic efforts.

2. **Adaptability**:
    - **Simple Language**: If the user uses simple language or short sentences, respond in a clear, straightforward manner suitable for children, while maintaining educational and action elements.
    - **Complex Language**: If the user employs complex vocabulary and sophisticated sentence structures, respond with equally advanced language, providing in-depth and nuanced action sequences.
    - **Mixed Inputs**: If the user shows a mix of both, balance your responses to be accessible yet informative and action-oriented.

3. **Realism & Modern Technology**:
    - Base scenarios on realistic space missions and current technologies.
    - Highlight advancements in space technology, engineering, and related fields through action-driven plot points.

4. **Immersive Imagery**:
    - When generating image prompts, ensure they evoke a strong sense of presence and immersion within intense space environments.
    - Utilize vivid descriptions to create compelling and lifelike visuals that complement the action.

5. **Educational Focus**:
    - Seamlessly integrate factual information within thrilling narratives to educate users about space and technology.
    - Introduce scientific concepts and technological advancements as integral parts of overcoming challenges.

6. **Engagement**:
    - Craft narratives that are captivating, with clear objectives and intriguing, high-stakes challenges.
    - Encourage user participation by posing critical decisions or actions that influence the story's direction.

7. **Inclusivity**:
    - Use diverse characters and scenarios to appeal to a broad audience.
    - Avoid jargon unless appropriate for the user's language level, and provide explanations when necessary.

Example Scenarios:
- A sudden meteor shower threatens the Gateway Space Station, requiring immediate defensive measures.
- A critical life-support system failure forces the team to perform high-risk repairs in zero gravity.
- An unexpected solar flare disrupts communications, and the user must navigate the station to restore connectivity.

Always tailor your responses to match the user's input complexity, ensuring accessibility, educational value, and high-action engagement across all interactions.
Ensure that your response fits in the token context. Don't talk more than 200 words. Your job is to present them an intense scenario with options, and ask them what their next choice will be in some way. 
"""

def create_mp3_using_openai(script, voice="alloy", output_file="output.mp3"):
    """
    Generate an MP3 file from a given script using OpenAI's audio speech API.

    Args:
        script (str): The input text to convert to audio.
        voice (str): The voice setting for audio generation (default: "alloy").
        output_file (str): The name of the MP3 file to save (default: 'output.mp3').

    Returns:
        str: Path to the generated MP3 file or None if failed.
    """
    try:
        client = OpenAI()

        speech_file_path = Path(output_file)

        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=script
        )

        response.stream_to_file(speech_file_path)

        logging.info(f"MP3 file created successfully: {speech_file_path}")
        return str(speech_file_path)
    except Exception as e:
        logging.error(f"An error occurred during MP3 creation: {e}")
        return None

# ----------------------------
# 1. Image Optimization Function
# ----------------------------

def optimize_image(input_path, output_path, size=(800, 600)):
    """
    Resize and compress images to optimize performance.
    """
    try:
        with PILImage.open(input_path) as img:
            img.thumbnail(size, PILImage.ANTIALIAS)
            img.save(output_path, optimize=True, quality=85)
            print(f"Optimized image saved to {output_path}")
    except Exception as e:
        print(f"Error optimizing image {input_path}: {e}")

# ----------------------------
# 2. Define the CircularButton Class
# ----------------------------

class CircularButton(RecycleDataViewBehavior, ButtonBehavior, Label):
    """
    A circular button that behaves like a button and displays no text.
    Inherits from RecycleDataViewBehavior to work seamlessly with RecycleView.
    """
    exp_name = StringProperty("")
    navigate_callback = ObjectProperty(None)

    def refresh_view_attrs(self, rv, index, data):
        """
        Called when the view is refreshed. Sets the navigate_callback.
        """
        self.navigate_callback = rv.navigate_callback
        self.exp_name = data['exp_name']
        return super(CircularButton, self).refresh_view_attrs(rv, index, data)

    def on_release(self):
        """
        Called when the button is released. Triggers navigation.
        """
        if self.navigate_callback:
            self.navigate_callback(self.exp_name)

    def on_size(self, *args):
        """
        Ensures the button remains circular.
        """
        self.width = self.height

# Register CircularButton with Factory
Factory.register('CircularButton', cls=CircularButton)

# ----------------------------
# 3. Define the DashboardRecycleView Class
# ----------------------------

class DashboardRecycleView(RecycleView):
    """
    Custom RecycleView for displaying experiment buttons.
    """
    navigate_callback = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(DashboardRecycleView, self).__init__(**kwargs)
        self.data = []

    def populate_buttons(self, experiments, navigate_callback):
        """
        Populate RecycleView with experiment buttons.
        """
        self.navigate_callback = navigate_callback
        self.data = []
        for exp in experiments:
            self.data.append({
                'exp_name': exp['name'],
            })

# Register DashboardRecycleView with Factory
Factory.register('DashboardRecycleView', cls=DashboardRecycleView)

# ----------------------------
# 4. Define Screens
# ----------------------------

# Define the ExperimentScreen class
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
    experiments = ListProperty([])  # List to hold experiment data

    def on_pre_enter(self):
        print("DashboardScreen is setting up experiment buttons.")
        rv = self.ids.dashboard_recycleview
        rv.populate_buttons(self.experiments, self.navigate_to_experiment)

    def navigate_to_experiment(self, name):
        print(f"Navigating to {name} screen.")
        self.manager.current = name

    def ask_question(self):
        """
        Handles the 'Ask' button press. Sends the user's query to ChatGPT and displays the response.
        """
        user_query = self.ids.search_input_dashboard.text.strip()
        if not user_query:
            self.show_popup("Input Required", "Please enter a question before asking.")
            return

        # Clear previous results
        self.ids.search_results_label.text = "Loading..."

        # Disable the Ask button to prevent multiple requests
        self.ids.search_input_dashboard.disabled = True
        self.ids.children[0].disabled = True  # Assuming the first child is the 'Ask' button

        # Start a new thread to handle the API call
        threading.Thread(target=self.process_query, args=(user_query,)).start()

    def process_query(self, query):
        """
        Sends the user's query to OpenAI's ChatCompletion API using the specified client method and updates the UI with the response.
        """
        try:
            # Call OpenAI's ChatCompletion API
            response = client.chat.completions.create(
                model="gpt-4o",  # Using the GPT-4 Turbo model
                messages=[
                    {"role": "system", "content": """
                        You are an expert on the International Space Station (ISS). Provide concise and educational answers 
                        to questions about the ISS and its equipment without straying off topic. Ensure responses are clear, 
                        accurate, and suitable for an educational audience.
                    """},
                    {"role": "user", "content": query}
                ],
                max_tokens=100,  # Adjust token limit for the expected response length
                temperature=0.5,  # Balances creativity and factual accuracy
            )
            
            # Extract the assistant's reply
            answer = response.choices[0].message.content

            # Update the search results in the main thread
            Clock.schedule_once(lambda dt: self.display_answer(answer))

        except Exception as e:
            logging.error(f"Error during API call: {e}")
            Clock.schedule_once(lambda dt: self.display_answer("An error occurred while fetching the answer. Please try again later."))

    def display_answer(self, answer):
        """
        Displays the answer in the search_results_label and re-enables the input fields.
        """
        self.ids.search_results_label.text = f"[b]Q:[/b] {self.ids.search_input_dashboard.text}\n\n[b]A:[/b] {answer}"
        self.ids.search_input_dashboard.disabled = False
        self.ids.children[0].disabled = False  # Re-enable the 'Ask' button
        self.ids.search_input_dashboard.text = ""  # Clear the input field

    def show_popup(self, title, message):
        """
        Displays a popup with the given title and message.
        """
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message))
        btn = Button(text="OK", size_hint=(1, 0.25))
        content.add_widget(btn)
        popup = Popup(title=title, content=content, size_hint=(0.6, 0.4))
        btn.bind(on_release=popup.dismiss)
        popup.open()

# Define the HomeScreen
class HomeScreen(Screen):
    def go_to_dashboard(self, *args):
        self.manager.current = 'dashboard'

    def go_to_adventure(self, *args):
        self.manager.current = 'adventure'

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
        feedback_label = self.ids.feedback
        if selected_option == correct_answer:
            feedback_label.text = "Correct!"
            feedback_label.color = (0, 1, 0, 1)  # Green color
            print("User selected the correct answer.")
        else:
            feedback_label.text = "Incorrect. Try again."
            feedback_label.color = (1, 0, 0, 1)  # Red color
            print("User selected an incorrect answer.")

# Define the AdventureScreen
class AdventureScreen(Screen):
    story = StringProperty("")
    context = ListProperty([])
    interaction_count = 0
    max_interactions = 5
    difficulty = StringProperty("Medium")  # Default difficulty
    latest_audio_file = StringProperty("")
    is_audio_playing = BooleanProperty(False)
    recurring_elements = ListProperty([])  # For image consistency

    def __init__(self, **kwargs):
        super(AdventureScreen, self).__init__(**kwargs)
        self.recurring_elements = []  # List to track recurring elements

    def on_enter(self):
        logging.info("AdventureScreen entered.")
        self.story = "**Gateway Space Station Adventure**\n\n"
        self.context = []
        self.interaction_count = 0
        self.latest_audio_file = ""
        self.is_audio_playing = False
        self.start_adventure()

    def go_back_to_dashboard(self, *args):
        """
        Navigates back to the dashboard screen and resets the adventure.
        """
        logging.info("Navigating back to Dashboard from AdventureScreen.")
        self.reset_adventure()
        self.manager.current = 'dashboard'

    def reset_adventure(self):
        """
        Resets the adventure state to allow restarting.
        """
        self.story = "**Gateway Space Station Adventure**\n\n"
        self.context = []
        self.interaction_count = 0
        self.latest_audio_file = ""
        self.is_audio_playing = False
        self.ids.adventure_image.source = "assets/images/default.png"
        self.ids.adventure_image.reload()

    def start_adventure(self):
        """
        Initializes the adventure by generating the initial scenario using OpenAI.
        """
        initial_prompt = (
            "Begin your adventure at the Gateway Space Station orbiting the moon. Its the year 2024, and you are a NASA astronaut."
            "A sudden meteor shower hits the station's perimeter, causing extensive damage to the outer modules. "
            "As the lead engineer, you must act swiftly to secure the compromised areas and ensure the safety of the crew. "
            "Describe the immediate actions you take, the challenges you face, and how you utilize modern technology to stabilize the situation."
        )
        threading.Thread(target=self.generate_narration, args=(initial_prompt,)).start()
        

    def generate_narration(self, prompt):
        """
        Sends a prompt to OpenAI and appends the response to the story.
        """
        # Ensure OpenAI API key is set
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if not openai_api_key:
            logging.error("OpenAI API key not found. Please set the 'OPENAI_API_KEY' environment variable.")
            Clock.schedule_once(lambda dt: self.update_story("Narration could not be generated due to missing API key.\n"))
            return

        # Initialize the client
        client = openai.OpenAI(api_key=openai_api_key)

        # Initialize the message list with a system message if context is empty
        if not self.context:
            system_message = system_prompt
            self.context.append({"role": "system", "content": system_message})

        # Adjust prompt based on difficulty
        difficulty_prompt = f" The current difficulty level is {self.difficulty}. Adjust the intensity and complexity accordingly."

        # Append user prompt with difficulty
        full_prompt = prompt + difficulty_prompt
        self.context.append({"role": "user", "content": full_prompt})

        try:
            response = client.chat.completions.create(
                model="gpt-4o",  # Ensure this model exists and supports audio
                messages=self.context,
                max_tokens=350,
                temperature=0.7,  # Adjusted for balanced creativity
            )

            # Extract the narrated response from the API
            narration = response.choices[0].message.content
            # Format the narration with a divider and color
            formatted_narration = f"[color=00ff00]**Mission Control:**[/color]\n{narration}\n\n"  # Green color for AI
            Clock.schedule_once(lambda dt: self.update_story(formatted_narration))
            
            # Append assistant's response to context
            self.context.append({"role": "assistant", "content": narration})

            # Generate and save MP3 audio in a separate thread
            threading.Thread(target=self.generate_audio, args=(narration,)).start()

            # Generate and display image based on narration
            threading.Thread(target=self.generate_and_display_image, args=(narration,)).start()

            self.interaction_count += 1

            # If maximum interactions reached, generate performance rating
            if self.interaction_count >= self.max_interactions:
                Clock.schedule_once(lambda dt: self.rate_performance(), 1)

        except Exception as e:
            logging.error(f"Error generating narration: {e}")
            Clock.schedule_once(lambda dt: self.update_story("An error occurred while generating the narration. Please try again later.\n"))

    def generate_audio(self, text):
        """
        Generates an MP3 file from the AI's narration and stores the file path.
        """
        voice = "alloy"  # Define as needed
        output_file = "latest_response.mp3"

        audio_file_path = create_mp3_using_openai(
            script=text,
            voice=voice,
            output_file=output_file
        )

        if audio_file_path:
            # Update the latest audio file path
            Clock.schedule_once(lambda dt: setattr(self, 'latest_audio_file', audio_file_path))
        else:
            Clock.schedule_once(lambda dt: self.update_story("Failed to generate audio for the latest response.\n"))

    def play_audio(self):
        """
        Plays the latest AI response audio.
        """
        if not self.latest_audio_file:
            self.show_popup("No Audio Available", "There is no audio to play for the latest response.")
            return

        if self.is_audio_playing:
            self.show_popup("Audio Playing", "Audio is already playing.")
            return

        sound = SoundLoader.load(self.latest_audio_file)
        if sound:
            self.is_audio_playing = True
            sound.bind(on_stop=self.on_audio_stop)
            sound.play()
        else:
            self.show_popup("Error", "Failed to load the audio file.")

    def on_audio_stop(self, sound):
        """
        Callback when audio playback stops.
        """
        self.is_audio_playing = False

    def show_popup(self, title, message):
        """
        Shows a popup with the given title and message.
        """
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message))
        btn = Button(text="OK", size_hint=(1, 0.25))
        content.add_widget(btn)
        popup = Popup(title=title, content=content, size_hint=(0.6, 0.4))
        btn.bind(on_release=popup.dismiss)
        popup.open()

    def update_story(self, new_text):
        """
        Appends new_text to the story.
        """
        self.story += new_text
        self.ids.adventure_story.text = self.story

    def process_adventure_action(self):
        """
        Handles the user's action, sends it to OpenAI, and updates the story.
        """
        user_action = self.ids.adventure_input.text.strip()
        if not user_action:
            logging.info("No action entered.")
            self.show_popup("Input Required", "Please type an action before submitting.")
            return

        # Append user's action to the story with divider and color
        formatted_action = f"[color=ff0000]**You:**[/color] {user_action}\n\n"  # Red color for user
        Clock.schedule_once(lambda dt: self.update_story(formatted_action))

        # Append user action to context
        self.context.append({"role": "user", "content": user_action})

        # Clear the input field
        self.ids.adventure_input.text = ""

        # Generate AI response
        threading.Thread(target=self.generate_narration, args=(user_action,)).start()

    def rate_performance(self):
        """
        Generates a performance rating based on the user's decisions.
        """
        rating_prompt = (
            "Based on the following adventure, provide a performance rating for the player's decisions. "
            "Be honest but encouraging, highlighting both strengths and areas for improvement. Esnure the response is less than 200 words."
            "Format the rating as follows:\n\n"
            "Performance Rating:\n"
            "Score: X/10\n"
            "Comments: [Your comments here]"
        )
        
        # Append rating prompt to context
        self.context.append({"role": "user", "content": rating_prompt})

        # Send the rating prompt to OpenAI
        threading.Thread(target=self.generate_rating, args=(rating_prompt,)).start()

    def generate_rating(self, prompt):
        """
        Sends a prompt to OpenAI to rate the user's performance.
        """
        # Ensure OpenAI API key is set
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if not openai_api_key:
            logging.error("OpenAI API key not found. Please set the 'OPENAI_API_KEY' environment variable.")
            Clock.schedule_once(lambda dt: self.update_story("Performance rating could not be generated due to missing API key.\n"))
            return

        # Initialize the client
        client = openai.OpenAI(api_key=openai_api_key)

        try:
            response = client.chat.completions.create(
                model="gpt-4o",  # Ensure this model exists and supports audio
                messages=self.context,
                max_tokens=250,
                temperature=0.5,  # Balanced creativity
            )

            # Extract the rating from the response
            rating = response.choices[0].message.content
            # Format the rating with a divider and color
            formatted_rating = f"[color=ffff00]**Performance Rating:**[/color]\n{rating}\n"
            Clock.schedule_once(lambda dt: self.update_story(formatted_rating))

            # Generate and save MP3 audio of the rating
            threading.Thread(target=self.generate_audio, args=(rating,)).start()

            # Generate and display image based on rating
            threading.Thread(target=self.generate_and_display_image, args=(rating,)).start()

            # Disable input after rating
            Clock.schedule_once(lambda dt: self.disable_input())

        except Exception as e:
            logging.error(f"Error generating performance rating: {e}")
            Clock.schedule_once(lambda dt: self.update_story("An error occurred while generating the performance rating.\n"))

    def disable_input(self):
        """
        Disables the input field and submit button after performance rating.
        """
        self.ids.adventure_input.disabled = True
        self.ids.submit_button.disabled = True

    def toggle_difficulty(self, toggle, is_active):
        """
        Toggles the difficulty level based on user input.
        """
        if is_active:
            self.difficulty = "Hard"
            self.ids.difficulty_toggle.text = "Hard"
        else:
            self.difficulty = "Easy"
            self.ids.difficulty_toggle.text = "Easy"
        logging.info(f"Difficulty set to: {self.difficulty}")

        # Inform the AI about the difficulty change
        difficulty_message = f"The difficulty level has been set to {self.difficulty}."
        self.context.append({"role": "system", "content": difficulty_message})

        # Optionally, inform the user
        self.story += f"[color=ffff00]Difficulty set to {self.difficulty}.[/color]\n\n"
        self.ids.adventure_story.text = self.story


    def generate_and_display_image(self, narration):
        """
        Generates an image based on the narration and displays it in the UI.
        Ensures consistency by maintaining a base description or recurring elements.
        """
        try:
            # Smart Prompting for Consistency
            # Define a base description for the Gateway Space Station
            base_description = (
                    "the Gateway Moon Base, a modular and advanced lunar-orbiting space station, "
                    "featuring interconnected habitat modules with large observation windows, "
                    "robotic arms for maintenance and construction, solar panel arrays for power, "
                    "holographic communication centers, and multiple docking ports for spacecraft. "
                    "The base is illuminated by Earthlight and equipped with cutting-edge scientific equipment."
                )
            # Create a prompt for the image by combining the base description with the narration
            # Include recurring elements
            if self.recurring_elements:
                recurring_prompt = ", ".join(self.recurring_elements)
                image_prompt = f"{base_description}, featuring {recurring_prompt}. Scene: {narration}. Ensure the style is consistent with previous images for continuity."
            else:
                image_prompt = f"{base_description}. Scene: {narration}. Ensure the style is consistent with previous images for continuity."

            # Generate image using OpenAI's image API
            response = client.images.generate(
                model="dall-e-3",
                prompt=image_prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )

            image_url = response.data[0].url
            logging.info(f"Image URL generated: {image_url}")

            # Download the image
            image_path = self.download_image(image_url, "latest_scene.png")

            if image_path:
                # Optimize the image
                optimized_image_path = Path('assets/images/optimized') / "latest_scene.png"
                optimized_image_path.parent.mkdir(parents=True, exist_ok=True)
                optimize_image(image_path, optimized_image_path)

                # Update the image widget in the main thread
                Clock.schedule_once(lambda dt: self.update_image(str(optimized_image_path)))
            else:
                Clock.schedule_once(lambda dt: self.update_story("Failed to generate image for the latest response.\n"))

        except Exception as e:
            logging.error(f"Error generating image: {e}")
            Clock.schedule_once(lambda dt: self.update_story("An error occurred while generating the image.\n"))


    def extract_key_elements(self, text):
        """
        Extract key elements from text to maintain consistency.
        Placeholder for actual NLP extraction.
        """
        # Placeholder: return a list of key elements
        # Implement actual extraction logic as needed
        # For demonstration, let's return some dummy elements based on keywords
        elements = []
        keywords = ["control room", "central hub", "landing bay", "observation deck", "engine room"]
        for word in keywords:
            if word in text.lower():
                elements.append(word)
        return elements

    def download_image(self, url, filename):
        """
        Downloads an image from the given URL and saves it locally.
        """
        try:
            response = requests.get(url)
            if response.status_code == 200:
                image_path = Path('assets/images/downloaded') / filename
                image_path.parent.mkdir(parents=True, exist_ok=True)
                with open(image_path, 'wb') as f:
                    f.write(response.content)
                logging.info(f"Image downloaded and saved to {image_path}")
                return image_path
            else:
                logging.error(f"Failed to download image. Status code: {response.status_code}")
                return None
        except Exception as e:
            logging.error(f"Exception during image download: {e}")
            return None

    def update_image(self, image_path):
        """
        Updates the Image widget with the new image.
        """
        self.ids.adventure_image.source = image_path
        self.ids.adventure_image.reload()

    def reset_adventure(self):
        """
        Resets the adventure state to allow restarting.
        """
        self.story = "**Gateway Space Station Adventure**\n\n"
        self.context = []
        self.interaction_count = 0
        self.latest_audio_file = ""
        self.is_audio_playing = False
        self.ids.adventure_image.source = "assets/images/default.png"
        self.ids.adventure_image.reload()


# ----------------------------
# 5. Define the ScreenManager and App
# ----------------------------

class ISSExperimentApp(App):
    # Define window position variables here
    # (0, 0) represents the top-left corner
    WINDOW_X = 50  # X-coordinate for the window's left edge
    WINDOW_Y = 50  # Y-coordinate for the window's top edge

    def build(self):
        print("Building the application.")
        self.title = "ISS Experiments Educational App"
        Window.size = (1200, 800)  # Increased window size for better visibility

        # Set window position based on variables
        self.set_window_position(self.WINDOW_X, self.WINDOW_Y)

        # Load the KV file
        Builder.load_file('myapp.kv')

        # Initialize ScreenManager with a fade transition
        sm = ScreenManager(transition=FadeTransition(duration=1))  # 1-second fade

        # Add static screens to the manager
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        sm.add_widget(QuizScreen(name='quiz'))
        sm.add_widget(AdventureScreen(name='adventure'))

        # Load and optimize experiment data
        experiments = self.load_experiments()

        # Dynamically add ExperimentScreens
        for exp in experiments:
            print(f"Adding screen: {exp['name']}")
            # Determine image path
            experiment_image_path = Path(exp['image'])
            if not experiment_image_path.exists():
                print(f"Image for {exp['name']} not found at {experiment_image_path}. Using default image.")
                experiment_image_path = Path('assets/images/default.png')

            # Optimize image
            optimized_image_path = Path('assets/images/optimized') / experiment_image_path.name
            optimized_image_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists

            optimize_image(experiment_image_path, optimized_image_path)

            screen = ExperimentScreen(
                name=exp['name'],
                title=exp['title'],
                content=exp['content'],
                image_source=str(optimized_image_path)
            )
            sm.add_widget(screen)

        # Pass experiment data to DashboardScreen
        dashboard_screen = sm.get_screen('dashboard')
        dashboard_screen.experiments = experiments

        # Start with the splash screen
        sm.current = 'splash'

        # Bring the window to the front and focus it
        Clock.schedule_once(self.bring_window_to_front, 0)

        print("Application built successfully.")
        return sm

    def set_window_position(self, x, y):
        """
        Sets the window's top-left position based on the provided (x, y) coordinates.
        (0, 0) corresponds to the top-left corner of the primary display.
        """
        Window.left = x
        Window.top = y
        print(f"Window position set to ({x}, {y})")

    def bring_window_to_front(self, *args):
        """
        Brings the window to the front.
        """
        print("Bringing window to the front.")
        Window.raise_window()
        # Note: Removed Window.focus = True because focus is read-only

    def on_request_close(self, *args):
        print("Application is closing.")
        self.stop()  # Gracefully stop the Kivy application
        return True  # Indicate that the close request has been handled

    def on_stop(self):
        # Optional: Add any cleanup code here
        print("Application has closed gracefully.")

    def load_experiments(self):
        """
        Load experiments from the database and return a list of dictionaries.
        """
        locations = [
            "JEM EFU1", "JEM EFU2", "JEM EFU3", "JEM EFU4", "JEM EFU5", "JEM EFU6", "JEM EFU7",
            "JEM EFU8", "JEM EFU9", "JEM EFU10", "JEM EFU11", "JEM EFU12", "JEM EFU13",
            "Bartolomeo Slot2", "Bartolomeo Slot3", "Bartolomeo Slot5",
            "ELC-1 FRAM 3", "ELC-3 FRAM 3", "ELC-1 FRAM 8", "ELC-2 FRAM 3",
            "ELC-2 FRAM 7", "ELC-3 FRAM 5", "ELC-4 FRAM 2", "ELC-4 FRAM 3",
            "Columbus EPF1", "Columbus EPF3"
        ]

        db_data = []

        def query_by_location(location):
            # Connect to the database
            try:
                conn = sqlite3.connect("experiments.db")
                cursor = conn.cursor()

                # Query the database for the specified location
                cursor.execute('''
                    SELECT ExperimentName, Description, Image
                    FROM Experiments
                    WHERE Location = ?
                ''', (location,))

                result = cursor.fetchone()

                # Close the connection
                conn.close()

                # Check if a record was found
                if result:
                    experiment_name, description, image = result
                    db_data_input = {
                        'name': f'experiment_{len(db_data)+1}',
                        'module': location,
                        'title': experiment_name,
                        'content': description,
                        'image': f"assets/images/{image if image else 'default.png'}", 
                        #Adjust the location here. use a dictionary or a list to assign a location to each experiment
                        'location': (0.5, 0.5)  # Adjust as needed or retrieve from DB
                    }
                    return db_data_input
                else:
                    print(f"No data found for Location: {location}")
                    return None
            except sqlite3.Error as e:
                print(f"Database error: {e}")
                return None

        # Load and append experiment data
        for location in locations:
            data = query_by_location(location)
            if data:
                db_data.append(data)
            else:
                print(f"Skipping location '{location}' as no data was found.")

        print(f"Total experiments loaded: {len(db_data)}")
        return db_data

# Register HomeScreen with Factory
Factory.register('HomeScreen', cls=HomeScreen)

if __name__ == '__main__':
    ISSExperimentApp().run()
