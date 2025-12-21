# -*- coding: utf-8 -*-
"""
Created on Fri Nov 14 20:22:39 2025

@author: rehma
"""
from rtimports import *
from color import get_color, write_color
class camera:
    def __init__(self, aspect_ratio, image_width, camera_center:point3 = point3(0,0,0), port_height:float=2, focal_length: float = 1.0, ray_tmin = 0, ray_tmax = 10):
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
        
    def render(self, world, out_file = "image.ppm"):
        with open(out_file, "w") as file:
             
             file.write(f"P3\n{self.image_width} {self.image_height}\n255\n")
             
             for j in range(self.image_height):
                 for i in range(self.image_width):
                    pixel_center = self.pixel00_loc + i * self.pixel_u + j * self.pixel_v
                    ray_direction = pixel_center - self.camera_center
                    r = ray(self.camera_center, ray_direction)
                    pixel_color = get_color(world, r, self.ray_tmin, self.ray_tmax)
                    write_color(file, pixel_color)
                 if j%4 == 0:   
                    print(f"Progress: {round((j/self.image_height) *100,2)} %")
        print("Progress: Complete")

        


