#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  8 04:20:33 2026

@author: AGU
"""

from camera import camera
from list_hittable import list_hittable
from objects import sphere, quad
from materials import lambertian, metal, dielectric, diffuse_light
from Vec3 import vec3
from textures import checker_texture, perlin_noise, image_texture
from random import random, uniform
color = vec3
point3 = vec3

def main_1():
    cam = camera(16/9, 1920, samples_per_pixel=10000, defocus_angle=0, focus_distance=10, max_depth=5, background_color=[1,1,1], lookfrom=[2,0,-1], lookat=[0,0,-1])
    world = list_hittable()
    world.add(sphere(vec3(0,0,-1), 0.5, lambertian(image_texture("image.jpg"))))
    world.add(sphere(vec3(0,-100.5,-1), 100, lambertian(checker_texture(vec3(0.5,0.5,0.5), vec3(0.1,0.1,0.1), 1))))
    world.add(sphere(vec3(-1,0,-1), 0.5, lambertian(image_texture("earthmap.jpg"))))
    cam.render(world)

#main_1()


def main_2():
    cam = camera(1, 720, samples_per_pixel=10, zoom=5, lookfrom=[278, 278, -800], lookat=[278, 278, 0], background_color=[0,0,0])
    world = list_hittable()
    red   = lambertian(vec3(.65, .05, .05))
    white = lambertian(vec3(.73, .73, .73))
    green = lambertian(vec3(.12, .45, .15))
    light = diffuse_light(vec3(25, 25, 25))

    world.add(quad(vec3(555,0,0), vec3(0,555,0), vec3(0,0,555), green))
    world.add(quad(vec3(0,0,0), vec3(0,555,0), vec3(0,0,555), red))
    world.add(quad(vec3(343, 554, 332), vec3(-130,0,0), vec3(0,0,-105), light))
    world.add(quad(vec3(0,0,0), vec3(555,0,0), vec3(0,0,555), white))
    world.add(quad(vec3(555,555,555), vec3(-555,0,0), vec3(0,0,-555), white))
    world.add(quad(vec3(0,0,555), vec3(555,0,0), vec3(0,555,0), white))
    cam.render(world)
    
main_2()

def main_3():
    
    cam = camera(16.0 / 9.0, 1920, samples_per_pixel=100, background_color=[0.70, 0.80, 1.00])
    
    world = list_hittable()
    
    material_ground = lambertian(vec3(0.8, 0.8, 0.0))
    material_center = lambertian(vec3(0.1, 0.2, 0.5))
    material_left   = dielectric(1.50)
    material_bubble = dielectric(1.00 / 1.50)
    material_right  = metal(vec3(0.8, 0.6, 0.2), 1.0)
    
    world.add(sphere(vec3( 0.0, -100.5, -1.0), 100.0, material_ground))
    world.add(sphere(vec3( 0.0,    0.0, -1.2),   0.5, material_center))
    world.add(sphere(vec3(-1.0,    0.0, -1.0),   0.5, material_left))
    world.add(sphere(vec3(-1.0,    0.0, -1.0),   0.4, material_bubble))
    world.add(sphere(vec3( 1.0,    0.0, -1.0),   0.5, material_right))
    
    cam.render(world)

#main_3()

def main_4():
    
    cam = camera(16/9, 400,samples_per_pixel=10, lookfrom=[26,3,6], lookat=[0,2,0], zoom=7, background_color=[0,0,0])
    world = list_hittable()
    world.add(sphere(vec3(0,-1000,0), 1000, lambertian(perlin_noise(4))))
    world.add(sphere(vec3(0,2,0), 2, lambertian(perlin_noise(4))))
    world.add(quad(vec3(3,1,-2), vec3(2,0,0), vec3(0,2,0), diffuse_light(vec3(4,4,4))))
    world.add(sphere(vec3(0,7,0), 2, diffuse_light(vec3(4,4,4))))
    cam.render(world)
    
#main_4()

def week1_final_render():
    
    cam = camera(16/9, 800, samples_per_pixel=10, lookfrom=[13,2,3] ,lookat=[0,0,0], zoom=7, background_color=[0.5, 0.7, 1.0], defocus_angle=0.6, focus_distance=10.0)
    world = list_hittable()

    ground_material = lambertian(color(0.5, 0.5, 0.5))
    world.add(sphere(point3(0, -1000, 0), 1000, ground_material))

    for a in range(-11, 11):
        for b in range(-11, 11):
            choose_mat = random()
            center = point3(a + 0.9 * random(),0.2,b + 0.9 * random())
            if (center - point3(4, 0.2, 0)).length() > 0.9:
                if choose_mat < 0.8:
                    center2 = vec3(0,uniform(0, .5), 0 )
                    albedo = color.random(0,1) * color.random(0,1)
                    sphere_material = lambertian(albedo)
                    world.add(sphere(center, 0.2, sphere_material, center2=center2))
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
    
    cam.render(world)

#week1_final_render()