# -*- coding: utf-8 -*-
"""
Created on Fri Nov 14 20:22:39 2025

@author: rehma
"""
from rtimports import *
from color import get_color, write_color, ray_color
from random import random
import time
import math

class camera:
    def __init__(self, aspect_ratio, image_width, lookfrom:point3 = point3(0,0,0), lookat:point3 = point3(0,0,-1), zoom: float = 1.0 , rotate_camera: int = 0, clockwise = True, ray_tmin = 0.001, ray_tmax = float('inf'), samples_per_pixel:int=5, saturation:float = 1, max_depth:int = 10):
        self.image_width = image_width
        self.image_height = int(self.image_width / aspect_ratio)
        self.camera_center = lookfrom
        self.lookat = lookat
        focal_length = (self.camera_center - self.lookat).length()
        vfov = 90
        angle = math.radians(rotate_camera)
        if clockwise:
            angle = -angle
        vup = point3(math.sin(angle), math.cos(angle),0)
        
        
        theta = math.radians(vfov)
        h = math.tan(theta/2)
        port_height = 2 * h * focal_length
        port_width = port_height * (self.image_width / self.image_height)
        
        w = unit_vector(lookfrom - lookat)
        u = unit_vector(cross(vup, w))
        v = cross(w, u)
        

        port_u = port_width * u
        port_v = port_height * -v
        self.pixel_u = port_u / self.image_width
        self.pixel_v = port_v / self.image_height
        port_upperleft = self.camera_center - (zoom* focal_length * w) - port_u/2 - port_v/2
        self.pixel00_loc = port_upperleft + 0.5*(self.pixel_u + self.pixel_v)
        
        self.ray_tmin = ray_tmin
        self.ray_tmax = ray_tmax
        self.samples_per_pixel = samples_per_pixel
        self.saturation = saturation
        self.max_depth = max_depth
        
        
        
        
    def render(self, world, out_file = "image.ppm"):
        start_time = time.time()
        with open(out_file, "w") as file:
             
             file.write(f"P3\n{self.image_width} {self.image_height}\n255\n")
             
             for j in range(self.image_height):
                 for i in range(self.image_width):
                    current_color = color(0,0,0)
                    for n in range(self.samples_per_pixel):
                        pixel_center = self.pixel00_loc + (i+random()-0.5)* self.pixel_u + (j+random()-0.5) * self.pixel_v
                        ray_direction = pixel_center - self.camera_center
                        r = ray(self.camera_center, ray_direction)
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

        


