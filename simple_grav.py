#!/usr/bin/env python3
# A compilation of different functions to calculate gravity anomalies of different simple shapes
# Author: Mitchell Hastings

############################################# SCAFFOLD #############################################
## Add more simple geometries
## build option to use defaults if not specified
## make the x position of the object variable


####################################################################################################

def buried_sphere(XVECTOR,RHO_C,DEPTH,RADIUS):
    # function to calculate the gravity across the profile of a buried sphere in mGals.
    # this function assumes that the sphere is buried at point (0,DEPTH)
    # xvector must be in meters
    # density contrast (rho_c) must be in kg/m^3
    # depth and radius must be in meters

    # modules
    import numpy as np
    
    # Constants
    pi = np.pi
    G = 6.67408e-11 # Gravitational Constant [m^3/kg s^2]
    
    # Consolidate terms
    term1 = (4*pi*G*RHO_C*(RADIUS**3))/3
    
    # initialize array for storing gravity values
    gz = []
    
    # loop for calculating gravity values
    for i in XVECTOR:
        grav = term1*(DEPTH/((i**2)+(DEPTH**2))**(3/2))
        grav = grav*1e5 # convert from m/s^2 to mGals
        gz.append(grav)

    return gz
    
    gz = []
    
    for i in x:
        L = np.arctan(i/depth)
        R = np.arctan((length-i)/depth)
        grav = term1*(pi+L+R)
        grav = grav*1e5
        gz.append(grav)
    


def finite_slab(xvector,length,rho_c, thickness, depth):
    # Calculate the gravit anomaly for a finite slab. 
    # xvector is the x array of points at which to calculate gravity (m),length is the length of 
    # the slab (m), rho_c is the density contrast between the slab and the surrounding rock {kg/m^3)
    # thickness is the thickness of the slab (m), and depth is the depth to the top of the slab (m). 
    # The output is a list of gravity values in mGals (divide by 1e5 if you want it in m/s^2) that
    # has the same dimensions as the xvector input variable.
    # Note: finite_slab assumes the left edge of the slab is at point (0,depth) and the right edge 
    # is at (length,depth). If you want to shift the position of the slab use finite_slab2() which
    # changes the input of length to the x position of the left and right edges of the slab.
    
    # import modules
    import numpy as np 
    
    # Constants and conslidating terms
    pi = np.pi
    G = 6.67408e-11
    term1 = (2*pi*G*rho_c*thickness)
    
    # initialize the list to store gravity values
    gz = []
    
    # loop for calculating and storing gravity values
    for i in xvector:
        L = np.arctan(i/depth)
        R = np.arctan((length-i)/depth)
        grav = term1*(pi+L+R)
        grav = grav*1e5
        gz.append(grav)
    
    return gz
    
def finite_slab2(xvector, pos, rho_c, thickness, depth):
    # Calculate the gravit anomaly for a finite slab. xvector is the array of x values for which you
    # want to calculate the gravity at (m). pos is a list containing the left edge and right edge 
    # position of the slab, respectively. 
    # i.e. pos = [0, 500] means the left edge is at 0 m and the right edge is at 500 m
    # rho_c is the density contrast between the slab and the surrounding rock in kg/m^3, thickness
    # is the thickness of the slab in meters, and depth is the depth to the top of the slab (m).
    # Note: the only difference between finite_slab() and finite_slab2() is that finite_slab() 
    # assumes the position of the slab while you can specify the position of the slab with finite_slab2()
    
    # modules
    import numpy as np
    
    # Constants
    pi = np.pi
    G = 6.67408e-11 # Gravitational Constant [m^3/kg s^2]
    xL = pos[0] # left edge of the slab [m]
    xR = pos[1] # right edge of the slab [m]
    
    # Consolidate terms
    term1 = (2*pi*G*rho_c*thickness)
    
    # initialize array for storing gravity values
    gz = []
    for i in xvector:
         L = np.arctan((i-xL)/depth)
         R = np.arctan((xR-i)/depth)
         grav = term1*(pi+L+R)
         grav = grav*1e5 # convert from m/s^2 to mGals
         gz.append(grav)
    return gz
    


# Test lines
'''import numpy as np
x = np.arange(-10000,10000,10)
gz = finite_slab(x,5000,600,1000,5000)
POS = [0,5000]
gztest = finite_slab2(x,POS,600,1000,5000)

import matplotlib.pyplot as plt

plt.figure()
plt.plot(x,gztest)


plt.figure()
plt.plot(x,gz)
plt.scatter(0,gz[1000])
plt.scatter(5000,gz[1500])
'''
    
    
    
    
    
    
    