# -*- coding: utf-8 -*-
"""
Created on Fri Nov 14 20:22:39 2025

@author: rehma
"""
from rtimports import *
from color import get_color, write_color, ray_color
from random import random

class camera:
    def __init__(self, aspect_ratio, image_width, camera_center:point3 = point3(0,0,0), port_height:float=2, focal_length: float = 1, ray_tmin = 0.01, ray_tmax = float('inf'), samples_per_pixel:int=5, saturation:float = 1, max_depth:int = 50, gamma:int = 0.5):
        self.image_width = image_width
        self.image_height = int(self.image_width / aspect_ratio)
        port_width = port_height * (self.image_width / self.image_height)
        self.camera_center = camera_center
        port_u = vec3(port_width, 0, 0)
        port_v = vec3(0, -port_height, 0)
        self.pixel_u = port_u / self.image_width
        self.pixel_v = port_v / self.image_height
        port_upperleft = self.camera_center - vec3(0,0,focal_length) - port_u/2 - port_v/2
        self.pixel00_loc = port_upperleft + 0.5*(self.pixel_u + self.pixel_v)
        self.ray_tmin = ray_tmin
        self.ray_tmax = ray_tmax
        self.samples_per_pixel = samples_per_pixel
        self.saturation = saturation
        self.max_depth = max_depth
        self.gamma = gamma
        
    def render(self, world, out_file = "image.ppm"):
        with open(out_file, "w") as file:
             
             file.write(f"P3\n{self.image_width} {self.image_height}\n255\n")
             
             for j in range(self.image_height):
                 for i in range(self.image_width):
                    current_color = color(0,0,0)
                    for n in range(self.samples_per_pixel):
                        pixel_center = self.pixel00_loc + (i+random()-0.5)* self.pixel_u + (j+random()-0.5) * self.pixel_v
                        ray_direction = pixel_center - self.camera_center
                        r = ray(self.camera_center, ray_direction)
                        pixel_color = ray_color(r,self.max_depth,world,self.gamma)
                        current_color += pixel_color
                    
                    current_color /= self.samples_per_pixel
                    current_color = current_color**self.saturation
                    write_color(file, current_color)
                 if j%4 == 0:   
                    print(f"Progress: {round((j/self.image_height) *100,2)} %")
        print("Progress: Complete")

        


