 
from scenes import *

def main():
    picture = scene()
    aspect_ratio = 16/9
    image_width = 1200
    cam1 = camera(aspect_ratio, image_width, samples_per_pixel=200, lookfrom = point3(13,2,3), lookat= point3(0,0,0), defocus_angle = 0.6, focus_distance  = 10, zoom = 7, max_depth=20)
    cam1.render_multicore(picture, processes=12, tasks=2000)
main()
