# -*- coding: utf-8 -*-
"""
Created on Sun Dec 21 21:59:49 2025

@author: rehma
"""

from rtimports import *
from random import random, uniform

def week1_final_scene():
    world = list_hittable()

    ground_material = lambertian(color(0.5, 0.5, 0.5))
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



def cornel_box_scene():
    world = list_hittable()
    red   = lambertian(color(0.65, 0.05, 0.05))
    white = lambertian(color(0.73, 0.73, 0.73))
    green = lambertian(color(0.12, 0.45, 0.15))
    light = diffuse_light(color(7, 7, 7))

    world.add(quad(point3(555,0,0), vec3(0,555,0), vec3(0,0,555), green))
    world.add(quad(point3(0,0,0), vec3(0,555,0), vec3(0,0,555), red))
    world.add(quad(point3(113,554,127), vec3(330,0,0), vec3(0,0,305), light))
    world.add(quad(point3(0,555,0), vec3(555,0,0), vec3(0,0,555), white))
    world.add(quad(point3(0,0,0), vec3(555,0,0), vec3(0,0,555), white))
    world.add(quad(point3(0,0,555), vec3(555,0,0), vec3(0,555,0), white))
    
    box1 = box(point3(0,0,0), point3(165,330,165), white)
    box1 = rotate_y(box1 , math.radians(15))
    box1 = translate(box1 ,vec3(265,0,295))
    world.add(volume(box1,0.01 ,isotropic(color(0,0,0))))

   
    box1 = box(point3(0,0,0), point3(165,165,165), white)
    box1 = rotate_y(box1 , math.radians(-18))
    box1 = translate(box1 ,vec3(130,0,65))
    world.add(volume(box1,0.01 ,isotropic(color(1,1,1))))
    
    
    return world



def week2_final_scene():
    world = list_hittable()
    
    ground = lambertian(color(0.48, 0.83, 0.53))
    
    boxes1 = list_hittable()
    boxes_per_side = 20
    
    for i in range(boxes_per_side):
        for j in range(boxes_per_side):
            w = 100.0
            x0 = -1000.0 + i*w
            z0 = -1000.0 + j*w
            y0 = 0.0
            x1 = x0 + w
            y1 = uniform(1,101)
            z1 = z0 + w
            
            boxes1.add(translate(box(point3(x0,y0,z0), point3(x1,y1,z1), ground)))
    
    world.add(translate(boxes1))
    
    light = diffuse_light(color(7, 7, 7))
    
    world.add(quad(point3(123,554,147), vec3(300,0,0), vec3(0,0,265), light))
    
    center1 = point3(400, 400, 200)
    center2 = center1 + vec3(30,0,0)
    sphere_material = lambertian(color(0.7, 0.3, 0.1))
    world.add(sphere(center1, 50, sphere_material, center2=center2))
    
    world.add(sphere(point3(260, 150, 45), 50, dielectric(1.5)))
    
    world.add(sphere(point3(0, 150, 145), 50, metal(color(0.8, 0.8, 0.9), 1.0)))
    
    boundary = sphere(point3(360,150,145), 70, dielectric(1.5))
    
    world.add(boundary)
    
    boundary = sphere(point3(360,150,145), 70, dielectric(1.5))
    
    world.add(volume(boundary, 0.2, isotropic(color(0.2, 0.4, 0.9))))
    
    boundary = sphere(point3(0,0,0), 5000, dielectric(1.5))
    
    world.add(volume(boundary, 0.0001, isotropic(color(1,1,1))))
    
    
    
    emat = lambertian(image_texture("earthmap.jpg"))
    
    world.add(sphere(point3(400,200,400), 100, emat))
    
    pertext = noise_texture(0.2)
    
    world.add(sphere(point3(220,280,300), 80, lambertian(pertext)))
    
    boxes2 = list_hittable()
    
    white = lambertian(color(.73, .73, .73))
    
    ns = 1000
    
    for i in range(ns):
        boxes2.add(sphere(vec3.random(a = 0, b = 165), 10, white))
    
    world.add(translate(rotate_y(boxes2, math.radians(15)),vec3(-100,270,395)))
    
    
    return world
    
            
    