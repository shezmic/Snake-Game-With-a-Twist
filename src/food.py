import pygame
import random
import math
from config import SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE, FOOD_COLOR

class Food:
    def __init__(self):
        self.position = self.randomize_position()
        self.pulse_value = 0
        self.spawn_time = pygame.time.get_ticks()

    def randomize_position(self):
        x = random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        y = random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        return (x, y)

    def update(self):
        self.pulse_value = (self.pulse_value + 0.1) % (2 * math.pi)
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > 7000:  # 7 seconds
            self.teleport()

    def teleport(self):
        self.position = self.randomize_position()
        self.spawn_time = pygame.time.get_ticks()

    def draw(self, screen):
        pulse_size = int(GRID_SIZE + math.sin(self.pulse_value) * 4)
        pulse_offset = (GRID_SIZE - pulse_size) // 2
        
        glow_surf = pygame.Surface((GRID_SIZE * 2, GRID_SIZE * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*FOOD_COLOR, 64), (GRID_SIZE, GRID_SIZE), GRID_SIZE)
        screen.blit(glow_surf, (self.position[0] - GRID_SIZE // 2, self.position[1] - GRID_SIZE // 2))
        
        pygame.draw.rect(screen, FOOD_COLOR, (self.position[0] + pulse_offset, self.position[1] + pulse_offset, pulse_size, pulse_size))

    def is_far_from_snake(self, snake_head, min_distance=200):
        dx = self.position[0] - snake_head[0]
        dy = self.position[1] - snake_head[1]
        distance = math.sqrt(dx**2 + dy**2)
        return distance >= min_distance