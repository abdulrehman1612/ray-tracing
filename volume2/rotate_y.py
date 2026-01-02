#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 30 08:06:35 2025

@author: AGU
"""

from hittable import hit_record, hittable
from list_hittable import list_hittable
import math
from bvhnode import *
from bvh import make_BVH
from Vec3 import vec3
from aabb import AABB
from ray import ray


class rotate_y(hittable):
    def __init__(self, obj, radians):
        self.obj = obj
        self.rad = radians
        self.sin_theta = math.sin(radians);
        self.cos_theta = math.cos(radians);
        
        if isinstance(obj, list_hittable):
            self.bvh = make_BVH(self.obj.objects)
            old_aabb = self.bvh.aabb()
        else:
            self.bvh = None
            old_aabb = AABB(self.obj.axis_min(), self.obj.axis_max())
            
        min_corner = vec3(float('inf'), float('inf'), float('inf'))
        max_corner = vec3(-float('inf'), -float('inf'), -float('inf'))

        for i in range(2):
            for j in range(2):
                for k in range(2):
                    x = i*old_aabb.axis_max().x() + (1-i)*old_aabb.axis_min().x()
                    y = j*old_aabb.axis_max().y() + (1-j)*old_aabb.axis_min().y()
                    z = k*old_aabb.axis_max().z() + (1-k)*old_aabb.axis_min().z()

                    newx = self.cos_theta * x + self.sin_theta * z
                    newz = -self.sin_theta * x + self.cos_theta * z
                    tester = vec3(newx, y, newz)

                    min_corner = vec3(min(min_corner.x(), tester.x()),
                                      min(min_corner.y(), tester.y()),
                                      min(min_corner.z(), tester.z()))
                    max_corner = vec3(max(max_corner.x(), tester.x()),
                                      max(max_corner.y(), tester.y()),
                                      max(max_corner.z(), tester.z()))

        self.aabb = AABB(min_corner, max_corner)
        
    def axis_min(self):
        return self.aabb.axis_min()
    
    def axis_max(self):
        return self.aabb.axis_max()
    
    def hit(self, r, ray_tmin: float, ray_tmax: float, rec: hit_record):
        
        origin = vec3((self.cos_theta * r.origin().x()) - (self.sin_theta * r.origin().z()), r.origin().y(), (self.sin_theta * r.origin().x()) + (self.cos_theta * r.origin().z()))
        
        direction = vec3((self.cos_theta * r.direction().x()) - (self.sin_theta * r.direction().z()), r.direction().y(), (self.sin_theta * r.direction().x()) + (self.cos_theta * r.direction().z()))
        
        rotated_r = ray(origin, direction, r.time())
        
        if self.bvh:
            if hit_BVH(self.bvh, rotated_r, ray_tmin, ray_tmax, rec):
                rec.p = vec3((self.cos_theta * rec.p.x()) + (self.sin_theta * rec.p.z()),rec.p.y(),(-self.sin_theta * rec.p.x()) + (self.cos_theta * rec.p.z()))
                rec.normal = vec3((self.cos_theta * rec.normal.x()) + (self.sin_theta * rec.normal.z()), rec.normal.y(), (-self.sin_theta * rec.normal.x()) + (self.cos_theta * rec.normal.z()))
                return True
        else:
            if self.obj.hit(rotated_r, ray_tmin, ray_tmax, rec):
                rec.p = vec3((self.cos_theta * rec.p.x()) + (self.sin_theta * rec.p.z()),rec.p.y(),(-self.sin_theta * rec.p.x()) + (self.cos_theta * rec.p.z()))
                rec.normal = vec3((self.cos_theta * rec.normal.x()) + (self.sin_theta * rec.normal.z()), rec.normal.y(), (-self.sin_theta * rec.normal.x()) + (self.cos_theta * rec.normal.z()))
                return True
            
        return False