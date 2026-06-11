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

# create player object
player = Player((screen.get_width() / 2, screen.get_height() / 2))

# create empty list of planets
planets = []

# set gravity constant
GRAVITY = 100000 * .75

# populate planets list with planets with random size, color and position and empty aliens list
for i in range(5):
    planet_radius = random.randint(100, 500)
    color = pygame.Color(random.randint(122, 255), random.randint(122, 255), random.randint(122, 255))
    pos = pygame.Vector2(random.randint(-2000, 2000), random.randint(-2000, 2000))
    # aliens = [Alien(pos + pygame.Vector2(random.randint(-20, 20), random.randint(-20, 20)), pygame.Vector2(0,0)) for _ in range(5)]
    aliens = []
    planets.append(Planet(pos, planet_radius, i, aliens, color))

# main game loop
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if player.health <= 0:
        running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # create camera vector centered around player object
    camera = player.pos - (screen.get_width() / 2, screen.get_height() / 2)

    # draw grid lines
    for i in range(-2000, 2100, 100):
        pygame.draw.line(screen, "white", pygame.Vector2(i, -2000) - camera, pygame.Vector2(i, 2000) - camera)
        pygame.draw.line(screen, "white", pygame.Vector2(-2000, i) - camera, pygame.Vector2(2000, i) - camera)

    # draw player centered on screen
    player.draw(screen, camera)

    
    # loop through planets
    for planet in planets:
        pygame.draw.circle(screen, planet.color, planet.pos - camera, planet.radius)

        # get distance to and direction between player and planet
        dist = planet.pos.distance_to(player.pos)
        direction = planet.pos - player.pos

        # affect gravity force on player towards planet if within certain radius that scales based on distance to planet
        if dist <= (planet.radius * 3) and dist >= planet.radius:
            direction = direction.normalize()
            force = (GRAVITY / dist) * (planet.radius / 100)
            player.vel += direction * force * dt
        elif dist < planet.radius:
            outward = (player.pos - planet.pos).normalize()
            player.pos = planet.pos + outward * planet.radius
            player.vel = pygame.Vector2(0, 0) 

        for alien in planet.aliens:
            pygame.draw.circle(screen, planet.color, alien.pos - camera, alien.radius)
            pygame.draw.line(screen, "white", alien.pos - camera, alien.pos + (alien.vel * 2) - camera)
            target = None

            # if the planet is friendly, all aliens from planet are friendly, target their home planet, otherwise target the player
            if planet.friendly:
                alien.friendly = True
                pygame.draw.circle(screen, "green", pygame.Vector2(alien.pos.x, alien.pos.y - 10) - camera, 3)
                target = planet
            else:
                pygame.draw.circle(screen, "red", pygame.Vector2(alien.pos.x, alien.pos.y - 10) - camera, 3)
                target = player
                if target.pos.distance_to(alien.pos) <= player.radius + alien.radius:
                    alien.attack(player, dt)

            alien.update(target, dt, planet.aliens)

        planet.update(dt, dist, screen, camera)

    # get input and send to player object
    keys = pygame.key.get_pressed()
    player.handle_input(keys, dt)
    player.update(dt)
    if player.pos.x < -2000 or player.pos.x > 2000:
        player.vel.x = 0
        player.pos.x = max(-2000, min(player.pos.x, 2000))
    if player.pos.y < -2000 or player.pos.y > 2000:
        player.vel.y = 0
        player.pos.y = max(-2000, min(player.pos.y, 2000))

    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()