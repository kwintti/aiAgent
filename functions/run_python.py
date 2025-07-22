import os
import subprocess


def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    working_directory_full_path = os.path.abspath(working_directory)
    if not os.path.commonpath([working_directory_full_path, full_path]) == working_directory_full_path:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'
    if not full_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        run_out = subprocess.run(["uv", "run", full_path, *args], timeout=30, capture_output=True, text=True)
    except OSError as e:
        return f"Error: executing Python file: {e}"
    if run_out.returncode != 0:
        return f'STDOUT:\n{run_out.stdout} \nSTDERR: {run_out.stderr}\nProcess exited with code {run_out.returncode}'
    if len(run_out.stdout) == 0 and len(run_out.stderr) == 0:
        return f'No output produced'

    return f'STDOUT:\n{run_out.stdout} \nSTDERR: {run_out.stderr}'
