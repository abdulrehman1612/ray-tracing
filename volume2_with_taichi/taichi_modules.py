#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  6 22:49:59 2026

@author: AGU
"""


import taichi as ti
import taichi_world
#####

Ray = ti.types.struct(origin=ti.types.vector(3, ti.f32),direction=ti.types.vector(3, ti.f32),time=ti.f32)

#####

@ti.func
def cross(a,b):
    return ti.Vector([a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0]])

@ti.func
def random_in_unit_sphere():
    p = ti.Vector([0.0, 0.0, 0.0])
    while True:
        candidate = ti.Vector([ti.random() * 2 - 1, ti.random() * 2 - 1, ti.random() * 2 - 1])
        if candidate.norm_sqr() <= 1.0:
            p = candidate
            break
    return p

@ti.func
def random_unit_vector():
    p = ti.Vector([0.0, 0.0, 0.0])
    while True:
        candidate = ti.Vector([ti.random() * 2 - 1, ti.random() * 2 - 1, ti.random() * 2 - 1])
        lnsq = candidate.dot(candidate)
        if 1e-160 < lnsq <= 1.0:
            p = (candidate/(lnsq**0.5))
            break
        
    return p

@ti.func
def random_on_hemisphere(normal):
    p = random_unit_vector()
    if p.dot(normal) > 0.0:
        return p
    else:
        return -p


@ti.func
def random_in_unit_disk():
    p = ti.Vector([0.0, 0.0, 0.0])
    while True:
        candidate = ti.Vector([ti.random() * 2 - 1, ti.random() * 2 - 1, 0.0])
        if candidate.norm_sqr() < 1:
            p = candidate
            break
    return p

@ti.func
def random_disk_sample(center, disk_u, disk_v):
    p = random_in_unit_disk()
    return center + p[0] * disk_u + p[1] * disk_v

@ti.func
def reflect(v, n):
    return v - 2 * v.dot(n) * n

@ti.func
def refract(r, n, etai_over_etat):
    cos_theta = min((-r).dot(n), 1.0)
    r_out_perp = etai_over_etat * (r + cos_theta * n)
    r_out_parallel = -ti.sqrt(abs(1.0 - r_out_perp.norm_sqr())) * n
    return r_out_perp + r_out_parallel

@ti.func
def reflectance(cosine, ref_idx):
    r0 = (1.0 - ref_idx) / (1.0 + ref_idx)
    r0 = r0 * r0
    return r0 + (1 - r0) * ((1 - cosine) ** 5)

@ti.func
def set_face_normal(r, outward_normal):
    front_face = r.direction.dot(outward_normal) < 0
    normal = outward_normal if front_face else -outward_normal
    return front_face, normal
    
@ti.func
def get_sphere_uv(p):
    pi = 3.141592653589793
    theta = ti.acos(-p[1])
    phi = ti.atan2(-p[2], p[0]) + pi
    u = phi / (2 * pi)
    v = theta / pi
    return u, v


@ti.func
def perlin_noise(p):
    accum = 0.0
    u = p[0] - ti.floor(p[0])
    v = p[1] - ti.floor(p[1])
    w = p[2] - ti.floor(p[2])
    
    i = int(ti.floor(p[0]))
    j = int(ti.floor(p[1]))
    k = int(ti.floor(p[2]))
    
    for di in range(2):
        for dj in range(2):
            for dk in range(2):
                taichi_world.perlin_c[di, dj, dk] = taichi_world.perlin_random_vec[taichi_world.perlin_perm_x[(i+di) & 255] ^ taichi_world.perlin_perm_y[(j+dj) & 255] ^ taichi_world.perlin_perm_z[(k+dk) & 255]] 

    uu = u*u*(3-2*u)
    vv = v*v*(3-2*v)
    ww = w*w*(3-2*w)
    
    for l in range(2):
        for m in range(2):
            for n in range(2):
                weight_v = ti.Vector([u-l, v-m, w-n], dt=ti.f32)
                accum += (l*uu + (1-l)*(1-uu)) * (m*vv + (1-m)*(1-vv)) * (n*ww + (1-n)*(1-ww)) *  ((taichi_world.perlin_c[l,m,n][0]) * weight_v[0] + (taichi_world.perlin_c[l,m,n][1]) * weight_v[1] + (taichi_world.perlin_c[l,m,n][2]) * weight_v[2])
    return accum

@ti.func
def perlin_terbulance(p, depth):
    accum = 0.0
    temp_p = p
    weight = 1.0
    
    for i in range(depth):
        accum += weight*perlin_noise(temp_p)
        weight *= 0.5
        temp_p *= 2
        
    accum = abs(accum)
    
    return accum

    

@ti.func
def material_scatter(r, rec_tuple):
    scatter = False
    scattered = Ray(origin=ti.Vector([0,0,0],dt=ti.f32), direction=ti.Vector([0,0,0],dt=ti.f32), time=0.0)
    attenuation = ti.Vector([0,0,0],dt=ti.f32)
    emitted = ti.Vector([0.0, 0.0, 0.0])
    (t,p,front_face,normal,u,v,mat_type, mat_idx) = rec_tuple
    
    if mat_type == 0:
        scatter = True
        texture_type = taichi_world.lambertian_texture_type[mat_idx]
        texture_idx = taichi_world.lambertian_texture_index[mat_idx]
        scatter_direction = normal + random_unit_vector()
        if (abs(scatter_direction[0]) < 1e-8 and abs(scatter_direction[1]) < 1e-8 and abs(scatter_direction[2]) < 1e-8):
            scatter_direction = normal
        scattered = Ray(origin=p,direction=scatter_direction, time=r.time)
        attenuation = texture_value(texture_type, texture_idx, u, v, p)
    
    elif mat_type == 1:
        texture_type = taichi_world.metal_texture_type[mat_idx]
        texture_idx = taichi_world.metal_texture_index[mat_idx]
        reflected = reflect(r.direction, normal)
        reflected = reflected.normalized() + (taichi_world.metal_fuzz[mat_idx] * random_unit_vector())
        scattered = Ray(origin=p, direction=reflected, time=r.time)
        scatter = scattered.direction.dot(normal) > 0
        attenuation = texture_value(texture_type, texture_idx, u, v, p)
    
    elif mat_type == 2:
        
        scatter = True
        unit_direction = r.direction.normalized()
        cos_theta = min((-unit_direction).dot(normal), 1.0)
        sin_theta = (1.0 - cos_theta*cos_theta)**0.5
        attenuation = ti.Vector([1.0,1.0,1.0])
        refractive_index = 1/taichi_world.dielectric_refractive_index[mat_idx] if front_face else taichi_world.dielectric_refractive_index[mat_idx]
        r_direction = ti.Vector([0.0,0.0,0.0])
        if (refractive_index * sin_theta > 1.0) or (reflectance(cos_theta, refractive_index) > ti.random()):
            r_direction = reflect(unit_direction, normal)
        
        else:
            r_direction = refract(unit_direction, normal, refractive_index)
        
        scattered = Ray(origin=p, direction=r_direction, time=r.time)
    
    elif mat_type == 3:
        albedo_index = taichi_world.diffuse_light_albedo[mat_idx]
        emitted = taichi_world.solid_color_vec[albedo_index]
        
        
    return (scatter, scattered, attenuation, emitted)





@ti.func
def texture_value(texture_type, texture_idx, u, v, p):
    color = ti.Vector([0,0,0],dt=ti.f32)
    
    if texture_type == 0:
        color = taichi_world.solid_color_vec[texture_idx]

    elif texture_type == 1:
        scale = taichi_world.checker_texture_scale[texture_idx]
        x_int = int(ti.floor(scale * p[0]))
        y_int = int(ti.floor(scale * p[1]))
        z_int = int(ti.floor(scale * p[2]))
        is_even = (x_int+y_int+z_int)%2 == 0
        
        if is_even:
            even_type = taichi_world.checker_texture_even_type[texture_idx]
            even_idx = taichi_world.checker_texture_even_index[texture_idx]
            if even_type == 0:
                color = taichi_world.solid_color_vec[even_idx]
        else:
            odd_type = taichi_world.checker_texture_odd_type[texture_idx]
            odd_idx = taichi_world.checker_texture_odd_index[texture_idx]
            if odd_type == 0:
                color = taichi_world.solid_color_vec[odd_idx]
    elif texture_type == 2:
        scale = taichi_world.perlin_scale[texture_idx]
        color = ti.Vector([0.5,0.5,0.5]) * (1 + ti.sin(scale * p[2] + 10 * perlin_terbulance(p, 7)))
    
    elif texture_type == 3:
        
        u = max(0.0, min(1.0, u))
        v = 1.0 - max(0.0, min(1.0, v))
        i = int(u*taichi_world.image_texture_width[texture_idx])
        j = int(v*taichi_world.image_texture_height[texture_idx])
        
        i = max(0, min(i, taichi_world.image_texture_width[texture_idx] - 1))
        j = max(0, min(j, taichi_world.image_texture_height[texture_idx] - 1))
        
        color = taichi_world.image_texture_data[j, taichi_world.image_texture_width_start[texture_idx] + i]
        
    return color

@ti.func
def hit_aabb(r, ray_tmin, ray_tmax, min_cords, max_cords):
    hit = True
    
    tmin = (min_cords[0] - r.origin[0]) / r.direction[0]
    tmax = (max_cords[0] - r.origin[0]) / r.direction[0]
    
    temp = 0.0
    if 1/r.direction[0] < 0:
        temp = tmin
        tmin = tmax
        tmax = temp
    
    t0 = max(ray_tmin, tmin)
    t1 = min(ray_tmax, tmax)
    
    if t1 <= t0:
        hit = False
    
    tmin = (min_cords[1] - r.origin[1]) / r.direction[1]
    tmax = (max_cords[1] - r.origin[1]) / r.direction[1]
    
    temp = 0.0
    if 1/r.direction[1] < 0:
        temp = tmin
        tmin = tmax
        tmax = temp
    
    t0 = max(t0, tmin)
    t1 = min(t1, tmax)
    
    if t1 <= t0:
        hit = False
    
    tmin = (min_cords[2] - r.origin[2]) / r.direction[2]
    tmax = (max_cords[2] - r.origin[2]) / r.direction[2]
    
    temp = 0.0
    if 1/r.direction[2] < 0:
        temp = tmin
        tmin = tmax
        tmax = temp
    
    t0 = max(t0, tmin)
    t1 = min(t1, tmax)
    
    if t1 <= t0:
        hit = False

    
    return hit
    




@ti.func
def quad_hit(obj_index, r, ray_tmin, ray_tmax):
    
    hit = True
    t = -1.0
    p = ti.Vector([0,0,0],dt=ti.f32)
    front_face = False
    normal = ti.Vector([0,0,0],dt=ti.f32)
    u = -1.0
    v = -1.0
    material_type = -1
    material_index = -1
    
    current_Q = taichi_world.quad_Q[obj_index]
    current_U = taichi_world.quad_U[obj_index]
    current_V = taichi_world.quad_V[obj_index]
    
    n = cross(current_U,current_V)
    normal = n.normalized()
    w = n / n.dot(n)
    D = normal.dot(current_Q)
    denom = normal.dot(r.direction)
    if abs(denom) < 1e-8:
        hit = False
    t = (D - normal.dot(r.origin)) / denom
    if not (ray_tmin <= t <= ray_tmax):
        hit = False
    
    intersection = r.origin + t * r.direction
    p = intersection - current_Q
    alpha = w.dot(cross(p, current_V))
    beta = w.dot(cross(current_U, p))
    
    if not (0 <= alpha <= 1) or not (0 <= beta <= 1):
        hit = False
    
    if hit:
        t = t
        p = intersection
        front_face, normal = set_face_normal(r, normal)
        u = alpha
        v = beta
        material_type = taichi_world.quad_material_type[obj_index]
        material_index = taichi_world.quad_material_index[obj_index]
    
    return (hit, t, p, front_face, normal, u, v, material_type, material_index)
    
    
    

@ti.func
def sphere_hit(obj_index, r, ray_tmin, ray_tmax):
    
    hit = True
    t = -1.0
    p = ti.Vector([0,0,0],dt=ti.f32)
    front_face = False
    normal = ti.Vector([0,0,0],dt=ti.f32)
    u = -1.0
    v = -1.0
    material_type = -1
    material_index = -1
    
    current_center = taichi_world.sphere_center0[obj_index] + r.time * taichi_world.sphere_center1[obj_index]
    current_radius = taichi_world.sphere_radius[obj_index]
    oc = current_center - r.origin
    a = r.direction.norm_sqr()
    h = r.direction.dot(oc)
    c = oc.norm_sqr()-current_radius**2
    discriminent = h*h-a*c
    if discriminent < 0:
        hit = False
    
    sqrt_d = discriminent**0.5
    root = (h - sqrt_d) / a
    if root <= ray_tmin or ray_tmax <= root:
        root = (h + sqrt_d) / a
        if root <= ray_tmin or ray_tmax <= root:
            hit = False
    if hit:
        t = root
        p = r.origin + root * r.direction
        outward_normal = (p - current_center)/current_radius
        front_face, normal = set_face_normal(r, outward_normal)
        u,v = get_sphere_uv(outward_normal)
        material_type = taichi_world.sphere_material_type[obj_index]
        material_index = taichi_world.sphere_material_index[obj_index]

    return (hit, t, p, front_face, normal, u, v, material_type, material_index)



@ti.func
def box_hit(obj_index, r, ray_tmin, ray_tmax):
    
    hit = False
    t = -1.0
    p = ti.Vector([0,0,0],dt=ti.f32)
    front_face = False
    normal = ti.Vector([0,0,0],dt=ti.f32)
    u = -1.0
    v = -1.0
    material_type = -1
    material_index = -1
    
    
    
    
    temp_hit = False
    temp_t = -1.0
    temp_p = ti.Vector([0,0,0],dt=ti.f32)
    temp_front_face = False
    temp_normal = ti.Vector([0,0,0],dt=ti.f32)
    temp_u = -1.0
    temp_v = -1.0
    temp_material_type = -1
    temp_material_index = -1
    
    
    
    closest = ray_tmax
    side_start_idx = taichi_world.box_prim_indices_start[obj_index]
    
    for i in range(6):
        temp_hit, temp_t, temp_p, temp_front_face, temp_normal, temp_u, temp_v, temp_material_type, temp_material_index = quad_hit(side_start_idx+i, r, ray_tmin, closest)
        if temp_hit:
            closest = temp_t
            hit, t, p, front_face, normal, u, v, material_type, material_index = temp_hit, temp_t, temp_p, temp_front_face, temp_normal, temp_u, temp_v, temp_material_type, temp_material_index


    return (hit, t, p, front_face, normal, u, v, material_type, material_index)




@ti.func
def translate_hit(obj_index, r, ray_tmin, ray_tmax):
    
    hit = False
    t = -1.0
    p = ti.Vector([0,0,0],dt=ti.f32)
    front_face = False
    normal = ti.Vector([0,0,0],dt=ti.f32)
    u = -1.0
    v = -1.0
    material_type = -1
    material_index = -1
    
    offset = taichi_world.translate_offset[obj_index]
    node_index = taichi_world.translate_parent_node[obj_index]
    
    offset_r  = Ray(origin= r.origin-offset, direction=r.direction, time=r.time ) 
    
    
    stack = ti.Vector([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    top = 0
    stack[top] = node_index
    top +=1
    
    
    closest_t = ray_tmax
    
    
    
    while top > 0:
        top -= 1
        node_idx = stack[top]
        
        if taichi_world.translate_bvh_node_prim_start[node_idx] != -1:
            
            num_of_objects = taichi_world.translate_bvh_node_prim_count[node_idx]
            
            for i in range(num_of_objects):
                
                prim_idx = taichi_world.translate_prim_indices[taichi_world.translate_bvh_node_prim_start[node_idx]+i]
                
                current_obj_type = taichi_world.translate_prim_type[prim_idx]
                
                geo_idx = taichi_world.translate_prim_geo[prim_idx]
                
                if current_obj_type == 0:
                    
                    temp_hit, temp_t, temp_p, temp_front_face, temp_normal, temp_u, temp_v, temp_material_type, temp_material_index = sphere_hit(geo_idx, offset_r, ray_tmin, closest_t)
                    if temp_hit:
                        closest_t = temp_t
                        temp_p += offset
                        hit, t, p, front_face, normal, u, v, material_type, material_index = temp_hit, temp_t, temp_p, temp_front_face, temp_normal, temp_u, temp_v, temp_material_type, temp_material_index
                    
                elif current_obj_type == 1:
                    
                    temp_hit, temp_t, temp_p, temp_front_face, temp_normal, temp_u, temp_v, temp_material_type, temp_material_index = quad_hit(geo_idx, offset_r, ray_tmin, closest_t)
                    if temp_hit:
                        temp_p += offset
                        closest_t = temp_t
                        hit, t, p, front_face, normal, u, v, material_type, material_index = temp_hit, temp_t, temp_p, temp_front_face, temp_normal, temp_u, temp_v, temp_material_type, temp_material_index
                
                elif current_obj_type == 2:
                    
                    temp_hit, temp_t, temp_p, temp_front_face, temp_normal, temp_u, temp_v, temp_material_type, temp_material_index = box_hit(geo_idx, offset_r, ray_tmin, closest_t)
                    if temp_hit:
                        closest_t = temp_t
                        temp_p += offset
                        hit, t, p, front_face, normal, u, v, material_type, material_index = temp_hit, temp_t, temp_p, temp_front_face, temp_normal, temp_u, temp_v, temp_material_type, temp_material_index
                
                elif current_obj_type == 3:
                    
                    temp_hit, temp_t, temp_p, temp_front_face, temp_normal, temp_u, temp_v, temp_material_type, temp_material_index = rotate_y_hit(geo_idx, offset_r, ray_tmin, closest_t)
                    if temp_hit:
                        closest_t = temp_t
                        temp_p += offset
                        hit, t, p, front_face, normal, u, v, material_type, material_index = temp_hit, temp_t, temp_p, temp_front_face, temp_normal, temp_u, temp_v, temp_material_type, temp_material_index
                
                    
        else:
            
            left_idx = taichi_world.translate_bvh_node_left[node_idx]
            if hit_aabb(offset_r, ray_tmin, closest_t, taichi_world.translate_bvh_node_min[left_idx], taichi_world.translate_bvh_node_max[left_idx]):
                stack[top] = left_idx
                top += 1
                
                
            right_idx = taichi_world.translate_bvh_node_right[node_idx]
            if hit_aabb(offset_r, ray_tmin, closest_t, taichi_world.translate_bvh_node_min[right_idx], taichi_world.translate_bvh_node_max[right_idx]):
                stack[top] = right_idx
                top += 1 

    return (hit, t, p, front_face, normal, u, v, material_type, material_index)


@ti.func
def rotate_y_hit(obj_index, r, ray_tmin, ray_tmax):
    
    hit = False
    t = -1.0
    p = ti.Vector([0,0,0],dt=ti.f32)
    front_face = False
    normal = ti.Vector([0,0,0],dt=ti.f32)
    u = -1.0
    v = -1.0
    material_type = -1
    material_index = -1
    
    angle = taichi_world.rotate_y_angle[obj_index]
    node_index = taichi_world.rotate_y_parent_node[obj_index]
    
    cos_theta = ti.cos(angle)
    sin_theta = ti.sin(angle)
    
    origin = ti.Vector([(cos_theta * r.origin[0]) - (sin_theta * r.origin[2]), r.origin[1], (sin_theta * r.origin[0]) + (cos_theta * r.origin[2])])
        
    direction = ti.Vector([(cos_theta * r.direction[0]) - (sin_theta * r.direction[2]), r.direction[1], (sin_theta * r.direction[0]) + (cos_theta * r.direction[2])])
        
    rotated_r = Ray(origin = origin, direction = direction, time= r.time)
    
    stack = ti.Vector([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    top = 0
    stack[top] = node_index
    top +=1
    
    
    closest_t = ray_tmax
    
    
    
    while top > 0:
        top -= 1
        node_idx = stack[top]
        
        if taichi_world.rotate_y_bvh_node_prim_start[node_idx] != -1:
            
            num_of_objects = taichi_world.rotate_y_bvh_node_prim_count[node_idx]
            
            for i in range(num_of_objects):
                
                prim_idx = taichi_world.rotate_y_prim_indices[taichi_world.rotate_y_bvh_node_prim_start[node_idx]+i]
                
                current_obj_type = taichi_world.rotate_y_prim_type[prim_idx]
                
                geo_idx = taichi_world.rotate_y_prim_geo[prim_idx]
                
                if current_obj_type == 0:
                    
                    temp_hit, temp_t, temp_p, temp_front_face, temp_normal, temp_u, temp_v, temp_material_type, temp_material_index = sphere_hit(geo_idx, rotated_r, ray_tmin, closest_t)
                    if temp_hit:
                        temp_p = ti.Vector([(cos_theta * temp_p[0]) + (sin_theta * temp_p[2]), temp_p[1],(-sin_theta * temp_p[0]) + (cos_theta * temp_p[2])])
                        temp_normal = ti.Vector([(cos_theta * temp_normal[0]) + (sin_theta * temp_normal[2]), temp_normal[1], (-sin_theta * temp_normal[0]) + (cos_theta * temp_normal[2])])
                        closest_t = temp_t
                        hit, t, p, front_face, normal, u, v, material_type, material_index = temp_hit, temp_t, temp_p, temp_front_face, temp_normal, temp_u, temp_v, temp_material_type, temp_material_index
                    
                elif current_obj_type == 1:
                    
                    temp_hit, temp_t, temp_p, temp_front_face, temp_normal, temp_u, temp_v, temp_material_type, temp_material_index = quad_hit(geo_idx, rotated_r, ray_tmin, closest_t)
                    if temp_hit:
                        temp_p = ti.Vector([(cos_theta * temp_p[0]) + (sin_theta * temp_p[2]), temp_p[1],(-sin_theta * temp_p[0]) + (cos_theta * temp_p[2])])
                        temp_normal = ti.Vector([(cos_theta * temp_normal[0]) + (sin_theta * temp_normal[2]), temp_normal[1], (-sin_theta * temp_normal[0]) + (cos_theta * temp_normal[2])])
                        closest_t = temp_t
                        hit, t, p, front_face, normal, u, v, material_type, material_index = temp_hit, temp_t, temp_p, temp_front_face, temp_normal, temp_u, temp_v, temp_material_type, temp_material_index
                
                elif current_obj_type == 2:
                    
                    temp_hit, temp_t, temp_p, temp_front_face, temp_normal, temp_u, temp_v, temp_material_type, temp_material_index = box_hit(geo_idx, rotated_r, ray_tmin, closest_t)
                    if temp_hit:
                        closest_t = temp_t
                        temp_p = ti.Vector([(cos_theta * temp_p[0]) + (sin_theta * temp_p[2]), temp_p[1],(-sin_theta * temp_p[0]) + (cos_theta * temp_p[2])])
                        temp_normal = ti.Vector([(cos_theta * temp_normal[0]) + (sin_theta * temp_normal[2]), temp_normal[1], (-sin_theta * temp_normal[0]) + (cos_theta * temp_normal[2])])
                        hit, t, p, front_face, normal, u, v, material_type, material_index = temp_hit, temp_t, temp_p, temp_front_face, temp_normal, temp_u, temp_v, temp_material_type, temp_material_index
                
                
                    
        else:
            
            left_idx = taichi_world.rotate_y_bvh_node_left[node_idx]
            if hit_aabb(rotated_r, ray_tmin, closest_t, taichi_world.rotate_y_bvh_node_min[left_idx], taichi_world.rotate_y_bvh_node_max[left_idx]):
                stack[top] = left_idx
                top += 1
                
                
            right_idx = taichi_world.rotate_y_bvh_node_right[node_idx]
            if hit_aabb(rotated_r, ray_tmin, closest_t, taichi_world.rotate_y_bvh_node_min[right_idx], taichi_world.rotate_y_bvh_node_max[right_idx]):
                stack[top] = right_idx
                top += 1 

    return (hit, t, p, front_face, normal, u, v, material_type, material_index)
    
    


@ti.func
def object_hit(obj_type, obj_index, r, ray_tmin, ray_tmax):
    
    hit = False
    t = -1.0
    p = ti.Vector([0,0,0],dt=ti.f32)
    front_face = False
    normal = ti.Vector([0,0,0],dt=ti.f32)
    u = -1.0
    v = -1.0
    material_type = -1
    material_index = -1
    
    if obj_type == 0: #sphere
    
        hit, t, p, front_face, normal, u, v, material_type, material_index = sphere_hit(obj_index, r, ray_tmin, ray_tmax)
            

    elif obj_type == 1:
        
        hit, t, p, front_face, normal, u, v, material_type, material_index = quad_hit(obj_index, r, ray_tmin, ray_tmax)
    
    
    elif obj_type == 2:
        
        hit, t, p, front_face, normal, u, v, material_type, material_index = box_hit(obj_index, r, ray_tmin, ray_tmax)
            
            
    elif obj_type == 3:
        
        hit, t, p, front_face, normal, u, v, material_type, material_index = rotate_y_hit(obj_index, r, ray_tmin, ray_tmax)
                    
        
        
    elif obj_type == 4:
        
        hit, t, p, front_face, normal, u, v, material_type, material_index = translate_hit(obj_index, r, ray_tmin, ray_tmax)
    
            
    return (hit, t, p, front_face, normal, u, v, material_type, material_index)
        
        
        
        
        
        
        
        
  
    