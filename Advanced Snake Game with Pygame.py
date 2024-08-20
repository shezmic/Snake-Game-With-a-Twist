import pygame
import random
import math
import colorsys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
SNAKE_SEGMENT_RADIUS = 10
FPS = 60
INITIAL_SNAKE_LENGTH = 20

# Colors (Material Design palette)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PRIMARY_COLOR = (33, 150, 243)  # Blue 500
ACCENT_COLOR = (255, 64, 129)   # Pink A400
BACKGROUND_COLOR = (250, 250, 250)  # Grey 50

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smooth Gradient Snake Game")

# Fonts
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

class SnakeSegment:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color

class Snake:
    def __init__(self):
        self.direction = (1, 0)
        self.speed = 2
        self.length = INITIAL_SNAKE_LENGTH
        self.hue_start = 0.3
        self.hue_range = 0.2
        self.segments = [SnakeSegment((WIDTH // 2 - i * self.speed, HEIGHT // 2), self.get_color(i)) 
                         for i in range(self.length)]

    def move(self):
        new_head = ((self.segments[0].pos[0] + self.direction[0] * self.speed) % WIDTH,
                    (self.segments[0].pos[1] + self.direction[1] * self.speed) % HEIGHT)
        self.hue_start = (self.hue_start + 0.005) % 1.0
        self.segments.insert(0, SnakeSegment(new_head, self.get_color(0)))
        if len(self.segments) > self.length:
            self.segments.pop()
        for i, segment in enumerate(self.segments):
            segment.color = self.get_color(i)

    def get_color(self, index):
        hue = (self.hue_start + (index / self.length) * self.hue_range) % 1.0
        return tuple(int(x * 255) for x in colorsys.hsv_to_rgb(hue, 1, 1))

    def grow(self):
        self.length += 1

    def check_collision(self):
        return self.segments[0].pos in [seg.pos for seg in self.segments[1:]]

    def change_direction(self, new_direction):
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def draw(self, screen):
        for segment in self.segments:
            pygame.draw.circle(screen, segment.color, (int(segment.pos[0]), int(segment.pos[1])), SNAKE_SEGMENT_RADIUS)
        head = self.segments[0].pos
        eye_offset = 5
        for eye_pos in [(head[0] - eye_offset * self.direction[1], head[1] + eye_offset * self.direction[0]),
                        (head[0] + eye_offset * self.direction[1], head[1] - eye_offset * self.direction[0])]:
            pygame.draw.circle(screen, BLACK, (int(eye_pos[0]), int(eye_pos[1])), 3)

class Food:
    def __init__(self):
        self.position = self.random_position()

    def random_position(self):
        return (random.randint(SNAKE_SEGMENT_RADIUS, WIDTH - SNAKE_SEGMENT_RADIUS),
                random.randint(SNAKE_SEGMENT_RADIUS, HEIGHT - SNAKE_SEGMENT_RADIUS))

    def draw(self, screen):
        pygame.draw.circle(screen, ACCENT_COLOR, self.position, SNAKE_SEGMENT_RADIUS)

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False
        self.paused = False

    def update(self):
        if not self.paused and not self.game_over:
            self.snake.move()
            if self.check_food_collision():
                self.score += 1
                self.snake.grow()
                self.food = Food()
            if self.snake.check_collision():
                self.game_over = True

    def check_food_collision(self):
        return math.hypot(self.snake.segments[0].pos[0] - self.food.position[0],
                          self.snake.segments[0].pos[1] - self.food.position[1]) < SNAKE_SEGMENT_RADIUS * 2

    def draw(self, screen):
        screen.fill(BACKGROUND_COLOR)
        self.snake.draw(screen)
        self.food.draw(screen)
        self.draw_score(screen)
        if self.paused:
            self.draw_pause_overlay(screen)

    def draw_score(self, screen):
        score_surface = pygame.Surface((150, 50), pygame.SRCALPHA)
        pygame.draw.rect(score_surface, (*PRIMARY_COLOR, 220), (0, 0, 150, 50), border_radius=25)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        score_surface.blit(score_text, (10, 10))
        screen.blit(score_surface, (20, 20))

    def draw_pause_overlay(self, screen):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))
        pause_text = large_font.render("PAUSED", True, WHITE)
        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - pause_text.get_height() // 2))

def draw_material_button(screen, text, x, y, width, height, color, text_color):
    button_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(button_surface, (*color, 220), (0, 0, width, height), border_radius=height // 2)
    pygame.draw.rect(button_surface, (*color, 255), (0, 0, width, height - 5), border_radius=height // 2)
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=(width // 2, height // 2 - 2))
    button_surface.blit(text_surf, text_rect)
    screen.blit(button_surface, (x, y))

def main():
    clock = pygame.time.Clock()
    game = Game()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    game.snake.change_direction((0, -1))
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    game.snake.change_direction((0, 1))
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    game.snake.change_direction((-1, 0))
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    game.snake.change_direction((1, 0))
                elif event.key == pygame.K_p:
                    game.paused = not game.paused
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if WIDTH - 130 <= event.pos[0] <= WIDTH - 30 and 20 <= event.pos[1] <= 70:
                    game.paused = not game.paused

        game.update()
        game.draw(screen)
        
        # Draw Material Design pause button
        draw_material_button(screen, "Pause" if not game.paused else "Resume", 
                             WIDTH - 130, 20, 100, 50, PRIMARY_COLOR, WHITE)
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()