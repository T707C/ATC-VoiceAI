# session_runner.py
import whisper
import sounddevice as sd
from scipy.io.wavfile import write
from rapidfuzz import fuzz
import os
from phrase_library import standard_phrases, cowboy_variants

def record_audio(filename="recorded.wav", duration=5):
    print("\nRecording... Speak now!")
    recording = sd.rec(int(duration * 44100), samplerate=44100, channels=1, dtype='int16')
    sd.wait()
    write(filename, 44100, recording)
    print("Recording saved.")

def transcribe_audio(filename="recorded.wav"):
    model = whisper.load_model("base")
    result = model.transcribe(filename)
    return result["text"]

def match_phrase(transcript, cowboy_mode=False):
    best_match = None
    highest_score = 0

    all_phrases = standard_phrases.copy()
    if cowboy_mode:
        # Merge cowboy phrases into the match pool
        for phrase, variants in cowboy_variants.items():
            all_phrases[phrase] += variants

    for standard, variants in all_phrases.items():
        for test_phrase in [standard] + variants:
            score = fuzz.ratio(transcript.lower(), test_phrase.lower())
            if score > highest_score:
                highest_score = score
                best_match = standard

    return best_match, highest_score

def run_session(config):
    record_audio()
    transcript = transcribe_audio()
    print(f"\nYou said: \"{transcript}\"")

    if config["phrase_matching"]:
        matched, score = match_phrase(transcript, cowboy_mode=config["cowboy_mode"])
        if matched:
            print(f"✅ Interpreted as: \"{matched}\" (Score: {score})")
        else:
            print("❌ No close phrase match found.")
    else:
        print("⚠ Phrase matching is off. Transcript only:")
        print(transcript)

    if config["live_feedback"]:
        input("\n[Press Enter to return to main menu]")
