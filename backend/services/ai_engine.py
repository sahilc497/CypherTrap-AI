import os
import json
import random
import sys
from typing import Dict, Any, List
from dotenv import load_dotenv

# Robust Google GenAI Import (Handling namespace conflicts)
try:
    from google import genai
    from google.genai import types
except ImportError:
    try:
        # Fallback for some environment configurations
        import google.genai as genai
        from google.genai import types
    except ImportError:
        genai = None
        types = None
        print("WARNING: Google GenAI SDK could not be imported. Check your installation.")

# Robust Mistral Import
try:
    from mistralai import Mistral
except ImportError:
    try:
        from mistralai.client import MistralClient as Mistral
    except ImportError:
        Mistral = None

load_dotenv()

class AIDeceptionEngine:
    def __init__(self):
        # Initialize Google Gemini
        self.gemini_client = None
        gemini_key = os.getenv("GEMINI_API_KEY")
        if gemini_key and genai:
            try:
                self.gemini_client = genai.Client(api_key=gemini_key)
            except Exception as e:
                print(f"Gemini Init Error: {e}")
            
        # Initialize Mistral as fallback
        self.mistral_client = None
        mistral_key = os.getenv("MISTRAL_API_KEY")
        if mistral_key and Mistral:
            try:
                self.mistral_client = Mistral(api_key=mistral_key)
            except Exception as e:
                print(f"Mistral Init Error: {e}")

    async def generate_fake_db_result(self, query: str) -> List[Dict[str, Any]]:
        """
        Generates a highly realistic, context-aware fake database result using LLM.
        """
        system_prompt = """
        You are a realistic production database. You must generate 3-5 rows of fake data in JSON format based on the user's SQL query.
        RULES:
        1. Output MUST be a valid JSON list of objects.
        2. Data must be highly realistic (e.g., internal company emails, realistic hashes, UUIDs).
        3. If the query asks for passwords, return bcrypt-like hashes.
        4. If the query is destructive (DROP/DELETE), return an empty list but your overall system will handle the success message.
        5. DO NOT include any explanatory text. ONLY the JSON list.
        """
        
        user_prompt = f"SQL QUERY: {query}"
        
        # Try Gemini first
        if self.gemini_client and genai:
            try:
                response = self.gemini_client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=[system_prompt, user_prompt],
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json"
                    )
                )
                return json.loads(response.text)
            except Exception as e:
                print(f"Gemini Error: {e}")

        # Try Mistral as fallback
        if self.mistral_client:
            try:
                # Handling both v1 and v2 client signatures
                if hasattr(self.mistral_client, 'chat'):
                    response = self.mistral_client.chat.complete(
                        model="mistral-tiny",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ]
                    )
                    return json.loads(response.choices[0].message.content)
            except Exception as e:
                print(f"Mistral Error: {e}")

        # Fallback to empty if both fail (Simulator will handle it)
        return []
