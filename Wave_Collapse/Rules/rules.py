#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 01:30:13 2026

@author: AGU
"""


void = ["void"]
air = ["air"]
base = ["base"]
roads = ['road_corner_000', 'road_corner_090', 'road_corner_180', 'road_corner_270', 'road_junction_000', 'road_junction_090', 'road_junction_180', 'road_junction_270', 'road_straight_crossing_000', 'road_straight_crossing_090','road_straight_crossing_180', 'road_straight_crossing_270', 'road_straight_180', 'road_straight_270', 'road_straight_000', 'road_straight_090', 'road_tsplit_000', 'road_tsplit_090', 'road_tsplit_180', 'road_tsplit_270']
straight_roads = ['road_straight_180', 'road_straight_270', 'road_straight_000', 'road_straight_090']
road_crossings = ['road_straight_crossing_000', 'road_straight_crossing_090','road_straight_crossing_180', 'road_straight_crossing_270']
buildings = ['building_000', 'building_090', 'building_180', 'building_270']
bound = ["bound"]

def set_rotated_objects(constraints):
    angles = [0, 90, 180, 270]

    prev_dir = {
        "N": "W",
        "E": "N",
        "S": "E",
        "W": "S",
        "U": "U",
        "D": "D"
    }

    defined_constraints = {
        "road_corner": {
            "N": straight_roads,
            "E": straight_roads,
            "S": bound+ base + buildings,
            "W": bound+ base + buildings,
            "U": bound+air,
            "D": bound+void
        },
        
        "road_junction": {"N": road_crossings,
                          "S": road_crossings,
                          "E": road_crossings,
                          "W": road_crossings,
                          "U": bound+air,
                          "D": bound+void},
        
        "road_straight_crossing": {"N": roads,
                          "S": roads,
                          "E": bound+base+buildings,
                          "W": bound+base+buildings,
                          "U": bound+air,
                          "D": bound+void},
        
        "road_straight": {"N": roads,
                          "S": roads,
                          "E": bound+base+buildings,
                          "W": bound+base+buildings,
                          "U": bound+air,
                          "D": bound+void},
        
        "road_tsplit": {"N": roads,
                          "S": roads,
                          "E": straight_roads+road_crossings,
                          "W": bound+base+buildings,
                          "U": bound+air,
                          "D": bound+void},
        
        "building": {"N": roads,
                          "S": bound+base+buildings+roads,
                          "E": bound+base+buildings+roads,
                          "W": bound+base+buildings+roads,
                          "U": bound+air,
                          "D": bound+void},
        
    }

    for name, base_constraints in defined_constraints.items():
        current = base_constraints
        for angle in angles:
            constraints[f"{name}_{angle:03}"] = current
            rotated = {}

            for direction in current:
                rotated[direction] = current[prev_dir[direction]]

            current = rotated
                

    


def give_constraints():
    opp = {"N": "S", "S": "N", "E": "W", "W": "E", "U": "D", "D": "U"}
    
    constraints=  {"void": {"N": bound+void,
                            "E": bound+void,
                            "S": bound+void,
                            "W": bound+void,
                            "U": bound+void+base+roads+buildings,
                            "D": bound+void},
             
             "air": {"N": bound+air,
                     "E": bound+air,
                     "S": bound+air,
                     "W": bound+air,
                     "U": bound+air,
                     "D": bound+air+base+roads+buildings},
        
             "base": {"N": bound+base+roads+buildings,
                      "E": bound+base+roads+buildings,
                      "S": bound+base+roads+buildings,
                      "W": bound+base+roads+buildings,
                      "U": bound+air,
                      "D": bound+void},
             
             }
    
    set_rotated_objects(constraints)
    
    for tile, directions in constraints.items():
        for direction, candidates in directions.items():
            opposite = opp[direction]
            symmetric = []

            for c in candidates:
                if c == "bound":
                    symmetric.append(c)
                elif tile in constraints[c][opposite]:
                    symmetric.append(c)
            constraints[tile][direction] = symmetric
    
    return constraints