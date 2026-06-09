# Example file showing a circle moving on screen
import pygame
import random
from alien import Alien

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
player_vel = pygame.Vector2(0, 0)

planets = []
planet_radius = 50

aliens = Alien(pygame.Vector2(random.randint(0, screen.get_width()), random.randint(0, screen.get_height())))

GRAVITY = 100000

for i in range(10):
    planets.append(pygame.Vector2(random.randint(planet_radius, screen.get_width() - planet_radius), random.randint(planet_radius, screen.get_height() - planet_radius)))

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    pygame.draw.circle(screen, "white", player_pos, 20)

    for planet in planets:
        pygame.draw.circle(screen, "grey", planet, planet_radius)
        dist = planet.distance_to(player_pos)
        direction = planet - player_pos
        if dist <= (planet_radius * 3) and dist >= planet_radius:
            direction = direction.normalize()
            force = GRAVITY / dist
            player_vel += direction * force * dt

    pygame.draw.circle(screen, "purple", aliens.pos, 5)
    aliens.update(player_pos, dt)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_vel.y -= 1000 * dt
    if keys[pygame.K_s]:
        player_vel.y += 1000 * dt
    if keys[pygame.K_a]:
        player_vel.x -= 1000 * dt
    if keys[pygame.K_d]:
        player_vel.x += 1000 * dt

    
    
    player_pos += player_vel * dt

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()