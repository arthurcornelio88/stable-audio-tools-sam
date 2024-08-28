import os
import shutil
from datetime import datetime
from dotenv import set_key

def reorganize_files(source_folders, destination_folder):
    """
    Reorganizes all files from multiple source folders into a single destination folder,
    renaming them with prefixes based on their original folder names and a sequential number.

    Args:
        source_folders: A list of paths to the source folders containing files.
        destination_folder: The path to the destination folder where the reorganized files will be placed.
    """

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    destination_folder = f"{destination_folder}_{timestamp}"

    os.makedirs(destination_folder, exist_ok=True)

    for source_folder in source_folders:
        file_counter = 1
        for filename in os.listdir(source_folder):
            prefix = os.path.basename(source_folder)
            # Keep the original filename as is (no timestamp removal)
            new_filename = f"{prefix}_{filename}"
            shutil.copy2(os.path.join(source_folder, filename), os.path.join(destination_folder, new_filename))
            print(f"Copied {filename} to {destination_folder}/{new_filename}")
            file_counter += 1

    # Store the timestamp in the .env file
    set_key(".env", "TIMESTAMP_DF", timestamp)
    print(f"Timestamp '{timestamp}' added to .env file!")

if __name__ == "__main__":
    source_folders = ["dataframes/checked", "dataframes/filtered_by_genre", "dataframes/scrapped"]
    destination_folder = "dataframes"

    reorganize_files(source_folders, destination_folder)
