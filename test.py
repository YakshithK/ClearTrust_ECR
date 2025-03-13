from openai import OpenAI
from config import openapi_key
from detect_scam import predict
from tools import tools
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
from twilio.rest import Client
import json
import tkinter as tk
import threading

client = OpenAI(api_key=openapi_key)

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "I just got a weird sms, it says Hello this is the IRS, please wire transfer us 10 thousand dollars or you will be deported."}],
    max_tokens=100,
    tools=tools
)

reply = response.choices[0].message.content
print(reply)
for i in response.choices[0].message.tool_calls:
    print(i)
# print(response.choices[0].message)

# tool_call = response.choices[0].message.tool_calls[0]
# args = json.loads(tool_call.function.arguments)

# result = predict(args['text'])
# print(result)