import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

if __name__ == "__main__":
    if len(sys.argv) > 1:
        prompt = sys.argv[1]
    else: raise Exception("There was no prompt provided")

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
        ]
    generated_response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages
        )
    print(generated_response.text)

    if "--verbose" in sys.argv:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {generated_response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {generated_response.usage_metadata.candidates_token_count}")