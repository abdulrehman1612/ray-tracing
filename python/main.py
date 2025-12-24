 
from scenes import *

def main():
    picture = scene()
    aspect_ratio = 16/9
    image_width = 800
    cam1 = camera(aspect_ratio, image_width, samples_per_pixel=20, lookfrom = point3(13,2,3), lookat= point3(0,0,0), defocus_angle = 0.6, focus_distance  = 10, zoom = 7, max_depth=15)
    cam1.render_multicore(picture, tasks = 1200)
main()
