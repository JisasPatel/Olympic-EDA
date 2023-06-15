#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 08:31:51 2023

@author: jisaspatel
"""

import pandas as pd
#data_noc = pd.read_csv('noc_regions.csv')
#/Users/jisaspatel/Desktop/DATA-S/PROJECTS/olympics
#data_athlete = pd.read_csv('athlete_events.csv')
import zipfile



def process():
    l = []
    with zipfile.ZipFile("athlete_events.csv.zip", mode="r")  as files:
        for files_list in files.namelist():
             l.append(files_list)
    x = l[0]
    data_noc = pd.read_csv('noc_regions.csv')
    data_athlete = pd.read_csv(x)
    data_athlete_summer = data_athlete[data_athlete['Season']=='Summer']
    data = data_athlete_summer.merge(data_noc,'left','NOC')
    data.drop_duplicates(inplace=True)
    medal = pd.get_dummies(data['Medal'])
    data = pd.concat([data,medal],axis=1)
    data = data.drop(['notes'],axis=1)
    return data