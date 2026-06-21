import os
import argparse
from dotenv import load_dotenv
from google.genai import types
from utils.fetch_client import fetch_client
from utils.ai_prompt_response import ai_prompt_response
from call_function import call_function

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
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    messages: list[types.Content] = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(20):
        #fetch text based response from gemini client
        response = ai_prompt_response(client, messages)
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)
            
        if(response.function_calls != None):
            function_results = []
            for i in range(len(response.function_calls)):
                function_call_result = call_function(response.function_calls[i], args.verbose)
                if(function_call_result.parts == None or len(function_call_result.parts) == 0 ):
                    raise Exception(f"No parts returned from function call: {response.function_calls[i].name}")
                if(function_call_result.parts[0].function_response == None):
                    raise Exception(f"No function response in result for: {response.function_calls[i].name}")
                if(function_call_result.parts[0].function_response.response == None):
                    raise Exception(f"No response data in function response for: {response.function_calls[i].name}")
                function_results.append(function_call_result.parts[0])
                if(args.verbose):
                    print(f"-> {function_call_result.parts[0].function_response.response}")
            messages.append(types.Content(role="user", parts=function_results))
        else:
            if(response.usage_metadata == None):
                raise RuntimeError('API request failed')
            if(args.verbose):
                print(f"User prompt: {args.user_prompt}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            print(response.text)
            break
    else:
        print(f"Maximum number of iterations has been reached: {20}")
        exit(1)

if __name__ == '__main__': main()
