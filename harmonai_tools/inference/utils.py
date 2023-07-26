from ..data.utils import PadCrop

from torchaudio import transforms as T

def prepare_audio(audio, in_sr, target_sr, target_length, target_channels, device):
    
    audio = audio.to(device)

    if in_sr != target_sr:
        resample_tf = T.Resample(in_sr, target_sr).to(device)
        audio = resample_tf(audio)

    audio = PadCrop(target_length, randomize=False)(audio)

    # Add batch dimension if needed
    if len(audio.shape) == 2:
        audio = audio.unsqueeze(0)

    if target_channels == 1:
        # Convert to mono
        audio = audio.mean(1, keepdim=True)
    elif target_channels == 2:
        # Convert to stereo
        if audio.shape[1] == 1:
            audio = audio.repeat(1, 2, 1)
        elif audio.shape[1] > 2:
            audio = audio[:, :2, :]

    return audio