import sys
import pygame
from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import *
from player import Player
from shot import Shot

def main():
  pygame.init()

  print("Starting asteroids!")
  print(f"Screen width: {SCREEN_WIDTH}")
  print(f"Screen height: {SCREEN_HEIGHT}")

  updatable = pygame.sprite.Group()
  drawable = pygame.sprite.Group()
  asteroids = pygame.sprite.Group()
  shots = pygame.sprite.Group()

  Player.containers = (updatable, drawable)
  Asteroid.containers = (asteroids, updatable, drawable)
  AsteroidField.containers = updatable
  Shot.containers = (shots, updatable, drawable) 

  player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
  asteroid_field = AsteroidField()

  delta = pygame.time.Clock()
  dt = 0
  screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          return
      
    for obj in updatable:
      obj.update(dt)
      
    for asteroid in asteroids:
      if asteroid.collides_with(player):
        print("Game over!")
        
        pygame.quit()
        sys.exit()

      for shot in shots:
        if asteroid.collides_with(shot):
          shot.kill()
          asteroid.kill()

    screen.fill("#000000")
    for obj in drawable:
      obj.draw(screen)

    dt = delta.tick(60) / 1000
    pygame.display.flip()


if __name__ == "__main__":
  main()