#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 01:22:07 2026

@author: AGU
"""
from Vec3 import vec3
from list_hittable import list_hittable
import BVH
import math

class sphere:
    def __init__(self, center1, radius, material, center2 = vec3(0,0,0)):
        
        self.center1 = center1
        self.center2 = center2
        self.radius = radius
        self.material = material
        self.type = 0
        
        cen1 = self.center1
        cen2 = self.center1 + self.center2
        max_cen1 = vec3(cen1.x()+self.radius, cen1.y()+self.radius, cen1.z()+self.radius)
        min_cen1 = vec3(cen1.x()-self.radius, cen1.y()-self.radius, cen1.z()-self.radius)
        max_cen2 = vec3(cen2.x()+self.radius, cen2.y()+self.radius, cen2.z()+self.radius)
        min_cen2 = vec3(cen2.x()-self.radius, cen2.y()-self.radius, cen2.z()-self.radius)
        
        self.max = vec3(max(max_cen1.x(), max_cen2.x()),max(max_cen1.y(), max_cen2.y()),max(max_cen1.z(), max_cen2.z()))
        self.min = vec3(min(min_cen1.x(), min_cen2.x()),min(min_cen1.y(), min_cen2.y()),min(min_cen1.z(), min_cen2.z()))
        self.centroid = (self.max+self.min) * 0.5


class quad:
    def __init__(self, Q,U,V, material):
        self.Q = Q
        self.U = U
        self.V = V
        self.material = material
        self.type = 1
        
        p0 = self.Q
        p1 = self.Q + self.U
        p2 = self.Q + self.V
        p3 = self.Q + self.U + self.V
        
        min_x = min(p0.x(), p1.x(), p2.x(), p3.x())
        min_y = min(p0.y(), p1.y(), p2.y(), p3.y())
        min_z = min(p0.z(), p1.z(), p2.z(), p3.z())

        max_x = max(p0.x(), p1.x(), p2.x(), p3.x())
        max_y = max(p0.y(), p1.y(), p2.y(), p3.y())
        max_z = max(p0.z(), p1.z(), p2.z(), p3.z())
        
        self.min = vec3(min_x, min_y, min_z)
        self.max = vec3(max_x, max_y, max_z)
        self.centroid = (self.max+self.min) * 0.5

class box:
    def __init__(self, a, b, mat):
        self.sides = list_hittable()
        self.material = None
        self.type = 2
        
        min_ = vec3(min(a.x(),b.x()), min(a.y(),b.y()),min(a.z(),b.z()))
        max_ = vec3(max(a.x(),b.x()), max(a.y(),b.y()),max(a.z(),b.z()))
    
        dx = vec3(max_.x() - min_.x(), 0, 0);
        dy = vec3(0, max_.y() - min_.y(), 0);
        dz = vec3(0, 0, max_.z() - min_.z());
    
        self.sides.add(quad(vec3(min_.x(), min_.y(), max_.z()),  dx,  dy, mat))
        self.sides.add(quad(vec3(max_.x(), min_.y(), max_.z()), -dz,  dy, mat))
        self.sides.add(quad(vec3(max_.x(), min_.y(), min_.z()), -dx,  dy, mat))
        self.sides.add(quad(vec3(min_.x(), min_.y(), min_.z()),  dz,  dy, mat))
        self.sides.add(quad(vec3(min_.x(), max_.y(), max_.z()),  dx, -dz, mat))
        self.sides.add(quad(vec3(min_.x(), min_.y(), min_.z()),  dx,  dz, mat))
        
        self.min = min_
        self.max = max_
        self.centroid = (self.max+self.min) * 0.5

class translate:
    def __init__(self, objects: list_hittable, offset):
        self.type = 3
        self.offset = offset
        self.objects = objects.objects
        
        for i, obj in enumerate(self.objects):
            obj.prim_id = i
        
        self.bvh = BVH.make_BVH(self.objects)
        
        
        BVH.bvh_nodes = []
        BVH.bvh_primitive_indices = []
        BVH.flatten_bvh(self.bvh)
        self.bvh_nodes = BVH.bvh_nodes
        self.bvh_primitive_indices = BVH.bvh_primitive_indices
        
        
        global_min = vec3(float('inf'), float('inf'), float('inf'))
        global_max = vec3(-float('inf'), -float('inf'), -float('inf'))
        
        for obj in self.objects:
            global_min = vec3(
                min(global_min.x(), obj.min.x()),
                min(global_min.y(), obj.min.y()),
                min(global_min.z(), obj.min.z()))
            
            global_max = vec3(
                max(global_max.x(), obj.max.x()),
                max(global_max.y(), obj.max.y()),
                max(global_max.z(), obj.max.z()))
        self.min = global_min + self.offset 
        self.max = global_max + self.offset
        self.centroid = (self.max+self.min) * 0.5
        
class rotate_y:
    def __init__(self, objects:list_hittable, angle):
        self.type = 4
        self.angle = math.radians(angle)
        self.objects = objects.objects
        
        for i, obj in enumerate(self.objects):
            obj.prim_id = i
        
        self.bvh = BVH.make_BVH(self.objects)
        
        
        BVH.bvh_nodes = []
        BVH.bvh_primitive_indices = []
        BVH.flatten_bvh(self.bvh)
        self.bvh_nodes = BVH.bvh_nodes
        self.bvh_primitive_indices = BVH.bvh_primitive_indices
        
        
        global_min = vec3(float('inf'), float('inf'), float('inf'))
        global_max = vec3(-float('inf'), -float('inf'), -float('inf'))
        
        for obj in self.objects:
            global_min = vec3(
                min(global_min.x(), obj.min.x()),
                min(global_min.y(), obj.min.y()),
                min(global_min.z(), obj.min.z()))
            
            global_max = vec3(
                max(global_max.x(), obj.max.x()),
                max(global_max.y(), obj.max.y()),
                max(global_max.z(), obj.max.z()))
        
        
        sin_theta = math.sin(self.angle)
        cos_theta = math.cos(self.angle)
        min_corner = vec3(float('inf'), float('inf'), float('inf'))
        max_corner = vec3(-float('inf'), -float('inf'), -float('inf'))
        
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    x = i*global_max.x() + (1-i)*global_min.x()
                    y = j*global_max.y() + (1-j)*global_min.y()
                    z = k*global_max.z() + (1-k)*global_min.z()
        
                    newx = cos_theta * x + sin_theta * z
                    newz = -sin_theta * x + cos_theta * z
                    tester = vec3(newx, y, newz)
        
                    min_corner = vec3(
                        min(min_corner.x(), tester.x()),
                        min(min_corner.y(), tester.y()),
                        min(min_corner.z(), tester.z())
                    )
                    max_corner = vec3(
                        max(max_corner.x(), tester.x()),
                        max(max_corner.y(), tester.y()),
                        max(max_corner.z(), tester.z())
                    )
        
        self.min = min_corner
        self.max = max_corner
        self.centroid = (self.max + self.min) * 0.5
        
        