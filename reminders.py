import json
import time
import os
import re

def parse_frequency(frequency):
    """Parses a frequency string and returns the duration in seconds."""
    # Regex patterns to match frequency strings
    daily_pattern = r"once a day"
    hourly_pattern = r"every (\d+) hours"
    daily_pattern_alt = r"every day"

    # Match 'once a day' or 'every day'
    if re.match(daily_pattern, frequency) or re.match(daily_pattern_alt, frequency):
        return 86400  # 24 hours in seconds
    
    # Match 'every X hours'
    match = re.match(hourly_pattern, frequency)
    if match:
        hours = int(match.group(1))
        return hours * 3600  # Convert hours to seconds
    
    return None  # Invalid frequency format



def add_medication_to_json(medication_details):
    """Adds a medication record to a JSON file."""
    # Extract medication details
    name = medication_details.get("medication_name")
    dosage = medication_details.get("dosage")
    frequency = medication_details.get("frequency")
    
    if not name or not dosage or not frequency:
        return "Missing required medication details."

    medication = {
        "name": name,
        "dosage": dosage,
        "frequency": frequency,
        "start": time.time(),
    }

    # Check if the JSON file exists
    if os.path.exists("medications.json"):
        with open("medications.json", "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    # Append the new medication
    data.append(medication)

    # Save back to the JSON file
    with open("medications.json", "w") as file:
        json.dump(data, file, indent=4)

    return "Medication added successfully to JSON."

def check_medication_reminder():
    """Checks if any medication reminders are due."""
    try:
        with open("medications.json", "r") as file:
            medications = json.load(file)
    except FileNotFoundError:
        return None
    
    current_time = time.time()

    # Check each medication and its frequency
    for medication in medications:
        time_diff = current_time - medication["start"]

        # Parse the frequency to get the interval in seconds
        frequency_duration = parse_frequency(medication["frequency"])
        
        if frequency_duration is None:
            continue  # Skip if the frequency format is invalid

        # If the time difference exceeds the frequency duration, the medication is due
        if time_diff >= frequency_duration:
            return medication
    
    return None
