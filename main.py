import sys
from time import sleep
import pygame
from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import *
from player import Player
from shot import Shot

def main():
  pygame.init()
  pygame.display.set_caption("Asteroids - Pew, Pew, Pew!")

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

  font = pygame.font.Font(None, 32)
  welcome_text = font.render("Asteroids - Pew, Pew, Pew!", True, "white")
  welcome_text_rect = welcome_text.get_rect(centerx=SCREEN_WIDTH/2, y=SCREEN_HEIGHT/4)
  ship_crashed = False

  while True:
    screen.fill("#000000")
    screen.blit(welcome_text, welcome_text_rect)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          return
      
    for obj in updatable:
      if not ship_crashed:
        obj.update(dt)
        if welcome_text.get_alpha() > 0:
          welcome_text.set_alpha(welcome_text.get_alpha() - 0.1)
      
    for asteroid in asteroids:
      if asteroid.collides_with(player):
        ship_crashed = True

      for shot in shots:
        if asteroid.collides_with(shot):
          shot.kill()
          asteroid.split()

    for obj in drawable:
      obj.draw(screen)

    if (ship_crashed):
      dt = 0
      init_text = """Game over! see you space cowboy...
Press esc to exit"""
      lines = init_text.splitlines()
      y_pos = SCREEN_HEIGHT/2

      for line in lines:
        game_over_text = font.render(line, True, "White")
        game_over_text_rect = game_over_text.get_rect(centerx=SCREEN_WIDTH/2, y=y_pos)
        screen.blit(game_over_text, game_over_text_rect)
        y_pos += font.get_height()

      keys = pygame.key.get_pressed()
      if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()
        return
    
    else:
      dt = delta.tick(60) / 1000

    pygame.display.flip()


if __name__ == "__main__":
  main()