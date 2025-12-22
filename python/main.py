 
from scenes import *

def main():
    picture = scene()
    aspect_ratio = 16/9
    image_width = 720
    cam1 = camera(aspect_ratio, image_width,samples_per_pixel=40)
    cam1.render(picture)
main()
