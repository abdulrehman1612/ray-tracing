#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  8 04:20:33 2026

@author: AGU
"""

from camera import camera
from list_hittable import list_hittable
from objects import sphere, quad, box, translate, rotate_y, volume, mesh
from materials import lambertian, metal, dielectric, diffuse_light, isotropic
from Vec3 import vec3
from textures import checker_texture, perlin_noise, image_texture
from random import random, uniform
color = vec3
point3 = vec3

def week_1_final_render():
    cam = camera(16/9, 1920, samples_per_pixel=300, lookfrom=[13,2,3] ,lookat=[0,0,0], zoom=7, background_color=[0.5, 0.7, 1.0], defocus_angle=0.6, focus_distance=10.0)
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


def cornel_box_render():
    cam = camera(1, 400, samples_per_pixel=50, zoom=5, lookfrom=[278, 278, -800], lookat=[278, 278, 0], background_color=[0,0,0])
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
    box1 = list_hittable()
    box2 = list_hittable()
    box1.add(box(point3(0,0,0), point3(165,330,165), white))
    box2.add(box(point3(0,0,0), point3(165,165,165), white))
    rotated_box1 = list_hittable()
    rotated_box2 = list_hittable()
    rotated_box1.add(rotate_y(box1, 15))
    rotated_box2.add(rotate_y(box2, -18))
    translated_box1 = translate(rotated_box1, vec3(265,0,295))
    translated_box2 = translate(rotated_box2, vec3(130,0,65))
    world.add(volume(translated_box1, 0.01, isotropic(color(0,0,0))))
    world.add(volume(translated_box2, 0.01, isotropic(color(1,1,1))))
    cam.render(world)
    

def perlin_noise_render():
    cam = camera(16/9, 1920,samples_per_pixel=30, lookfrom=[26,3,6], lookat=[0,2,0], zoom=7, background_color=[0,0,0])
    world = list_hittable()
    world.add(sphere(vec3(0,-1000,0), 1000, lambertian(perlin_noise(4))))
    world.add(sphere(vec3(0,2,0), 2, lambertian(perlin_noise(4))))
    world.add(quad(vec3(3,1,-2), vec3(2,0,0), vec3(0,2,0), diffuse_light(vec3(4,4,4))))
    world.add(sphere(vec3(0,7,0), 2, diffuse_light(vec3(4,4,4))))
    cam.render(world)
    

def week_2_final_render():
    cam = camera(1, 1000, samples_per_pixel=250, lookfrom =[478, 278, -600],lookat = [278, 278, 0],defocus_angle = 0, zoom = 5, max_depth=50, background_color=[0, 0, 0])

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
            
            boxes1.add(box(point3(x0,y0,z0), point3(x1,y1,z1), ground))
    
    world.add(translate(boxes1, vec3(0,0,0)))
    
    light = diffuse_light(color(7, 7, 7))
    
    world.add(quad(point3(123,554,147), vec3(300,0,0), vec3(0,0,265), light))
    
    center1 = point3(400, 400, 200)
    center2 = vec3(30,0,0)
    
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
    
    pertext = perlin_noise(0.2)
    world.add(sphere(point3(220,280,300), 80, lambertian(pertext)))
    boxes2 = list_hittable()
    white = lambertian(color(.73, .73, .73))
    ns = 1000
    for i in range(ns):
        boxes2.add(sphere(vec3.random(a = 0, b = 165), 10, white))
    
    rotated_boxes2 = list_hittable()
    rotated_boxes2.add(rotate_y(boxes2, 15))
    world.add(translate(rotated_boxes2, vec3(-100,270,395)))
    cam.render(world)
    
def real_time_render():
    cam = camera(16/9, 800, samples_per_pixel=4, lookfrom=[13,2,3] ,lookat=[0,0,0], zoom=7, background_color=[0.5, 0.7, 1.0], defocus_angle=0.6, focus_distance=10.0)
    world = list_hittable()
    ground_material = lambertian(color(0.5, 0.5, 0.5))
    world.add(sphere(point3(0, -1000, 0), 1000, ground_material))
    for a in range(-11, 11):
        for b in range(-11, 11):
            choose_mat = random()
            center = point3(a + 0.9 * random(),0.2,b + 0.9 * random())
            if (center - point3(4, 0.2, 0)).length() > 0.9:
                if choose_mat < 0.8:
                    albedo = color.random(0,1) * color.random(0,1)
                    sphere_material = lambertian(albedo)
                    world.add(sphere(center, 0.2, sphere_material))
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
    cam.render(world, realtime=True)

def house():
    cam = camera(1000, 1000, samples_per_pixel=1, lookfrom=[+20,10,23] ,lookat=[-8,0,0],background_color=[0,0,0])

    world = list_hittable()

    # Materials
    cottage_lambertian = lambertian(image_texture("/home/AGU/Documents/cottage_diffuse.png"))
    green = lambertian(color(0.1, 0.8, 0.1))
    
    
    boundary = sphere(point3(0,0,0), 5000, dielectric(1.5))
    world.add(volume(boundary, 0.0001, isotropic(color(1,1,1))))
    world.add(mesh("/home/AGU/Documents/cottage_ground.obj", green))
    world.add(mesh("/home/AGU/Documents/cottage_light1.obj", diffuse_light(color(4, 4, 4))))
    world.add(mesh("/home/AGU/Documents/cottage_obj.obj", cottage_lambertian))
    
    dead_tree_material = lambertian(image_texture("/home/AGU/Documents/textures/DeadTree_LoPoly_DeadTree_Diffuse.png"))
    tree = list_hittable()
    world.add(mesh("/home/AGU/Documents/source/DeadTree_LoPoly.obj", dead_tree_material,0.2, [-10,0,20],180))
    cam.render(world)