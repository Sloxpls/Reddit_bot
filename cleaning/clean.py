import os
import shutil


def remove_subdirectories():
    directory_to_remove = "assets/temp/mp3"
    try:
        for item in os.listdir(directory_to_remove):
            item_path = os.path.join(directory_to_remove, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

