import os
import json
import logging
from dotenv import load_dotenv
from google import genai
from mistralai.client import Mistral

load_dotenv()
logger = logging.getLogger("AIDeceptionEngine")

class AIDeceptionEngine:
    def __init__(self):
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.mistral_key = os.getenv("MISTRAL_API_KEY")
        
        # Initialize Gemini (using new google-genai SDK)
        self.gemini_client = None
        if self.gemini_key:
            try:
                self.gemini_client = genai.Client(api_key=self.gemini_key)
                logger.info("AI Engine: Gemini provider initialized.")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini: {e}")
        
        # Initialize Mistral
        self.mistral_client = None
        if self.mistral_key:
            try:
                self.mistral_client = Mistral(api_key=self.mistral_key)
                logger.info("AI Engine: Mistral provider initialized.")
            except Exception as e:
                logger.error(f"Failed to initialize Mistral: {e}")

    async def _call_llm(self, prompt: str, system_instruction: str = ""):
        """Call the available LLM provider (Gemini preferred, then Mistral)."""
        # 1. Try Gemini
        if self.gemini_client:
            try:
                # Synchronous call for now (SDK supports sync/async)
                response = self.gemini_client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=prompt,
                    config={'system_instruction': system_instruction}
                )
                return response.text
            except Exception as e:
                logger.error(f"Gemini error: {e}")

        # 2. Try Mistral
        if self.mistral_client:
            try:
                chat_response = self.mistral_client.chat.complete(
                    model="mistral-tiny",
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": prompt}
                    ]
                )
                return chat_response.choices[0].message.content
            except Exception as e:
                logger.error(f"Mistral error: {e}")

        return None

    async def generate_fake_db_result(self, query: str):
        """Generates realistic synthetic data based on a SQL query."""
        system_instruction = "You are a realistic database engine simulator. Return ONLY pure JSON data."
        prompt = f"""
        The user executed: "{query}"
        Generate a realistic, synthetic JSON response representing the rows of data.
        - If SELECT query, return a JSON list of objects.
        - Use realistic mock data (names, emails, dates).
        - No markdown formatting, no explanations, just the JSON array.
        """

        content = await self._call_llm(prompt, system_instruction)
        if content:
            try:
                # Clean up markdown if AI included it
                clean_content = content.replace("```json", "").replace("```", "").strip()
                return json.loads(clean_content)
            except Exception as e:
                logger.error(f"JSON parsing error: {e}")
        
        return self._get_mock_response(query)

    def _get_mock_response(self, query: str):
        """Fallback mock response if AI is unavailable."""
        if "users" in query.lower():
            return [
                {"id": 1, "username": "admin", "email": "admin@internal.local", "role": "superuser"},
                {"id": 2, "username": "backup_agent", "email": "agent@internal.local", "role": "backup"}
            ]
        return {"status": "success", "rows_affected": 0}

    async def generate_error_message(self, context: str):
        """Generates a believable system error message."""
        system_instruction = "You are a technical system administrator."
        prompt = f"Generate a highly realistic, technical system error message for this context: {context}. Keep it under 20 words."
        
        content = await self._call_llm(prompt, system_instruction)
        return content.strip() if content else "ERR_CONNECTION_REFUSED: Internal socket error."
