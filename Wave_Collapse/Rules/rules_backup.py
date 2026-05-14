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
buildings = ['building_000', 'building_090', 'building_180', 'building_270']
boundry = ["boundry"]
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
        
        
        
        "road_corner": {"N": base+buildings,
                        "E": roads,
                        "S": roads,
                        "W": base + buildings,
                        "U": air,
                        "D": void},
        
        "road_junction": {"N": roads,
                          "S": roads,
                          "E": roads,
                          "W": roads,
                          "U": air,
                          "D": void},
        
        "road_straight_crossing": {"N": roads,
                          "S": roads,
                          "E": base+buildings,
                          "W": base+buildings,
                          "U": air,
                          "D": void},
        
        "road_straight": {"N": roads,
                          "S": roads,
                          "E": base+buildings,
                          "W": base+buildings,
                          "U": air,
                          "D": void},
        
        "road_tsplit": {"N": roads,
                          "S": roads,
                          "E": roads,
                          "W": base+buildings,
                          "U": air,
                          "D": void},
        
        "building": {"N": air+base+buildings+roads,
                          "S": roads,
                          "E": base+buildings+roads,
                          "W": base+buildings+roads,
                          "U": air,
                          "D": void},
        
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
    
    constraints=  {"void": {"N": boundry+void,
                            "E": boundry+void,
                            "S": boundry+void,
                            "W": boundry+void,
                            "U": void+base+roads+buildings,
                            "D": boundry+void},
             
                   "air": {"N": boundry+air,
                           "E": boundry+air,
                           "S": boundry+air,
                           "W": boundry+air,
                           "U": boundry+air,
                           "D": boundry+air+base+roads+buildings},
                   
                   "boundry": {"N": boundry+air+void+base+buildings+roads,
                               "E": boundry+air+void+base+buildings+roads,
                               "S": boundry+air+void+base+buildings+roads,
                               "W": boundry+air+void+base+buildings+roads,
                               "U": boundry+air+void+base+buildings+roads,
                               "D": boundry+air+void+base+buildings+roads},
                   
                   
                
                   "base": {"N": boundry+base+roads+buildings,
                            "E": boundry+base+roads+buildings,
                            "S": boundry+base+roads+buildings,
                            "W": boundry+base+roads+buildings,
                            "U": boundry+air,
                            "D": boundry+void},
                   
             
             }
    
    set_rotated_objects(constraints)
    
    for tile, directions in constraints.items():
        for direction, candidates in directions.items():
            opposite = opp[direction]
            symmetric = [c for c in candidates if tile in constraints[c][opposite]]
            constraints[tile][direction] = symmetric
    
    return constraints