"""
 Pygame base template for opening a window

 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/

 Explanation video: http://youtu.be/vRB_983kUMc
"""

import pygame
import random
from colour import COLOR_NAME_TO_RGB as C

pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake")
font = pygame.font.SysFont(None, 20, False, False)

# Some Coordinates
TOP_LEFT = [0, 0]
TOP_RIGHT = [WINDOW_WIDTH, 0]
BOTTOM_LEFT = [0, WINDOW_HEIGHT]
BOTTOM_RIGHT = [WINDOW_WIDTH, WINDOW_HEIGHT]

# Game speed
game_speed = 12
time_tracker = 0

# Border Color
BORDER_COLOR = C['white']

# Snake code
snake_pixel_size = 20
snake_coords = [[400, 300]]
snake_speeds = ((0, snake_pixel_size), (snake_pixel_size, 0), (0, -snake_pixel_size), (-snake_pixel_size, 0))
snake_speed_x, snake_speed_y = snake_speeds[0]
SNAKE_HEAD_COLOR = C['limegreen']
SNAKE_BODY_COLOR = C['darkgreen']
# cherry
cherry_coord_x, cherry_coord_y = 400, 320


def cherry_random_coordinates():
    while True:
        new_x = random.randrange(snake_pixel_size * 2, WINDOW_WIDTH - snake_pixel_size * 2, snake_pixel_size)
        new_y = random.randrange(snake_pixel_size * 2, WINDOW_HEIGHT - snake_pixel_size * 2, snake_pixel_size)
        if not ([new_x, new_y] in snake_coords):
            break
    return new_x, new_y


clock = pygame.time.Clock()
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snake_speed_x, snake_speed_y = snake_speeds[snake_speeds.index((snake_speed_x, snake_speed_y)) - 3]
            if event.key == pygame.K_RIGHT:
                snake_speed_x, snake_speed_y = snake_speeds[snake_speeds.index((snake_speed_x, snake_speed_y)) - 1]

    # Lose
    # --Hit a wall
    if snake_coords[0][0] < 0 + snake_pixel_size or snake_coords[0][0] > WINDOW_WIDTH - snake_pixel_size:
        done = True
    if snake_coords[0][1] < 0 + snake_pixel_size or snake_coords[0][1] > WINDOW_HEIGHT - snake_pixel_size:
        done = True
    # --Eat itself
    if snake_coords[0] in snake_coords[2:]:
        done = True

    # Snake Movement + Game Speed
    time_tracker += 1
    # Increase game speed every 20? secs(?)
    if time_tracker == 20 * 60:
        time_tracker = 0
        if game_speed > 1:
            game_speed += -1
    text = font.render(' '.join(['Game Speed:', str(13 - game_speed)]), True, C['black'])
    #
    if time_tracker % game_speed == 0:
        if len(snake_coords) > 1:
            snake_coords.pop()
            snake_coords.insert(0, snake_coords[0][:])
        snake_coords[0][0], snake_coords[0][1] = snake_coords[0][0] + snake_speed_x, snake_coords[0][1] + snake_speed_y

    # cherry eaten
    if (snake_coords[0][0], snake_coords[0][1]) == (cherry_coord_x, cherry_coord_y):
        snake_coords.append(snake_coords[-1][:])
        cherry_coord_x, cherry_coord_y = cherry_random_coordinates()
    screen.fill(C['black'])
    # Draw Borders
    pygame.draw.line(screen, BORDER_COLOR, TOP_LEFT, BOTTOM_LEFT, snake_pixel_size * 2)
    pygame.draw.line(screen, BORDER_COLOR, TOP_LEFT, TOP_RIGHT, snake_pixel_size * 2)
    pygame.draw.line(screen, BORDER_COLOR, BOTTOM_LEFT, BOTTOM_RIGHT, snake_pixel_size * 2)
    pygame.draw.line(screen, BORDER_COLOR, TOP_RIGHT, BOTTOM_RIGHT, snake_pixel_size * 2)
    # Draw Snake
    pygame.draw.rect(screen, C['red'], [cherry_coord_x, cherry_coord_y, snake_pixel_size, snake_pixel_size])
    for i in range(len(snake_coords)):
        if i == 0:
            pygame.draw.rect(screen, SNAKE_HEAD_COLOR,
                             [snake_coords[i][0], snake_coords[i][1], snake_pixel_size, snake_pixel_size])
        else:
            pygame.draw.rect(screen, SNAKE_BODY_COLOR,
                             [snake_coords[i][0], snake_coords[i][1], snake_pixel_size, snake_pixel_size])
    screen.blit(text, TOP_LEFT)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
