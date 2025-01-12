import random
import pygame
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, SCREEN_HEIGHT, SCREEN_WIDTH

class Asteroid(CircleShape):
  counter = 0

  def __init__(self, x, y, radius):
    super().__init__(x, y, radius)
  
  def draw(self, screen):
    pygame.draw.circle(screen, "#ffffff", self.position, self.radius, 2)
  
  def update(self, dt):
    self.position += self.velocity * dt

    # Check for wall collisions and bounce
    if self.position.x < -100 or self.position.x > SCREEN_WIDTH + 100:
      self.velocity.x = -self.velocity.x  # Reverse horizontal velocity (bounce left/right)
    
    if self.position.y < -100 or self.position.y > SCREEN_HEIGHT + 100:
      self.velocity.y = -self.velocity.y  # Reverse vertical velocity (bounce top/bottom)

  def split(self):
    self.kill()
    if self.radius <= ASTEROID_MIN_RADIUS:
      Asteroid.counter -= 1
      return
    
    Asteroid.counter += 1
    random_angle = random.uniform(20, 50)
    new_vector1 = self.velocity.rotate(random_angle)
    new_vector2 = self.velocity.rotate(-random_angle)
    new_radius = self.radius - ASTEROID_MIN_RADIUS

    asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
    asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)

    asteroid1.velocity = new_vector1 * 1.2
    asteroid2.velocity = new_vector2 * 1.2
    
    

