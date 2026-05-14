from random import randint, choices
from Wave_Collapse.Rules.rules import void, air, base, roads, buildings, give_constraints


class tile:
    def __init__(self):
        self.possible_tiles = void+air+base+roads+buildings
        self.is_collapsed = False

    def __str__(self):
        return str(self.possible_tiles[0])

    def __repr__(self):
        return self.__str__()


def fully_collapsed(grid):
    
    for h in grid:
        for r in h:
            for c in r:
                if not c.is_collapsed:
                    return False
            
    return True


def contradiction(grid):
    
    for h in grid:
        for r in h:
            for c in r:
                if len(c.possible_tiles) == 0:
                    return True
            
    return False

def min_entropy(grid):
    entropy = float("inf")
    nh = None
    nr = None
    nc = None
    
    for h in range(len(grid)):
        for r in range(len(grid[0])):
            for c in range(len(grid[0][0])):
                if not grid[h][r][c].is_collapsed and len(grid[h][r][c].possible_tiles) < entropy:
                    entropy = len(grid[h][r][c].possible_tiles)
                    nh = h
                    nr = r
                    nc = c
                    
    return (nh, nr, nc)


def collapse(grid, cell):
    h, r, c = cell

    if not grid[h][r][c].is_collapsed:
        grid[h][r][c].is_collapsed = True

        possible = grid[h][r][c].possible_tiles
        weights = []

        for t in possible:

            # basic terrain
            if t == "void":
                weights.append(1)

            elif t == "air":
                weights.append(1)

            elif t == "base":
                weights.append(3)

            # roads (classified)
            elif t in (
                "road_straight_000",
                "road_straight_090",
                "road_straight_180",
                "road_straight_270"
            ):
                weights.append(6)

            elif t in (
                "road_straight_crossing_000",
                "road_straight_crossing_090",
                "road_straight_crossing_180",
                "road_straight_crossing_270"
            ):
                weights.append(3)

            elif t in (
                "road_corner_000",
                "road_corner_090",
                "road_corner_180",
                "road_corner_270",
                "road_junction_000",
                "road_junction_090",
                "road_junction_180",
                "road_junction_270",
                "road_tsplit_000",
                "road_tsplit_090",
                "road_tsplit_180",
                "road_tsplit_270"
            ):
                weights.append(5)

            # buildings
            elif t in buildings:
                weights.append(5)

            # fallback
            else:
                weights.append(1)

        picked_tile = choices(possible, weights=weights, k=1)[0]
        grid[h][r][c].possible_tiles = [picked_tile]

        return picked_tile

    return grid[h][r][c].possible_tiles[0]
        

def get_neighbours(grid, cell):
    neighbours = []
    h,r,c = cell
    
    if h-1 >= 0:
        neighbours.append((h-1, r,c, False))
    else:
        neighbours.append((h-1, r,c, True))
    if h+1 < len(grid):
        neighbours.append((h+1, r, c, False))
    else:
        neighbours.append((h+1, r, c, True))
    if r-1 >= 0:
        neighbours.append((h,r-1,c, False))
    else:
        neighbours.append((h,r-1,c, True))
    if r+1 < len(grid[0]):
        neighbours.append((h, r+1, c, False))
    else:
        neighbours.append((h, r+1, c, True))
    if c-1 >= 0:
        neighbours.append((h,r,c-1, False))
    else:
        neighbours.append((h,r,c-1, True))
    if c+1 < len(grid[0][0]):
        neighbours.append((h,r,c+1,False))
    else:
        neighbours.append((h,r,c+1,True))

    
    return neighbours




def propagate_constraints(grid, cell, rules):
    offset_to_direction =  {(0, -1, 0): "D",
                            (0, +1, 0): "U",
                            (0, 0,  1): "N",
                            (0, 0, -1): "S",
                            (1, 0, 0): "E",
                            (-1, 0, 0): "W"}
    
    
    
    h, r, c = cell
    for neighbour in get_neighbours(grid, cell):
        nh, nr, nc, is_bound = neighbour
        direction = offset_to_direction[( nr - r, nh - h, nc - c)]
        
        if is_bound:
            new_possible = []
            for t_name in grid[h][r][c].possible_tiles:
                if "bound" in rules[t_name][direction]:
                    new_possible.append(t_name)
            if len(new_possible) < len(grid[h][r][c].possible_tiles):
                grid[h][r][c].possible_tiles = new_possible
                if len(new_possible) == 0:
                    return
            continue
        
        
        compatible_tiles = set()
        for t_name in grid[h][r][c].possible_tiles:
            for t in rules[t_name][direction]:
                compatible_tiles.add(t)
        
        new_possible = [t for t in grid[nh][nr][nc].possible_tiles if t in compatible_tiles]
        if len(new_possible) < len(grid[nh][nr][nc].possible_tiles):
            grid[nh][nr][nc].possible_tiles = new_possible
            if len(new_possible) == 0:
                return
            propagate_constraints(grid, (nh, nr, nc), rules)

def reset_grid(grid):
    for h in range(len(grid)):
        for r in range(len(grid[0])):
            for c in range(len(grid[0][0])):
                grid[h][r][c].is_collapsed = False
                grid[h][r][c].possible_tiles = void+air+base+roads+buildings
    


def wfc_algorithm(grid):
    
    while not fully_collapsed(grid):
        if contradiction(grid):
            reset_grid(grid)
            print("Restarted")
            continue
        cell = min_entropy(grid)
        collapse(grid, cell)
        propagate_constraints(grid, cell, give_constraints())
    
    return grid

def run_wfc(height, length, width):
    grid  = [[[tile() for _ in range(width)] for __ in range(length)] for ___ in range(height)]
    return wfc_algorithm(grid)
        
            
        
    
    
    