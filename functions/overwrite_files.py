from os import path

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