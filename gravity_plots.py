#!/usr/bin/env python3
# python code to plot a gravity anomaly using the functions form simple_grav module 

# Author: Mitchell Hastings

import matplotlib.pyplot as plt

'''# Section for plotting a buried sphere for Dr. Connor's homework 4

from simple_grav impot buried_sphere

x = list(range(-100,100,1)) # position range [m]
mass_xpos = 0 # x position of the mass anomaly [m]
rho_c = -2200 # density contrast between fractured volcanics and air [kg/m^3]
depth = 21 # [m]
radius = 14 # [m]
bottom = 35 # cave floor
gz = buried_sphere(x,rho_c,depth,radius)

# Ploting portion
plt.figure()

plt.subplot(2,1,1)
plt.plot(x,gz, 'r')
plt.ylabel('Gravity Anomaly (mGals)')
plt.title('Gravity Anomaly of a Tunnel')

plt.subplot(2,1,2)
plt.scatter(mass_xpos,depth, facecolors='none', edgecolors='r', s=9000)
plt.axis([1.1*min(x), 1.1*max(x), 0, bottom])
plt.gca().invert_yaxis()
plt.xlabel('Distance (m)')
plt.ylabel('Depth (m)')
plt.text(15, 5, 'Density Contrast = -2200 kg/m^3', fontsize=9)
''' # Section for plotting mulitple finite slabs for Dr. Connor's homework 4

import numpy as np
from simple_grav import finite_slab2

x = np.arange(-100000,100000,500) # profile over 200 km
rhoc_mantle = 600 # kg/m^3
rhoc_water = -1700 # kg/m^3
Hm_con = 1000 # thickness of mantle under continental crust (m)
Hw_marg = 1000 # thickness of water column in passive margin (m)
Hm_marg = 21000 # thickness of mantle under passive margin (m)
zw = 1 # depth to the top of the water (m)
zmc = 35000 # depth to the top of the mantle under continental crust (m)
zmm = 15000 # depth to the top of the mantle under passive margin (m)

# edges of the slabs
pos_mantlec = [-100000,0]
pos_mantlepm = [0,100000]
pos_water = [0,100000]

# Gravity anomaly calculations
gz_mantlec = finite_slab2(x,pos_mantlec,rhoc_mantle,Hm_con,zmc)
gz_mantlepm = finite_slab2(x,pos_mantlepm,rhoc_mantle,Hm_marg,zmm)
gz_water = finite_slab2(x,pos_water,rhoc_water,Hw_marg, zw)

# initialize list for summation
gz = []

# loop to sum
for i in range(0,len(x)):
    tmp = gz_mantlec[i] + gz_mantlepm[i] + gz_water[i]
    gz.append(tmp)
    
plt.figure()
plt.plot(x,gz)

plt.figure()
plt.plot(x,gz_mantlec,x,gz_mantlepm,x,gz_water)
plt.legend()
