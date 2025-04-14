

# phrasebook.py

phrasebook = {
    "Request taxi to runway two seven": {
        "expected_response": "Taxi to runway two seven via Alpha, Bravo",
        "definition": "Pilot is asking ATC for permission to taxi to Runway 27. ATC gives the route using taxiways Alpha and Bravo."
    },
    "Ready for departure runway one eight": {
        "expected_response": "Cleared for takeoff runway one eight",
        "definition": "Pilot is lined up and ready to depart. ATC clears the aircraft for takeoff from Runway 18."
    },
    "Inbound for landing, three mile final": {
        "expected_response": "Cleared to land runway two seven",
        "definition": "Pilot reports final approach at 3 miles. ATC issues landing clearance."
    },
    "Holding short of runway one six": {
        "expected_response": "Hold short of runway one six",
        "definition": "Pilot confirms stopping before Runway 16. ATC acknowledges the hold position."
    },
    "Request cross runway two seven": {
        "expected_response": "Cross runway two seven and contact ground on point eight",
        "definition": "Pilot needs to cross an active runway. ATC gives clearance and instructs frequency change."
    },
    "Approach, three in the green": {
        "expected_response": "Cleared to land runway one six",
        "definition": "Military slang confirming landing gear is down and locked. ATC clears aircraft to land."
    },
    "Triple Nickel": {
        "expected_response": "Five five five",
        "definition": "Slang for the call sign '555'. May be heard on military or casual radio calls."
    },
    "Lima Charlie": {
        "expected_response": "Loud and Clear",
        "definition": "Radio check term meaning signal is received clearly. Common NATO phonetic phrase."
    },

    # === In-Session Control ===
    "Exit": {
        "Ends the current simulation session and returns to the main menu."
    }
}
