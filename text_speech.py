import pygame
from gtts import gTTS
import os
import time
import edge_tts
import asyncio

async def speak(text):
    tts = edge_tts.Communicate(text, "en-US-AriaNeural")

    filename = 'response.mp3'

    await tts.save(filename)

    pygame.mixer.init()

    # Load and play the audio file
    pygame.mixer.music.load(filename=filename)
    pygame.mixer.music.play()

    # Wait until the sound finishes playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)  # Keep the program running while music plays

    # Explicitly stop music just in case
    pygame.mixer.music.stop()

    # Quit the mixer to release the resources
    pygame.mixer.quit()
    os.remove(filename)
