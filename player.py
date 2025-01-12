import pygame
from circleshape import CircleShape
from constants import PLAYER_HEALTH, PLAYER_RADIUS, PLAYER_SHOOT_COOLDOWN, PLAYER_SHOOT_SPEED, PLAYER_SPEED, PLAYER_TURN_SPEED, SCREEN_HEIGHT, SCREEN_WIDTH
from shot import Shot

class Player(CircleShape):
  def __init__(self, x, y):
    super().__init__(x, y, PLAYER_RADIUS)
    self.invisible = 0
    self.rotation = 0
    self.timer = 0
    self.health = PLAYER_HEALTH
  
  def triangle(self):
    forward = pygame.Vector2(0, 1).rotate(self.rotation)
    right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
    a = self.position + forward * self.radius
    b = self.position - forward * self.radius - right
    c = self.position - forward * self.radius + right
    return [a, b, c]
  
  def draw(self, screen):
    if self.invisible > 0:
      if int(self.invisible * 20) % 2 == 0:
        pygame.draw.polygon(screen, "#ffffff", self.triangle(), 2)
    else:
      pygame.draw.polygon(screen, "#ffffff", self.triangle(), 2)

  def rotate(self, dt):
    self.rotation += PLAYER_TURN_SPEED * dt

  def move(self, dt):
    forward = pygame.Vector2(0, 1).rotate(self.rotation)
    new_position = self.position + forward * PLAYER_SPEED * dt

    if new_position.x >= 0 and new_position.x <= SCREEN_WIDTH:
        self.position.x = new_position.x
    
    if new_position.y >= 0 and new_position.y <= SCREEN_HEIGHT:
        self.position.y = new_position.y

  def shoot(self, dt):
    if self.timer > 0:
      return
    self.timer = PLAYER_SHOOT_COOLDOWN
    shot = Shot(self.position.x, self.position.y)
    shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

  def update(self, dt):
    keys = pygame.key.get_pressed()
    self.timer -= dt
    self.invisible -= dt

    if keys[pygame.K_a]:
      self.rotate(dt * -1)

    if keys[pygame.K_d]:
      self.rotate(dt)

    if keys[pygame.K_w]:
      self.move(dt)

    if keys[pygame.K_s]:
      self.move(dt * -1)

    if keys[pygame.K_SPACE]:
      self.shoot(dt)