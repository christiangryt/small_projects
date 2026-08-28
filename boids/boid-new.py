import pygame
import math
import random

pygame.init()                           # starte opp pygame
size = width, height = 1520, 1040        # Bane
clock = pygame.time.Clock()             # Klokka

n = 1

black = (0,0,0)
white = (255,255,255)
red = (255, 0, 0)

# ==============
# Spatial Hashing
# ==============

# based on window size divide into n chunks and find in hash table
"""
spatial_hash

[x, y]
    x index first
    y index second
"""
spatial_hash = dict()
grid_s = 64

def create_hashes(width, height, n):
    """
    Given width and height create hash entries for grid size

    width, height [int]
        size of window

    n [int]
        size of grid (n by n)
    """

    x = width // n
    y = height // n

    for i in range(x):
        for j in range(y):
            spatial_hash[(i,j)] = []

def get_spatial_grid(x, y):
    """
    Given Cooridinates of spatial hash grid return list of boids there
    x [int]
        axis

    y [int]
        axis
    """

    return spatial_hash.get((x,y), 0)

def insert_into_grid(boid, grid_s):

    old_grid = spatial_hash.get(boid.last_grid_x, boid.last_grid_y)
    print (old_grid)
    old_grid.remove(boid)

    x = boid.x // grid_s
    y = boid.y // grid_s

    grid = spatial_hash.get((x,y), 0)

    if grid != 0:

        grid.append(boid)
        boid.last_grid_x = x
        boid.last_grid_y = y

create_hashes(width, height, grid_s)
print (spatial_hash)

# ==============
# Boid Class
# ==============
class boid(pygame.sprite.Sprite):

    def __init__(self, position, speed, color, radius):
        """
        Speed: length and angle
        Position: X and Y
        """

        pygame.sprite.Sprite.__init__(self) # pygame sprite constructor

        self.screen = pygame.display.get_surface()
        self.rect = pygame.Rect(position[0], position[1], radius, radius)
        self.speed = pygame.math.Vector2(speed)
        self.position = pygame.math.Vector2(position)

        self.last_grid_x = int(self.position.x) // grid_s
        self.last_grid_y = int(self.position.y) // grid_s

        insert_into_grid(self, grid_s)

        # Params
        self.max_speed = 7
        self.sight_range = 80
        self.wall_avoid_range = 75
        self.boid_avoid_range = 50

    def update(self):
        newpos = self.calcnewpos(self.rect, self.speed)

        # with new pos move into correct sptial hash

        self.rect = newpos

    def calcnewpos(self, rect, speed):
        return rect.move(speed)

    def get_pos_vector(self):
        return pygame.math.Vector2(self.rect[:2])

    # ==============
    # Rules for Boids
    # ==============
    def dodge_walls(self):

        "avoid edge of map, and also /structs/"

        away_from_wall_x = 0
        away_from_wall_y = 0

        pos = self.get_pos_vector()

        if pos[0] <  self.wall_avoid_range:
            away_from_wall_x = 1
        elif pos[0] > self.screen.get_width() - self.wall_avoid_range:
            away_from_wall_x = -1

        if pos[1] < self.wall_avoid_range:
            away_from_wall_y = 1
        elif pos[1] > self.screen.get_height() - self.wall_avoid_range:
            away_from_wall_y = -1

        return pygame.math.Vector2(away_from_wall_x, away_from_wall_y) * 2.5

    def update_movement(self, other_boids):
        """
        Oppdater speed vektor, update tar resten
        """

        avoid_boid = pygame.math.Vector2()
        perceived_velocity = pygame.math.Vector2()
        perceived_center = pygame.math.Vector2()
        dodge_movement = self.dodge_walls()

        self_pos = self.get_pos_vector()
        boids_in_range = 0

        for boid in other_boids:
            if boid != self:

                pos = boid.get_pos_vector()

                distance = self_pos - pos
                distance_abs = distance.length()

                if distance_abs < self.sight_range:

                    boids_in_range += 1

                    # Match veolocity and group
                    perceived_velocity = perceived_velocity + boid.speed
                    perceived_center = perceived_center + pos

                    if distance_abs < self.boid_avoid_range:
                        avoid_boid = avoid_boid + distance * (1 / (distance_abs + 0.01))

        if boids_in_range > 0:

            # Scale vectors
            perceived_center = ((perceived_center / boids_in_range) - self_pos) * 0.001
            perceived_velocity = (perceived_velocity / boids_in_range) - self.speed * 0.01
            avoid_boid = avoid_boid * 1

            # Boid perceived Center
            #pygame.draw.rect(screen, black, pygame.Rect(perceived_center, [5, 5]))

            # Avoid boid line
            #pygame.draw.line(screen, black, self_pos, avoid_boid)

            self.speed = self.speed + perceived_center + perceived_velocity + avoid_boid
            #self.speed = self.speed + avoid_boid + dodge_movement

        self.speed +=  dodge_movement

        # Visualize Boid Sight Range
        #pygame.draw.circle(self.screen, black, self.get_pos_vector(), self.sight_range, 1)

        if self.speed.length() > self.max_speed:
            self.speed.scale_to_length(self.max_speed)

# ==============
# Simulation vars
# ==============
def make_boids(n, width, height):

    instanser = []

    for i in range(n):

        # random spawn
        x = random.randint(1, width)
        y = random.randint(1, height)
        position = pygame.math.Vector2(x, y)

        sped_x = random.randint(-3, 3)
        sped_y = random.randint(-3, 3)

        speed = pygame.math.Vector2([sped_x,sped_y])

        b = boid(position, speed, "red", 5)
        instanser.append(b)

    return instanser

screen = pygame.display.set_mode(size)

instanser = make_boids(n, screen.get_width(), screen.get_height())

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(white)

    for b in instanser:
        pygame.draw.rect(screen, red, b.rect)

        b.update_movement(instanser)
        b.update()

    pygame.display.flip()

    clock.tick(30)
