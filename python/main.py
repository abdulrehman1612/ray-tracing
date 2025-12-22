 
from scenes import *

def main():
    picture = scene()
    aspect_ratio = 16/9
    image_width = 500
    cam1 = camera(aspect_ratio, image_width,samples_per_pixel=50)
    cam1.render(picture)
main()
