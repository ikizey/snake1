import pygame
import random
from colour import COLOR_NAME_TO_RGB as C


WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
BASE_PIXEL_WIDTH = 20

pygame.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake")
font = pygame.font.SysFont(None, 20, False, False)
game_speed_text = font.render('Game Speed: 1', True, C['black'])

done = False
clock = pygame.time.Clock()

game_speed = 12
time_tracker = 0


class Pixel(pygame.sprite.Sprite):
    def __init__(self, color, coords):
        super().__init__()
        self.image = pygame.Surface([BASE_PIXEL_WIDTH, BASE_PIXEL_WIDTH])
        self.set_color(color)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coords

    def set_color(self, color):
        self.image.fill(color)


class Cherry(Pixel):
    def __init__(self, coords):
        super().__init__(C['red'], coords)

    # Infinite loop possible if snake occupies almost all screen area
    def new_pos(self, forbidden_coords):
        while True:
            new_x = random.randrange(BASE_PIXEL_WIDTH * 2, WINDOW_WIDTH - BASE_PIXEL_WIDTH * 2, BASE_PIXEL_WIDTH)
            new_y = random.randrange(BASE_PIXEL_WIDTH * 2, WINDOW_HEIGHT - BASE_PIXEL_WIDTH * 2, BASE_PIXEL_WIDTH)
            if not ([new_x, new_y] in forbidden_coords):
                break
        self.rect.x = new_x
        self.rect.y = new_y


class Snake:
    def __init__(self):
        self.pixels = [Pixel(C['darkgreen'], [400, 300])]
        self.DIRECTIONS = ((0, BASE_PIXEL_WIDTH), (BASE_PIXEL_WIDTH, 0), (0, -BASE_PIXEL_WIDTH), (-BASE_PIXEL_WIDTH, 0))
        self.speed = self.DIRECTIONS[0]

    def move(self):
        if len(self.pixels) > 1:
            self.pixels.pop().kill()
            self.pixels.insert(0, Pixel(C['limegreen'], self.get_head_pos()))
        self.pixels[0].rect.x += self.speed[0]
        self.pixels[0].rect.y += self.speed[1]
        self._reclor()

    def turn(self, direction):
        self.speed = self.DIRECTIONS[self.DIRECTIONS.index(self.speed) - direction]

    def grow(self):
        self.pixels.insert(0, Pixel(C['limegreen'], self.get_head_pos()))

    def get_head_pos(self):
        return [self.pixels[0].rect.x, self.pixels[0].rect.y]

    def on(self, surface):
        return surface.get_rect().contains(self.pixels[0].rect)

    def _reclor(self):
        for pix in self.pixels:
            if pix is not self.pixels[0]:
                pix.set_color(C['darkgreen'])


background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(C['black'])
pygame.draw.rect(background, C['white'], background.get_rect(), BASE_PIXEL_WIDTH * 2)

snake = Snake()
cherry = Cherry([400, 330])
snake_sprites = pygame.sprite.RenderPlain(snake.pixels)
cherry_sprites = pygame.sprite.RenderPlain(cherry)
cherry_eaten = []
snake_body_sprites = []

# ---Main loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snake.turn(3)
            if event.key == pygame.K_RIGHT:
                snake.turn(1)

    snake_bitten = pygame.sprite.spritecollide(snake.pixels[0], snake_body_sprites, False)
    if not snake_bitten and snake.on(screen):

        cherry_eaten = pygame.sprite.spritecollide(cherry, snake_sprites, False)
        if cherry_eaten:
            cherry_eaten = []
            cherry.new_pos(snake.get_head_pos())
            snake.grow()

        if game_speed > 1:
            time_tracker += 1
            if time_tracker == 20 * 60:
                time_tracker = 0
                game_speed -= 1
                game_speed_text = font.render(' '.join(['Game Speed:', str(13 - game_speed)]), True, C['black'])
        if time_tracker % game_speed == 0:
            screen.blit(background, screen.get_rect())
            snake.move()
            snake_sprites = pygame.sprite.RenderPlain(snake.pixels)
            snake_body_sprites = pygame.sprite.RenderPlain(snake.pixels[1:])
            screen.blit(game_speed_text, screen.get_rect())
            cherry_sprites.draw(screen)
            snake_sprites.draw(screen)
            pygame.display.flip()

        clock.tick(60)
    else:
        done = True

pygame.quit()
