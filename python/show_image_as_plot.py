#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 25 22:53:46 2025

@author: AGU
"""

import matplotlib.pyplot as plt
def show_image():
    img = plt.imread("image.ppm")
    plt.figure(figsize=(20,20))
    plt.imshow(img)
    plt.axis("off")
    plt.tight_layout()
    plt.show()

