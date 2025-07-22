import os

def write_file(working_directory, file_path, content):
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    working_directory_full_path = os.path.abspath(working_directory)
    if not os.path.commonpath([working_directory_full_path, full_path]) == working_directory_full_path:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    try:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
    except OSError as e:
        return f'Error: Couldn\'t create needed directories {file_path}: {e}'
    try:
        with open(full_path, "w") as file:
            file.write(content)

    except OSError as e:
        return f'Error: Couldn\'t write to file {file_path}: {e}'

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
