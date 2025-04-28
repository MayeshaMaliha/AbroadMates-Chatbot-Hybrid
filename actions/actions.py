from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Dict, Text, Any, List
from dotenv import load_dotenv
import os
import requests
import random

class ActionAskGemini(Action):
    def name(self) -> Text:
        return "action_ask_gemini"

    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")  # Ensure your API key is loaded correctly
        self.model = "models/gemini-1.5-flash"  # Ensure the model name is correct
        self.url = f"https://generativelanguage.googleapis.com/v1beta/{self.model}:generateContent"
        self.headers = {"Content-Type": "application/json"}

        self.fallback_responses = {
            "scholarships in japan": "🎓 Scholarships in Japan:\n\n1. MEXT\n2. JASSO\n3. University-specific grants",
            "universities in germany": "🏛️ Top German universities:\n\n1. TU Munich\n2. LMU Munich\n3. Heidelberg",
            "default": "🤖 Sorry, I’m having trouble finding that. Try again later or rephrase!"
        }

        # List of funny responses for weird or philosophical queries
        self.funny_responses = [
            "Why don't skeletons fight each other? They don't have the guts.",
            "I told my computer I needed a break, and now it won't stop sending me Kit-Kats.",
            "Why don’t scientists trust atoms? Because they make up everything!",
            "I’m reading a book on anti-gravity. It’s impossible to put down!"
        ]

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        user_message = tracker.latest_message.get("text", "").strip().lower()

        if not self.api_key:
            dispatcher.utter_message("⚠️ Gemini API key missing.")
            return []

        # Check for funny or philosophical questions and provide a funny response
        if any(phrase in user_message for phrase in ["joke", "funny", "tell me a joke", "meaning of life", "do you know Allah", "robot"]):
            funny_reply = random.choice(self.funny_responses)  # Get a random funny reply
            dispatcher.utter_message(funny_reply)  # Send the funny message
            dispatcher.utter_message("Goodbye! Wishing you the best on your journey. 🌍")  # Say goodbye
            return []  # Exit after the response

        # Check for predefined fallback responses (like scholarships, universities)
        for key in self.fallback_responses:
            if key in user_message:
                dispatcher.utter_message(self.fallback_responses[key])
                return []

        # Prepare the payload for Gemini when fallback happens (unrecognized input)
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"You are a helpful AI assistant for study abroad questions. Please answer: {user_message}"
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 512
            }
        }

        try:
            # Send the request to Gemini API
            response = requests.post(
                self.url,
                headers=self.headers,
                params={"key": self.api_key},
                json=payload,
                timeout=10
            )
            response.raise_for_status()  # Raise an error if the API call fails
            result = response.json()

            if "candidates" in result and result["candidates"]:
                # Return the first valid response from Gemini
                reply = result["candidates"][0]["content"]["parts"][0]["text"]
                dispatcher.utter_message(reply)
            else:
                dispatcher.utter_message(self.fallback_responses["default"])

        except requests.exceptions.RequestException as e:
            # Handle exceptions when the API request fails
            print(f"Gemini API Error: {e}")
            dispatcher.utter_message(self.fallback_responses["default"])

        return []
