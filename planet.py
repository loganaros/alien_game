import pygame
from alien import Alien

class Planet:
    timer = 3
    capture_timer = 5

    GRAVITY = 100000 * .75

    def __init__(self, pos, radius, id, aliens, color):
        self.pos = pygame.Vector2(pos)
        self.radius = radius
        self.id = id
        self.aliens = aliens
        self.color = color
        self.friendly = False

    def draw(self, screen, camera):
        pygame.draw.circle(screen, self.color, self.pos - camera, self.radius)

    def apply_gravity(self, target, dt):
        dist = self.pos.distance_to(target.pos)
        if dist <= (self.radius * 3) and dist >= self.radius > 0:
            direction = self.pos - target.pos
            direction = direction.normalize()
            force = (self.GRAVITY / dist) * (self.radius / 100)
            target.vel += direction * force * dt

    def resolve_collision(self, target):
        dist = self.pos.distance_to(target.pos)
        if dist < self.radius:
            outward = (target.pos - self.pos).normalize()
            target.pos = self.pos + outward * self.radius
            target.vel = pygame.Vector2(0, 0) 

    def update(self, dt, player, screen, camera):
        if len(self.aliens) < 3:
            self.timer -= dt
            if self.timer <= 0:
                self.aliens.append(Alien(self.pos, radius=8, friendly=self.friendly))
                self.timer = 3

        distance_to_player = self.pos.distance_to(player.pos)
        if distance_to_player <= self.radius + 10 and not self.friendly:
            self.capture_timer -= dt
            if self.capture_timer <= 0:
                self.friendly = True

        pygame.draw.rect(screen, "green", pygame.Rect(self.pos.x - 25 - camera.x, self.pos.y - 5 - camera.y, self.capture_timer * 10, 10))
        
