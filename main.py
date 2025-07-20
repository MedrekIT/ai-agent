import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.config import system_prompt
from functions.get_files_info import *
from functions.overwrite_files import *
from functions.run_files import *

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else: print(f" - Calling function: {function_call_part.name}")

    function_args = {'working_directory': './calculator'}
    function_args.update(function_call_part.args)

    if function_call_part.name == 'get_files_info':
        function_result = get_files_info(**function_args)
    elif function_call_part.name == 'get_file_content':
        function_result = get_file_content(**function_args)
    elif function_call_part.name == 'write_file':
        function_result = write_file(**function_args)
    elif function_call_part.name == 'run_python_file':
        function_result = run_python_file(**function_args)
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function_result},
            )
        ],
    )

if __name__ == "__main__":
    verbose = "--verbose" in sys.argv
    if len(sys.argv) > 1:
        prompt = sys.argv[1]
    else: raise Exception("There was no prompt provided")

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file
        ]
    )

    try:
        for _ in range(20):
            generated_response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                )
            )


            for response_variant in generated_response.candidates:
                messages.append(response_variant.content)

            if generated_response.function_calls:
                for function in generated_response.function_calls:
                    function_response = call_function(function, verbose)
                    if not function_response.parts[0].function_response.response:
                        raise Exception("Fatal error: no response")
                    if verbose:
                        print(f"-> {function_response.parts[0].function_response.response}")
                    messages.append(function_response)
            else:
                print(f"Final response:\n{generated_response.text}")
                break

        if verbose:
            print(f"User prompt: {prompt}")
            print(f"Prompt tokens: {generated_response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {generated_response.usage_metadata.candidates_token_count}")
    except Exception as e:
        print(f"{e}")