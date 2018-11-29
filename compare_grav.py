#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 12:00:02 2018

@author: mitch
"""

import pandas as pd
import numpy as np

G1 = pd.read_csv('/home/mitch/Gravity/Potential_Fields/blkft_grav.dat', sep=' ', header=0)
G2 = pd.read_csv('/home/mitch/Gravity/Potential_Fields/blkft_utep_reprocessed.dat', sep=' ', header=0)

x_usf=[]
y_usf=[]
x_utep=[]
y_utep=[]
distance=[]
g_usf=[]
g_utep=[]
g_diff=[]

tolerance = float(50) # meters

for N, E, BA in zip(G1.Northing, G1.Easting, G1.BAB):
    for N2, E2, BA2 in zip(G2.Northing, G2.Easting, G2.Boug_An):
        N_diff = np.abs(N-N2)
        E_diff = np.abs(E-E2)
        dist = (N_diff**2 + E_diff**2)**0.5
        if dist <= tolerance:
            x_usf.append(E)
            y_usf.append(N)
            x_utep.append(E2)
            y_utep.append(N2)
            g_usf.append(BA)
            g_utep.append(BA2)
            distance.append(dist)
            tmp = BA2 - BA
            g_diff.append(tmp)
            
sum = 0
for elm in g_diff:
    sum = sum + elm
    
avg_diff = sum/len(g_diff)

