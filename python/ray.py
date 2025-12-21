# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 23:47:10 2025

@author: rehma
"""
from Vec3 import vec3
class ray:
    def __init__(self, origin=None, direction=None):
        # Default constructor -> zero vectors (same as empty C++ constructor)
        if origin is None:
            origin = vec3(0, 0, 0)
        if direction is None:
            direction = vec3(0, 0, 0)

        self.orig = origin
        self.dir = direction

    def origin(self):
        return self.orig

    def direction(self):
        return self.dir

    def at(self, t):
        return self.orig + t * self.dir

    def __repr__(self):
        return f"ray(origin={self.orig}, direction={self.dir})"
