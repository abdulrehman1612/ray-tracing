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
    
    if len(list_objects) <= 1:
        min_cords , max_cords = enclose(list_objects)
        return BVHNode(min_cords,max_cords, objects = list_objects)    

    axis = axis % 3
    objects = sorted(list_objects, key=lambda obj: obj.centroid[axis])
    mid = len(objects) // 2
    left_objs = objects[:mid]
    right_objs = objects[mid:]
    left_node = make_BVH(left_objs, axis + 1)
    right_node = make_BVH(right_objs, axis + 1)
    
    min_cords, max_cords = enclose([left_node, right_node])

    return BVHNode(min_cords, max_cords, left=left_node, right=right_node)
    
    
    
bvh_nodes = []
bvh_primitive_indices = []

def flatten_bvh(node):

    node_index = len(bvh_nodes)
    bvh_nodes.append({"min": node.min.as_list(),
                      "max": node.max.as_list(),
                      "left": -1,
                      "right": -1,
                      "first_prim": -1,
                      "prim_count": 0})

    if node.left is None and node.right is None:
        first_prim = len(bvh_primitive_indices)
        for obj in node.objects:
            bvh_primitive_indices.append(obj.prim_id)
        bvh_nodes[node_index]["first_prim"] = first_prim
        bvh_nodes[node_index]["prim_count"] = len(node.objects)
    else:
        left_idx = flatten_bvh(node.left)
        right_idx = flatten_bvh(node.right)

        bvh_nodes[node_index]["left"] = left_idx
        bvh_nodes[node_index]["right"] = right_idx
    return node_index




