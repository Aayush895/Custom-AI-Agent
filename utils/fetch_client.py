from google import genai

def fetch_client(api_key: str) -> genai.Client:
  client = genai.Client(api_key=api_key)
  return client