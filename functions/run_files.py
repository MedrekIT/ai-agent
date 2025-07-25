from os import path
from subprocess import run
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes the specified Python file and returns the output from the interpreter, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file with code to run, relative to the working directory. Has to be provided and has to be a python file",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"]
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    try:
        full_path = path.abspath(path.join(path.abspath(working_directory), file_path))
        if not full_path.startswith(path.abspath(working_directory)):
            raise Exception(f"Cannot execute \"{file_path}\" as it is outside the permitted working directory")
        
        if not path.isfile(full_path):
            raise Exception(f"File \"{file_path}\" not found.")
        
        if not file_path.endswith(".py"):
            raise Exception(f"\"{file_path}\" is not a Python file.")
        
        commands = ["python", full_path]
        if args:
            commands.extend(args)
        
        completed_result = run(commands, capture_output=True, text=True, timeout=30, cwd=path.abspath(working_directory))

        output = []
        if completed_result.stdout:
            output.append(f"STDOUT:\n{completed_result.stdout}")
        if completed_result.stderr:
            output.append(f"STDERR:\n{completed_result.stderr}")
        
        if completed_result.returncode != 0:
            output.append(f"Process exited with code {completed_result.returncode}")
        
        return "\n".join(output) if output else "No output produced."

    except Exception as e:
        return f"Error: {e}"