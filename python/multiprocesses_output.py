#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 24 19:24:33 2025

@author: AGU
"""
import random
from color import *

def append_color(pixel_color):
    r,g,b = pixel_color
    r = linear_to_gamma(r)
    g = linear_to_gamma(g)
    b = linear_to_gamma(b)
    rbyte = int(255.999 * clamp(r))
    gbyte = int(255.999 * clamp(g))
    bbyte = int(255.999 * clamp(b))
    return (f"{rbyte} {gbyte} {bbyte}\n ")


def multiprocess(input_tuple):
    list_color = ""
    world,image_height, image_width, samples_per_pixel,max_depth ,camera_center, defocus_angle, defocus_disk_v,defocus_disk_u, pixel_u, pixel_v, ray_tmin, ray_tmax, pixel00_loc,saturation , process, processes = input_tuple
    out_string = ""
    for j in range(int(image_height*process), int((image_height*process)+(image_height/processes))):
        for i in range(image_width):
            current_color = color(0,0,0)
            for n in range(samples_per_pixel):
                pixel_center = pixel00_loc + (i+random.random()-0.5)* pixel_u + (j+random.random()-0.5) * pixel_v
                ray_origin = camera_center if (defocus_angle <= 0) else random_disk_sample(camera_center, defocus_disk_u, defocus_disk_v)
                ray_direction = pixel_center - ray_origin
                r = ray(ray_origin, ray_direction)
                pixel_color = ray_color(r,ray_tmin, ray_tmax, world, max_depth)
                current_color += pixel_color
            
            current_color /= samples_per_pixel
            current_color = current_color**saturation
            list_color+=(append_color(current_color))
    return list_color