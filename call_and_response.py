import random
from session_runner import record_audio, transcribe_audio, match_phrase

# Sample FAA phrase pairs
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

# Sample Military phrase pairs
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

# Fallback or custom pool
mixed_pairs = faa_pairs + military_pairs

def run_call_and_response_session(config):
    print("\n--- ATC Call-and-Response Session ---")

    if config["mode"] == "FAA":
        phrase_pairs = faa_pairs
    elif config["mode"] == "Military":
        phrase_pairs = military_pairs
    else:
        phrase_pairs = mixed_pairs

    selected_pair = random.choice(phrase_pairs)
    pilot_phrase = selected_pair["pilot"]
    expected_response = selected_pair["expected_controller"]

    print(f"\n🛩️ Pilot says: \"{pilot_phrase}\"")

    # Record user response
    record_audio()
    user_transcript = transcribe_audio()
    print(f"\n🎧 You said: \"{user_transcript}\"")

    # Match to expected controller response
    matched, score = match_phrase(user_transcript, cowboy_mode=config["cowboy_mode"])

    print(f"\nExpected Response: \"{expected_response}\"")
    print(f"AI Best Match: \"{matched}\" (Score: {score})")

    if config["live_feedback"]:
        if score >= 90:
            print("✅ Perfect response!")
        elif score >= 70:
            print("⚠ Close, but not exact.")
        else:
            print("❌ Not a recognized ATC response. Try again.")

    input("\n[Press Enter to return to the main menu]")

