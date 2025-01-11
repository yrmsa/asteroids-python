import pygame
from constants import *

def main():
  pygame.init()

  print("Starting asteroids!")
  print(f"Screen width: {SCREEN_WIDTH}")
  print(f"Screen height: {SCREEN_HEIGHT}")

  delta = pygame.time.Clock()
  dt = 0
  screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          return
      
    screen.fill("#000000")

    dt = delta.tick(60) / 1000
    pygame.display.flip()


if __name__ == "__main__":
  main()