import os
from dotenv import load_dotenv
from google import genai
from functions.get_files_info import available_functions
from functions.call_function import call_function
import sys

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. When plan is ready you may call proper functions and invistigate further. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

Remember to list all steps. You are going to make multiple iterations and calls to get a correct answer. Use functions to investigate your solution and give response.text only at the end.


All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

if len(sys.argv) < 2:
    print("No enough arguments provided")
    sys.exit(1)
else:
    user_prompt = sys.argv[1]
    messages = [
                genai.types.Content(role="user", parts=[genai.types.Part(text=user_prompt)]),
                ]
    for i in range(20):
        response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=genai.types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
                )
        if response.text and not response.function_calls:
            print(response.text)
            break
        for candidate in response.candidates:
            messages.append(candidate.content)
        result = call_function(response.function_calls[0], True)
        if not result.parts[0].function_response.response:
            raise Exception("Return value is empty")
        messages.append(result)

    if len(sys.argv) == 3:
        if sys.argv[2] == "--verbose":
            print("User prompt: " + user_prompt)
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
