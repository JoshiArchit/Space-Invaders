"""
Filename : updates.py
Author : Archit Joshi
Date Created : 6/2/2024
Description : Script to define all the render and update functions which will be called in the game
loop.
Language : python3
"""
import pygame

DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480
SURFACE_WIDTH = 320
SURFACE_HEIGHT = 240


# # Original movement with dictionary
# def movement(game):
#     """
#     Helper function for jagged enemy movement.
#     :return: None
#     """
#     game.enemy_update_counter += 1
#     if game.enemy_update_counter >= game.enemy_update_delay:
#         game.enemy_update_counter = 0
#
#         # Check the leftmost and rightmost enemies
#         leftmost_enemy = game.enemies[min(game.enemies.keys())][0]
#         rightmost_enemy = game.enemies[max(game.enemies.keys())][0]
#
#         # Doesn't matter if they are alive or dead. They will move together. Alive or dead is
#         # handled in collision
#         for enemy, info in game.enemies.items():
#             enemy_rect = info[0]  # Rect object is the first element in the tuple
#             enemy_rect.x += game.enemy_speed
#
#         # Check if the leftmost enemy has hit the left wall
#         if leftmost_enemy.left <= 0:
#             game.enemy_speed = abs(game.enemy_speed)
#             for enemy, info in game.enemies.items():
#                 enemy_rect = info[0]
#                 enemy_rect.y += 10
#         # Check if the rightmost enemy has hit the right wall
#         elif rightmost_enemy.right >= SURFACE_WIDTH:
#             game.enemy_speed = -abs(game.enemy_speed)
#             for enemy, info in game.enemies.items():
#                 enemy_rect = info[0]
#                 enemy_rect.y += 10

def movement(self):
    self.enemy_update_counter += 1
    if self.enemy_update_counter >= self.enemy_update_delay:
        self.enemy_update_counter = 0

        # Check the leftmost and rightmost enemies
        leftmost_enemy = self.enemies[0][0]
        rightmost_enemy = self.enemies[len(self.enemies) - 1][0]

        # Use left_most and right_most to calculate bounds for the row
        left_most = leftmost_enemy.left
        right_most = rightmost_enemy.right

        # Check if the leftmost enemy has hit the left wall
        if left_most <= 0:
            self.enemy_speed = abs(self.enemy_speed)
            for enemy_rect in self.enemies:
                enemy_rect[0].y += 10
        # Check if the rightmost enemy has hit the right wall
        elif right_most >= SURFACE_WIDTH:
            self.enemy_speed = -abs(self.enemy_speed)
            for enemy_rect in self.enemies:
                enemy_rect[0].y += 10

        # Move all enemies
        for enemy in self.enemies:
            enemy[0].x += self.enemy_speed


def fire_bullet(game):
    """
    Helper function to fire a bullet from the player object.
    :return: None
    """
    if game.bullet_fired:
        # Move bullet up (subtract speed)
        game.bullet.y -= game.bullet_speed
        # Out of bounds condition
        if game.bullet.top <= 0:
            game.bullet_fired = False
            # Reset y to player center
            game.bullet.y = game.player.centery


def collision(game):
    """
    Helper function to detect collision between bullet and enemies. Successful collision
    removes enemy from list.

    :return: None
    """
    # Original collision detection with dictionary
    # if game.bullet_fired:
    #     for enemy, enemy_info in game.enemies.items():
    #         rect_enemy, isalive = enemy_info
    #         if rect_enemy.colliderect(game.bullet) and isalive:
    #             game.bullet_fired = False
    #             game.bullet.y = game.player.centery
    #             game.enemies[enemy] = (rect_enemy, False)

    if game.bullet_fired:
        for enemy in game.enemies:
            rect_enemy = enemy[0]
            if rect_enemy.colliderect(game.bullet):
                game.bullet_fired = False
                game.bullet.y = game.player.centery
                game.enemies.remove(enemy)
                game.score += 1


def scorebar(game):
    # Display score and lives
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {game.score}", True, (255, 255, 255))
    lives_text = font.render(f"Lives: {game.lives}", True, (255, 255, 255))
    game.display.blit(score_text, (10, 10))
    game.display.blit(lives_text, (10, 40))


def render_enemy():
    """
    Helper to create a list of enemy objects (Rectangles) on screen.
    The list will have gaps between each enemy.
    If collision is detected, remove the enemy from the list.
    :return:
    """
    # # ORIGINAL enemies dictionary to store enemy objects and alive status
    # enemies = list()
    # enemy_y = 50
    # enemy_x = 15
    # counter = 0
    # while True:
    #     enemies[counter] = (pygame.Rect(enemy_x, enemy_y, 10, 10), True)
    #     enemy_x += enemies[counter][0].width + 10
    #     if enemy_x >= SURFACE_WIDTH or enemies[counter][0].right > SURFACE_WIDTH:
    #         enemies.pop(counter)
    #         return enemies
    #     counter += 1

    # List of enemies
    enemies = list()
    enemy_y = 50
    enemy_x = 15
    counter = 0
    while True:
        enemies.append((pygame.Rect(enemy_x, enemy_y, 10, 10), True))
        enemy_x += enemies[counter][0].width + 10
        if enemy_x >= SURFACE_WIDTH or enemies[counter][0].right > SURFACE_WIDTH:
            enemies.pop(counter)
            return enemies
        counter += 1


def player_movement(game):
    """
    Helper function to move the player object.
    :return: None
    """
    # Move player
    if game.move_left and game.player.left > 0:
        game.player.x -= game.player_speed
    if game.move_right and game.player.right < SURFACE_WIDTH:
        game.player.x += game.player_speed

    # Update bullet position with player's position
    if not game.bullet_fired:
        game.bullet.x = game.player.centerx - 2
        game.bullet.y = game.player.centery
