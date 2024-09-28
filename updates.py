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


def movement(enemy_obj):
    """
    Helper function to move the enemies left and right. If the leftmost enemy hits the left wall,
    the enemies will move down and change direction. If the rightmost enemy hits the right wall,
    the enemies will move down and change direction. In case of absent enemies in the list, the
    function will account for the absence and move the enemies to the extremes by calculating new
    bounds.

    To demonstrate jagged movement, the positions of the enemies are everytime with a value equal to
    enemy_update_delay parameter in the Enemy class in entities.py.

    :param enemy_obj: Enemy object containing list of active enemies and movement properties.
    :return: None
    """
    enemy_obj.enemy_update_counter += 1
    if enemy_obj.enemy_update_counter >= enemy_obj.enemy_update_delay:
        enemy_obj.enemy_update_counter = 0

        # Check the leftmost and rightmost enemies
        if not enemy_obj.enemies:
            return

        leftmost_enemy = min(enemy_obj.enemies, key=lambda e: e[0].left)[0]
        rightmost_enemy = max(enemy_obj.enemies, key=lambda e: e[0].right)[0]

        # Check if the leftmost enemy has hit the left wall
        if leftmost_enemy.left <= 0:
            enemy_obj.enemy_speed = abs(enemy_obj.enemy_speed)
            for enemy in enemy_obj.enemies:
                enemy[0].y += 10  # Move down by a fixed step
        # Check if the rightmost enemy has hit the right wall
        elif rightmost_enemy.right >= SURFACE_WIDTH:
            enemy_obj.enemy_speed = -abs(enemy_obj.enemy_speed)
            for enemy in enemy_obj.enemies:
                enemy[0].y += 10  # Move down by a fixed step

        # Move all enemies horizontally
        for enemy in enemy_obj.enemies:
            enemy[0].x += enemy_obj.enemy_speed


def fire_bullet(bullet_obj, player_obj):
    """
    Helper function to fire a bullet from the player object.
    :return: None
    """
    if bullet_obj.bullet_fired:
        # Move bullet up (subtract speed)
        bullet_obj.bullet.y -= bullet_obj.bullet_speed
        # Out of bounds condition
        if bullet_obj.bullet.top <= 0:
            bullet_obj.bullet_fired = False
            # Reset y to player center
            bullet_obj.bullet.y = player_obj.player.centery


def collision(bullet_obj, enemy_obj, player_obj):
    """
    Helper function to detect collision between bullet and enemies. Successful collision
    removes enemy from list.

    :return: None
    """
    # Check if bullet is fired and if it collides with an enemy
    if bullet_obj.bullet_fired:
        for enemy in enemy_obj.enemies:
            rect_enemy = enemy[0]
            if rect_enemy.colliderect(bullet_obj.bullet):
                # Reset bullet position
                bullet_obj.bullet_fired = False
                bullet_obj.bullet.y = player_obj.player.centery
                # Remove enemy from list and return 1 point
                enemy_obj.enemies.remove(enemy)
                return 1, False

    for enemy in enemy_obj.enemies:
        if enemy[0].colliderect(player_obj.player):
            return 0, True

    return 0, False


def render_enemy(waves, num_enemies_per_wave, assets):
    """
    Helper to create a list of enemy objects (Rectangles) on screen.
    The list will have gaps between each enemy.
    If collision is detected, remove the enemy from the list.

    :param waves: Number of waves in the current level
    :param num_enemies_per_wave: Number of enemies in each wave
    :param assets: Dictionary of enemy sprites
    :return:
    """
    # List of enemies
    enemies = list()
    enemy_y = 50
    enemy_x = 15
    index = 0
    enemy_types = len(assets)

    while waves > 0:
        pointer = num_enemies_per_wave
        current_type = 1
        while pointer > 0:
            enemy_rect = pygame.Rect(enemy_x, enemy_y, 10, 10)
            enemy_sprite = assets[str(current_type)]
            enemies.append([enemy_rect, enemy_sprite])
            enemy_x += enemy_rect.width + 10
            if enemy_x >= SURFACE_WIDTH or enemy_rect.right > SURFACE_WIDTH:
                enemies.pop(index)
                break
            # Move to next enemy
            index += 1
            pointer -= 1
            current_type = (current_type % enemy_types) + 1  # Cycle through enemy types
        # Move to next row
        enemy_y += 20
        enemy_x = 15
        waves -= 1
    return enemies


def player_movement(player_obj, bullet_obj):
    """
    Helper function to move the player object.
    :return: None
    """
    # Move player
    if player_obj.move_left and player_obj.player.left > 0:
        player_obj.player.x -= player_obj.player_speed
    if player_obj.move_right and player_obj.player.right < SURFACE_WIDTH:
        player_obj.player.x += player_obj.player_speed

    # Update bullet position with player's position
    if not bullet_obj.bullet_fired:
        bullet_obj.bullet.x = player_obj.player.centerx - 2
        bullet_obj.bullet.y = player_obj.player.centery
