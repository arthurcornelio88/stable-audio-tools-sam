import os
import argparse

def rename_json_files(json_folder, audio_folder):
    """
    Renames JSON files in `json_folder` to match the corresponding audio file names in `audio_folder`,
    assuming a consistent "1_filename" pattern.

    Args:
        json_folder: The path to the folder containing JSON files.
        audio_folder: The path to the folder containing audio files.
    """

    for audio_file in os.listdir(audio_folder):
        if audio_file.endswith((".mp3", ".wav", ".flac")):
            audio_prefix = audio_file.split("_")[0]  # Extract the integer prefix

            for json_file in os.listdir(json_folder):
                if json_file.startswith(audio_prefix + "_") and json_file.endswith(".json"):
                    new_json_name = audio_file.replace(audio_file.split(".")[-1], "json")
                    os.rename(os.path.join(json_folder, json_file), os.path.join(json_folder, new_json_name))
                    print(f"Renamed {json_file} to {new_json_name}")
                    break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rename JSON files to match corresponding audio file names.")
    parser.add_argument("json_folder", help="Path to the folder containing JSON files.")
    parser.add_argument("audio_folder", help="Path to the folder containing audio files.")
    args = parser.parse_args()

    rename_json_files(args.json_folder, args.audio_folder)
