import pygame

class Player:

    thrust = 1000
    radius = 20

    def __init__(self, pos, vel=None):
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(vel) if vel is not None else pygame.Vector2(0, 0)

    def handle_input(self, keys, dt):
        if keys[pygame.K_w]:
            self.vel.y -= self.thrust * dt
        if keys[pygame.K_s]:
            self.vel.y += self.thrust * dt
        if keys[pygame.K_a]:
            self.vel.x -= self.thrust * dt
        if keys[pygame.K_d]:
            self.vel.x += self.thrust * dt

    def update(self, dt):
        self.pos += self.vel * dt

    def draw(self, screen, camera):
        pygame.draw.circle(screen, "white", self.pos - camera, self.radius)
