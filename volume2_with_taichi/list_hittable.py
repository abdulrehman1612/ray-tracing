#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 02:27:30 2026

@author: AGU
"""

class list_hittable:
    def __init__(self):
        self.objects = []
        
    def add(self, obj):
        self.objects.append(obj)