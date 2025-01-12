import sys
from time import sleep
import pygame
from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import *
from player import Player
from shot import Shot

def create_text_box(font, text, text_color, box_color, margin_x=0, margin_y=0):
  text_surf = font.render(text, True, text_color)
  box_surf = pygame.Surface(text_surf.get_rect().inflate(margin_x, margin_y).size)
  box_surf.fill(box_color)
  box_surf.set_alpha(255)
  box_surf.blit(text_surf, text_surf.get_rect(center = box_surf.get_rect().center))
  return box_surf

def display_ui_elements(screen, font, score, player, asteroid_count):
    # Define the elements and their initial positions
    ui_elements = [
      {"text": f"Score: {score}", "color": "#000000", "bg_color": "#ffffff", "pos": (5, 10)},
      {"text": f"Asteroids: {asteroid_count}", "color": "#000000", "bg_color": "#ffffff", "pos": (0, 10)},  # x=0 will be adjusted later
      {"text": f"Health: {player.health}", "color": "#000000", "bg_color": "#ffffff", "pos": (0, 10)}  # x=0 will be adjusted later
    ]

    # Calculate positions dynamically, adjust x position for each element
    x_offset = 5  # Starting x position
    for element in ui_elements:
      text_surf = create_text_box(font, element["text"], element["color"], element["bg_color"], 10, 5)
      element["pos"] = (x_offset, element["pos"][1])  # Set x position dynamically
      screen.blit(text_surf, text_surf.get_rect(topleft=element["pos"]))
      x_offset += text_surf.get_width() + 10  # Move x_offset to the right for the next element

def handle_game_over(font, screen):
  """
  Displays the game over screen and waits for player input to exit.
  """
  game_over_text = [
    "Game over! see you space cowboy...",
    "Press ESC to exit"
  ]
  y_pos = SCREEN_HEIGHT / 2

  for text in game_over_text:
      game_over_surf = create_text_box(font, text, "white", "black")
      screen.blit(game_over_surf, game_over_surf.get_rect(centerx=SCREEN_WIDTH / 2, y=y_pos))
      y_pos += font.get_height()

  keys = pygame.key.get_pressed()
  if keys[pygame.K_ESCAPE]:
      pygame.quit()
      sys.exit()

def update_score(font, score, score_info):
  """
  Updates the score display.
  """
  score_info["text"] = f"Score: {score}"
  return create_text_box(font, score_info["text"], score_info["color"], score_info["bg_color"], 10, 5)

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
  score = 0

  screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

  font = pygame.font.Font(None, 32)
  welcome_text_surf = create_text_box(font, "Asteroids - Pew, Pew, Pew!", "white", "black")

  score_info = {
    "text": f"Score: {score}",
    "color": "#000000",
    "bg_color": "#ffffff"
  }
  ship_crashed = False

  while True:
    screen.fill("#000000")
    screen.blit(welcome_text_surf, welcome_text_surf.get_rect(centerx=SCREEN_WIDTH/2, y=SCREEN_HEIGHT/4))
    display_ui_elements(screen, font, score, player, Asteroid.counter)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          return
      
    for obj in updatable:
      if not ship_crashed:
        obj.update(dt)
        asteroid_counter_text_surf = create_text_box(font, f"Asteroid: {Asteroid.counter}", "black", "white", 10, 5)
        if welcome_text_surf.get_alpha() > 0:
          welcome_text_surf.set_alpha(welcome_text_surf.get_alpha() - 0.1)
      
    for asteroid in asteroids:
      if asteroid.collides_with(player) and player.invisible <= 0:

        player.health -= 1
        player.invisible = 1
        player_health_text_surf = create_text_box(font, f"Health: {player.health}", "Black", "White", 10, 5)


        if player.health == 0:
          ship_crashed = True

      for shot in shots:
        if asteroid.collides_with(shot):
          shot.kill()
          asteroid.split()
          score += 1
          score_text_surf = update_score(font, score, score_info)

    for obj in drawable:
      obj.draw(screen)

    if (ship_crashed):
      dt = 0
      handle_game_over(font, screen)

    else:
      dt = delta.tick(60) / 1000

    pygame.display.flip()


if __name__ == "__main__":
  main()