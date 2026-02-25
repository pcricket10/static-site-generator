import os
import shutil


def copy_files_recursive(source, destination):
    if not os.path.exists(destination):
        os.mkdir(destination)
    dir_list = os.listdir(source)
    if dir_list == []:
        return
    for item in dir_list:
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)
        if os.path.isdir(source_path):
            copy_files_recursive(source_path, destination_path)
        elif os.path.isfile(source_path):
            shutil.copy(source_path, destination_path)
