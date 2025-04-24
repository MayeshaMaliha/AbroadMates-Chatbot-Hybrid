from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from typing import Dict, Text, Any, List
from dotenv import load_dotenv
import os
import requests
import json

class ActionAskGemini(Action):
    def name(self) -> Text:
        return "action_ask_gemini"

    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = "models/gemini-1.5-flash"
        self.url = f"https://generativelanguage.googleapis.com/v1beta/{self.model}:generateContent"
        self.headers = {"Content-Type": "application/json"}

        self.fallback_responses = {
            "scholarships in japan": (
                "🎓 Scholarships in Japan:\n\n1. MEXT\n2. JASSO\n3. University-specific grants"
            ),
            "universities in germany": (
                "🏛️ Top German universities:\n\n1. TU Munich\n2. LMU Munich\n3. Heidelberg"
            ),
            "default": (
                "🤖 Sorry, I’m having trouble finding that. Try again later or rephrase!"
            )
        }

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

        # Check for simple fallback patterns first
        for key in self.fallback_responses:
            if key in user_message:
                dispatcher.utter_message(self.fallback_responses[key])
                return []

        # Prepare payload for Gemini
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
            response = requests.post(
                self.url,
                headers=self.headers,
                params={"key": self.api_key},
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            result = response.json()

            if "candidates" in result and result["candidates"]:
                reply = result["candidates"][0]["content"]["parts"][0]["text"]
                dispatcher.utter_message(reply)
            else:
                dispatcher.utter_message(self.fallback_responses["default"])

        except Exception as e:
            print(f"Gemini API Error: {e}")
            dispatcher.utter_message(self.fallback_responses["default"])

        return []
