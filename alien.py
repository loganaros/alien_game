import pygame

class Alien:

    separate_weight = 1
    align_weight = .3
    cohesion_weight = .1
    max_speed = 10

    radius = 300

    def __init__(self, pos, vel=None, friendly=False):
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(vel) if vel is not None else pygame.Vector2(0, 0)
        self.speed = 10
        self.friendly = friendly

    def separate(self, neighbors, dt):
        for neighbor in neighbors:
            if self.pos.distance_to(neighbor.pos) < self.radius and neighbor != self:
                direction = self.pos - neighbor.pos
                if direction.length() > 0:
                    direction = direction.normalize()
                    self.vel += direction * dt * self.separate_weight

    def align(self, neighbors, dt):
        average_vel = pygame.Vector2(self.vel)
        count = 1
        for neighbor in neighbors:
            if self.pos.distance_to(neighbor.pos) < self.radius and neighbor != self:
                average_vel += neighbor.vel
                count += 1

        if count > 1:
            average_vel /= count
            self.vel += (average_vel - self.vel) * dt * self.align_weight

    def cohesion(self, neighbors, dt):
        average_pos = pygame.Vector2(self.pos)
        count = 1
        for neighbor in neighbors:
            if self.pos.distance_to(neighbor.pos) < self.radius and neighbor != self:
                average_pos += neighbor.pos
                count += 1
        
        if count > 1:
            average_pos /= count
            self.vel += (average_pos - self.pos) * dt * self.cohesion_weight

    def avoid(self, target, dt):
        if self.pos.distance_to(target) < 40:
            direction = self.pos - target
            if direction.length() > 0:
                direction = direction.normalize()
                self.vel += direction * self.speed * dt * 10


    def update(self, target, dt, neighbors):
        direction = target - self.pos
        if direction.length() > 0:
            direction = direction.normalize()
            self.vel += direction * self.speed * dt * 1.5
        self.pos += self.vel
        self.separate(neighbors, dt)
        self.align(neighbors, dt)
        self.cohesion(neighbors, dt)
        self.avoid(target, dt)
        if self.vel.length() > self.max_speed:
            self.vel.scale_to_length(self.max_speed)