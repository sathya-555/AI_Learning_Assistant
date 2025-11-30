import os
from google import genai
from google.genai import types

class AIStudyBuddy:
    def __init__(self, model_name='gemini-2.5-pro'):
        self.model = model_name
        self.client = None
        self.chat_session = None

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            api_key = "AIzaSyAin9LWjKoczb0kgJgC_Dnem_YMtdvWhSk"  # Replace with your key

        try:
            self.client = genai.Client(api_key=api_key)
        except Exception as e:
            print("Error:", e)
            self.client = None

    def _generate_response(self, system_instruction, user_prompt):
        if not self.client:
            return "Error: AI client not available."

        config = types.GenerateContentConfig(system_instruction=system_instruction)

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=user_prompt,
                config=config
            )
            return response.text
        except Exception as e:
            return f"API Error: {e}"

    # ---------- CHAT SYSTEM ----------
    def start_chat(self, topic):
        if not self.client:
            return "Error: AI not initialized."

        config = types.GenerateContentConfig(
            system_instruction=(
                f"You are a friendly study tutor for topic: {topic}. "
                "Keep explanations simple and clear."
            )
        )

        self.chat_session = self.client.chats.create(model=self.model, config=config)
        return f"Chat started! Ask anything about **{topic}**."

    def send_chat_message(self, message):
        if not self.chat_session:
            return "Chat not started yet."

        try:
            response = self.chat_session.send_message(message)
            return response.text
        except Exception as e:
            return f"Error sending message: {e}"

    # ---------- ONE-OFF FEATURES ----------
    def explain_concept(self, topic, target_level):
        system_instruction = (
            "Explain in simple terms. Use examples. Keep it student-friendly."
        )
        user_prompt = f"Explain '{topic}' for {target_level}."
        return self._generate_response(system_instruction, user_prompt)

    def summarize_notes(self, notes, format_style):
        system_instruction = "Summarize text concisely and extract important points."
        user_prompt = f"Summarize in {format_style}:\n{notes}"
        return self._generate_response(system_instruction, user_prompt)

    def generate_quiz(self, content, count, output_type):
        if output_type == "quiz":
            system_instruction = (
                "Generate MCQs with 4 options and provide answer key."
            )
            prompt = f"Create {count} MCQs from:\n{content}"
        else:
            system_instruction = (
                "Generate flashcards. Use 'Front:' and 'Back:'."
            )
            prompt = f"Create {count} flashcards from:\n{content}"

        return self._generate_response(system_instruction, prompt)
