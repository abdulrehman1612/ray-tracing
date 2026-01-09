#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  8 01:49:16 2026

@author: AGU
"""

import taichi as ti
from taichi_modules import Ray, random_disk_sample, cross
from color import ray_color



def make_field_pic(width, height):
    global samples_per_pixel_completed
    global image_pixels
    samples_per_pixel_completed = ti.field(ti.i32, shape = 1)
    image_pixels = ti.Vector.field(3, ti.f32, shape=(width, height))


@ti.kernel
def run_kernal(image_width: ti.i32,
               image_height: ti.i32,
               lookfrom: ti.types.vector(3, ti.f32),
               lookat: ti.types.vector(3, ti.f32),
               zoom: ti.f32,
               rotate_camera: ti.f32,
               defocus_angle: ti.f32,
               focus_distance: ti.f32,
               samples_per_pixel: ti.i32,
               max_depth: ti.i32,
               background_color: ti.types.vector(3, ti.f32)):
    
    vfov = 90.0 - (zoom * 10.0)
    angle = -rotate_camera * 3.14159265 / 180.0
    vup = ti.Vector([ti.sin(angle), ti.cos(angle), 0.0])
    theta = vfov * 3.14159265 / 180.0
    h = ti.tan(theta / 2.0)
    port_height = 2.0 * h * focus_distance
    port_width = port_height * (image_width / image_height)
    w = (lookfrom - lookat) / (lookfrom - lookat).norm()
    u = cross(vup, w)
    u = u / u.norm()
    v = cross(w, u)
    port_u = port_width * u
    port_v = port_height * v
    pixel_u = port_u / image_width
    pixel_v = port_v / image_height
    port_upperleft = lookfrom - focus_distance * w - 0.5 * port_u - 0.5 * port_v
    pixel00_loc = port_upperleft + 0.5 * (pixel_u + pixel_v)
    defocus_radius = focus_distance * ti.tan(defocus_angle * 0.5 * 3.14159265 / 180.0)
    defocus_disk_u = u * defocus_radius
    defocus_disk_v = v * defocus_radius
    ray_tmin = ti.cast(0.001, ti.f32)
    ray_tmax = ti.cast(1e30, ti.f32)
    
    ti.loop_config(block_dim=32)
    for a in ti.ndrange(samples_per_pixel):
        
        ti.loop_config(block_dim=32)
        for i,j in ti.ndrange(image_width, image_height):
            
            pixel_center = pixel00_loc + (i+ti.random()-0.5)* pixel_u + (j+ti.random()-0.5) * pixel_v
            ray_origin = lookfrom if (defocus_angle <= 0) else random_disk_sample(lookfrom, defocus_disk_u, defocus_disk_v)
            ray_direction = pixel_center - ray_origin
            ray_time = ti.random()
            r = Ray(origin=ray_origin, direction=ray_direction, time=ray_time)
            pixel_color = ray_color(r, ray_tmin, ray_tmax, max_depth, background_color)
            image_pixels[i, j] += pixel_color
            #image_pixels[i, j] += (pixel_color - image_pixels[i, j]) / (a + 1)
            
        #samples_per_pixel_completed[0] += 1
    for i,j in ti.ndrange(image_width, image_height):
        image_pixels[i, j] /= samples_per_pixel
            
    
    
    
    
