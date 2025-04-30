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
import re
from num2words import num2words
import string

# Load Whisper Model
model = whisper.load_model("base")

#Normalize text: lowercase and remove punctuation
def normalize_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text.strip()

def record_audio(duration=5, sample_rate=16000):
    print("Recording...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
    sd.wait()
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    wav.write(temp_file.name, sample_rate, recording)
    return temp_file.name

def normalize_numbers(text):
    """Normalize numbers into words, but avoid combining multi-digit numbers."""
    def replace_func(match):
        number = match.group(0)
        # Only convert individual digits
        if len(number) == 1:
            return num2words(number).replace("-", " ")  # e.g., "2" → "two"
        return number  # Do not convert multi-digit numbers like "27"
    
    return re.sub(r'\b\d+\b', replace_func, text)

def transcribe_audio(filename):
    print("Transcribing...")
    result = model.transcribe(filename)
    text = result["text"]                   # Save the transcription text
    text = normalize_numbers(text.lower())  # Normalize numbers and convert to lowercase
    return text

def digits_to_words(text):
    """Convert individual digits to words, e.g., 1 → one, 7 → seven."""
    digit_word_map = {
        "0": "zero", "1": "one", "2": "two", "3": "three",
        "4": "four", "5": "five", "6": "six",
        "7": "seven", "8": "eight", "9": "nine"
    }

    def split_number(match):
        number = match.group()
        return ' '.join(digit_word_map.get(d, d) for d in number)
    
    text = text.replace("-", " ")  # Replace hyphens with spaces
    text = re.sub(r'\b\d+\b', split_number, text)
    return text

def normalize_transcript(text):
    """Normalize the transcript (convert to lowercase and strip extra spaces)."""
    return text.lower().strip()

def match_phrase(transcript, pilot_phrase, parent=None):
    from phrasebook import faa_phrases

    transcript = digits_to_words(transcript)           #digit to word conversion
    normalized_transcript = normalize_text(transcript)  #remove punctuation too

    expected = faa_phrases.get(pilot_phrase, {}).get("expected_response", "")

    if not expected:
        return "Unmatched/Incorrect", 0

    expected = digits_to_words(expected)                 #also run digits_to_words on expected
    expected_normalized = normalize_text(expected)       #normalize expected text too

    score = fuzz.ratio(normalized_transcript, expected_normalized)

    if score >= 70:
        return expected, score
    else:
        if parent is not None:
            response = messagebox.askyesno(
                "Low Match Score",
                f"Match score is {score}%.\nAccept this response?",
                parent=parent
            )
        else:
            response = messagebox.askyesno(
                "Low Match Score",
                f"Match score is {score}%.\nAccept this response?"
            )

        if response:
            return expected, score
        else:
            return "Unmatched/Incorrect", score
