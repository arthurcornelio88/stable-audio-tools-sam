import os
import pandas as pd
from pathlib import Path
import logging
import argparse

def verify_renaming_with_csv(folder_path, csv_path):
    """
    Verify the consistency of renamed files by comparing them with the 'Title_URL' column
    in a CSV file, ensuring the filenames match the expected format: '<index>_<filename>'.

    Parameters:
    - folder_path: Path to the folder containing the renamed files.
    - csv_path: Path to the CSV file containing the 'Title_URL' column.
    """
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        logging.error(f"Error reading CSV file: {e}")
        return

    if 'Title_URL' not in df.columns:
        logging.error("'Title_URL' column is missing from the CSV file.")
        return

    files = [f for f in Path(folder_path).iterdir() if f.is_file()]

    discrepancies = []
    missing_files = []

    for index, row in df.iterrows():
        url_key = row['Title_URL'].rstrip('/').split('-')[-1]

        # Simplified expected filename pattern
        expected_filename_pattern = f"{index + 1}_"

        matching_files = [f for f in files if f.stem.startswith(expected_filename_pattern)]

        if not matching_files:
            missing_files.append(f"Row {index + 1}: Missing audio file with URL key '{url_key}'")
            logging.warning(f"Row {index + 1}: Missing audio file with URL key '{url_key}'")
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

    audio_files = [f for f in Path(folder_path).iterdir() if f.is_file()]
    json_files = [f for f in Path(json_folder_path).iterdir() if f.is_file()]

    audio_indices = set()  # To keep track of audio file indices
    json_indices = set()  # To keep track of JSON file indices
    duplicated_audio_files = []  # To store duplicated audio files

    for audio_file in audio_files:
        try:
            index = int(audio_file.stem.split("_")[0])
            if index in audio_indices:
                duplicated_audio_files.append(audio_file.name)
            else:
                audio_indices.add(index)
        except ValueError:
            logging.warning(f"Invalid audio filename format: {audio_file.name}")

    for json_file in json_files:
        try:
            index = int(json_file.stem.split("_")[0])
            json_indices.add(index)
        except ValueError:
            logging.warning(f"Invalid JSON filename format: {json_file.name}")

    missing_json_indices = audio_indices - json_indices
    extra_json_indices = json_indices - audio_indices

    if missing_json_indices or extra_json_indices or duplicated_audio_files:
        if missing_json_indices:
            print("Missing JSON files for the following audio indices: ", missing_json_indices)
        if extra_json_indices:
            print("Extra JSON files found for the following indices (no corresponding audio): ", extra_json_indices)
        if duplicated_audio_files:
            print("Duplicated audio files found: ", duplicated_audio_files)
    else:
        print("No discrepancies found between audio and JSON files, and no duplicated audio files.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Verify the consistency of renamed files with a CSV file and JSON files.')
    parser.add_argument('folder_path', type=str, help='Path to the folder containing renamed files')
    parser.add_argument('--csv', type=str, help='Path to the CSV file containing the title column', required=True)
    parser.add_argument('--json_folder', type=str, help='Path to the folder containing the JSON files', required=True)

    args = parser.parse_args()

    # Add logging configuration for better debugging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    verify_renaming_with_csv(args.folder_path, args.csv)
    verify_audio_with_json(args.folder_path, args.json_folder)
