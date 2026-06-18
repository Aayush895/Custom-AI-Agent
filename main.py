import os
import argparse
from dotenv import load_dotenv
from utils.fetch_client import fetch_client
from utils.ai_prompt_response import ai_prompt_response

def main() -> None:
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if(api_key == None):
        raise RuntimeError("API key was not found")
    
    #fetch the api client of gemini
    client = fetch_client(api_key)

    # fetch the user prompt which is passed as a command line argument
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument('user_prompt', type=str, help='User prompt')
    
    args = parser.parse_args()

    #fetch text based response from gemini client
    response = ai_prompt_response(client, args.user_prompt)
    if(response.usage_metadata == None):
        raise RuntimeError('API request failed')
    
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(response.text)

if __name__ == '__main__': main()
