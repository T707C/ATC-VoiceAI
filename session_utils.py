# session_utils.py

import sounddevice as sd
import numpy as np
import whisper
import os
import tempfile
import scipy.io.wavfile as wav
from rapidfuzz import fuzz
import tkinter as tk
from tkinter import messagebox

# Load Whisper Model (once)
model = whisper.load_model("base")

def record_audio(duration=5, sample_rate=16000):
    print("Recording...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
    sd.wait()
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    wav.write(temp_file.name, sample_rate, recording)
    return temp_file.name

def transcribe_audio(filename):
    print("Transcribing...")
    result = model.transcribe(filename)
    return result["text"]

def normalize_transcript(text):
    # Simple spoken number map
    num_map = {
        "zero": "0", "one": "1", "two": "2", "three": "3",
        "four": "4", "five": "5", "six": "6",
        "seven": "7", "eight": "8", "nine": "9"
    }

    words = text.lower().split()
    normalized = [num_map.get(word, word) for word in words]
    return " ".join(normalized)

def match_phrase(transcript, cowboy_mode=False):
    from phrasebook import faa_phrases

    normalized_transcript = normalize_transcript(transcript)

    best_match = None
    best_score = -1

    for call, data in faa_phrases.items():
        score = fuzz.ratio(normalized_transcript, call.lower())
        if score > best_score:
            best_match = call
            best_score = score

    expected = faa_phrases.get(best_match, {}).get("expected_response", "")

    if best_score >= 70:
        return expected, best_score
    else:
        root = tk.Tk()
        root.withdraw()
        response = messagebox.askyesno(
            "Low Match Score",
            f"Match score is {best_score}%.\nAccept this response?"
        )
        root.destroy()

        if response:
            return expected, best_score
        else:
            return "Unmatched/Incorrect", best_score
