import os
import pandas as pd
from pathlib import Path

def verify_renaming_with_csv(folder_path, csv_path):
    """
    Verify the consistency of renamed files by comparing them with the 'Title' column
    in a CSV file, ensuring the filenames match the expected format: '<index>_<Title>'.

    Parameters:
    - folder_path: Path to the folder containing the renamed files.
    - csv_path: Path to the CSV file containing the 'Title' column.
    Prompt pre-configured:

    python script_name.py /home/user/data/audio_files \
        --csv /home/user/data/titles.csv \
        --json_folder /home/user/data/json_files

    """
    # Read the CSV file
    df = pd.read_csv(csv_path)

    # Get a list of all files in the directory
    files = [f for f in Path(folder_path).iterdir() if f.is_file()]

    # Extract the expected filenames from the CSV
    discrepancies = []
    for file in files:
        # Extract the index from the filename
        file_index = file.stem.split('_')[0]

        # Find the corresponding row in the CSV by index
        try:
            expected_title = df.loc[int(file_index) - 1, 'Title']
            expected_filename = f"{file_index}_{expected_title}"

            # Compare only the index part
            if not file.name.startswith(f"{file_index}_"):
                discrepancies.append((file.name, expected_filename))
        except (IndexError, ValueError):
            discrepancies.append((file.name, "No corresponding index in CSV"))

    # Print results
    if not discrepancies:
        print("All files are correctly named according to the CSV.")
    else:
        print("Discrepancies found:")
        for actual, expected in discrepancies:
            print(f"File '{actual}' should be '{expected}'")

def verify_audio_with_json(folder_path, json_folder_path):
    """
    Verify that the index part of the filenames of audio files matches
    with the index part of JSON files in the specified folder and check for duplicated audio files.

    Parameters:
    - folder_path: Path to the folder containing the audio files.
    - json_folder_path: Path to the folder containing the JSON files.
    """
    # Get a list of all audio and JSON files in the directories
    audio_files = [f for f in Path(folder_path).iterdir() if f.is_file()]
    json_files = [f for f in Path(json_folder_path).iterdir() if f.is_file()]

    discrepancies = []
    duplicate_audio_files = []
    seen_files = set()

    for audio_file in audio_files:
        # Extract the index from the audio filename
        audio_index = audio_file.stem.split('_')[0]

        # Check for duplicates
        if audio_index in seen_files:
            duplicate_audio_files.append(audio_file.name)
        else:
            seen_files.add(audio_index)

        # Look for a matching JSON file by index
        matched = False
        for json_file in json_files:
            json_index = json_file.stem.split('_')[0]
            if audio_index == json_index:
                matched = True
                break

        if not matched:
            discrepancies.append(audio_file.name)

    # Print results
    if not discrepancies and not duplicate_audio_files:
        print("All audio files have matching JSON files and no duplicates were found.")
    else:
        if discrepancies:
            print("Discrepancies found:")
            for audio_file in discrepancies:
                print(f"Audio file '{audio_file}' does not have a matching JSON file.")
        if duplicate_audio_files:
            print("\nDuplicate audio files found:")
            for audio_file in duplicate_audio_files:
                print(f"Duplicate audio file: '{audio_file}'")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Verify the consistency of renamed files with a CSV file and JSON files.')
    parser.add_argument('folder_path', type=str, help='Path to the folder containing renamed files')
    parser.add_argument('--csv', type=str, help='Path to the CSV file containing the title column', required=True)
    parser.add_argument('--json_folder', type=str, help='Path to the folder containing the JSON files', required=True)

    args = parser.parse_args()

    verify_renaming_with_csv(args.folder_path, args.csv)
    verify_audio_with_json(args.folder_path, args.json_folder)
