# -*- coding: utf-8 -*-
"""
Created on Sun Dec 21 21:59:49 2025

@author: rehma
"""

from rtimports import *

def scene():
    world = list_hittable()
    obj = sphere(point3(0,-0.15,-1), 0.5, color(0.5,0.4,0.3))
    world.add(obj)
    obj = sphere(point3(0,-101,-1.5), 100, color(0.196, 0.804, 0.196))
    world.add(obj)
    
    return world