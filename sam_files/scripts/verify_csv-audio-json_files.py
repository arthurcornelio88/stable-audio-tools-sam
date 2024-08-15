import os
import pandas as pd
from pathlib import Path
import logging

def verify_renaming_with_csv(folder_path, csv_path):
    """
    Verify the consistency of renamed files by comparing them with the 'Title_URL' column
    in a CSV file, ensuring the filenames match the expected format: '<index>_<filename>'.

    Parameters:
    - folder_path: Path to the folder containing the renamed files.
    - csv_path: Path to the CSV file containing the 'Title_URL' column.
    """
    try:
        # Read the CSV file
        df = pd.read_csv(csv_path)
    except Exception as e:
        logging.error(f"Error reading CSV file: {e}")
        return

    # Ensure that the 'Title_URL' column exists
    if 'Title_URL' not in df.columns:
        logging.error("'Title_URL' column is missing from the CSV file.")
        return

    # Get a list of all files in the directory
    files = [f for f in Path(folder_path).iterdir() if f.is_file()]

    # Extract the expected filenames from the CSV
    discrepancies = []
    missing_files = []  # This will now track files that couldn't be downloaded

    for index, row in df.iterrows():
        # Extract the key (last number) from the 'Title_URL' column
        url_key = row['Title_URL'].rstrip('/').split('-')[-1]

        # Find the corresponding file in the folder (matching the key and the index)
        expected_filename = f"{index + 1}_"  # Start index from 1
        matching_files = [f for f in files if f.stem.startswith(expected_filename) and f.stem.endswith(url_key)]

        if not matching_files:
            # Since we couldn't find the audio file, check if there's a corresponding JSON
            json_filename = f"{index + 1}_"
            matching_json = [f for f in Path(args.json_folder).iterdir() if f.is_file() and f.stem.startswith(json_filename)]

            if not matching_json:
                # If no JSON, it means the download failed
                missing_files.append(f"Row {index + 1}: Failed to download file with URL key '{url_key}'")
                logging.warning(f"Row {index + 1}: Failed to download file with URL key '{url_key}'")
        elif len(matching_files) > 1:
            discrepancies.append(f"Row {index + 1}: Multiple audio files found for URL key '{url_key}': {[f.name for f in matching_files]}")
            logging.warning(f"Row {index + 1}: Multiple audio files found for URL key '{url_key}': {[f.name for f in matching_files]}")

    # Print results
    if not discrepancies and not missing_files:
        print("All files are correctly named according to the CSV, and no downloads failed.")
        logging.info("All files are correctly named according to the CSV, and no downloads failed.")
    else:
        if discrepancies:
            print("Discrepancies found:")
            logging.info("Discrepancies found:")
            for discrepancy in discrepancies:
                print(discrepancy)
                logging.info(discrepancy)
        if missing_files:
            print("\nFailed downloads:")
            logging.info("Failed downloads:")
            for missing_file in missing_files:
                print(missing_file)
                logging.info(missing_file)

def verify_audio_with_json(folder_path, json_folder_path):
    """
    Verify that the index part of the filenames of audio files matches
    with the index part of JSON files in the specified folder and check for duplicated audio files.

    Parameters:
    - folder_path: Path to the folder containing the audio files.
    - json_folder_path: Path to the folder containing the JSON files.
    """
    # ... (rest of the verify_audio_with_json function remains the same)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Verify the consistency of renamed files with a CSV file and JSON files.')
    parser.add_argument('folder_path', type=str, help='Path to the folder containing renamed files')
    parser.add_argument('--csv', type=str, help='Path to the CSV file containing the title column', required=True)
    parser.add_argument('--json_folder', type=str, help='Path to the folder containing the JSON files', required=True)

    args = parser.parse_args()

    verify_renaming_with_csv(args.folder_path, args.csv)
    verify_audio_with_json(args.folder_path, args.json_folder)
