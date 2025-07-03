from openai import OpenAI
from speech_text import listen_for_command  
from text_speech import speak  
from config import openapi_key
from detect_scam import predict_sms, predict_email
from tools import tools
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
from twilio.rest import Client
import asyncio
import json
import sys
import tkinter as tk
from tkinter import scrolledtext
import threading
from datetime import datetime
from reminders import reminder_manager
from rag.retrieve import retrieve  # Add this import at the top

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

async def get_response_from_openai(prompt):
    global conversation_history

    # --- RAG Integration ---
    RAG_THRESHOLD = 1.0  # Lower is more similar; tune as needed
    try:
        rag_results = retrieve(prompt, top_k=3, threshold=RAG_THRESHOLD)
    except Exception as e:
        print(f"RAG retrieval error: {e}")
        rag_results = []
    if rag_results:
        context = "\n".join([p for p, d in rag_results])
        print("RAG is being used: context retrieved and added to prompt.")
        augmented_prompt = f"Context from trusted knowledge base:\n{context}\n\nUser: {prompt}"
    else:
        augmented_prompt = prompt
    # --- End RAG Integration ---

    conversation_history.append({"role": "user", "content": augmented_prompt})

    if len(conversation_history) > 10:
        conversation_history = conversation_history[-10:]

    try:
        response = await asyncio.to_thread(client.chat.completions.create,  
            model="ft:gpt-3.5-turbo-0125:personal::BaA9dvYQ",
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

        conversation_history.append({"role": "assistant", "content": reply})

    except Exception as e:
        print(f"OpenAI API error: {e}")
        reply = "I'm having trouble right now. Please try again later."

    return reply

class VoiceChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ECR - Elderly Companion Robot")
        self.root.geometry("600x800")
        
        self.status_label = tk.Label(
            root, 
            text="Press 'Start Listening' to begin", 
            font=("Arial", 14)
        )
        self.status_label.pack(pady=20)
        
        self.chat_area = scrolledtext.ScrolledText(
            root, 
            wrap=tk.WORD, 
            height=25,
            font=("Arial", 12)
        )
        self.chat_area.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        self.listen_button = tk.Button(
            root, 
            text="Start Listening",
            command=self.toggle_listening,
            height=2,
            font=("Arial", 16, "bold"),
            bg="#4CAF50",
            fg="white"
        )
        self.listen_button.pack(pady=20)
        
        self.is_listening = False
        self.conversation_history = []
        
        # Create event loop for async operations
        self.loop = asyncio.new_event_loop()
        self.thread = None

    def display_message(self, message, sender):
        timestamp = datetime.now().strftime("%I:%M %p")
        self.chat_area.insert(tk.END, f"[{timestamp}] {sender}: {message}\n\n")
        self.chat_area.see(tk.END)

    def update_status(self, status):
        self.status_label.config(text=status)

    async def process_message(self, message):
        response = await get_response_from_openai(message)
        
        # Update GUI from the main thread
        self.root.after(0, self.display_message, response, "ECR")
        self.root.after(0, self.update_status, "Press 'Start Listening' to speak again")
        
        # Speak the response
        await speak(response)

    async def listen_loop(self):
        while self.is_listening:
            try:
                self.root.after(0, self.update_status, "Listening... Please speak")
                command = await listen_for_command()
                
                if command:
                    self.root.after(0, self.display_message, command, "You")
                    self.root.after(0, self.update_status, "Processing your message...")
                    await self.process_message(command)
                    
                    if 'bye' in command.lower():
                        self.is_listening = False
                        self.root.after(0, lambda: self.listen_button.config(text="Start Listening", bg="#4CAF50"))
                        await speak("Goodbye! Have a great day!")
                        break
            except Exception as e:
                print(f"Error in listen loop: {e}")
                self.root.after(0, self.update_status, "Error occurred. Please try again")
                self.is_listening = False
                self.root.after(0, lambda: self.listen_button.config(text="Start Listening", bg="#4CAF50"))

    def run_async_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def start_listening(self):
        if not self.thread or not self.thread.is_alive():
            self.thread = threading.Thread(target=self.run_async_loop, daemon=True)
            self.thread.start()
        
        self.is_listening = True
        asyncio.run_coroutine_threadsafe(self.listen_loop(), self.loop)

    def stop_listening(self):
        self.is_listening = False
        self.update_status("Listening stopped")

    def toggle_listening(self):
        if not self.is_listening:
            self.listen_button.config(text="Stop Listening", bg="#f44336")
            self.start_listening()
        else:
            self.listen_button.config(text="Start Listening", bg="#4CAF50")
            self.stop_listening()

# --- Reminder Tool Handlers ---
def add_medication_reminder(medication, time, frequency='daily'):
    reminder_manager.add_reminder(medication, time, frequency)
    return f"Reminder set for {medication} at {time} {frequency}."

def list_medication_reminders():
    reminders = reminder_manager.list_reminders()
    if not reminders:
        return "You have no active medication reminders."
    return "Here are your medication reminders: " + ", ".join([
        f"{r['medication']} at {r['time']} {r['frequency']}" for r in reminders
    ])

def remove_medication_reminder(medication, time=None):
    reminder_manager.remove_reminder(medication, time)
    return f"Removed reminder for {medication}."

def update_medication_reminder(medication, new_time=None, new_frequency=None):
    reminder_manager.update_reminder(medication, new_time, new_frequency)
    return f"Updated reminder for {medication}."

def mark_medication_as_taken(medication):
    reminder_manager.mark_as_taken(medication)
    return f"Marked {medication} as taken for today."

# --- Voice-Only Main Loop ---
async def main_loop():
    # Start reminder scheduler in the background
    asyncio.create_task(reminder_manager.schedule_reminders(speak))
    print("ECR is ready. Say 'bye' to exit.")
    while True:
        command = await listen_for_command()
        if not command:
            continue
        print(f"You: {command}")
        if 'bye' in command.lower():
            await speak("Goodbye! Have a great day!")
            break
        response = await get_response_from_openai(command)
        print(f"ECR: {response}")
        await speak(response)

if __name__ == "__main__":
    asyncio.run(main_loop())
