#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  8 00:33:55 2026

@author: AGU
"""

from taichi_world import init_world
import taichi as ti
from taichi_kernal_main import run_kernal, make_field_pic, set_camera
import time
import numpy as np

class camera:
    def __init__(self, aspect_ratio, image_width, lookfrom=[0,0,0], lookat=[0,0,-1], zoom: float = 1.0 , rotate_camera: int = 0,defocus_angle = 0, focus_distance = 10 , samples_per_pixel:int=5, saturation:float = 1, background_color = [0,0,0], max_depth:int = 50):
        self.image_width = image_width
        self.image_height = int(self.image_width / aspect_ratio)
        self.lookfrom = lookfrom
        self.lookat = lookat
        self.zoom = zoom
        self.rotate_camera = rotate_camera
        self.defocus_angle = defocus_angle
        self.focus_distance = focus_distance
        self.samples_per_pixel = samples_per_pixel
        self.saturation = saturation
        self.max_depth = max_depth
        self.background_color = background_color
    
    def render(self, world):
        
        ti.init(arch=ti.gpu, debug=False,kernel_profiler=False)
        
        compile_time_start = time.time()
        print()
        print("Compiling world...")
        
        init_world(world)
        
        compile_time_end = time.time()
        elapsed = int(compile_time_end - compile_time_start)
        hours = elapsed // 3600
        minutes = (elapsed % 3600) // 60
        seconds = elapsed % 60
        print()
        print(f"World compilation succesful! | Time_taken: {hours:02d}:{minutes:02d}:{seconds:02d}")
        
        image_width = self.image_width
        image_height = self.image_height
        lookfrom = ti.Vector(self.lookfrom)
        lookat = ti.Vector(self.lookat)
        zoom = self.zoom
        rotate_camera = self.rotate_camera
        defocus_angle = self.defocus_angle
        focus_distance = self.focus_distance
        samples_per_pixel = self.samples_per_pixel
        max_depth = self.max_depth
        background_color = ti.Vector(self.background_color)
        make_field_pic(self.image_width, self.image_height)
        set_camera(lookfrom, lookat)
        gui = ti.GUI("Ray Tracer", res=(self.image_width, self.image_height))
        
        import taichi_kernal_main
        start_time = time.time()
        print()
        print("Rendering image...")
        
        
        current_time = time.time()
        elapsed = int(current_time - start_time)
        hours = elapsed // 3600
        minutes = (elapsed % 3600) // 60
        seconds = elapsed % 60
        print()
        print("Rendering Complete!")
        print(f"Time_taken: {hours:02d}:{minutes:02d}:{seconds:02d}")
        from taichi_world import flag
        print(f"{flag[0]}")
        while gui.running:
            run_kernal(image_width, image_height, zoom, rotate_camera, defocus_angle, focus_distance, samples_per_pixel,max_depth, background_color)
            ti.sync()
            gui.set_image(taichi_kernal_main.image_pixels)
            camera_lookfrom = taichi_kernal_main.look_from[0].to_numpy().astype(np.float32)
            camera_lookat = taichi_kernal_main.look_at[0].to_numpy().astype(np.float32)
            forward = (camera_lookat- camera_lookfrom)
            
            forward /= np.linalg.norm(forward)
            up = np.array([0.0,1.0,0.0])
            right = np.cross(forward, up)
            right /= np.linalg.norm(right)/0.5
            step = 0.1
            for e in gui.get_events(gui.PRESS):
                if e.key == gui.ESCAPE:
                    gui.running = False
                if e.key == 'a':
                    camera_lookfrom -= right * step
                    camera_lookat   -= right * step
                    
                if e.key == 'd':
                    camera_lookfrom += right * step
                    camera_lookat   += right * step
                if e.key == 's':
                    camera_lookfrom -= forward * step
                    camera_lookat   -= forward * step
                    
                if e.key == 'w':
                    camera_lookfrom += forward * step
                    camera_lookat   += forward * step
                
                if e.key == ti.GUI.UP:
                    camera_lookat += np.array([0,step,0])/2
                if e.key == ti.GUI.DOWN:
                    camera_lookat -= np.array([0,step,0])/2
                if e.key == ti.GUI.LEFT:
                    camera_lookat   -= (right * step)*2
                if e.key == ti.GUI.RIGHT:
                    camera_lookat   += (right * step)*2
                    
                    
                    
            taichi_kernal_main.look_from[0][0] = camera_lookfrom[0]
            taichi_kernal_main.look_from[0][1] = camera_lookfrom[1]
            taichi_kernal_main.look_from[0][2] = camera_lookfrom[2]
            taichi_kernal_main.look_at[0][0] = camera_lookat[0]
            taichi_kernal_main.look_at[0][1] = camera_lookat[1]
            taichi_kernal_main.look_at[0][2] = camera_lookat[2]
            gui.show()
            
            
        