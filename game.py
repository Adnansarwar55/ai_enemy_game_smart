import pygame
import random
import math
import sys

# Initialize Pygame
pygame.init()

# Music setup
pygame.mixer.music.load("rider.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Enemy Game - Smart Enemies")

# Colors
WHITE = (255, 255, 255)
RED = (255, 60, 60)
BLUE = (50, 150, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Player settings
player_size = 40
player_speed = 5
player_x, player_y = WIDTH // 2, HEIGHT // 2

# Enemy settings
enemy_size = 50
enemy_speed = 2

# Game variables
font = pygame.font.SysFont("Arial", 30)
running = True
game_over = False
frame_count = 0
level = 1
score = 0

# Enemy types
ENEMY_TYPES = ["chaser", "zigzag", "circle", "predict"]

def spawn_enemies(count):
    """Spawn enemies with random types and positions."""
    enemies = []
    for _ in range(count):
        x = random.randint(0, WIDTH - enemy_size)
        y = random.randint(0, HEIGHT - enemy_size)
        etype = random.choice(ENEMY_TYPES)
        enemies.append({"x": x, "y": y, "type": etype, "angle": 0})
    return enemies

enemy_list = spawn_enemies(1)

def move_enemy(enemy, player_x, player_y, speed):
    """Move enemy based on its type."""
    dx = player_x - enemy["x"]
    dy = player_y - enemy["y"]
    distance = math.hypot(dx, dy)

    if distance == 0:
        return

    # Normalize direction
    nx, ny = dx / distance, dy / distance

    # Movement logic by type
    if enemy["type"] == "chaser":
        # Direct chase
        enemy["x"] += speed * nx
        enemy["y"] += speed * ny

    elif enemy["type"] == "zigzag":
        # Zigzag around player
        enemy["x"] += speed * nx + math.sin(pygame.time.get_ticks() * 0.005) * 3
        enemy["y"] += speed * ny + math.cos(pygame.time.get_ticks() * 0.005) * 3

    elif enemy["type"] == "circle":
        # Orbit around player before closing in
        enemy["angle"] += 0.05
        enemy["x"] += speed * nx + math.cos(enemy["angle"]) * 2
        enemy["y"] += speed * ny + math.sin(enemy["angle"]) * 2

    elif enemy["type"] == "predict":
        # Predict player movement slightly
        enemy["x"] += speed * nx * 1.1
        enemy["y"] += speed * ny * 1.1


while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
        if keys[pygame.K_UP]:
            player_y -= player_speed
        if keys[pygame.K_DOWN]:
            player_y += player_speed

        # Keep player on screen
        player_x = max(0, min(WIDTH - player_size, player_x))
        player_y = max(0, min(HEIGHT - player_size, player_y))

        # Move enemies
        for enemy in enemy_list:
            move_enemy(enemy, player_x, player_y, enemy_speed)

            # Collision detection
            if abs(player_x - enemy["x"]) < player_size - 10 and abs(player_y - enemy["y"]) < player_size - 10:
                game_over = True

        # Draw player and enemies
        pygame.draw.rect(screen, BLUE, (player_x, player_y, player_size, player_size))
        for enemy in enemy_list:
            color = RED if enemy["type"] == "chaser" else (
                GREEN if enemy["type"] == "zigzag" else (
                    YELLOW if enemy["type"] == "circle" else (255, 100, 255)
                )
            )
            pygame.draw.rect(screen, color, (enemy["x"], enemy["y"], enemy_size, enemy_size))

        # Update frame count and score
        frame_count += 1
        score = frame_count // FPS

        # Level up every 15 seconds
        if frame_count % (15 * FPS) == 0:
            level += 1
            enemy_speed += 0.3
            new_enemies = spawn_enemies(len(enemy_list))
            enemy_list.extend(new_enemies)

        # Draw HUD
        screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
        screen.blit(font.render(f"Level: {level}", True, YELLOW), (10, 40))

    else:
        text1 = font.render("Game Over! Press R to Restart", True, WHITE)
        text2 = font.render(f"Final Score: {score}", True, GREEN)
        screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, HEIGHT // 2 - 20))
        screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT // 2 + 20))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            # Reset
            player_x, player_y = WIDTH // 2, HEIGHT // 2
            enemy_list = spawn_enemies(1)
            enemy_speed = 2
            frame_count = 0
            level = 1
            score = 0
            game_over = False

    pygame.display.flip()
    clock.tick(FPS)
