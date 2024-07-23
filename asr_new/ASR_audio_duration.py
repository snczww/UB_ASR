import librosa

def calculate_audio_duration(audio):
    y, sr = librosa.load(audio, sr=None)
    duration = librosa.get_duration(y=y, sr=sr)
    return duration
