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

# Set the width and height of the screen [width, height]
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

font = pygame.font.SysFont(None, 20, False, False)

# Some Coordinates
TOP_LEFT = [0, 0]
TOP_RIGHT = [WINDOW_WIDTH, 0]
BOTTOM_LEFT = [0, WINDOW_HEIGHT]
BOTTOM_RIGHT = [WINDOW_WIDTH, WINDOW_HEIGHT]

# Game speed
game_speed = 5
time_tracker = 0

# Border Color
BORDER_COLOR = C['white']

pygame.display.set_caption("Snake")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Snake code
snake_pixel_size = 10
snake_coords = [[400, 300]]
snake_speeds = ((0, snake_pixel_size), (snake_pixel_size, 0), (0, -snake_pixel_size), (-snake_pixel_size, 0))
snake_speed_x, snake_speed_y = snake_speeds[0]
SNAKE_HEAD_COLOR = C['limegreen']
SNAKE_BODY_COLOR = C['darkgreen']
# cherry
cherry_coord_x, cherry_coord_y = 400, 330


def cherry_random_coordinates():
    while True:
        new_x = random.randrange(snake_pixel_size * 2, WINDOW_WIDTH - snake_pixel_size * 2, snake_pixel_size)
        new_y = random.randrange(snake_pixel_size * 2, WINDOW_HEIGHT - snake_pixel_size * 2, 10)
        if not ([new_x, new_y] in snake_coords):
            break
    return new_x, new_y

# -------- Main Program Loop -----------


while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snake_speed_x, snake_speed_y = snake_speeds[snake_speeds.index((snake_speed_x, snake_speed_y)) - 3]
            if event.key == pygame.K_RIGHT:
                snake_speed_x, snake_speed_y = snake_speeds[snake_speeds.index((snake_speed_x, snake_speed_y)) - 1]
    # --- Game logic should go here

    # Game Speeed
    time_tracker += 1
    if time_tracker % 100 == 0:
        game_speed += 1
    text = font.render('Game Speed: ' + str(game_speed), True, C['black'])

    # Lose
    # --Hit a wall
    if snake_coords[0][0] < 0 + snake_pixel_size or snake_coords[0][0] > WINDOW_WIDTH - snake_pixel_size:
        done = True
    if snake_coords[0][1] < 0 + snake_pixel_size or snake_coords[0][1] > WINDOW_HEIGHT - snake_pixel_size:
        done = True
    # --Eat itself
    if snake_coords[0] in snake_coords[2:]:
        done = True

    # Snake Movement
    if len(snake_coords) > 1:
        snake_coords.pop()
        snake_coords.insert(0, snake_coords[0][:])
    snake_coords[0][0], snake_coords[0][1] = snake_coords[0][0] + snake_speed_x, snake_coords[0][1] + snake_speed_y

    # cherry eaten
    if (snake_coords[0][0], snake_coords[0][1]) == (cherry_coord_x, cherry_coord_y):
        snake_coords.append(snake_coords[-1][:])
        cherry_coord_x, cherry_coord_y = cherry_random_coordinates()
    # --- Screen-clearing code goes here

    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.

    # If you want a background image, replace this clear with blit'ing the
    # background image.
    screen.fill(C['black'])
    # Draw Borders
    pygame.draw.line(screen, BORDER_COLOR, TOP_LEFT, BOTTOM_LEFT, snake_pixel_size * 2)
    pygame.draw.line(screen, BORDER_COLOR, TOP_LEFT, TOP_RIGHT, snake_pixel_size * 2)
    pygame.draw.line(screen, BORDER_COLOR, BOTTOM_LEFT, BOTTOM_RIGHT, snake_pixel_size * 2)
    pygame.draw.line(screen, BORDER_COLOR, TOP_RIGHT, BOTTOM_RIGHT, snake_pixel_size * 2)
    # pygame.draw.rect(screen, c['limegreen'], [0, 0, snakePixelSize, snakePixelSize])
    # pygame.draw.rect(screen, c['limegreen'], [WINDOW_WIDTH-snakePixelSize, 0, snakePixelSize, snakePixelSize])
    # --- Drawing code should go here
    pygame.draw.rect(screen, C['red'], [cherry_coord_x, cherry_coord_y, snake_pixel_size, snake_pixel_size])
    for i in range(len(snake_coords)):
        if i == 0:
            pygame.draw.rect(screen, SNAKE_HEAD_COLOR,
                             [snake_coords[i][0], snake_coords[i][1], snake_pixel_size, snake_pixel_size])
        else:
            pygame.draw.rect(screen, SNAKE_BODY_COLOR,
                             [snake_coords[i][0], snake_coords[i][1], snake_pixel_size, snake_pixel_size])
    screen.blit(text, TOP_LEFT)
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    # --- FPS
    clock.tick(game_speed)

# Close the window and quit.
pygame.quit()
