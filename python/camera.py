# -*- coding: utf-8 -*-
"""
Created on Fri Nov 14 20:22:39 2025

@author: rehma
"""
from rtimports import *
from color import *
from random import random
import time
import math
from multiprocessing import Pool
from multiprocesses_output import multiprocess






class camera:
    def __init__(self, aspect_ratio, image_width, lookfrom:point3 = point3(0,0,0), lookat:point3 = point3(0,0,-1), zoom: float = 1.0 , rotate_camera: int = 0,defocus_angle = 0, focus_distance = 10 ,ray_tmin = 0.001, ray_tmax = float('inf'), samples_per_pixel:int=5, saturation:float = 1, max_depth:int = 10):
        self.image_width = image_width
        self.image_height = int(self.image_width / aspect_ratio)
        self.camera_center = lookfrom
        self.lookat = lookat
        vfov = 90-(zoom*10)
        angle = -math.radians(rotate_camera)
        vup = point3(math.sin(angle), math.cos(angle),0)
        theta = math.radians(vfov)
        h = math.tan(theta/2)
        port_height = 2 * h * focus_distance
        port_width = port_height * (self.image_width / self.image_height) 
        w = unit_vector(lookfrom - lookat)
        u = unit_vector(cross(vup, w))
        v = cross(w, u)
        self.defocus_angle = defocus_angle
        port_u = port_width * u
        port_v = port_height * -v
        self.pixel_u = port_u / self.image_width
        self.pixel_v = port_v / self.image_height
        port_upperleft = self.camera_center - (focus_distance * w) - port_u/2 - port_v/2
        self.pixel00_loc = port_upperleft + 0.5*(self.pixel_u + self.pixel_v)      
        defocus_radius = focus_distance * math.tan(math.radians(self.defocus_angle/2))
        self.defocus_disk_u = u * defocus_radius
        self.defocus_disk_v = v * defocus_radius        
        self.ray_tmin = ray_tmin
        self.ray_tmax = ray_tmax
        self.samples_per_pixel = samples_per_pixel
        self.saturation = saturation
        self.max_depth = max_depth    
        
    def render(self, world, out_file = "image.ppm"):
        start_time = time.time()
        print()
        print("Rendering...")
        print()
        with open(out_file, "w") as file:          
             file.write(f"P3\n{self.image_width} {self.image_height}\n255\n")            
             for j in range(self.image_height):
                 for i in range(self.image_width):
                    current_color = color(0,0,0)
                    for n in range(self.samples_per_pixel):
                        pixel_center = self.pixel00_loc + (i+random()-0.5)* self.pixel_u + (j+random()-0.5) * self.pixel_v
                        ray_origin = self.camera_center if (self.defocus_angle <= 0) else random_disk_sample(self.camera_center, self.defocus_disk_u, self.defocus_disk_v)
                        ray_direction = pixel_center - ray_origin
                        r = ray(ray_origin, ray_direction)
                        pixel_color = ray_color(r,self.ray_tmin, self.ray_tmax, world, self.max_depth)
                        current_color += pixel_color
                    current_color /= self.samples_per_pixel
                    current_color = current_color**self.saturation
                    write_color(file, current_color)
                 if j%4 == 0:
                     current_time = time.time()
                     elapsed = int(current_time - start_time)
                     hours = elapsed // 3600
                     minutes = (elapsed % 3600) // 60
                     seconds = elapsed % 60
                     print(f"Elapsed_time: {hours:02d}:{minutes:02d}:{seconds:02d} | Progress: {round((j/self.image_height) *100,2)} %")
                     print()
        end_time = time.time()
        elapsed = int(end_time - start_time)
        hours = elapsed // 3600
        minutes = (elapsed % 3600) // 60
        seconds = elapsed % 60
        print("Progress: Complete")
        print(f"Time taken: {hours:02d}:{minutes:02d}:{seconds:02d}")

        
    def render_multicore(self,world,out_file = "image.ppm", processes=50):
        start_time = time.time()
        list_input = []
        for process in range(processes):
            list_input.append((world, self.image_height, self.image_width, self.samples_per_pixel, self.max_depth,self.camera_center, self.defocus_angle, self.defocus_disk_v,self.defocus_disk_u, self.pixel_u, self.pixel_v, self.ray_tmin, self.ray_tmax, self.pixel00_loc,self.saturation , process/processes, processes))
        with Pool(processes) as p:
            out_list = p.map(multiprocess, list_input)
        with open(out_file, "w") as file:  
             file.write(f"P3\n{self.image_width} {self.image_height}\n255\n")
             file.write(" ".join(out_list))
        end_time = time.time()
        elapsed = int(end_time - start_time)
        hours = elapsed // 3600
        minutes = (elapsed % 3600) // 60
        seconds = elapsed % 60
        print("Progress: Complete")
        print(f"Time taken: {hours:02d}:{minutes:02d}:{seconds:02d}")