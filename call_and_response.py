import random
from session_runner import record_audio, transcribe_audio, match_phrase
from phrase_library import standard_phrases  # we’ll expand this later

# Simple pilot → expected ATC response pairs
call_and_response_pairs = [
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

def run_call_and_response_session(cowboy_mode=False):
    print("\n--- ATC Call-and-Response Session ---")
    
    selected_pair = random.choice(call_and_response_pairs)
    pilot_phrase = selected_pair["pilot"]
    expected_response = selected_pair["expected_controller"]

    print(f"\n🛩️ Pilot says: \"{pilot_phrase}\"")
    
    # Record user response
    record_audio()
    user_transcript = transcribe_audio()
    print(f"\n🎧 You said: \"{user_transcript}\"")

    # Match to expected controller response
    matched, score = match_phrase(user_transcript, cowboy_mode)

    print(f"\nExpected Response: \"{expected_response}\"")
    print(f"AI Best Match: \"{matched}\" (Score: {score})")

    # Feedback logic
    if score >= 90:
        print("✅ Perfect response!")
    elif score >= 70:
        print("⚠ Close, but not exact.")
    else:
        print("❌ Not a recognized ATC response. Try again.")
