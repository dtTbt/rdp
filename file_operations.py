import shutil
import json
import os

from sundries import *


def move_files_and_delete_subfolders(folder_path):
    '''
    Input:
        folder_path (str) - The path of the folder where files and subfolders need to be processed.
    Output:
        None
    Func:
        Moves files from subfolders to the specified folder while handling naming conflicts, and then deletes empty
        subfolders within the specified folder.
    '''
    folder_path = uniform_path_format(folder_path)
    # Move files to the specified folder
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            dest_path = os.path.join(folder_path, file)
            if os.path.exists(dest_path):
                # Rename the file to avoid conflicts
                file_name, file_extension = os.path.splitext(file)
                counter = 1
                while os.path.exists(dest_path):
                    new_file_name = f"{file_name}_{counter}{file_extension}"
                    dest_path = os.path.join(folder_path, new_file_name)
                    counter += 1
            shutil.move(file_path, dest_path)
    # Delete empty subfolders
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)


def get_most_recent_subfolder(folder_path):
    '''
    Input:
        folder_path: A string representing the path of the folder.
    Output:
        most_recent_subfolder: A string representing the name of the most recent subfolder within the given folder.
    Func:
        This function takes a folder path as input and returns the name of the most recent subfolder within that folder.
        It first retrieves all the subfolders within the specified folder path. If no subfolders are found, it returns
        None. Otherwise, it identifies the most recent subfolder by comparing their creation times using the os.path.
        getctime function. Finally, it returns the name of the most recent subfolder.
    '''
    folder_path = uniform_path_format(folder_path)
    subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
    if not subfolders:
        return None
    most_recent_subfolder = max(subfolders, key=lambda f: os.path.getctime(os.path.join(folder_path, f)))
    return most_recent_subfolder


def modify_first_number(folder_path, A):
    '''
    for yolov8 format datasets
    2 inputs, one is a folder path and the other is an integer A. This folder has many txt files. Each txt file has
    many rows. Each line has 5 numbers, the first number is an integer, followed by 4 decimals.
    This function modifies the first number (i.e. that integer) in each line of each txt file to the integer A
    and then saves the file.
    '''
    folder_pathuniform_path_format = (folder_path)
    # Get a list of all files in the folder
    file_list = os.listdir(folder_path)
    # Iterate over each file
    for file_name in file_list:
        if file_name.endswith('.txt'):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as file:
                lines = file.readlines()
            # Modify the first number in each line
            modified_lines = []
            for line in lines:
                numbers = line.strip().split()
                if len(numbers) >= 5:
                    numbers[0] = str(A)
                    modified_lines.append(' '.join(numbers) + '\n')
            # Save the modified lines back to the file
            with open(file_path, 'w') as file:
                file.writelines(modified_lines)


def modify_autodl_gpu_txt_file(path):
    path = uniform_path_format(path)
    try:
        # Read the contents of the file
        with open(path, 'r') as file:
            lines = file.readlines()
        # Parse the contents and extract the required values
        port = lines[0].split('-p ')[1].split(' ')[0]
        username = lines[0].split('@')[0].split(' ')[-1]
        address = lines[0].split('@')[1].split('\n')[0]
        password = lines[1]
        # Modify the contents
        modified_content = f"Address:\n{address}\n\nPort:\n{port}\n\nUsername:\n{username}\n\nPassword:\n{password}"
        # Write the modified contents back to the file
        with open(path, 'w') as file:
            file.write(modified_content)
        print(f"File '{path}' successfully modified.")
    except FileNotFoundError:
        print(f"File '{path}' not found.")

def remove_empty_lines(file_path):
    """
    Removes empty lines from a text file.

    Args:
        file_path (str): The path to the text file.

    Returns:
        None
    """
    file_path = uniform_path_format(file_path)
    # Read the contents of the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Remove empty lines
    non_empty_lines = [line for line in lines if line.strip()]

    # Write the non-empty lines back to the file
    with open(file_path, 'w') as file:
        file.writelines(non_empty_lines)


def save_code_blocks_as_py(ipynb_file_path):
    """
    Saves the contents of all code blocks in an IPython Notebook (.ipynb) file as a .py file.

    Args:
        ipynb_file_path (str): The path to the IPython Notebook file.
    """
    ipynb_file_path = uniform_path_format(ipynb_file_path)
    # Read the contents of the .ipynb file
    with open(ipynb_file_path, 'r') as file:
        notebook = json.load(file)

    # Extract code from code cells
    code_blocks = []
    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            code_blocks.append(''.join(cell['source']))

    # Create a new .py file path
    ipynb_file_name = os.path.basename(ipynb_file_path)
    py_file_name = os.path.splitext(ipynb_file_name)[0] + '_py.py'
    py_file_path = os.path.join(os.path.dirname(ipynb_file_path), py_file_name)
    py_file_path = uniform_path_format(py_file_path)
    # Write code blocks to the .py file
    with open(py_file_path, 'w') as file:
        file.write('\n\n'.join(code_blocks))

    print(f"Code blocks saved to {py_file_path}")

def delete_all_files(folder_path):
    """
    Deletes all files within a folder.

    Args:
        folder_path (str): The path to the folder.

    Returns:
        None
    """
    try:
        # 遍历文件夹中的所有文件和子文件夹
        for root, dirs, files in os.walk(folder_path, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                os.rmdir(dir_path)
        print(f"All files in '{folder_path}' have been deleted.")
    except Exception as e:
        print(f"An error occurred: {e}")


def clear_large_file(file_path, max_size_mb):
    try:
        file_size = os.path.getsize(file_path)
        max_size_bytes = max_size_mb * 1024 * 1024
        if file_size > max_size_bytes:
            with open(file_path, 'w') as file:
                file.truncate(0)
            print(f"file '{file_path}' cleared.")
        else:
            print(f"file '{file_path}' is not large enough to be cleared.")

    except FileNotFoundError:
        print(f"file '{file_path}' not found.")


def get_folder_size_mb(folder_path):
    total_size = 0
    folder_path = os.path.abspath(folder_path)

    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)

    # Convert bytes to megabytes
    total_size_mb = total_size / (1024 * 1024)

    return total_size_mb


def get_disk_space(path='/'):
    statvfs = os.statvfs(path)

    # 块大小
    block_size = statvfs.f_frsize

    # 剩余块数
    blocks_available = statvfs.f_bavail

    # 计算剩余磁盘空间（以MB为单位）
    free_space_mb = (block_size * blocks_available) / (1024 ** 2)

    return free_space_mb
