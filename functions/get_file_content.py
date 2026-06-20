import os
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:

  try:
    absolute_path = os.path.abspath(working_directory)
    target_file_directory = os.path.normpath(os.path.join(absolute_path, file_path))
    is_valid_file_path = os.path.commonpath([target_file_directory, absolute_path]) == absolute_path
    if(is_valid_file_path == False):
      return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if(os.path.isfile(target_file_directory) == False):
      return f'Error: File not found or is not a regular file: "{file_path}"'
  
    #Reading a file till MAX_CHARS length
    content = read_file_contents(target_file_directory)
    return content
  
  except Exception as e:
    return f"Error: {e}"

def read_file_contents(file_path: str) -> str:
  with open(file_path, "r") as f:
      file_content_string = f.read(MAX_CHARS)
      # After reading the first MAX_CHARS...
      if f.read(1):
        file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
      return file_content_string