import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()
    api_key = os.environ.get('GEMINI_API_KEY')
    if api_key == None:
        raise RuntimeError('API key not found')
    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description='Custom AI agent based on Gemini model')
    parser.add_argument('user_prompt', type=str, help='Please provide a prompt by user')
    args = parser.parse_args()

    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]

    response = client.models.generate_content(model='gemini-2.5-flash', contents=messages)

    if(response.usage_metadata == None): 
        raise RuntimeError('API request has been failed, please check your token limit!')
    
    print(f"User Prompt: {args.user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(f"Response: {response.text}")

if __name__ == "__main__":
    main()
