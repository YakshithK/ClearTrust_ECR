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
    }
]
