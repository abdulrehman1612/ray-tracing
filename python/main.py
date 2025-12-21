
from rtimports import *

world = list_hittable()

obj = sphere(point3(0,-0.15,-1), 0.5, color(0.5,0.4,0.3))
world.add(obj)

obj = sphere(point3(0,-101,-1.5), 100, color(0.196, 0.804, 0.196))
world.add(obj)


def main():
    
    aspect_ratio = 16/9
    image_width = 720
    camera_center = point3(0,0,0)
    cam1 = camera(aspect_ratio, image_width)
    cam1.render(world)

main()









             