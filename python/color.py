# -*- coding: utf-8 -*-
"""
Created on Sun Dec 21 20:30:48 2025

@author: rehma
"""
from hittable import hit_record
from Vec3 import *
from ray import ray


def clamp(color):
    return max(0, min(0.999, color))

def linear_to_gamma(linear):
    if linear > 0:
        return linear**0.5
    return 0

def write_color(out_file, pixel_color):
    r,g,b = pixel_color
    r = linear_to_gamma(r)
    g = linear_to_gamma(g)
    b = linear_to_gamma(b)
    rbyte = int(255.999 * clamp(r))
    gbyte = int(255.999 * clamp(g))
    bbyte = int(255.999 * clamp(b))
    out_file.write(f"{rbyte} {gbyte} {bbyte}\n ")
    
def get_color(world, r, ray_tmin, ray_tmax,  sky_color = color(0.529, 0.808, 0.922)):
    rec = hit_record()
    ray_tmin = 1
    ray_tmax = 2
    if world.hit(r, ray_tmin, ray_tmax, rec):
        return rec.color
    return sky_color

def ray_color(r, ray_tmin, ray_tmax, world, max_depth):
    if (max_depth <= 0):
            return color(0,0,0)
    rec = hit_record()
    if world.hit(r, ray_tmin, ray_tmax, rec):
        flag, attenuation, scattered = rec.material.scatter(r, rec)
        if flag:
            return attenuation * ray_color(scattered,ray_tmin, ray_tmax, world, max_depth-1)
        return color(0,0,0)
    
    unit_direction = unit_vector(r.direction())
    a = 0.5 * (unit_direction.y() + 1.0)
    return (1.0 - a) * color(1.0, 1.0, 1.0) + a * color(0.5, 0.7, 1.0)