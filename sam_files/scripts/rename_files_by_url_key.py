import os
from pathlib import Path
import pandas as pd

def rename_files_by_url_key(folder_path, df, url_column='Title_URL'):
    """
    Rename files in the given folder based on the unique key extracted from the Title_URL column in a DataFrame.

    Parameters:
    - folder_path: Path to the folder containing the files to rename.
    - df: DataFrame containing file information.
    - url_column: The column in the DataFrame that contains the URLs to extract the key for renaming.
    """
    # Get a list of all files in the directory
    files = [f for f in Path(folder_path).iterdir() if f.is_file()]

    for index, row in df.iterrows():
        # Extract the unique key from the Title_URL (last part after the final hyphen)
        url_key = row[url_column].rstrip('/').split('-')[-1]

        # Find the matching file based on the URL key
        matching_files = [f for f in files if f.stem.endswith(url_key)]

        if matching_files:
            # Assuming the key uniquely identifies each file
            matching_file = matching_files[0]

            # Create new filename with index prefix
            new_name = f"{index+1}_{matching_file.name}"
            new_path = matching_file.with_name(new_name)

            # Rename the file
            matching_file.rename(new_path)
            print(f"Renamed '{matching_file.name}' to '{new_name}'")
        else:
            print(f"No matching file found for URL key '{url_key}'")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Rename files based on the unique key from the Title_URL column in a DataFrame.')
    parser.add_argument('folder_path', type=str, help='Path to the folder containing files to rename')
    parser.add_argument('csv_path', type=str, help='Path to the CSV file containing the DataFrame')
    parser.add_argument('--url_column', type=str, default='Title_URL', help='Column name in the DataFrame with URLs to extract the key (default is "Title_URL")')

    args = parser.parse_args()

    # Load the DataFrame, skipping the header row (index starts at 1 naturally)
    df = pd.read_csv(args.csv_path)

    rename_files_by_url_key(args.folder_path, df, args.url_column)
