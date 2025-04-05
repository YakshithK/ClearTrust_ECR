tools = [
    {
        "type": "function",
        "function": {
            "name": "predict_sms",
            "description": "Detect if a suspicious SMS is a scam or not and also tell the user the keywords",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The SMS or message text to analyze for scam detection."
                    },
                },
                "required": ["text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "predict_email",
            "description": "Detect if an email is a scam or not and identify the keywords",
            "parameters": {
                "type": "object",
                "properties": {
                    "body": {
                        "type": "string",
                        "description": "The body of the email."
                    }
                },
                "required": ["body"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_medication_to_json",
            "description": "Add a medication reminder to JSON format. Automatically extract details like medication name, dosage, and frequency from user input.",
            "parameters": {
                "type": "object",
                "properties": {
                    "medication_details": {
                        "type": "object",
                        "properties": {
                            "medication_name": {
                                "type": "string",
                                "description": "The name of the medication."
                            },
                            "dosage": {
                                "type": "string",
                                "description": "The dosage of the medication (e.g., 500mg, 1 tablet)."
                            },
                            "frequency": {
                                "type": "string",
                                "description": "The frequency of the medication (e.g., once a day, every 6 hours)."
                            }
                        },
                        "required": ["medication_name", "dosage", "frequency"]
                    }
                },
                "required": ["medication_details"]
            }
        }
    }
]
