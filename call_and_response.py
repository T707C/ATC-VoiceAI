import random
import csv
import datetime
import os
import pyttsx3
from session_utils import record_audio, transcribe_audio, match_phrase


# === Text-to-Speech: Speaks a line aloud ===
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 175)
    engine.setProperty('volume', 1.0)
    engine.say(text)
    engine.runAndWait()

# === Built-in FAA phrase pairs ===
faa_pairs = [
    {
        "pilot": "Request taxi to runway two seven",
        "expected_controller": "Taxi to runway two seven via Alpha, Bravo"
    },
    {
        "pilot": "Ready for departure runway one eight",
        "expected_controller": "Cleared for takeoff runway one eight"
    },
    {
        "pilot": "Inbound for landing, three mile final",
        "expected_controller": "Cleared to land runway two seven"
    }
]

# === Built-in Military phrase pairs ===
military_pairs = [
    {
        "pilot": "Request departure on runway one six",
        "expected_controller": "Cleared for departure runway one six, proceed with climb"
    },
    {
        "pilot": "Approach, three in the green",
        "expected_controller": "Cleared to land runway one six"
    }
]

# === Entry point for running the session ===
def run_call_and_response_session(config, custom_phrase_pairs=[]):
    print("\n--- ATC Call-and-Response Session ---")

    # Select phrase pool based on session mode
    if config["mode"] == "FAA":
        phrase_pairs = faa_pairs.copy()
    elif config["mode"] == "Military":
        phrase_pairs = military_pairs.copy()
    else:
        phrase_pairs = faa_pairs + military_pairs

    # Add any custom phrase pairs provided
    phrase_pairs += custom_phrase_pairs

    # Prepare session log
    if not os.path.exists("logs"):
        os.makedirs("logs")

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = f"logs/session_log_{timestamp}.csv"

    with open(log_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Pilot Phrase", "User Response", "Matched As", "Score"])

    print("🎙️ Beginning session. Say 'exit' at any time to end.\n")

    # === Continuous session loop ===
    while True:
        selected_pair = random.choice(phrase_pairs)
        pilot_phrase = selected_pair["pilot"]
        expected_response = selected_pair["expected_controller"]

        print(f"\n🛩️ Pilot says: \"{pilot_phrase}\"")
        speak(pilot_phrase)

        record_audio()
        user_transcript = transcribe_audio()
        print(f"\n🎧 You said: \"{user_transcript}\"")

        # Exit condition
        if user_transcript.strip().lower() == "exit":
            print("\n🛑 Ending session...")
            break

        matched, score = match_phrase(user_transcript)

        print(f"\nExpected Response: \"{expected_response}\"")
        print(f"AI Best Match: \"{matched}\" (Score: {score})")

        if config["live_feedback"]:
            if score >= 90:
                print("✅ Perfect response!")
            elif score >= 70:
                print("⚠ Close, but not exact.")
            else:
                print("❌ Not a recognized ATC response. Try again.")

        # Log result
        with open(log_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                pilot_phrase,
                user_transcript,
                matched,
                score
            ])

        input("\n[Press Enter to continue]")

    print(f"\n📁 Session log saved to: {log_file}")
    input("[Press Enter to return to the main menu]")
