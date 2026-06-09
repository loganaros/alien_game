import pygame

class Alien:
    def __init__(self, pos):
        self.pos = pos
        self.speed = 100
    
    def update(self, target, dt):
        direction = target - self.pos
        direction = direction.normalize()
        self.pos += direction * self.speed * dt