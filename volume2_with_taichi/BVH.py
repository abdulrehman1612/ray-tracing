#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 02:54:53 2026

@author: AGU
"""

from Vec3 import vec3

class BVHNode:
    def __init__(self, min_cords, max_cords, left=None, right=None, objects = None):
        self.min = min_cords
        self.max = max_cords
        self.left = left
        self.right = right
        self.objects = objects

def enclose(objects):
    eps = 0.0001
    x_min = float('inf')
    y_min = float('inf')
    z_min = float('inf')
    x_max = -float('inf')
    y_max = -float('inf')
    z_max = -float('inf')
    
    for obj in objects:
        x_min = min(x_min, obj.min.x())
        y_min = min(y_min, obj.min.y())
        z_min = min(z_min, obj.min.z())

        x_max = max(x_max, obj.max.x())
        y_max = max(y_max, obj.max.y())
        z_max = max(z_max, obj.max.z())
    
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
    
    return min_, max_


def make_BVH(list_objects, axis = 0):
    
    if len(list_objects) <= 4 :
        min_cords , max_cords = enclose(list_objects)
        return BVHNode(min_cords,max_cords, objects = list_objects)    

    axis = axis % 3
    objects = sorted(list_objects, key=lambda obj: obj.centroid[axis])
    mid = len(objects) // 2
    left_objs = objects[:mid]
    right_objs = objects[mid:]
    left_node = make_BVH(left_objs, axis + 1)
    right_node = make_BVH(right_objs, axis + 1)
    min_cords, max_cords = enclose(objects)

    return BVHNode(min_cords, max_cords, left=left_node, right=right_node)