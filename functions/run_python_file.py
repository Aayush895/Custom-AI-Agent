import os
import subprocess
from google.genai import types

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
  try:
    # Find the absolute path of the working directory
    working_directory_abs_path = os.path.abspath(working_directory)

    # Join the file path with the abs path of the working directory
    joined_file_path = os.path.join(working_directory_abs_path, file_path)

    # Normalize the joined path
    normalised_joined_path = os.path.normpath(joined_file_path)

    # Check whether the normalised path and the working directory abs path have a common path which is equal to the working directory absolute path
    is_valid_normalised_path = os.path.commonpath([working_directory_abs_path, normalised_joined_path]) == working_directory_abs_path

    if(is_valid_normalised_path == False):
      return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if(os.path.isfile(normalised_joined_path) == False):
      return f'Error: "{file_path}" does not exist or is not a regular file'
    if(normalised_joined_path.endswith('.py') == False):
      return f'Error: "{file_path}" is not a Python file'
    
    # Starting sub-processes
    command = ['python', normalised_joined_path]
    if(args != None and len(args) != 0):
      command.extend(args)
    
    completed_process = subprocess.run(command, cwd=working_directory_abs_path, capture_output=True, text=True, timeout=30)
    if(completed_process.returncode != 0):
      return f'Process exited with code {completed_process.returncode}'
    if(completed_process.stderr == '' and completed_process.stdout == ''):
      return f'No output produced'
    
    output_string = ''
    if(completed_process.stdout):
      output_string += f'STDOUT: {completed_process.stdout}'
    if(completed_process.stderr):
      output_string += f'STDERR: {completed_process.stderr}'
    return output_string
  
  except Exception as e:
    return f"Error: executing Python file: {e}"
  
schema_run_python_file = types.FunctionDeclaration(
  name='run_python_file',
  description='This functions runs the specified python file defined in the file path if it is in the working directory',
  parameters=types.Schema(
    type=types.Type.OBJECT,
    required=['file_path'],
    properties= {
      'file_path': types.Schema(
        type=types.Type.STRING,
        description='Path of the file which the LLM is supposed to run'
      ),
      'args': types.Schema(
        type=types.Type.ARRAY,
        description='Contains additional arguments which may be required for file execution',
        items=types.Schema(type=types.Type.STRING)
      )
    }
  )
)