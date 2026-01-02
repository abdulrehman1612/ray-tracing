#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 28 23:45:36 2025

@author: AGU
"""


from setuptools import setup
from Cython.Build import cythonize


setup(
    name='Vec3',
    ext_modules=cythonize("Vec3.pyx",compiler_directives={'language_level': "3"}),
)

setup(
    name='ray',
    ext_modules=cythonize("ray.pyx",compiler_directives={'language_level': "3"}),
)

setup(
    name='aabb',
    ext_modules=cythonize("aabb.pyx",compiler_directives={'language_level': "3"}),
)

setup(
    name='bvhnode',
    ext_modules=cythonize("bvhnode.pyx",compiler_directives={'language_level': "3"}),
)