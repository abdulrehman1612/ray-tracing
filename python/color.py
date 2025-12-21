# -*- coding: utf-8 -*-
"""
Created on Sun Dec 21 20:30:48 2025

@author: rehma
"""
from hittable import hit_record
from Vec3 import color

def write_color(out_file, pixel_color):
    r,g,b = pixel_color
    rbyte = int(255.999 * r)
    gbyte = int(255.999 * g)
    bbyte = int(255.999 * b)
    out_file.write(f"{rbyte} {gbyte} {bbyte}\n ")
    
def get_color(world, r, ray_tmin, ray_tmax,  sky_color = color(0.529, 0.808, 0.922)):
    rec = hit_record()
    ray_tmin = 1
    ray_tmax = 2
    if world.hit(r, ray_tmin, ray_tmax, rec):
        return rec.color
    return sky_color
        