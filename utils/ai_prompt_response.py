import os
from google import genai

def ai_prompt_response(client: genai.Client, user_prompt:str) -> object:
  gemini_model = os.environ.get('GEMINI_MODEL')
  text_response = client.models.generate_content(model= gemini_model, contents=user_prompt)

  return text_response