# -*- coding: utf-8 -*-
"""
Created on Sat Nov 15 18:35:50 2025

@author: rehma
"""

from hittable import hittable, hit_record
from ray import ray
from Vec3 import point3

class AABB(hittable):
    def __init__(self, center: point3, length_x: float, length_y: float, length_z: float):
        self.center = center
        self.length_x = length_x
        self.length_y = length_y
        self.length_z = length_z
        self.min = point3(center.x() - length_x/2, center.y() - length_y/2, center.z() - length_z/2)
        self.max = point3(center.x() + length_x/2, center.y() + length_y/2, center.z() + length_z/2)
        
    def axis_min(self):
        return self.min
    
    def axis_max(self):
        return self.max

    def hit(self, r: ray, ray_tmin: float, ray_tmax: float):
        
        tmin = (self.min.x() - r.origin().x()) / r.direction().x()
        tmax = (self.max.x() - r.origin().x()) / r.direction().x()
        if 1/r.direction().x() < 0:
            tmin, tmax = tmax, tmin
        t0 = max(ray_tmin, tmin)
        t1 = min(ray_tmax, tmax)
        if t1 <= t0:
            return False
        
        tmin = (self.min.y() - r.origin().y()) / r.direction().y()
        tmax = (self.max.y() - r.origin().y()) / r.direction().y()
        if 1/r.direction().y() < 0:
            tmin, tmax = tmax, tmin
        t0 = max(t0, tmin)
        t1 = min(t1, tmax)
        if t1 <= t0:
            return False
        

        tmin = (self.min.z() - r.origin().z()) / r.direction().z()
        tmax = (self.max.z() - r.origin().z()) / r.direction().z()
        if 1/r.direction().z() < 0:
            tmin, tmax = tmax, tmin
        t0 = max(t0, tmin)
        t1 = min(t1, tmax)
        if t1 <= t0:
            return False
        
        return True


def enclose(objects):
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
    
    center = point3((x_min+x_max)/2,(y_min+y_max)/2,(z_min+z_max)/ 2)  
    box = AABB(center, (x_max-x_min), (y_max-y_min), (z_max-z_min))
    return box


class list_hittable:
    def __init__(self):
        self.objects = []
    
    def add(self,obj):
        self.objects.append(obj)


class BVHNode:
    def __init__(self, box, left=None, right=None, objects=None):
        self.box = box
        self.left = left 
        self.right = right
        self.objects = objects


def make_BVH(objects, axis=0):
    if len(objects) <= 2:
        box = enclose(objects)
        return BVHNode(box, objects=objects)
    
    axis = axis % 3
    objects = sorted(objects, key=lambda obj: obj.aabb.center[axis])
    mid = len(objects) // 2
    left_objs = objects[:mid]
    right_objs = objects[mid:]
    left_node = make_BVH(left_objs, axis + 1)
    right_node = make_BVH(right_objs, axis + 1)
    box = enclose(objects)

    return BVHNode(box, left=left_node, right=right_node)
        
def BVH(objects):
    return make_BVH(objects) 
            
def hit_BVH(node, r, ray_tmin, ray_tmax, rec):
    if not node.box.hit(r, ray_tmin, ray_tmax):
        return False

    hit_anything = False
    closest = ray_tmax
    temp = hit_record()

    if node.objects is not None:
        for obj in node.objects:
            if obj.hit(r, ray_tmin, closest, temp):
                hit_anything = True
                closest = temp.t
                rec.copy_from(temp)
        return hit_anything

    if hit_BVH(node.left, r, ray_tmin, closest, rec):
        hit_anything = True
        closest = rec.t
    if hit_BVH(node.right, r, ray_tmin, closest, rec):
        hit_anything = True
    return hit_anything
        
    
    
    
        
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    