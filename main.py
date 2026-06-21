import pygame
import random
# from alien import Alien
from planet import Planet
from player import Player

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player = Player((screen.get_width() / 2, screen.get_height() / 2))

alien_positions = []
alien_velocities = []
alien_friendly = []
alien_homes = []

alien_radius = 8
alien_speed = 10

planets = []

TOPBOUND, RIGHTBOUND, BOTTOMBOUND, LEFTBOUND = -2000, 2000, 2000, -2000

def is_visible(camera, obj):
    return (0 - obj.radius <= obj.pos.x - camera.x <= screen.get_width() + obj.radius) and (0 - obj.radius <= obj.pos.y - camera.y <= screen.get_height() + obj.radius)

# populate planets list with planets with random size, color and position and empty aliens list
def initialize_planets(numPlanets):
    for i in range(numPlanets):
        planet_radius = random.randint(100, 500)
        color = pygame.Color(random.randint(122, 255), random.randint(122, 255), random.randint(122, 255))
        pos = pygame.Vector2(random.randint(LEFTBOUND, RIGHTBOUND), random.randint(TOPBOUND, BOTTOMBOUND))
        planets.append(Planet(pos, planet_radius, i, color))

def draw_grid(camera):
    for i in range(LEFTBOUND, RIGHTBOUND + 100, 100):
        if 0 <= i - camera.x <= screen.get_width():
            pygame.draw.line(screen, "white", pygame.Vector2(i, TOPBOUND) - camera, pygame.Vector2(i, BOTTOMBOUND) - camera)
    for i in range(TOPBOUND, BOTTOMBOUND + 100, 100):
        if 0 <= i - camera.y <= screen.get_height():
            pygame.draw.line(screen, "white", pygame.Vector2(LEFTBOUND, i) - camera, pygame.Vector2(RIGHTBOUND, i) - camera)

def update_aliens():
    for i in range(len(alien_positions)):
        pygame.draw.circle(screen, planets[alien_homes[i]].color, alien_positions[i] - camera, alien_radius)
        pygame.draw.line(screen, "white", alien_positions[i] - camera, alien_positions[i] + (alien_velocities[i] * 2) - camera)
        marker_color = "green" if alien_friendly[i] else "red"
        pygame.draw.circle(screen, marker_color, pygame.Vector2(alien_positions[i].x, alien_positions[i].y - 10) - camera, 3)
        direction = player.pos - alien_positions[i]
        if direction.length() > 0:
            direction = direction.normalize()
            alien_velocities[i] += direction * alien_speed * dt * 2
        alien_positions[i] += alien_velocities[i]
        if alien_velocities[i].length() > alien_speed:
            alien_velocities[i].scale_to_length(alien_speed)
    

initialize_planets(5)

# main game loop
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if player.health <= 0:
        running = False

    screen.fill("black")

    # create camera vector centered around player object
    camera = player.pos - (screen.get_width() / 2, screen.get_height() / 2)

    draw_grid(camera)

    player.draw(screen, camera)

    for planet in planets:
        if alien_homes.count(planet.id) < 3:
            planet.timer -= dt
            if planet.timer <= 0:
                alien_positions.append(pygame.Vector2(planet.pos))
                alien_velocities.append(pygame.Vector2(0,0))
                alien_friendly.append(planet.friendly)
                alien_homes.append(planet.id)

                planet.timer = 3
        if is_visible(camera, planet):
            planet.draw(screen, camera)

        # affect gravity force on player towards planet if within certain radius that scales based on distance to planet
        planet.apply_gravity(player, dt)
        planet.resolve_collision(player)
        planet.update(dt, player, screen, camera)

    update_aliens()

    # get input and send to player object
    keys = pygame.key.get_pressed()
    player.handle_input(keys, dt)
    player.update(dt)

    if player.pos.x < LEFTBOUND or player.pos.x > RIGHTBOUND:
        player.vel.x = 0
        player.pos.x = max(LEFTBOUND, min(player.pos.x, RIGHTBOUND))
    if player.pos.y < TOPBOUND or player.pos.y > BOTTOMBOUND:
        player.vel.y = 0
        player.pos.y = max(TOPBOUND, min(player.pos.y, BOTTOMBOUND))

    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()