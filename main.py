from openai import OpenAI
from speech_text import listen_for_command  
from text_speech import speak  
from sent import analyze_sentiment
from config import openapi_key
from detect_scam import predict
from tools import tools
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
from twilio.rest import Client
import asyncio
import json
import sys

client = OpenAI(api_key=openapi_key)

TWILIO_PHONE_NUMBER = "+12892778167"
FAMILY_MEMBER_PHONE = "+14374994222" 

def send_sms_alert(message):
    """Sends an SMS alert to a family member."""
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=message,
        from_=TWILIO_PHONE_NUMBER,
        to=FAMILY_MEMBER_PHONE
    )

conversation_history = []

async def get_response_from_openai(prompt, sentiment):
    global conversation_history

    conversation_history.append({"role": "user", "content": prompt, "sentiment": sentiment})

    if len(conversation_history) > 10:
        conversation_history = conversation_history[-10:]

    try:
        response = await asyncio.to_thread(client.chat.completions.create,  
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a friendly AI companion for an elderly individual who is not tech-savvy. Keep responses warm and empathetic and your name is also ECR, short for Elderly Companion Robot."}]
            + conversation_history,
            max_tokens=100,
            tools=tools
        )

        reply = response.choices[0].message.content

        if response.choices[0].message.tool_calls:
            name = response.choices[0].message.tool_calls[0].function.name
            args = json.loads(response.choices[0].message.tool_calls[0].function.arguments)

            result = await asyncio.to_thread(getattr(sys.modules[__name__], name), **args)

            conversation_history.append(response.choices[0].message)

            conversation_history.append({
                "role": "tool",
                "tool_call_id": response.choices[0].message.tool_calls[0].id,
                "content": str(result)
            })

            response = await asyncio.to_thread(client.chat.completions.create,  
                model="gpt-3.5-turbo",
                messages=conversation_history,
                max_tokens=100,
                tools=tools
            )

            reply = response.choices[0].message.content

        conversation_history.append({"role": "assistant", "content": reply, "sentiment": sentiment})

    except Exception as e:
        print(f"OpenAI API error: {e}")
        reply = "I'm having trouble right now. Please try again later."

    return reply

async def speak_loop():
    """Main event loop for voice interaction."""
    print("Say something...")

    command = await listen_for_command()

    while 'bye' not in command.lower():
        print(f"User: {command}")
        sentiment = analyze_sentiment(command)
        response = await get_response_from_openai(command, sentiment)
        print(conversation_history)

        if response: 
            print(f"AI: {response}")
            await speak(response)

        command = await listen_for_command()

    await speak("Bye! Have a great day!")

if __name__ == "__main__":
    asyncio.run(speak_loop())
