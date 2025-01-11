import pygame
from constants import *
from player import Player

def main():
  pygame.init()

  print("Starting asteroids!")
  print(f"Screen width: {SCREEN_WIDTH}")
  print(f"Screen height: {SCREEN_HEIGHT}")

  updatable = pygame.sprite.Group()
  drawable = pygame.sprite.Group()
  Player.containers = (updatable, drawable)

  player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
  delta = pygame.time.Clock()
  dt = 0
  screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          return
      
    for obj in updatable:
      obj.update(dt)
      
    screen.fill("#000000")

    for obj in drawable:
      obj.draw(screen)

    dt = delta.tick(60) / 1000
    pygame.display.flip()


if __name__ == "__main__":
  main()