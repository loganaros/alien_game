import pygame
from alien import Alien

class Planet:
    timer = 3
    capture_timer = 5

    def __init__(self, pos, radius, id, aliens, color):
        self.pos = pygame.Vector2(pos)
        self.radius = radius
        self.id = id
        self.aliens = aliens
        self.color = color
        self.friendly = False

    def update(self, dt, distance_to_player):
        if len(self.aliens) < 5:
            self.timer -= dt
            if self.timer <= 0:
                self.aliens.append(Alien(self.pos, friendly=self.friendly))
                self.timer = 3

        if distance_to_player <= 60 and not self.friendly:
            self.capture_timer -= dt
            if self.capture_timer <= 0:
                self.friendly = True
        
