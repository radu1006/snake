import pygame
import random
import time
import numpy as np

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 500, 500
GRID_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Snake Game")

# Generate sounds dynamically
def generate_sound(frequency, duration=0.1, sample_rate=44100):
    samples = np.sin(2 * np.pi * np.arange(sample_rate * duration) * frequency / sample_rate)
    samples = (samples * 32767).astype(np.int16)
    return pygame.sndarray.make_sound(np.column_stack([samples, samples]))

eat_sound = generate_sound(800)
game_over_sound = generate_sound(200)

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

FRUIT_TYPES = {
    (255, 0, 0): 1,    # Red fruit - 1 point
    (0, 0, 255): 3,    # Blue fruit - 3 points
    (255, 165, 0): 5   # Orange fruit - 5 points
}

font = pygame.font.SysFont(None, 30)

def main_menu():
    while True:
        screen.fill(BLACK)
        title = font.render("Snake Game", True, WHITE)
        option1 = font.render("1. Start Game", True, WHITE)
        option2 = font.render("2. Automatically Play", True, WHITE)
        option3 = font.render("3. Exit Game", True, WHITE)
        
        screen.blit(title, (WIDTH // 2 - 50, HEIGHT // 4))
        screen.blit(option1, (WIDTH // 2 - 50, HEIGHT // 3))
        screen.blit(option2, (WIDTH // 2 - 50, HEIGHT // 3 + 40))
        screen.blit(option3, (WIDTH // 2 - 50, HEIGHT // 3 + 80))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "player"
                if event.key == pygame.K_2:
                    return "ai"
                if event.key == pygame.K_3:
                    pygame.quit()
                    exit()

def game_loop(auto_play):
    while True:
        result = play_game(auto_play)
        if result == "menu":
            mode = main_menu()
            auto_play = (mode == "ai")
        else:
            break

def play_game(auto_play):
    snake = [(100, 100), (80, 100), (60, 100)]
    direction = (GRID_SIZE, 0)
    next_direction = direction
    food = (random.randrange(0, WIDTH, GRID_SIZE), random.randrange(0, HEIGHT, GRID_SIZE))
    food_color = random.choice(list(FRUIT_TYPES.keys()))
    clock = pygame.time.Clock()
    score = 0
    running = True
    
    while running:
        screen.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"
                if not auto_play:
                    if event.key == pygame.K_UP and direction != (0, GRID_SIZE):
                        next_direction = (0, -GRID_SIZE)
                    elif event.key == pygame.K_DOWN and direction != (0, -GRID_SIZE):
                        next_direction = (0, GRID_SIZE)
                    elif event.key == pygame.K_LEFT and direction != (GRID_SIZE, 0):
                        next_direction = (-GRID_SIZE, 0)
                    elif event.key == pygame.K_RIGHT and direction != (-GRID_SIZE, 0):
                        next_direction = (GRID_SIZE, 0)
        
        if auto_play:
            next_direction = ai_move(snake, food)
        
        direction = next_direction
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        
        if new_head in snake or new_head[0] < 0 or new_head[1] < 0 or new_head[0] >= WIDTH or new_head[1] >= HEIGHT:
            game_over_sound.play()
            print("Game Over!")
            time.sleep(2)
            return "menu"
        
        snake.insert(0, new_head)
        
        if new_head == food:
            eat_sound.play()
            score += FRUIT_TYPES[food_color]
            food = (random.randrange(0, WIDTH, GRID_SIZE), random.randrange(0, HEIGHT, GRID_SIZE))
            food_color = random.choice(list(FRUIT_TYPES.keys()))
        else:
            snake.pop()
        
        pygame.draw.rect(screen, food_color, (food[0], food[1], GRID_SIZE, GRID_SIZE))
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], GRID_SIZE, GRID_SIZE))
        
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(10)
        
        if score >= 100:
            print("Victory! Score 100 reached!")
            time.sleep(2)
            return "menu"

def ai_move(snake, food):
    head_x, head_y = snake[0]
    food_x, food_y = food
    
    possible_moves = [(GRID_SIZE, 0), (-GRID_SIZE, 0), (0, GRID_SIZE), (0, -GRID_SIZE)]
    safe_moves = [move for move in possible_moves if (head_x + move[0], head_y + move[1]) not in snake and 0 <= head_x + move[0] < WIDTH and 0 <= head_y + move[1] < HEIGHT]
    
    if safe_moves:
        best_move = min(safe_moves, key=lambda move: abs((head_x + move[0]) - food_x) + abs((head_y + move[1]) - food_y))
        return best_move
    return direction

while True:
    mode = main_menu()
    game_loop(mode == "ai")

pygame.quit()
