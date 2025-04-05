import json
import time
import os
import re

def parse_frequency(frequency):
    """Parses a frequency string and returns the duration in seconds."""
    # Regex patterns to match frequency strings
    daily_pattern = r"once a day"
    hourly_pattern = r"every (\d+(\.\d+)?) hours"
    daily_pattern_alt = r"every day"

    # Match 'once a day' or 'every day'
    if re.match(daily_pattern, frequency) or re.match(daily_pattern_alt, frequency):
        return 86400  # 24 hours in seconds
    
    # Match 'every X hours'
    match = re.match(hourly_pattern, frequency)
    if match:
        hours = float(match.group(1))
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

# Function to update medication start_time when it's time to take it
def update_medication(medication_name):
    """Updates the start time of the medication in the JSON file when it's taken."""
    
    # Check if the medications file exists
    if not os.path.exists("medications.json"):
        return "No medications found."
    
    # Load current data from medications.json
    with open("medications.json", "r") as file:
        try:
            medications = json.load(file)
        except json.JSONDecodeError:
            medications = []
    
    # Iterate through the medications to find the one that matches
    for medication in medications:
        if medication["name"].lower() == medication_name.lower():
            # Update the start_time to the current time (time.time() records seconds since the epoch)
            medication["start"] = time.time()
            
            # Save the updated list of medications back to the file
            with open("medications.json", "w") as file:
                json.dump(medications, file, indent=4)
                
            return f"Before, you need to take your medication: {medication['name']} with a dosage of {medication['dosage']}."
    
    # If medication wasn't found
    return f"Medication '{medication_name}' not found."
