# screens/quiz.py
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ListProperty

class QuizScreen(Screen):
    question = StringProperty("What does ISS stand for?")
    options = ListProperty([
        "International Space Station",
        "Interstellar Space Shuttle",
        "Integrated Satellite System",
        "None of the above"
    ])
    correct_answer = StringProperty("International Space Station")

    def check_answer(self, selected_option):
        feedback_label = self.ids.feedback
        if selected_option == self.correct_answer:
            feedback_label.text = "Correct!"
            feedback_label.theme_text_color = "Custom"
            feedback_label.text_color = (0, 1, 0, 1)  # Green
        else:
            feedback_label.text = "Incorrect. Try again."
            feedback_label.theme_text_color = "Custom"
            feedback_label.text_color = (1, 0, 0, 1)  # Red

    def go_back_to_dashboard(self, *args):
        self.manager.current = 'dashboard'
