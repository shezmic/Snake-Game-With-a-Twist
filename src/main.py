import pygame
import sys
import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT, INITIAL_SPEED, SPEED_INCREMENT, GRID_SIZE
from snake import Snake, AISnake
from food import Food
from ui import UI
from sound import SoundManager

def spawn_food(snake, ai_snake):
    while True:
        food = Food()
        if food.position not in snake.body and (not ai_snake.visible or food.position not in ai_snake.body):
            return food

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    ui = UI()
    sound_manager = SoundManager()
    snake = Snake(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, (0, 255, 0), (0, 200, 0))  # Green color for main snake
    ai_snake = AISnake(0, 0)
    food = spawn_food(snake, ai_snake)

    score = 0
    speed = INITIAL_SPEED
    game_over = False
    paused = False
    game_start_time = pygame.time.get_ticks()
    ai_snake_timer = 0

    sound_manager.play_background_music()

    running = True
    while running:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if not game_over and not paused:
                    if event.key == pygame.K_UP:
                        snake.change_direction((0, -1))
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction((0, 1))
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction((1, 0))
                elif game_over:
                    if event.key == pygame.K_r:
                        # Restart the game
                        snake = Snake(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, (0, 255, 0), (0, 200, 0))
                        ai_snake = AISnake(0, 0)
                        food = spawn_food(snake, ai_snake)
                        score = 0
                        speed = INITIAL_SPEED
                        game_over = False
                        game_start_time = current_time
                        sound_manager.play_background_music()

            # ... (handle mouse events as before)

        if not game_over and not paused:
            snake.move()
            food.update()

            # AI Snake logic
            if current_time - game_start_time > 30000:  # 30 seconds after game start
                if not ai_snake.visible:
                    if current_time - ai_snake_timer > random.randint(5000, 15000):  # Random interval between 5-15 seconds
                        ai_snake.spawn_near_main_snake(snake)
                        ai_snake.set_target(food.position)
                        ai_snake_timer = current_time
                else:
                    ai_snake.move_towards_target()
                    if ai_snake.has_eaten_food():
                        sound_manager.play_eat_sound()
                        food = spawn_food(snake, ai_snake)
                        ai_snake.disappear()
                        ai_snake_timer = current_time
            
            # Check for collision with food
            if snake.body[0] == food.position:
                snake.grow()
                score += 1
                speed += SPEED_INCREMENT
                sound_manager.play_eat_sound()
                food = spawn_food(snake, ai_snake)
                if ai_snake.visible:
                    ai_snake.set_target(food.position)

            # Check for collision with self
            if snake.body[0] in snake.body[1:]:
                game_over = True
                sound_manager.play_collision_sound()
                sound_manager.stop_background_music()

        ui.update_background()
        ui.draw_background(screen)
        snake.draw(screen)
        if ai_snake.visible:
            ai_snake.draw(screen)
        food.draw(screen)
        ui.draw_score(screen, score)
        ui.draw_menu_button(screen)

        if game_over:
            ui.draw_game_over(screen, score)
        elif paused:
            if ui.menu_open:
                ui.draw_menu(screen, sound_manager.music_volume, sound_manager.sfx_volume)
            else:
                ui.draw_pause_overlay(screen)

        pygame.display.flip()

        clock.tick(speed)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()