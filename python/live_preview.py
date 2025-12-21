# -*- coding: utf-8 -*-
"""
Created on Sat Dec 20 02:38:10 2025

@author: rehma
"""

#!/usr/bin/env python3
"""Fast PPM viewer with auto-reload using Pillow + tkinter."""

import argparse
import os
import tkinter as tk
from PIL import Image, ImageTk

parser = argparse.ArgumentParser(description='Watch a PPM file and display it.')
parser.add_argument('--input', default='image.ppm', help='Path to the PPM file')
parser.add_argument('--max-width', type=int, help='Maximum display width')
parser.add_argument('--interval', type=int, default=500, help='Refresh interval in ms')
args = parser.parse_args()

class Viewer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f"PPM Viewer: {args.input}")
        self.label = tk.Label(self.root)
        self.label.pack()
        self.last_mtime = 0
        self.refresh()
    
    def refresh(self):
        try:
            mtime = os.path.getmtime(args.input)
            if mtime != self.last_mtime:
                self.last_mtime = mtime
                img = Image.open(args.input)
                
                if args.max_width and img.width > args.max_width:
                    ratio = args.max_width / img.width
                    new_size = (args.max_width, int(img.height * ratio))
                    img = img.resize(new_size, Image.NEAREST)
                
                photo = ImageTk.PhotoImage(img)
                self.label.configure(image=photo)
                self.label.image = photo
        except Exception as e:
            print(f"Error: {e}")
        
        self.root.after(args.interval, self.refresh)
    
    def run(self):
        self.root.mainloop()

Viewer().run()