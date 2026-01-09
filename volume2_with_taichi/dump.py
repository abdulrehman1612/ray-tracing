#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 03:13:25 2026

@author: AGU
"""

from materials import *
from textures import *
from objects import *
from list_hittable import *
from BVH import *
from Vec3 import *

def flatten_bvh(node):
    bvh_nodes = []
    primitive_indices = []
    node_index = len(bvh_nodes)
    bvh_nodes.append({
        "min": node.min,
        "max": node.max,
        "left": -1,
        "right": -1,
        "first_prim": -1,
        "prim_count": 0
    })

    if node.left is None and node.right is None:
        first_prim = len(primitive_indices)

        for obj in node.objects:
            primitive_indices.append(obj.prim_id)  # index into primitive buffer

        bvh_nodes[node_index]["first_prim"] = first_prim
        bvh_nodes[node_index]["prim_count"] = len(node.objects)

    # Internal node
    else:
        left_idx = flatten_bvh(node.left)
        right_idx = flatten_bvh(node.right)

        bvh_nodes[node_index]["left"] = left_idx
        bvh_nodes[node_index]["right"] = right_idx

    return node_index

world = list_hittable()

for i in range(3):
    for j in range(3):
        world.add(sphere(vec3(i,j,i+j), 1, None))

for i, obj in enumerate(world.objects):
    obj.prim_id = i

bvh = make_BVH(world.objects)


flatten_bvh(bvh)
sphere_count = 0
quad_count = 0
prim_geom = [0] * len(primitive_indices)

for prim_id, obj in enumerate(world.objects):
    if isinstance(obj, sphere):
        prim_geom[prim_id] = sphere_count
        sphere_count += 1
    elif isinstance(obj, quad):
        prim_geom[prim_id] = quad_count
        quad_count += 1

