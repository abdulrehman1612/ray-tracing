#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  8 03:21:00 2026

@author: AGU
"""

import taichi as ti
from taichi_modules import object_hit, material_scatter
import taichi_world


@ti.func
def ray_color(r, ray_tmin, ray_tmax, max_depth, background_color):
    
    color = ti.Vector([0.0,0.0,0.0])
    attenuation = ti.Vector([1.0, 1.0, 1.0])
    current_r = r
    
    for depth in range(max_depth):
        
        if depth == max_depth:
            attenuation *= ti.Vector([1.0,0.0,0.0])
            
        else:
            hit_anything = False
            closest_t = ray_tmax
            p = ti.Vector([0.0,0.0,0.0])
            front_face = -1
            normal = ti.Vector([0.0,0.0,0.0])
            u = -1.0
            v = -1.0
            mat_type = -1
            mat_idx = -1
            
            for i in range(ti.static(taichi_world.num_of_prim)):
                prim_idx = taichi_world.prim_indices[i]
                obj_type = taichi_world.prim_type[prim_idx]
                geo_idx = taichi_world.prim_geo[prim_idx]
            
                hit, current_t, current_p, current_front_face, current_normal, current_u, current_v, current_mat_type, current_mat_idx = object_hit(obj_type, geo_idx, current_r, ray_tmin, closest_t)
                if hit:
                    hit_anything = True
                    closest_t = current_t
                    p = current_p
                    front_face = current_front_face
                    normal = current_normal
                    u = current_u
                    v = current_v
                    mat_type = current_mat_type
                    mat_idx = current_mat_idx
                    
                    
            if hit_anything:
                (scatter, scattered, atten, emitted) = material_scatter(current_r, (closest_t, p,front_face,normal,u,v,mat_type, mat_idx))
                if scatter:
                    current_r = scattered
                    attenuation *= emitted+atten
                else:
                    attenuation *= emitted
                    break
            
            else:
                attenuation *= background_color
                break
    
    
    color += attenuation
    return color
            



