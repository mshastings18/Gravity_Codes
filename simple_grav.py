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

    # modules
    import numpy as np
    
    # Constants
    pi = np.pi
    G = 6.67408e-11 # Gravitational Constant [m^3/kg s^2]
    
    # Consolidate terms
    term1 = (4*pi*G*RHO_C*(RADIUS**3))/3
    
    gz = []
    for i in XVECTOR:
        grav = term1*(DEPTH/((i**2)+(DEPTH**2))**(3/2))
        grav = grav/1e5 # convert from m/s^2 to mGals
        gz.append(grav)

    return gz


