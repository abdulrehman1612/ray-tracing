#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 31 10:30:40 2025

@author: AGU
"""

from list_hittable import list_hittable

from Vec3 import vec3
point3 = vec3
from quad import quad


def box(a,b, mat):
    sides = list_hittable()
    
    min_ = point3(min(a.x(),b.x()), min(a.y(),b.y()),min(a.z(),b.z()))
    max_ = point3(max(a.x(),b.x()), max(a.y(),b.y()),max(a.z(),b.z()))

    dx = vec3(max_.x() - min_.x(), 0, 0);
    dy = vec3(0, max_.y() - min_.y(), 0);
    dz = vec3(0, 0, max_.z() - min_.z());

    sides.add(quad(point3(min_.x(), min_.y(), max_.z()),  dx,  dy, mat))
    sides.add(quad(point3(max_.x(), min_.y(), max_.z()), -dz,  dy, mat))
    sides.add(quad(point3(max_.x(), min_.y(), min_.z()), -dx,  dy, mat))
    sides.add(quad(point3(min_.x(), min_.y(), min_.z()),  dz,  dy, mat))
    sides.add(quad(point3(min_.x(), max_.y(), max_.z()),  dx, -dz, mat))
    sides.add(quad(point3(min_.x(), min_.y(), min_.z()),  dx,  dz, mat))
    
    return sides
