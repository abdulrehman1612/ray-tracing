#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 30 07:57:35 2025

@author: AGU
"""

from hittable import hittable

class list_hittable:
    def __init__(self):
        self.objects = []
    
    def add(self,obj):
        if isinstance(obj, hittable):
            self.objects.append(obj)
        else:
            raise ValueError("Object not Identifiable")