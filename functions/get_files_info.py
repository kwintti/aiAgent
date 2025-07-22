import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get file's content, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file from where we are getting content from, relative to the working directory.",
            ),
        },
    ),
)
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a python script(file ending with .py) provided, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the python script that user provided in the prompt, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.OBJECT,
                description="Additional args for running the python script. Are optional.",
            ),
        },
    ),
)
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write provided content to the file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file in which we are going to write our content, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to be written to the file.",
            ),
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

def get_files_info(working_directory, directory="."):
    full_path = os.path.abspath(os.path.join(working_directory, directory))
    working_directory_full_path = os.path.abspath(working_directory)
    if not (
            full_path.startswith(working_directory_full_path + os.sep) or
            full_path == working_directory_full_path
            ):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'
    objects = os.listdir(full_path)
    to_return = []
    if directory == ".":
        to_return.append("Result for current directory:")
    else:
        to_return.append(f'Result for {directory} directory:')

    for obj in objects:
        try:
            size = os.path.getsize(os.path.join(full_path, obj))
            is_dir = os.path.isdir(os.path.join(full_path, obj))
        except OSError as e:
            size = f'Error: {str(e)}'
            is_dir = f'Error: {str(e)}'
        to_return.append(f' - {obj}: file_size={size} bytes, is_dir={is_dir}')

    return "\n".join(to_return)
