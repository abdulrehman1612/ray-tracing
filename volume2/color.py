# -*- coding: utf-8 -*-
"""
Created on Sun Dec 21 20:30:48 2025

@author: rehma
"""
from hittable import hit_record
from bvhnode import *
from Vec3 import *
from ray import ray
import random



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


def ray_color(r, ray_tmin, ray_tmax, max_depth, BVH, background):
    if (max_depth <= 0):
            return (color(0,0,0), max_depth)
    rec = hit_record()
    if hit_BVH(BVH, r, ray_tmin, ray_tmax, rec):
        color_emitted = rec.material.emitted(rec.u, rec.v, rec.p)
        flag, attenuation, scattered = rec.material.scatter(r, rec)
        if flag:
            if max_depth <= 45:
                p = max(attenuation.x(), attenuation.y(), attenuation.z())
                p = max(0.05, min(p, 0.95))
                if random.random() > p:
                    return (color(0,0,0), max_depth)
                attenuation = attenuation / p
            ray_col, depth = ray_color(scattered, ray_tmin, ray_tmax, max_depth-1, BVH, background)
            
            return (color_emitted + attenuation * ray_col , depth)
   
        return (color_emitted, max_depth)
    
    return (background, max_depth)