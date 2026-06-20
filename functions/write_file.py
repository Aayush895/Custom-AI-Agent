import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
  try:
    # fetch the absolute path of the working directory
    working_directory_abs_path = os.path.abspath(working_directory)

    # Join the path from working directory with the provided file path
    joined_file_path = os.path.join(working_directory_abs_path, file_path)

    # Normalise the file path / Clean the path from redundant things like '..', making it easier for the operating system to navigate the path
    normalised_file_path = os.path.normpath(joined_file_path)

    # Check if the normalised_file_path is within the working directory or not
    is_path_valid = os.path.commonpath([working_directory_abs_path, normalised_file_path]) == working_directory_abs_path
    if(is_path_valid == False):
      return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if(os.path.isdir(normalised_file_path) == True):
      return f'Error: Cannot write to "{file_path}" as it is a directory'
    
    os.makedirs(os.path.dirname(normalised_file_path), exist_ok=True)

    with open(normalised_file_path, "w") as f:
      f.write(content)
  
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
  except Exception as e:
    return f'Error: {e}'
