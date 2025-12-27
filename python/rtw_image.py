#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 01:13:58 2025

@author: AGU
"""

from PIL import Image
import os
import numpy as np

class rtw_image:
    def __init__(self, filename:str = None):
        self.image = None
        self.width = 0
        self.height = 0
        self.pixels = None
        
        if filename:
            self.load(filename)
    
    def load(self, filename):
        search_paths = ["",
                        "images/",
                        "../images/",
                        "../../images/",
                        "../../../images/",
                        "../../../../images/",
                        "../../../../../images/"]
        
        env_dir = os.getenv("RTW_IMAGES")
        if env_dir:
            search_paths.insert(0, env_dir + "/")
        
        for path in search_paths:
            try:
                full_path = path + filename
                img = Image.open(full_path).convert("RGB")
                self.image = img
                self.width, self.height = img.size
                self.pixels = np.array(img)
                return True
            except Exception:
                pass

        print(f"ERROR: Could not load image file '{filename}'")
        return False

    
    def pixel_data(self, x: int, y: int):
        if self.pixels is None:
            return (255, 0, 255)
        x = max(0, min(x, self.width - 1))
        y = max(0, min(y, self.height - 1))
        
        return self.pixels[y,x]
    
    