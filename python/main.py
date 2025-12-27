 
from scenes import *

def main():
    picture = scene()
    aspect_ratio = 16/9
    image_width = 400
    cam = camera(aspect_ratio, image_width, samples_per_pixel=25, lookfrom = point3(13,2,3), lookat= point3(0,0,0), defocus_angle = 0.6, focus_distance  = 10, zoom = 7, max_depth=15)
    cam.render_multicore(picture, processes=12, tasks=1200)
    #cam.render(picture)
    show_image()

def main3():
    picture = scene3()
    aspect_ratio = 16/9
    image_width = 400
    cam = camera(aspect_ratio, image_width, samples_per_pixel=25, lookfrom =  point3(13,2,3), lookat= point3(0,0,0),defocus_angle = 0.6, focus_distance  = 10, zoom = 7, max_depth=15)
    cam.render_multicore(picture, processes=12, tasks=1200)
    #cam.render(picture)
    show_image()

main3()