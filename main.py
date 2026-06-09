import pygame
import random
from alien import Alien
from planet import Planet
from player import Player

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player = Player((screen.get_width() / 2, screen.get_height() / 2))

planets = []

GRAVITY = 100000

for i in range(8,10):
    planet_radius = random.randint(35, 55)
    color = pygame.Color(random.randint(0, i * 25), random.randint(0, i * 25), random.randint(0, i * 25))
    pos = pygame.Vector2(random.randint(planet_radius, screen.get_width() - planet_radius), random.randint(planet_radius, screen.get_height() - planet_radius))
    # aliens = [Alien(pos + pygame.Vector2(random.randint(-20, 20), random.randint(-20, 20)), pygame.Vector2(0,0)) for _ in range(5)]
    aliens = []
    planets.append(Planet(pos, planet_radius, i, aliens, color))

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    player.draw(screen)

    for planet in planets:
        pygame.draw.circle(screen, planet.color, planet.pos, planet.radius)
        dist = planet.pos.distance_to(player.pos)
        direction = planet.pos - player.pos

        if dist <= (planet.radius * 3) and dist >= planet.radius:
            direction = direction.normalize()
            force = GRAVITY / dist
            player.vel += direction * force * dt

        for alien in planet.aliens:
            pygame.draw.circle(screen, planet.color, alien.pos, 8)
            target = None
            if planet.friendly:
                alien.friendly = True
                pygame.draw.circle(screen, "green", pygame.Vector2(alien.pos.x, alien.pos.y - 10), 3)
                target = planet.pos
            else:
                pygame.draw.circle(screen, "red", pygame.Vector2(alien.pos.x, alien.pos.y - 10), 3)
                target = player.pos
            alien.update(target, dt, planet.aliens)

        planet.update(dt, dist)

    keys = pygame.key.get_pressed()
    player.handle_input(keys, dt)
    player.update(dt)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()