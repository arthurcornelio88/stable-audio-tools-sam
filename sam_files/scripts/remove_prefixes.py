import os
import re
import argparse

def remove_integer_prefix_from_filenames(folder_path):
    """
    Rename files in the specified folder by removing integer prefixes followed by an underscore from filenames.

    Parameters:
    - folder_path: Path to the folder containing the files.
    """
    # List all files in the directory
    files = os.listdir(folder_path)

    for file in files:
        # Match files with an integer prefix followed by an underscore
        match = re.match(r'^(\d+_)', file)
        if match:
            # Create the new filename by removing the integer prefix and underscore
            new_filename = file[match.end():]
            old_file_path = os.path.join(folder_path, file)
            new_file_path = os.path.join(folder_path, new_filename)

            # Rename the file
            os.rename(old_file_path, new_file_path)
            print(f"Renamed '{file}' to '{new_filename}'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Rename files by removing integer prefixes from filenames.')
    parser.add_argument('folder_path', type=str, help='Path to the folder containing files to rename')

    args = parser.parse_args()

    remove_integer_prefix_from_filenames(args.folder_path)
