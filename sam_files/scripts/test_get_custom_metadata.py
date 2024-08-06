import os
import json

def get_custom_metadata(info, audio):
    """
    Retrieve custom metadata from a JSON file associated with the audio file.

    Parameters:
    - info: Dictionary containing metadata information about the audio file.
    - audio: The audio file object (if needed for processing).

    Returns:
    - A dictionary with custom metadata.
    """
    # Get the relative path of the audio file
    audio_path = info.get("relpath", "")

    # Construct the path to the associated JSON file
    json_path = os.path.splitext(audio_path)[0] + '.json'

    # Initialize custom metadata
    custom_metadata = {}

    if os.path.exists(json_path):
        # Load metadata from the JSON file
        with open(json_path, 'r') as f:
            json_data = json.load(f)

        # Extract necessary fields from the JSON data
        custom_metadata = {
            "prompt": json_data.get("prompt", ""),
        }

    return custom_metadata

# Test the function
if __name__ == "__main__":
    test_info = {
        "relpath": "test_data/Engenho Vermelho.mp3"
    }
    test_audio = None  # Placeholder, not used in this example

    # Get custom metadata
    metadata = get_custom_metadata(test_info, test_audio)
    print("Metadata for audio1.wav:")
    print(metadata)

    # Test another file
    test_info = {
        "relpath": "test_data/Ponta Cabeça.wav"
    }
    metadata = get_custom_metadata(test_info, test_audio)
    print("\nMetadata for audio2.mp3:")
    print(metadata)
