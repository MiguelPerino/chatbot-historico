from google import genai
from google.genai import types
import os

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
print("API KEY:", os.getenv('GEMINI_API_KEY'))
def call_llm(historico: list) -> str:
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=historico
        )
        return response.text
    except Exception as e:
        return f'Erro ao chamar a IA: {e}'

