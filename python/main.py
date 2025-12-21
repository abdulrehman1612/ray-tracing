
from scenes import *

def main():
    picture = scene()
    aspect_ratio = 16/9
    image_width = 720
    camera_center = point3(0,0,0)
    cam1 = camera(aspect_ratio, image_width)
    cam1.render(picture)

main()









             