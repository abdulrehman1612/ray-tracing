# -*- coding: utf-8 -*-
"""
Created on Sun Dec 21 21:59:49 2025

@author: rehma
"""

from rtimports import *
from random import random, uniform

def scene():
    world = list_hittable()

    ground_material = lambertian(checker_texture(0.32, color(.2, .3, .1), color(.9, .9, .9)))
    world.add(sphere(point3(0, -1000, 0), 1000, ground_material))

    for a in range(-11, 11):
        for b in range(-11, 11):
            choose_mat = random()
            center = point3(a + 0.9 * random(),0.2,b + 0.9 * random())
            if (center - point3(4, 0.2, 0)).length() > 0.9:
                if choose_mat < 0.8:
                    albedo = color.random() * color.random()
                    sphere_material = lambertian(albedo)
                    center2 = center+vec3(0, uniform(0,.5), 0)
                    world.add(sphere(center, 0.2, sphere_material, center2))
                elif choose_mat < 0.95:
                    albedo = color.random(0.5, 1.0)
                    fuzz = uniform(0.0, 0.5)
                    sphere_material = metal(albedo, fuzz)
                    world.add(sphere(center, 0.2, sphere_material))
                else:
                    sphere_material = dielectric(1.5)
                    world.add(sphere(center, 0.2, sphere_material))

    material1 = dielectric(1.5)
    world.add(sphere(point3(0, 1, 0), 1.0, material1))
    material2 = lambertian(color(0.4, 0.2, 0.1))
    world.add(sphere(point3(-4, 1, 0), 1.0, material2))
    material3 = metal(color(0.7, 0.6, 0.5), 0.0)
    world.add(sphere(point3(4, 1, 0), 1.0, material3))

    return world



def scene2():
    world = list_hittable()
    material_ground = lambertian(color(0.8, 0.8, 0.0))
    material_center = lambertian(color(0.1, 0.2, 0.5))
    material_left   = dielectric(1.5)
    material_right  = metal(color(0.8, 0.6, 0.2),0.9)
    material_bubble = dielectric(1.00 / 1.50)
    
    world.add(sphere(point3( 0.0, -100.5, -1.0), 100.0, material_ground))
    world.add(sphere(point3( 0.0,    0.0, -1.2),   0.5, material_center))
    world.add(sphere(point3(-1.0,    0.0, -1.0),   0.5, material_left))
    world.add(sphere(point3(-1.0,    0.0, -1.0),   0.4, material_bubble))
    world.add(sphere(point3( 1.0,    0.0, -1.0),   0.5, material_right))
    
    return world

def scene3():
    world = list_hittable()
    world.add(sphere(point3(0,-1000,0), 1000, lambertian(noise_texture(4))))
    world.add(sphere(point3(0,2,0), 2, lambertian(noise_texture(4))))
    return world