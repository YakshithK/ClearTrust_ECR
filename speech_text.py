import speech_recognition as sr
import asyncio

async def listen_for_command():
    recognizer = sr.Recognizer()
    
    with sr.Microphone(0) as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        
        loop = asyncio.get_running_loop()
        audio = await loop.run_in_executor(None, recognizer.listen, source)

    try:
        command = recognizer.recognize_google(audio)
        return command.lower()  # Convert to lowercase for consistency
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
        return ''
    except sr.RequestError:
        print("There seems to be a network issue.")
        return ''
