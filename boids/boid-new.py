import pygame
import math
import random

pygame.init()                           # starte opp pygame
size = width, height = 1520, 1040        # Bane
clock = pygame.time.Clock()             # Klokka

n = 200

black = (0,0,0)
white = (255,255,255)
red = (255, 0, 0)
green = (0, 255,0)

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

def get_spatial_grid(boid, n):
    """
    Get grid list from spatial grid

    x [int]
        positive of negative coordinate

    y [int]
        positive of negative coordinate

    n [int]
        size of grid (n by n)

    return [list]
    """

    grid_x = boid.position[0] // n
    grid_y = boid.position[1] // n

    return spatial_hash.get((grid_x,grid_y), [])

def get_spatial_grid_dict_coords(x, y, n):
    """
    Get grid coords from coords

    x [int]
        left to right coordinat 

    y [int]
        up and down coordinate

    n [int]
        Size of grid (nxn)
    """

    grid_x = x // n
    grid_y = y // n

    return grid_x, grid_y

def insert_into_grid(boid, grid_s):

    old_coords = (boid.last_grid_x, boid.last_grid_y)

    last_grid_x = int(boid.position[0] // grid_s)
    last_grid_y = int(boid.position[1] // grid_s)

    new_coords = (last_grid_x, last_grid_y)

    try:

        if old_coords != new_coords:
            grid = get_spatial_grid(boid, grid_s)

            grid.append(boid)

            boid.last_grid_x = last_grid_x
            boid.last_grid_y = last_grid_y

            spatial_hash[new_coords] = grid

            del spatial_hash[old_coords]

    except:
        None


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


        # Params
        self.max_speed = 7
        self.sight_range = 80
        self.wall_avoid_range = 75
        self.boid_avoid_range = 50

    def update(self):
        newpos = self.calcnewpos(self.rect, self.speed)

        # with new pos move into correct sptial hash

        self.rect = newpos

        # update position vector
        # Lowkye sikkert poopy TODO
        self.position = [self.rect[0], self.rect[1]]

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

        # Update grid position
        insert_into_grid(self, grid_s)

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

    # DEBUG, draws grid inhabited by boid
    for k, v in spatial_hash.items():
        #print (k)
        x, y = k

        left = x * grid_s
        top = y * grid_s

        r = pygame.Rect(left, top, grid_s, grid_s)

        pygame.draw.rect(screen, green, r, 1)

    for b in instanser:
        b.update_movement(instanser)

        pygame.draw.rect(screen, red, b.rect)
        b.update()


    pygame.display.flip()

    clock.tick(30)
