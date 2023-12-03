import librosa

# It is written to analze tempo of the sound tracks in Beats Per Second
fileName = 'Crema/1091_WSI_DIS_XX.wav'

# Load a built-in audio sample (example: Beat loop)
y, sr = librosa.load(fileName)
# Estimate the tempo and beat events
tempo, beats = librosa.beat.beat_track(y=y, sr=sr)

print(f"Estimated Tempo of {fileName}: {tempo} BPM")
print("Beat Frames:", beats)
