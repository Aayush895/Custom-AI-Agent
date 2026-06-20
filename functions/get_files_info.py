import os
from google.genai import types

def get_files_info(working_directory: str, directory: str = ".") -> str:
  try:
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    # Will be True or False
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    if(valid_target_dir == False):
      return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if(os.path.isdir(target_dir) == False):
      return f'Error: "{directory}" is not a directory'

    fileContentList = [];
    for fileContent in os.listdir(target_dir):
      fileContentList.append({
        "name": fileContent,
        "size": os.path.getsize(os.path.join(target_dir, fileContent)),
        "is_dir": os.path.isdir(os.path.join(target_dir, fileContent))
      })

    fileInfo = ''
    for content in fileContentList:
      str = f"- {content['name']}: file_size={content['size']} bytes, is_dir={content['is_dir']}"
      fileInfo += str + "\n"

    return fileInfo
  except Exception as e:
    return f"Error: {e}"
  

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)