import pygame
import math
import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE

class Snake:
    def __init__(self, x, y, color_head, color_body):
        self.body = [(x, y)]
        self.direction = (1, 0)
        self.grow_next = False
        self.animation_offset = 0
        self.eating_animation = 0
        self.color_head = color_head
        self.color_body = color_body

    def move(self):
        head = self.body[0]
        new_head = (
            (head[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.body.insert(0, new_head)
        if not self.grow_next:
            self.body.pop()
        else:
            self.grow_next = False

    def grow(self):
        self.grow_next = True
        self.eating_animation = 10  # Start eating animation

    def change_direction(self, new_direction):
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def draw(self, screen):
        self.animation_offset = (self.animation_offset + 0.2) % (2 * math.pi)
        for i, segment in enumerate(self.body):
            color = self.color_head if i == 0 else self.color_body
            offset = math.sin(self.animation_offset + i * 0.2) * 2
            x_offset = offset * self.direction[1]
            y_offset = offset * self.direction[0]
            
            segment_size = GRID_SIZE
            if i == 0 and self.eating_animation > 0:
                segment_size += int(5 * math.sin(self.eating_animation * 0.5))
                self.eating_animation -= 1
            
            pygame.draw.rect(screen, color, (segment[0] + x_offset - (segment_size - GRID_SIZE) // 2, 
                                             segment[1] + y_offset - (segment_size - GRID_SIZE) // 2, 
                                             segment_size, segment_size))

class AISnake(Snake):
    def __init__(self, x, y):
        super().__init__(x, y, (0, 0, 255), (0, 0, 200))  # Blue color for AI snake
        self.speed = 1.5  # Slightly faster than the main snake
        self.visible = False
        self.target = None

    def set_target(self, food_position):
        self.target = food_position

    def move_towards_target(self):
        if self.target and self.visible:
            head = self.body[0]
            dx = self.target[0] - head[0]
            dy = self.target[1] - head[1]
            
            if abs(dx) > abs(dy):
                self.direction = (1 if dx > 0 else -1, 0)
            else:
                self.direction = (0, 1 if dy > 0 else -1)

            new_head = (
                (head[0] + self.direction[0] * GRID_SIZE * self.speed) % SCREEN_WIDTH,
                (head[1] + self.direction[1] * GRID_SIZE * self.speed) % SCREEN_HEIGHT
            )
            self.body.insert(0, new_head)
            self.body.pop()

    def spawn_near_main_snake(self, main_snake):
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(100, 200)
        x = (main_snake.body[0][0] + int(math.cos(angle) * distance)) % SCREEN_WIDTH
        y = (main_snake.body[0][1] + int(math.sin(angle) * distance)) % SCREEN_HEIGHT
        self.body = [(x, y)]
        # Match the length of the main snake
        while len(self.body) < len(main_snake.body):
            self.body.append(self.body[-1])
        self.visible = True

    def disappear(self):
        self.visible = False
        self.target = None
        self.body = []  # Clear the body to ensure complete disappearance

    def has_eaten_food(self):
        return self.visible and self.body[0] == self.target