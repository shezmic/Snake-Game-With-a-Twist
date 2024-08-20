import pygame
from config import BACKGROUND_MUSIC, EAT_SOUND, COLLISION_SOUND

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.background_music = pygame.mixer.Sound(f"assets/sounds/{BACKGROUND_MUSIC}")
        self.eat_sound = pygame.mixer.Sound(f"assets/sounds/{EAT_SOUND}")
        self.collision_sound = pygame.mixer.Sound(f"assets/sounds/{COLLISION_SOUND}")
        self.music_volume = 0.5
        self.sfx_volume = 0.5

    def play_background_music(self):
        self.background_music.play(-1)  # Loop indefinitely
        self.background_music.set_volume(self.music_volume)

    def stop_background_music(self):
        self.background_music.stop()

    def play_eat_sound(self):
        self.eat_sound.set_volume(self.sfx_volume)
        self.eat_sound.play()

    def play_collision_sound(self):
        self.collision_sound.set_volume(self.sfx_volume)
        self.collision_sound.play()

    def set_music_volume(self, volume):
        self.music_volume = volume
        self.background_music.set_volume(volume)

    def set_sfx_volume(self, volume):
        self.sfx_volume = volume