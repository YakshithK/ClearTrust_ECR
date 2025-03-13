tools = [
    {
        "type": "function",
        "function": {
            "name": "predict",
            "description": "Detect if a suspicous sms is a scam or not.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The SMS or message text to analyze for scam detection."
                    }
                },
                "required": ["text"]
            }
        }
    }
]