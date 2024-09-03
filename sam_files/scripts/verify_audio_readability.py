import os
import subprocess

def verify_audio_readability(folder_path):
    """
    Checks if audio files in a folder are readable by attempting to get their duration using ffprobe.

    Parameters:
    - folder_path: Path to the folder containing the audio files.

    Returns:
    - A tuple containing:
        - A list of readable files with their durations (list of tuples: (filename, duration))
        - A list of unreadable files (list of strings)
    """

    print(f"Checking audio files in: {folder_path}")
    readable_files = []
    unreadable_files = []

    for file in os.listdir(folder_path):
        if file.endswith((".mp3", ".wav", ".ogg", ".flac", ".m4a")):
            try:
                command = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', os.path.join(folder_path, file)]
                result = subprocess.run(command, capture_output=True, text=True)

                if result.returncode == 0:
                    duration = float(result.stdout)
                    if duration > 0:
                        readable_files.append((file, duration))  # Store filename and duration
                    else:
                        unreadable_files.append(file)
                        print(f"WARNING: Zero duration detected for {file}. Might be unreadable.")
                else:
                    unreadable_files.append(file)
                    print(f"Error reading {file}:")
                    print(result.stderr)

            except Exception as e:
                unreadable_files.append(file)
                print(f"Unexpected error checking {file}: {e}")

    if unreadable_files:
        print(f"\nWARNING: The following files might be unreadable: {unreadable_files}")
    else:
        print("\nAll audio files appear to be readable.")

    return readable_files, unreadable_files  # Return the results
