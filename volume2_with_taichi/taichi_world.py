#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  8 05:17:28 2026

@author: AGU
"""

import taichi as ti
from objects import *
from materials import *
from textures import *
from random import uniform, randint
from BVH import make_BVH, flatten_bvh




def init_world(world):
    
    
    for i, obj in enumerate(world.objects):
        obj.prim_id = i
    Prims_count = 0
    Sphere_count = 0
    Quad_count = 0
    box_count = 0
    lambertian_count = 0
    metal_count = 0
    dielctric_count = 0
    diffuse_light_count = 0
    solid_color_count = 0
    checker_texture_count = 0
    perlin_texture_count = 0
    image_texture_count = 0
    image_texture_max_height = 0
    image_texture_total_width = 0
    
    
    for obj in world.objects:
        
        if isinstance(obj, sphere):
            Prims_count += 1
            Sphere_count += 1
            if isinstance(obj.material, lambertian):
                lambertian_count += 1
                if isinstance(obj.material.texture, solid_color):
                    solid_color_count += 1
                    
                elif isinstance(obj.material.texture, checker_texture):
                    checker_texture_count += 1
                    if isinstance(obj.material.texture.even, solid_color):
                        solid_color_count += 1
                    if isinstance(obj.material.texture.odd, solid_color):
                        solid_color_count += 1
                elif isinstance(obj.material.texture, perlin_noise):
                    perlin_texture_count += 1
                    
                elif isinstance(obj.material.texture, image_texture):
                    image_texture_count += 1
                    image_texture_max_height = max(obj.material.texture.image.height, image_texture_max_height)
                    image_texture_total_width += obj.material.texture.image.width
                    
                    
            elif isinstance(obj.material, metal):
                metal_count += 1
                if isinstance(obj.material.texture, solid_color):
                    solid_color_count += 1
                    
                elif isinstance(obj.material.texture, checker_texture):
                    checker_texture_count += 1
                    if isinstance(obj.material.texture.even, solid_color):
                        solid_color_count += 1
                    if isinstance(obj.material.texture.odd, solid_color):
                        solid_color_count += 1
            elif isinstance(obj.material, dielectric):
                dielctric_count += 1
            elif isinstance(obj.material, diffuse_light):
                diffuse_light_count += 1
            
        elif isinstance(obj, quad):
            Prims_count += 1
            Quad_count += 1
            if isinstance(obj.material, lambertian):
                lambertian_count += 1
                if isinstance(obj.material.texture, solid_color):
                    solid_color_count += 1
                    
                elif isinstance(obj.material.texture, checker_texture):
                    checker_texture_count += 1
                    if isinstance(obj.material.texture.even, solid_color):
                        solid_color_count += 1
                    if isinstance(obj.material.texture.odd, solid_color):
                        solid_color_count += 1
                elif isinstance(obj.material.texture, perlin_noise):
                    perlin_texture_count += 1
                    
                elif isinstance(obj.material.texture, image_texture):
                    image_texture_count += 1
                    image_texture_max_height = max(obj.material.texture.image.height, image_texture_max_height)
                    image_texture_total_width += obj.material.texture.image.width
                    
                    
            elif isinstance(obj.material, metal):
                metal_count += 1
                if isinstance(obj.material.texture, solid_color):
                    solid_color_count += 1
                    
                elif isinstance(obj.material.texture, checker_texture):
                    checker_texture_count += 1
                    if isinstance(obj.material.texture.even, solid_color):
                        solid_color_count += 1
                    if isinstance(obj.material.texture.odd, solid_color):
                        solid_color_count += 1
            elif isinstance(obj.material, dielectric):
                dielctric_count += 1
            elif isinstance(obj.material, diffuse_light):
                diffuse_light_count += 1
            
        elif isinstance(obj, box):
            Prims_count += 1
            box_count += 1
            for side in obj.sides:
                if isinstance(side, quad):
                    Quad_count += 1
                    if isinstance(side.material, lambertian):
                        lambertian_count += 1
                        if isinstance(side.material.texture, solid_color):
                            solid_color_count += 1
                            
                        elif isinstance(side.material.texture, checker_texture):
                            checker_texture_count += 1
                            if isinstance(side.material.texture.even, solid_color):
                                solid_color_count += 1
                            if isinstance(side.material.texture.odd, solid_color):
                                solid_color_count += 1
                        elif isinstance(side.material.texture, perlin_noise):
                            perlin_texture_count += 1
                            
                        elif isinstance(side.material.texture, image_texture):
                            image_texture_count += 1
                            image_texture_max_height = max(side.material.texture.image.height, image_texture_max_height)
                            image_texture_total_width += side.material.texture.image.width
                            
                            
                    elif isinstance(side.material, metal):
                        metal_count += 1
                        if isinstance(side.material.texture, solid_color):
                            solid_color_count += 1
                            
                        elif isinstance(side.material.texture, checker_texture):
                            checker_texture_count += 1
                            if isinstance(side.material.texture.even, solid_color):
                                solid_color_count += 1
                            if isinstance(side.material.texture.odd, solid_color):
                                solid_color_count += 1
                    elif isinstance(side.material, dielectric):
                        dielctric_count += 1
                    elif isinstance(side.material, diffuse_light):
                        diffuse_light_count += 1
                
            

        
        
        
    
    
    
    Sphere_count = max(1,Sphere_count)
    Quad_count = max(1,Quad_count)
    lambertian_count = max(1,lambertian_count)
    metal_count = max(1,metal_count)
    dielctric_count = max(1, dielctric_count)
    diffuse_light_count = max(1, diffuse_light_count)
    solid_color_count = max(1,solid_color_count)
    checker_texture_count = max(1,checker_texture_count)
    perlin_texture_count = max(1,perlin_texture_count)
    Prims_count = max(1, Prims_count)
    image_texture_max_height = max(1,image_texture_max_height)
    image_texture_total_width = max(1,image_texture_total_width)
    image_texture_count = max(1,image_texture_count)
    
    
    global flag
    flag = ti.field(ti.i32, shape = 1)
    global num_of_prim
    global prim_indices
    global bvh_num_of_nodes
    global bvh_node_min
    global bvh_node_max
    global bvh_node_left
    global bvh_node_right
    global bvh_node_prim_start
    global bvh_node_prim_count
    global sphere_center0
    global sphere_center1
    global sphere_radius
    global sphere_material_type
    global sphere_material_index
    global quad_Q
    global quad_U
    global quad_V
    global quad_material_type
    global quad_material_index
    global prim_type
    global prim_geo
    global lambertian_texture_type
    global lambertian_texture_index
    global metal_texture_type
    global metal_texture_index
    global metal_fuzz
    global dielectric_refractive_index
    global diffuse_light_albedo
    global solid_color_vec
    global checker_texture_odd_type
    global checker_texture_odd_index
    global checker_texture_even_type
    global checker_texture_even_index
    global checker_texture_scale
    global perlin_random_vec
    global perlin_perm_x
    global perlin_perm_y
    global perlin_perm_z
    global perlin_c
    global perlin_scale
    global image_texture_data
    global image_texture_width_start
    global image_texture_width
    global image_texture_height
    global box_prim_indices
    global box_prim_indices_start
    
    
    bvh_node = make_BVH(world.objects)
    flatten_bvh(bvh_node)
    
    from BVH import bvh_nodes, bvh_primitive_indices
    
    
    
    
    num_of_prim = len(world.objects)
    prim_indices = ti.field(ti.i32, shape= Prims_count)
    prim_type = ti.field(ti.i32, shape= Prims_count)
    prim_geo = ti.field(ti.i32, shape= Prims_count)
    
    bvh_node_min = ti.Vector.field(3, ti.f32, shape = len(bvh_nodes))
    bvh_node_max = ti.Vector.field(3, ti.f32, shape = len(bvh_nodes))
    bvh_node_left = ti.field(ti.i32, shape = len(bvh_nodes))
    bvh_node_right = ti.field(ti.i32, shape = len(bvh_nodes))
    bvh_node_prim_start = ti.field(ti.i32, shape = len(bvh_nodes))
    bvh_node_prim_count = ti.field(ti.i32, shape = len(bvh_nodes))
    bvh_num_of_nodes = len(bvh_nodes)
    
    for i in range(len(bvh_primitive_indices)):
        prim_indices[i] = bvh_primitive_indices[i]
    
    for i in range(len(bvh_nodes)):
        bvh_node_min[i] = bvh_nodes[i]['min']
        bvh_node_max[i] = bvh_nodes[i]['max']
        bvh_node_left[i] = bvh_nodes[i]['left']
        bvh_node_right[i] = bvh_nodes[i]['right']
        bvh_node_prim_start[i] = bvh_nodes[i]['first_prim']
        bvh_node_prim_count[i] = bvh_nodes[i]['prim_count']
    
    sphere_center0 = ti.Vector.field(3, ti.f32, shape=Sphere_count)
    sphere_center1 = ti.Vector.field(3, ti.f32, shape=Sphere_count)
    sphere_radius = ti.field(ti.f32, shape = Sphere_count)
    sphere_material_type = ti.field(ti.i32, shape= Sphere_count)
    sphere_material_index = ti.field(ti.i32, shape= Sphere_count)
    
    quad_Q = ti.Vector.field(3, ti.f32, shape=Quad_count)
    quad_U = ti.Vector.field(3, ti.f32, shape=Quad_count)
    quad_V = ti.Vector.field(3, ti.f32, shape=Quad_count)
    quad_material_type = ti.field(ti.i32, shape= Quad_count)
    quad_material_index = ti.field(ti.i32, shape= Quad_count)
    
    
    lambertian_texture_type = ti.field(ti.i32, shape = lambertian_count)
    lambertian_texture_index = ti.field(ti.i32, shape = lambertian_count)
    metal_texture_type = ti.field(ti.i32, shape = metal_count)
    metal_texture_index = ti.field(ti.i32, shape = metal_count)
    metal_fuzz = ti.field(ti.f32, shape = metal_count)
    
    dielectric_refractive_index = ti.field(ti.f32, shape=dielctric_count)
    
    diffuse_light_albedo = ti.field(ti.i32, shape = diffuse_light_count)
    
    solid_color_vec = ti.Vector.field(3, ti.f32, shape=solid_color_count)
    
    checker_texture_odd_type = ti.field(ti.i32, shape = checker_texture_count)
    checker_texture_odd_index = ti.field(ti.i32, shape = checker_texture_count)
    checker_texture_even_type = ti.field(ti.i32, shape = checker_texture_count)
    checker_texture_even_index = ti.field(ti.i32, shape = checker_texture_count)
    checker_texture_scale = ti.field(ti.f32, shape = checker_texture_count)
    
    image_texture_data = ti.Vector.field(3, ti.f32, shape = (image_texture_max_height, image_texture_total_width))
    image_texture_height = ti.field(ti.i32, image_texture_count)
    image_texture_width = ti.field(ti.i32, image_texture_count)
    image_texture_width_start = ti.field(ti.i32, image_texture_count)
    
    perlin_scale = ti.field(ti.f32, shape = perlin_texture_count)
    perlin_random_vec = ti.Vector.field(3, ti.f32, shape = 256)
    perlin_perm_x = ti.field(ti.i32, 256)
    perlin_perm_y = ti.field(ti.i32, 256)
    perlin_perm_z = ti.field(ti.i32, 256)
    perlin_c = ti.Vector.field(3,ti.f32 ,shape=(2,2,2))
    
    for i in range(256):
        perlin_random_vec[i] = ti.Vector([uniform(-1, 1),uniform(-1, 1),uniform(-1, 1)])
        perlin_perm_x[i] = i
        perlin_perm_y[i] = i
        perlin_perm_z[i] = i
        
    for i in range(255, 0,-1):
        target = randint(0, i)
        perlin_perm_x[i], perlin_perm_x[target] = perlin_perm_x[target], perlin_perm_x[i]
        target = randint(0, i)
        perlin_perm_y[i], perlin_perm_y[target] = perlin_perm_y[target], perlin_perm_y[i]
        target = randint(0, i)
        perlin_perm_z[i], perlin_perm_z[target] = perlin_perm_z[target], perlin_perm_z[i]
    
    prim_index = -1
    sphere_index = -1
    quad_index = -1
    lambertian_index = -1
    metal_index = -1
    dielectric_index = -1
    diffuse_light_index = -1
    solid_color_vec_index = -1
    checker_index = -1
    perlin_index = -1
    image_texture_index = -1
    image_width_start = 0
    box_index = -1
    
    
    
    
    for obj in world.objects:
        prim_index += 1

        if isinstance(obj, sphere):
            sphere_index +=1
            prim_type[prim_index] = 0
            prim_geo[prim_index] = sphere_index
            sphere_center0[sphere_index] = ti.Vector(obj.center1.as_list())
            sphere_center1[sphere_index] = ti.Vector(obj.center2.as_list())
            sphere_radius[sphere_index] = obj.radius
            
            if isinstance(obj.material, lambertian):
                lambertian_index += 1
                sphere_material_type[sphere_index] = 0
                sphere_material_index[sphere_index] = lambertian_index
                
                if isinstance(obj.material.texture, solid_color):
                    solid_color_vec_index += 1
                    lambertian_texture_type[lambertian_index] = 0
                    lambertian_texture_index[lambertian_index] = solid_color_vec_index
                    solid_color_vec[solid_color_vec_index] = ti.Vector(obj.material.texture.albedo.as_list())
                
                elif isinstance(obj.material.texture, checker_texture):
                    checker_index += 1
                    lambertian_texture_type[lambertian_index] = 1
                    lambertian_texture_index[lambertian_index] = checker_index
                    
                    if isinstance(obj.material.texture.even, solid_color):
                        solid_color_vec_index += 1
                        checker_texture_even_type[checker_index] = 0
                        checker_texture_even_index[checker_index] = solid_color_vec_index
                        solid_color_vec[solid_color_vec_index] = ti.Vector(obj.material.texture.even.albedo.as_list())
                    
                    if isinstance(obj.material.texture.odd, solid_color):
                        solid_color_vec_index += 1
                        checker_texture_odd_type[checker_index] = 0
                        checker_texture_odd_index[checker_index] = solid_color_vec_index
                        solid_color_vec[solid_color_vec_index] = ti.Vector(obj.material.texture.odd.albedo.as_list())
                    
                    checker_texture_scale[checker_index] = obj.material.texture.scale
                
                elif isinstance(obj.material.texture, perlin_noise):
                    perlin_index += 1
                    lambertian_texture_type[lambertian_index] = 2
                    lambertian_texture_index[lambertian_index] = perlin_index
                    perlin_scale[perlin_index] = obj.material.texture.scale
                
                elif isinstance(obj.material.texture, image_texture):
                    image_texture_index += 1
                    lambertian_texture_type[lambertian_index] = 3
                    lambertian_texture_index[lambertian_index] = image_texture_index
                    image_texture_height[image_texture_index] = obj.material.texture.image.height
                    image_texture_width[image_texture_index] = obj.material.texture.image.width
                    image_texture_width_start[image_texture_index] = image_width_start
                    
                    for y in range(obj.material.texture.image.height):
                        for x in range(obj.material.texture.image.width):
                            image_texture_data[y, image_width_start + x] = ti.Vector(obj.material.texture.image.pixels[y, x])
                    
                    image_width_start += obj.material.texture.image.width
                
            elif isinstance(obj.material, metal):
                metal_index += 1
                sphere_material_type[sphere_index] = 1
                sphere_material_index[sphere_index] = metal_index
                
                if isinstance(obj.material.texture, solid_color):
                    solid_color_vec_index += 1
                    metal_texture_type[metal_index] = 0
                    metal_texture_index[metal_index] = solid_color_vec_index
                    solid_color_vec[solid_color_vec_index] = ti.Vector(obj.material.texture.albedo.as_list())
                
                metal_fuzz[metal_index] = obj.material.fuzz
            
            elif isinstance(obj.material, dielectric):
                dielectric_index += 1
                sphere_material_type[sphere_index] = 2
                sphere_material_index[sphere_index] = dielectric_index
                dielectric_refractive_index[dielectric_index] = obj.material.refractive_index
                
            elif isinstance(obj.material, diffuse_light):
                diffuse_light_index += 1
                sphere_material_type[sphere_index] = 3
                sphere_material_index[sphere_index] = diffuse_light_index
                
                if isinstance(obj.material.texture, solid_color):
                    solid_color_vec_index +=1
                    diffuse_light_albedo[diffuse_light_index] = solid_color_vec_index
                    solid_color_vec[solid_color_vec_index] = ti.Vector(obj.material.texture.albedo.as_list())
            
        elif isinstance(obj, quad):
            quad_index += 1
            prim_type[prim_index] = 1 
            prim_geo[prim_index] = quad_index
            quad_Q[quad_index] = ti.Vector(obj.Q.as_list())
            quad_U[quad_index] = ti.Vector(obj.U.as_list())
            quad_V[quad_index] = ti.Vector(obj.V.as_list())
            
            if isinstance(obj.material, lambertian):
                lambertian_index += 1
                quad_material_type[quad_index] = 0
                quad_material_index[quad_index] = lambertian_index
                
                if isinstance(obj.material.texture, solid_color):
                    solid_color_vec_index += 1
                    lambertian_texture_type[lambertian_index] = 0
                    lambertian_texture_index[lambertian_index] = solid_color_vec_index
                    solid_color_vec[solid_color_vec_index] = ti.Vector(obj.material.texture.albedo.as_list())
                
                elif isinstance(obj.material.texture, checker_texture):
                    checker_index += 1
                    lambertian_texture_type[lambertian_index] = 1
                    lambertian_texture_index[lambertian_index] = checker_index
                    
                    if isinstance(obj.material.texture.even, solid_color):
                        solid_color_vec_index += 1
                        checker_texture_even_type[checker_index] = 0
                        checker_texture_even_index[checker_index] = solid_color_vec_index
                        solid_color_vec[solid_color_vec_index] = ti.Vector(obj.material.texture.even.albedo.as_list())
                    
                    if isinstance(obj.material.texture.odd, solid_color):
                        solid_color_vec_index += 1
                        checker_texture_odd_type[checker_index] = 0
                        checker_texture_odd_index[checker_index] = solid_color_vec_index
                        solid_color_vec[solid_color_vec_index] = ti.Vector(obj.material.texture.odd.albedo.as_list())
                    
                    checker_texture_scale[checker_index] = obj.material.texture.scale
                
                elif isinstance(obj.material.texture, perlin_noise):
                    perlin_index += 1
                    lambertian_texture_type[lambertian_index] = 2
                    lambertian_texture_index[lambertian_index] = perlin_index
                    perlin_scale[perlin_index] = obj.material.texture.scale
                    
                elif isinstance(obj.material.texture, image_texture):
                    image_texture_index += 1
                    lambertian_texture_type[lambertian_index] = 3
                    lambertian_texture_index[lambertian_index] = image_texture_index
                    image_texture_height[image_texture_index] = obj.material.texture.image.height
                    image_texture_width[image_texture_index] = obj.material.texture.image.width
                    image_texture_width_start[image_texture_index] = image_width_start
                    
                    for y in range(obj.material.texture.image.height):
                        for x in range(obj.material.texture.image.width):
                            image_texture_data[y, image_width_start + x] = ti.Vector(obj.material.texture.image.pixels[y, x])
                    
                    image_width_start += obj.material.texture.image.width                   
                    
            elif isinstance(obj.material, metal):
                metal_index += 1
                quad_material_type[quad_index] = 1
                quad_material_index[quad_index] = metal_index
                
                if isinstance(obj.material.texture, solid_color):
                    solid_color_vec_index += 1
                    metal_texture_type[metal_index] = 0
                    metal_texture_index[metal_index] = solid_color_vec_index
                    solid_color_vec[solid_color_vec_index] = ti.Vector(obj.material.texture.albedo.as_list())
                
                metal_fuzz[metal_index] = obj.material.fuzz
            
            elif isinstance(obj.material, dielectric):
                dielectric_index += 1
                quad_material_type[quad_index] = 2
                quad_material_index[quad_index] = dielectric_index
                dielectric_refractive_index[dielectric_index] = obj.material.refractive_index
            
            elif isinstance(obj.material, diffuse_light):
                diffuse_light_index += 1
                quad_material_type[quad_index] = 3
                quad_material_index[quad_index] = diffuse_light_index
                
                if isinstance(obj.material.texture, solid_color):
                    solid_color_vec_index +=1
                    diffuse_light_albedo[diffuse_light_index] = solid_color_vec_index
                    solid_color_vec[solid_color_vec_index] = ti.Vector(obj.material.texture.albedo.as_list())
        
        elif isinstance(obj, box):
            box_index += 1
            prim_type[prim_index] = 2
            prim_geo[prim_index] = box_index
            box_prim_indices_start[box_index] = quad_index+1
            
            
            