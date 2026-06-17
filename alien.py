import pygame

class Alien:

    separate_weight = 1.3
    align_weight = .3
    cohesion_weight = .1
    max_speed = 10

    flock_radius = 300

    def __init__(self, pos, radius, vel=None, friendly=False, damage=10):
        self.pos = pygame.Vector2(pos)
        self.radius = radius
        self.vel = pygame.Vector2(vel) if vel is not None else pygame.Vector2(0, 0)
        self.speed = 10
        self.friendly = friendly
        self.damage = damage

    def separate(self, neighbors, dt):
        for neighbor in neighbors:
            if self.pos.distance_to(neighbor.pos) < self.flock_radius and neighbor != self:
                direction = self.pos - neighbor.pos
                if direction.length() > 0:
                    direction = direction.normalize()
                    self.vel += direction * dt * self.separate_weight

    def align(self, neighbors, dt):
        average_vel = pygame.Vector2(self.vel)
        count = 1
        for neighbor in neighbors:
            if self.pos.distance_to(neighbor.pos) < self.flock_radius and neighbor != self:
                average_vel += neighbor.vel
                count += 1

        if count > 1:
            average_vel /= count
            self.vel += (average_vel - self.vel) * dt * self.align_weight

    def cohesion(self, neighbors, dt):
        average_pos = pygame.Vector2(self.pos)
        count = 1
        for neighbor in neighbors:
            if self.pos.distance_to(neighbor.pos) < self.flock_radius and neighbor != self:
                average_pos += neighbor.pos
                count += 1
        
        if count > 1:
            average_pos /= count
            self.vel += (average_pos - self.pos) * dt * self.cohesion_weight

    def avoid(self, target, dt):
        if self.pos.distance_to(target.pos) < target.radius + self.radius:
            direction = self.pos - target.pos
            if direction.length() > 0:
                direction = direction.normalize()
                self.vel += direction * self.speed * dt * 10

    def attack(self, player, dt):
        player.health -= self.damage * dt
        self.vel += (self.pos - player.pos) * self.speed * dt * 2

    def draw(self, screen, camera, planet):
        pygame.draw.circle(screen, planet.color, self.pos - camera, self.radius)
        pygame.draw.line(screen, "white", self.pos - camera, self.pos + (self.vel * 2) - camera)
        marker_color = "green" if planet.friendly else "red"
        pygame.draw.circle(screen, marker_color, pygame.Vector2(self.pos.x, self.pos.y - 10) - camera, 3)


    def update(self, target, dt, neighbors):
        direction = target.pos - self.pos
        if direction.length() > 0:
            direction = direction.normalize()
            self.vel += direction * self.speed * dt * 2
        self.pos += self.vel
        self.separate(neighbors, dt)
        self.align(neighbors, dt)
        self.cohesion(neighbors, dt)
        self.avoid(target, dt)
        if self.vel.length() > self.max_speed:
            self.vel.scale_to_length(self.max_speed)