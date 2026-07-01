import os
import re
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

class GeminiClient:
    """Wrapper class for interacting with the Google Gemini API using the NEW SDK"""
    
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = None
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
            
    def _ensure_configured(self):
        """Ensures that the API key and client are configured before making requests"""
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable is not configured. "
                "Please configure it in your environment or a .env file."
            )
        if not self.client:
            self.client = genai.Client(api_key=self.api_key)

    def ask_gemini(self, query: str) -> str:
        """
        Sends a query to Gemini and returns the generated text.
        
        Args:
            query (str): The prompt query.
            
        Returns:
            str: The raw string response from the LLM.
        """
        self._ensure_configured()
        try:
            response = self.client.models.generate_content(
                model="gemini-1.5-flash",
                contents=query
            )
            return response.text
        except Exception as e:
            raise RuntimeError(f"Gemini API request failed: {str(e)}")

    def generate_code(self, prompt: str) -> str:
        """
        Generates Python code based on a prompt and returns the clean code blocks.
        
        Args:
            prompt (str): Prompt describing the code requirements.
            
        Returns:
            str: Clean Python code.
        """
        self._ensure_configured()
        system_instruction = (
            "You are an expert Python coder. Generate ONLY valid Python code based on the user request. "
            "Do not include explanations, comments (unless critical), or HTML markup. "
            "Format the output inside a standard python code block using backticks."
        )
        
        try:
            response = self.client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction
                )
            )
            return self.extract_python_code(response.text)
        except Exception as e:
            raise RuntimeError(f"Code generation failed: {str(e)}")

    @staticmethod
    def extract_python_code(markdown_text: str) -> str:
        """
        Parses a markdown string to extract clean Python code from backticks.
        
        Args:
            markdown_text (str): The raw markdown string containing code.
            
        Returns:
            str: The extracted Python code.
        """
        # Match markdown block ```python ... ``` or ``` ... ```
        pattern = r"```(?:python)?\s*(.*?)\s*```"
        matches = re.findall(pattern, markdown_text, re.DOTALL)
        
        if matches:
            # Join multiple matches if they exist
            clean_code = "\n".join(matches).strip()
            return clean_code
            
        return markdown_text.strip()
