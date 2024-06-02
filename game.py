"""
Filename : game.py
Author : Archit
Date Created : 6/2/2024
Description : Space Invaders Game entry script
Language : python3
"""

import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WINDOW_SIZE = (800, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Space Invaders")

# Set up the clock
clock = pygame.time.Clock()

# Set up the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the player
player = pygame.Rect(370, 480, 60, 60)
player_speed = 5

# Set up the enemy
enemy = pygame.Rect(370, 50, 60, 60)
enemy_speed = 2

# Set up the bullet
bullet = pygame.Rect(0, 0, 5, 10)
bullet_state = "ready"
bullet_speed = 5

# Set up the score
score = 0
font = pygame.font.Font("freesansbold.ttf", 32)
text_x = 10
text_y = 10

# Game loop
while True:
    # Fill the screen with black color
    screen.fill(BLACK)

    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Check for key press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.x -= player_speed
            if event.key == pygame.K_RIGHT:
                player.x += player_speed
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet.x = player.x + 25
                    bullet.y = player.y
                    bullet_state = "fire"

    # Move the enemy
    enemy.x += enemy_speed
    if enemy.x >= 740:
        enemy_speed = -2
        enemy.y += 40

    if enemy.x <= 0:
        enemy_speed = 2
        enemy.y += 40

    # Move the bullet
    if bullet_state == "fire":
        bullet.y -= bullet_speed
        if bullet.y <= 0:
            bullet_state = "ready"

    # Check for collision
    if bullet.colliderect(enemy):
        enemy.x = 370
        enemy.y = 50
        bullet_state = "ready"
        score += 1
    # Erase bullet if collision
    if bullet_state == "ready":
        bullet.y = 0

    # Draw the player
    pygame.draw.rect(screen, WHITE, player)

    # Draw the enemy
    pygame.draw.rect(screen, WHITE, enemy)

    # Draw the bullet
    pygame.draw.rect(screen, WHITE, bullet)

    # Draw the score
    score_text = font.render("Score : " + str(score), True, WHITE)
    screen.blit(score_text, (text_x, text_y))

    # Update the display
    pygame.display.update()

    # Set the frame rate
    clock.tick(60)

# End of the game loop
# End of the script



