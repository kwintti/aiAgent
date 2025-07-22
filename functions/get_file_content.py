import os

MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    working_directory_full_path = os.path.abspath(working_directory)
    if not full_path.startswith(working_directory_full_path + os.sep):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(full_path, "r") as file:
            file_content_string = file.read(MAX_CHARS)
            next_char = file.read(1)

            if next_char:
                return file_content_string + f' [...File "{file_path}" truncated at {MAX_CHARS} characters]'
    except OSError as e:
        return f'Error: Couldnt read from file {file_path}: {e}'

    return file_content_string
