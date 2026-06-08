# Example file showing a circle moving on screen
import pygame
import random

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

planets = []
planet_radius = 50
vertical_velocity, horizontal_velocity = 0, 0

GRAVITY = 10

for i in range(10):
    planets.append(pygame.Vector2(random.randint(planet_radius, screen.get_width() - planet_radius), random.randint(planet_radius, screen.get_height() - planet_radius)))

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    pygame.draw.circle(screen, "white", player_pos, 20)

    for planet in planets:
        pygame.draw.circle(screen, "grey", planet, planet_radius)
        dist = ((planet.x - player_pos.x) ** 2) + ((planet.y - player_pos.y) ** 2)
        if dist <= (planet_radius * 3) ** 2 and dist >= planet_radius ** 2:
            vertical_velocity += (planet.y - player_pos.y) * dt * GRAVITY
            horizontal_velocity += (planet.x - player_pos.x) * dt * GRAVITY

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        vertical_velocity -= 10
    if keys[pygame.K_s]:
        vertical_velocity += 10
    if keys[pygame.K_a]:
        horizontal_velocity -= 10
    if keys[pygame.K_d]:
        horizontal_velocity += 10

    
    
    player_pos.x += horizontal_velocity * dt
    player_pos.y += vertical_velocity * dt

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()