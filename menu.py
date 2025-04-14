# menu.py
import time
from session_runner import run_session
from call_and_response import run_call_and_response_session


session_config = {
    "mode": "FAA",
    "cowboy_mode": False,
    "phrase_matching": True,
    "live_feedback": True
}

def main_menu():
    while True:
        print("\n=== ATC Voice AI ===")
        print("[1] Start New Session")
        print("[2] Options")
        print("[3] Exit")
        choice = input("> ")

        if choice == '1':
            new_session()
        elif choice == '2':
            options_menu()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")

def new_session():
    print("\n--- Select Training Mode ---")
    print("[1] FAA")
    print("[2] Military")
    print("[3] University")
    print("[4] Custom")
    mode_choice = input("> ")

    mode_map = {
        '1': "FAA",
        '2': "Military",
        '3': "University",
        '4': "Custom"
    }

    session_config["mode"] = mode_map.get(mode_choice, "FAA")
    print(f"\nTraining Mode set to: {session_config['mode']}")
    print("Launching session...\n")

    # Placeholder for your future session logic
    time.sleep(1)
    run_session(session_config)
    for key, value in session_config.items():
        print(f" - {key}: {value}")

def options_menu():
    while True:
        print("\n--- Options ---")
        print(f"[1] Cowboy Mode: {'On' if session_config['cowboy_mode'] else 'Off'}")
        print(f"[2] Phrase Matching: {'On' if session_config['phrase_matching'] else 'Off'}")
        print(f"[3] Live Feedback: {'On' if session_config['live_feedback'] else 'Off'}")
        print(f"[4] Add Custom Phrase Pair")
        print("[5] Back to Main Menu")

        opt = input("> ")

        if opt == '1':
            session_config['cowboy_mode'] = not session_config['cowboy_mode']
        elif opt == '2':
            session_config['phrase_matching'] = not session_config['phrase_matching']
        elif opt == '3':
            session_config['live_feedback'] = not session_config['live_feedback']
        elif opt == '4':
            print("\n✍ Enter the pilot's spoken phrase:")
            pilot = input("> ").strip()
            print("✍ Enter the expected ATC controller response:")
            controller = input("> ").strip()

            if pilot and controller:
                custom_phrase_pairs.append({
                    "pilot": pilot,
                    "expected_controller": controller
                })
                print("✅ Custom phrase pair added successfully.")
            else:
                print("⚠ Both fields must be filled. Phrase not saved.")
        elif opt == '5':
            break
        else:
            print("Invalid option. Try again.")
