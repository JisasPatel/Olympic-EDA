#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 22:23:32 2023

@author: jisaspatel
"""

import zipfile

l = []
with zipfile.ZipFile("athlete_events.csv.zip", mode="r")  as files:
    for files_list in files.namelist():
         l.append(files_list)
print(l)