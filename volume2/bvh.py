# -*- coding: utf-8 -*-
"""
Created on Sat Nov 15 18:35:50 2025

@author: rehma
"""

from hittable import hit_record, hittable
from ray import ray
from numba import njit
from Vec3 import *
from aabb import AABB
from bvhnode import *


def enclose(objects):
    eps = 0.0001
    x_min = float('inf')
    y_min = float('inf')
    z_min = float('inf')
    x_max = -float('inf')
    y_max = -float('inf')
    z_max = -float('inf')
    
    for obj in objects:
        x_min = min(x_min, obj.axis_min().x())
        y_min = min(y_min, obj.axis_min().y())
        z_min = min(z_min, obj.axis_min().z())

        x_max = max(x_max, obj.axis_max().x())
        y_max = max(y_max, obj.axis_max().y())
        z_max = max(z_max, obj.axis_max().z())
    
    if x_max - x_min < eps:
        x_max += eps
        x_min -= eps
    if y_max - y_min < eps:
        y_max += eps
        y_min -= eps
    if z_max - z_min < eps:
        z_max += eps
        z_min -= eps
     
    min_ = vec3(x_min, y_min, z_min)
    max_ = vec3(x_max, y_max, z_max)
    
    return AABB(min_, max_)
            





def make_BVH(objects, axis=0):
    

    if len(objects) ==1 :
        return BVHNode(objects[0].aabb, objs=objects)    

    axis = axis % 3
    objects = sorted(objects, key=lambda obj: obj.aabb.center()[axis])
    mid = len(objects) // 2
    left_objs = objects[:mid]
    right_objs = objects[mid:]
    left_node = make_BVH(left_objs, axis + 1)
    right_node = make_BVH(right_objs, axis + 1)
    box = enclose(objects)

    return BVHNode(box, left=left_node, right=right_node)
        
def BVH(objects):
    return make_BVH(objects) 
            

    
    
    
        
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    