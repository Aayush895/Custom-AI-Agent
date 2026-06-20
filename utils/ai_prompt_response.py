import os
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions

def ai_prompt_response(client: genai.Client, messages:list) -> object:
  gemini_model = os.environ.get('GEMINI_MODEL')

  text_response = client.models.generate_content(
    model= gemini_model, 
    contents=messages, 
    config=types.GenerateContentConfig(system_instruction=system_prompt, temperature=0, tools=[available_functions]),  
  )

  return text_response