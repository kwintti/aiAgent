from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python import run_python_file
from functions.write_file import write_file
from google.genai import types

functions = {"get_files_info": get_files_info,
             "get_file_content": get_file_content,
             "run_python_file": run_python_file,
             "write_file": write_file}


def call_function(function_call, verbose=False):
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")
    args_add = {"working_directory": "./calculator"} | function_call.args

    result = functions[function_call.name](**args_add)

    if function_call.name not in functions:
        return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_call.name,
                        response={"error": f"Unknown function: {function_call.name}"},
                        )
                    ],
                )
    return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call.name,
                    response={"result": result},
                    )
                ],
            )

