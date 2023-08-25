import inspect
import os
import shutil
import platform
import subprocess
import time


def convert_to_unix_path(windows_path):
    unix_path = windows_path.replace('\\', '/')
    return unix_path


def uniform_path_format(path):
    if '\\' in path:  # Windows format
        return convert_to_unix_path(path)
    else:  # Linux format
        return path


def analyze_tensor(input_tensor):
    print("\n##### analyze_tensor_st #####")
    # Output the variable name
    print("1.Name:")
    frame = inspect.currentframe().f_back
    var_name = 'Unable'
    for name, value in frame.f_locals.items():
        if value is input_tensor:
            var_name = name
            break
    print(var_name)
    # Shape of the tensor
    print("2.Shape:")
    print(tuple(input_tensor.shape))
    # Content of the tensor
    tensor_content = input_tensor.tolist()
    print("3.Content:")
    print(str(input_tensor))
    print("##### analyze_tensor_ed #####")


def analyze_tensor_s(*args):
    for Unable in args:
        analyze_tensor(Unable)


def move_files_and_delete_subfolders(folder_path):
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


def shutdown_if_linux_not_windows(tim):
    time.sleep(tim)
    if platform.system() == 'Linux' and platform.system() != 'Windows':
        os.system('shutdown -h now')


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
