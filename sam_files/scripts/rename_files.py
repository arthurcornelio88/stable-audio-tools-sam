import os
from pathlib import Path

def rename_files_by_modification_time_reverse(folder_path):
    """
    Rename files in the given folder based on their last modification time in reverse order.

    Parameters:
    - folder_path: Path to the folder containing the files to rename.
    """
    # Get a list of all files in the directory
    files = [f for f in Path(folder_path).iterdir() if f.is_file()]

    # Sort files by last modified time in reverse order (most recent first)
    files.sort(key=lambda f: f.stat().st_mtime, reverse=True)

    # Rename files with a sequential index starting from 1
    for index, file in enumerate(files, start=1):
        # Create new filename with index prefix
        new_name = f"{index}_{file.name}"
        new_path = file.with_name(new_name)

        # Rename the file
        file.rename(new_path)
        print(f"Renamed '{file.name}' to '{new_name}'")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Rename files based on last modification time.')
    parser.add_argument('folder_path', type=str, help='Path to the folder containing files to rename')

    args = parser.parse_args()

    rename_files_by_modification_time_reverse(args.folder_path)
