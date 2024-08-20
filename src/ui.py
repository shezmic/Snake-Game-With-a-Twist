import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR_START, BACKGROUND_COLOR_END, GRID_SIZE

class Slider:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.value = 0.5

    def draw(self, screen):
        pygame.draw.rect(screen, (100, 100, 100), self.rect)
        slider_pos = self.rect.x + int(self.value * self.rect.width)
        pygame.draw.rect(screen, (200, 200, 200), (slider_pos - 5, self.rect.y, 10, self.rect.height))

    def update(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.value = (mouse_pos[0] - self.rect.x) / self.rect.width
            self.value = max(0, min(1, self.value))
            return True
        return False

class UI:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.gradient_surface = self.create_gradient_background()
        self.gradient_offset = 0
        self.grid_surface = self.create_grid_overlay()
        self.menu_open = False
        self.menu_button = pygame.Rect(SCREEN_WIDTH - 110, 10, 100, 40)
        self.music_slider = Slider(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 20)
        self.sfx_slider = Slider(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 10, 200, 20)
        self.quit_button = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 70, 100, 40)
        self.close_button = pygame.Rect(0, 0, 30, 30)

    def create_gradient_background(self):
        gradient = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT * 2))
        for y in range(SCREEN_HEIGHT * 2):
            r = BACKGROUND_COLOR_START[0] + (BACKGROUND_COLOR_END[0] - BACKGROUND_COLOR_START[0]) * y / (SCREEN_HEIGHT * 2)
            g = BACKGROUND_COLOR_START[1] + (BACKGROUND_COLOR_END[1] - BACKGROUND_COLOR_START[1]) * y / (SCREEN_HEIGHT * 2)
            b = BACKGROUND_COLOR_START[2] + (BACKGROUND_COLOR_END[2] - BACKGROUND_COLOR_START[2]) * y / (SCREEN_HEIGHT * 2)
            pygame.draw.line(gradient, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        return gradient

    def create_grid_overlay(self):
        grid = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(grid, (255, 255, 255, 30), (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(grid, (255, 255, 255, 30), (0, y), (SCREEN_WIDTH, y))
        return grid

    def update_background(self):
        self.gradient_offset = (self.gradient_offset + 0.5) % SCREEN_HEIGHT

    def draw_background(self, screen):
        screen.blit(self.gradient_surface, (0, -self.gradient_offset))
        screen.blit(self.gradient_surface, (0, SCREEN_HEIGHT - self.gradient_offset))
        screen.blit(self.grid_surface, (0, 0))

    def draw_score(self, screen, score):
        score_text = self.font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

    def draw_game_over(self, screen, final_score):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        game_over_font = pygame.font.Font(None, 72)
        game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
        score_text = self.font.render(f"Final Score: {final_score}", True, (255, 255, 255))
        restart_text = self.font.render("Press R to Restart", True, (255, 255, 255))

        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))

    def draw_menu_button(self, screen):
        pygame.draw.rect(screen, (100, 100, 100), self.menu_button)
        menu_text = self.font.render("Menu", True, (255, 255, 255))
        text_rect = menu_text.get_rect(center=self.menu_button.center)
        screen.blit(menu_text, text_rect)

    def draw_menu(self, screen, music_volume, sfx_volume):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        menu_width, menu_height = 300, 280
        menu_x = (SCREEN_WIDTH - menu_width) // 2
        menu_y = (SCREEN_HEIGHT - menu_height) // 2

        pygame.draw.rect(screen, (50, 50, 50), (menu_x, menu_y, menu_width, menu_height))
        pygame.draw.rect(screen, (100, 100, 100), (menu_x, menu_y, menu_width, menu_height), 2)

        title_text = self.font.render("Menu", True, (255, 255, 255))
        screen.blit(title_text, (menu_x + 10, menu_y + 10))

        music_text = self.font.render("Music", True, (255, 255, 255))
        screen.blit(music_text, (menu_x + 10, menu_y + 60))
        self.music_slider.rect.topleft = (menu_x + 10, menu_y + 90)
        self.music_slider.value = music_volume
        self.music_slider.draw(screen)

        sfx_text = self.font.render("SFX", True, (255, 255, 255))
        screen.blit(sfx_text, (menu_x + 10, menu_y + 120))
        self.sfx_slider.rect.topleft = (menu_x + 10, menu_y + 150)
        self.sfx_slider.value = sfx_volume
        self.sfx_slider.draw(screen)

        # Draw quit button
        self.quit_button.topleft = (menu_x + 10, menu_y + 220)
        pygame.draw.rect(screen, (200, 50, 50), self.quit_button)
        quit_text = self.font.render("Quit", True, (255, 255, 255))
        quit_text_rect = quit_text.get_rect(center=self.quit_button.center)
        screen.blit(quit_text, quit_text_rect)

        # Draw close button
        self.close_button.topleft = (menu_x + menu_width - 30, menu_y)
        pygame.draw.rect(screen, (200, 50, 50), self.close_button)
        close_text = self.font.render("X", True, (255, 255, 255))
        close_text_rect = close_text.get_rect(center=self.close_button.center)
        screen.blit(close_text, close_text_rect)

    def handle_menu_click(self, mouse_pos):
        if self.music_slider.update(mouse_pos):
            return "music", self.music_slider.value
        elif self.sfx_slider.update(mouse_pos):
            return "sfx", self.sfx_slider.value
        return None, None

    def is_click_outside_menu(self, mouse_pos):
        menu_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 125, 300, 250)
        return not menu_rect.collidepoint(mouse_pos)

    def draw_pause_overlay(self, screen):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(100)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        pause_text = self.font.render("PAUSED", True, (255, 255, 255))
        screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 2))

    def handle_menu_click(self, mouse_pos):
        if self.music_slider.update(mouse_pos):
            return "music", self.music_slider.value
        elif self.sfx_slider.update(mouse_pos):
            return "sfx", self.sfx_slider.value
        elif self.quit_button.collidepoint(mouse_pos):
            return "quit", None
        elif self.close_button.collidepoint(mouse_pos):
            return "close", None
        return None, None

    def is_click_outside_menu(self, mouse_pos):
        menu_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 150, 300, 300)
        return not menu_rect.collidepoint(mouse_pos)
