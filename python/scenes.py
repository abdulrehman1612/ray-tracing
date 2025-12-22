# -*- coding: utf-8 -*-
"""
Created on Sun Dec 21 21:59:49 2025

@author: rehma
"""

from rtimports import *

def scene():
    world = list_hittable()
    obj = sphere(point3(0,0,-1), 0.5)
    world.add(obj)
    obj = sphere(point3(0,-100.5,-1), 100)
    world.add(obj)
    
    return world