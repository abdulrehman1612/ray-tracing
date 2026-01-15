#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 28 19:54:51 2025

@author: AGU
"""


from libc.math cimport sqrt
from libc.math cimport pow
import random as rnd
from cpython cimport array
import array
import numpy as np

cdef class vec3:
    cdef double e[3]
    
    def __init__(self, double x, double y, double z):
        self.e[0] = x
        self.e[1] = y
        self.e[2] = z
    
    cpdef double x(self):
        return self.e[0]

    cpdef double y(self):
        return self.e[1]

    cpdef double z(self):
        return self.e[2]
    
    def __neg__(self):
        return vec3(-self.e[0], -self.e[1], -self.e[2])



    def __add__(self, vec3 o):
        return vec3(self.e[0] + o.e[0],
                self.e[1] + o.e[1],
                self.e[2] + o.e[2])

    def __sub__(self, vec3 o):
        return vec3(self.e[0] - o.e[0],
                    self.e[1] - o.e[1],
                    self.e[2] - o.e[2])


    def __mul__(self, other):
        if isinstance(other, vec3):

            return vec3(self.e[0] * other.x(),
                        self.e[1] * other.y(),
                        self.e[2] * other.z())
        else:

            return vec3(self.e[0] * other,
                        self.e[1] * other,
                        self.e[2] * other)
    
    def __rmul__(self, double t):
        return self * t
    
    def __truediv__(self, double t):
        cdef double inv = 1.0 / t
        return vec3(self.e[0] * inv,
                    self.e[1] * inv,
                    self.e[2] * inv)
    
    
    def __pow__(self, double exponent):
        return vec3(
            pow(self.e[0], exponent),
            pow(self.e[1], exponent),
            pow(self.e[2], exponent))

    def __getitem__(self, int i):
        if i < 0 or i > 2:
            raise IndexError("vec3 index out of range")
        return self.e[i]

    def __setitem__(self, int i, double value):
        if i < 0 or i > 2:
            raise IndexError("vec3 index out of range")
        self.e[i] = value


    cpdef double length(self):
        return sqrt(self.e[0]*self.e[0] +
                    self.e[1]*self.e[1] +
                    self.e[2]*self.e[2])
    
    cpdef double length_squared(self):
        return (self.e[0]*self.e[0] +
                self.e[1]*self.e[1] +
                self.e[2]*self.e[2])
    
    cpdef bint near_zero(self):
        cdef double s = 1e-8
        return (abs(self.e[0]) < s and
                abs(self.e[1]) < s and
                abs(self.e[2]) < s)
    
    @staticmethod
    def random(double a=-1, double b = 1):
        return vec3(rnd.uniform(a, b),
                    rnd.uniform(a, b),
                    rnd.uniform(a, b))
    
    def as_list(self):
        return np.array([self.e[0], self.e[1], self.e[2]])


cpdef double dot(vec3 a, vec3 b):
    return (a.x()*b.x() + a.y() * b.y() + a.z()*b.z())

cpdef vec3 cross(vec3 a, vec3 b):
    return vec3(a.y()*b.z() - a.z()*b.y(), a.z()*b.x() - a.x()*b.z(), a.x()*b.y() - a.y()*b.x())

cpdef vec3 unit_vector(vec3 a):
    return a/a.length()

cpdef vec3 random_unit_vector():
    cdef vec3 p
    cdef double lensq
    while True:
        p = vec3.random()
        lensq = p.length_squared()
        if (1e-160 < lensq <= 1):
            return (p/(lensq**0.5)) 

cpdef vec3 random_on_hemisphere(vec3 normal):
    cdef vec3 on_unit_sphere
    on_unit_sphere = random_unit_vector()
    if (dot(on_unit_sphere, normal)>0):
        return on_unit_sphere
    else:
        return -on_unit_sphere

cpdef vec3 random_in_unit_disk(double a, double b):
    cdef vec3 p
    cdef double lensq
    while True:
        p = vec3(rnd.uniform(a,b), rnd.uniform(a,b), 0)
        lensq = p.length_squared()
        if lensq < 1:
            return p

cpdef vec3 random_disk_sample(vec3 center, vec3 defocus_disk_u, vec3 defocus_disk_v):
    cdef vec3 p
    p = random_in_unit_disk(-1,1)
    return center + (p.x() * defocus_disk_u) + (p.y() * defocus_disk_v)

cpdef vec3 reflect(vec3 v,vec3 n):
    return v - 2*dot(v,n)*n

cpdef vec3 refract(vec3 r, vec3 n, double etai_over_etat):
    cdef double cos_theta
    cdef vec3 r_out_perp
    cdef vec3 r_out_parallel
    cos_theta = min(dot(-r, n), 1.0)
    r_out_perp =  etai_over_etat * (r + cos_theta*n)
    r_out_parallel = -((abs(1.0 - r_out_perp.length_squared()))**0.5) * n
    return r_out_perp + r_out_parallel

cpdef double reflectance(double cosine, double refraction_index):
    cdef double r0
    r0 = ((1 - refraction_index)/(1 + refraction_index))
    r0 = r0*r0
    return r0 + (1-r0)*((1 - cosine)**5)


color = vec3
point3 = vec3           
