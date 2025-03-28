from vapi import Vapi

API_KEY = "d457c0e6-3913-4137-86d2-6f7340261ba7"
CALL_ID = "5c298919-6dca-4136-bc5c-3cd2b9aa6861"

# Initialize the VAPI client
client = Vapi(token=API_KEY)

# Fetch call data
call_data = client.calls.get(id=CALL_ID)
print(client.calls.get(id=CALL_ID).analysis)
# Check if 'analysis' exists in the response
if 'analysis' in call_data:
    print(call_data)
    analysis_data = call_data['analysis']
    print(analysis_data)  # Display the analysis tab data
else:
    print("No analysis data found.")
