def get_custom_metadata(info, audio):
    """
    Associates a text prompt with each audio file based on its filename.

    Args:
        info (dict): Contains information about the audio file.
        audio (torch.Tensor): The audio tensor (you don't need to use this in this example).

    Returns:
        dict: A dictionary containing the custom metadata.
    """

    # 1. Get the filename from the info dictionary:
    filename = info["filename"]  # This is the full filename, including the extension (e.g., "file1.wav")
    print(filename)

    # 2. Extract the filename (without the extension) for your prompt lookup:
    filename_base = filename.split(".")[0]  # Now you have "file1"

    # 3. Create a dictionary of prompts (like a lookup table):
    prompts = {
        "audio1": "lofi",
        "audio2": "lofi",
        "audio3": "lofi",
        "audio4": "lofi",
        "audio5": "lofi",
        "audio6": "lofi",
        "audio7": "lofi",
        "audio8": "lofi",
        "audio9": "lofi",
        "audio10": "lofi"
    }

    # 4. Use the filename to get the prompt:
    prompt = prompts.get(filename_base, "A generic audio sample")

    # 5. Return the metadata:
    return {"prompt": prompt}
