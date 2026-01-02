 
from scenes import *

def main():
    picture = scene()
    aspect_ratio = 16/9
    image_width = 1280
    cam = camera(aspect_ratio, image_width, samples_per_pixel=1000, lookfrom = point3(13,2,3), lookat= point3(0,0,0), defocus_angle = 0.6, focus_distance  = 10, zoom = 7, max_depth=50, background_color=color(0.5, 0.7, 1.0))
    cam.render_multicore(picture, processes=12, tasks=3000)
    #cam.render(picture)
    show_image()

def main3():
    picture = scene3()
    aspect_ratio = 1
    image_width = 200
    cam = camera(aspect_ratio, image_width, samples_per_pixel=50, lookfrom =point3(278, 278, -800),lookat= point3(278, 278, 0),defocus_angle = 0, focus_distance  = 10, zoom = 5, max_depth=50, background_color=color(0, 0, 0))
    cam.render_multicore(picture, processes=12, tasks=200)
    #cam.render(picture)
    show_image()

def final_main():
    picture = final_scene()
    aspect_ratio = 1
    image_width = 200
    cam = camera(aspect_ratio, image_width, samples_per_pixel=200, lookfrom =point3(478, 278, -600),lookat = point3(278, 278, 0),defocus_angle = 0, focus_distance  = 10, zoom = 5, max_depth=50, background_color=color(0, 0, 0))
    cam.render_multicore(picture, processes=12, tasks=1000)
    #cam.render(picture)
    show_image()
    
final_main()