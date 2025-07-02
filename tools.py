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
            "name": "add_medication_reminder",
            "description": "Add a medication reminder for the user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "medication": {"type": "string", "description": "The name of the medication."},
                    "time": {"type": "string", "description": "The time to remind in HH:MM 24-hour format."},
                    "frequency": {"type": "string", "description": "How often to remind (e.g., daily, weekly).", "default": "daily"}
                },
                "required": ["medication", "time"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_medication_reminders",
            "description": "List all active medication reminders for the user.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "remove_medication_reminder",
            "description": "Remove a medication reminder.",
            "parameters": {
                "type": "object",
                "properties": {
                    "medication": {"type": "string", "description": "The name of the medication."},
                    "time": {"type": "string", "description": "The time of the reminder in HH:MM 24-hour format (optional)."}
                },
                "required": ["medication"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_medication_reminder",
            "description": "Update the time or frequency of a medication reminder.",
            "parameters": {
                "type": "object",
                "properties": {
                    "medication": {"type": "string", "description": "The name of the medication."},
                    "new_time": {"type": "string", "description": "The new time in HH:MM 24-hour format (optional)."},
                    "new_frequency": {"type": "string", "description": "The new frequency (optional)."}
                },
                "required": ["medication"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "mark_medication_as_taken",
            "description": "Mark a medication as taken for today.",
            "parameters": {
                "type": "object",
                "properties": {
                    "medication": {"type": "string", "description": "The name of the medication."}
                },
                "required": ["medication"]
            }
        }
    }
]
