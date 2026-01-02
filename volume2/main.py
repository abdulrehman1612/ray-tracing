 
from scenes import *

def week1_final():
    picture = week1_final_scene()
    aspect_ratio = 16/9
    image_width = 800
    cam = camera(aspect_ratio, image_width, samples_per_pixel=1000, lookfrom = point3(13,2,3), lookat= point3(0,0,0), defocus_angle = 0.6, focus_distance  = 10, zoom = 7, max_depth=50, background_color=color(0.5, 0.7, 1.0))
    cam.render_multicore(picture, processes=12, tasks=2000, out_file="week1_final.ppm")
    #cam.render(picture,out_file="week1_final.ppm")
    show_image()

def cornel_box():
    picture = cornel_box_scene()
    aspect_ratio = 1
    image_width = 800
    cam = camera(aspect_ratio, image_width, samples_per_pixel=1000, lookfrom =point3(278, 278, -800),lookat= point3(278, 278, 0),defocus_angle = 0, focus_distance  = 10, zoom = 5, max_depth=50, background_color=color(0, 0, 0))
    cam.render_multicore(picture, processes=12, tasks=3000,out_file="cornel_box.ppm")
    #cam.render(picture,out_file="week1_final.ppm")
    show_image()

def week2_final():
    picture = week2_final_scene()
    aspect_ratio = 1
    image_width = 800
    cam = camera(aspect_ratio, image_width, samples_per_pixel=5000, lookfrom =point3(478, 278, -600),lookat = point3(278, 278, 0),defocus_angle = 0, focus_distance  = 10, zoom = 5, max_depth=50, background_color=color(0, 0, 0))
    cam.render_multicore(picture, processes=12, tasks=5000,out_file="week2_final.ppm")
    #cam.render(picture,out_file="week1_final.ppm")
    show_image()
  
    
week1_final()
cornel_box()
week2_final()