from os import path
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the provided content to the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to be overwritten, relative to the working directory. If does not exist, will be created.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written to file",
            ),
        },
        required=["file_path", "content"],
    ),
)

def write_file(working_directory, file_path, content):
    try:
        full_path = path.abspath(path.join(path.abspath(working_directory), file_path))
        if not full_path.startswith(path.abspath(working_directory)):
            raise Exception(f"Error: Cannot write to \"{file_path}\" as it is outside the permitted working directory")
        
        with open(full_path, "w") as f:
            f.write(content)
        f.close()

        return f"Successfully wrote to \"{file_path}\" ({len(content)} characters written)"
    
    except Exception as e:
        return f"{e}"