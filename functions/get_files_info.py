from os import path, listdir
from functions.config import char_limit

def get_file_content(working_directory, file_path):
    try:
        full_path = path.abspath(path.join(path.abspath(working_directory), file_path))
        if not full_path.startswith(path.abspath(working_directory)):
            raise Exception(f"Error: Cannot read \"{file_path}\" as it is outside the permitted working directory")
        
        if not path.isfile(full_path):
            raise Exception(f"Error: File not found or is not a regular file: \"{file_path}\"")
        
        with open(full_path) as f:
            file_contents = f.read()
            if len(file_contents) >= char_limit:
                file_contents = f"{file_contents[:char_limit]}[...File \"{file_path}\" truncated at {char_limit} characters]"
        f.close()

        return file_contents
    
    except Exception as e:
        return f"{e}"

def get_files_info(working_directory, directory="."):    
    try:
        full_path = path.join(working_directory, directory)
        if not path.abspath(full_path).startswith(path.abspath(working_directory)):
            raise Exception(f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory")
        
        if not path.isdir(full_path):
            raise Exception(f"Error: \"{directory}\" is not a directory")
        
        dir_contents = []
        for element in listdir(full_path):
            dir_contents.append(f"- {element}: file_size={path.getsize(path.join(full_path, element))} bytes, is_dir={path.isdir(path.join(full_path, element))}")
        
        return "\n".join(dir_contents)
    
    except Exception as e:
        return f"{e}"