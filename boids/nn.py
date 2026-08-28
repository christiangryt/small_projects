import pygame

spatial_hash = dict()
grid_s = 64
size = width, height = 1520, 1040        # Bane

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

def get_spatial_grid(x, y, grid_s):

    i = x // grid_s
    j = y // grid_s

    return spatial_hash.get((i,j), 0)

create_hashes(width, height, grid_s)

print (get_spatial_grid(34, 45, grid_s))

b = pygame.math.Vector2(2,3)
