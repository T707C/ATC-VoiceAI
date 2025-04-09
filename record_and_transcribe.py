import sounddevice as sd
from scipy.io.wavfile import write
import whisper
import os

# === Settings ===
duration = 5  # seconds to record
filename = "recorded.wav"

print("Recording... Speak now!")
recording = sd.rec(int(duration * 44100), samplerate=44100, channels=1, dtype='int16')
sd.wait()
write(filename, 44100, recording)
print(f"Recording saved as {filename}")

# === Load Whisper and Transcribe ===
model = whisper.load_model("base")  # you can also try "tiny", "small", or "medium"

print("Transcribing...")
result = model.transcribe(filename)
print("\nTranscription:")
print(result["text"])

# Optional: clean up
# os.remove(filename)
