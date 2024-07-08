import pygame
import time
from gtts import gTTS
pygame.init()
pygame.mixer.init()


def display_text_and_audio(text):
    tts = gTTS(text, lang='en')  
    # Save the audio file
    audio_file = 'audio.mp3'
    tts.save(audio_file)

    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(30)

    screen = pygame.display.set_mode((800, 600))  
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(400, 300))  

    screen.fill((0, 0, 0))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    time.sleep(5)  

    pygame.quit()
if __name__ == '__main__':
    text_to_speak = "This is a sample synchronized text-to-speech animation."
    display_text_and_audio(text_to_speak)

