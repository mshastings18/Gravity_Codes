#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 17:46:35 2018

@author: Mitchell Hastings
"""

# my functions for the main corrections done to gravity data. Terrain to come...
def theoretical_cor(lat, lat_base):
    # This is the theoretical gravity correction sometimes called the latitude correction.
    # the more north you are the higher gravity is due to decreasing centripetal acceleration and
    # decreasing radius from the center of the earth (the latter causes increase but not as much
    # as the decrease from centripetal acceleration). So stations to the north have to be reduced
    # to the base (for the northern hemisphere, it is reversed in the southern hemissphere)
    
    # necessary modules
    import numpy as np
    
    # constnats
    e = 0.0066943800229 # dimensionless
    k = 0.001931851353 # dimensionless
    ge = 978032.67715 # mGal
    
    numerator = ge*(1+k*(np.sin(lat*np.pi/180))**2) # lat is converted to radians
    denominator = (1-e*(np.sin(lat*np.pi/180))**2)**0.5 # lat is converted to radians
    gt = numerator/denominator # theoretical gravity at the latitude of the point
    
    n_base = ge*(1+k*(np.sin(lat_base*np.pi/180))**2) # lat is converted to radians
    d_base = (1-e*(np.sin(lat_base*np.pi/180))**2)**0.5 # lat is converted to radians
    gt_base = n_base/d_base # theoretical gravity at the base
    
    theoretical_correction = gt-gt_base # see help (below function definition) for concept
    # new_grav = grav-theoretical_correction -------- this is the line to compute the new grav reading
    
    return theoretical_correction

def atm_cor(h,h_base):
    # This is the stmospheric gravity correction 
    
    # constants
    a = 0.874
    b = 9.9e-5
    c = 3.56e-9
    h_diff = h-h_base
    
    g = a-b*h_diff+c*h_diff**2
    
    
    return g

def FAC(lat,h,h_base):
    # This is the free-air correction. It accounts for decreasing gravity with increasing height.
    # the corrections returns a negative if it is above the base station and a positive if it is 
    # below the base station, subtracting this correction gives the appropriate answer
    # eg:
    #     grav - FAC = new_grav  if FAC is neg the gravity increases (closer to the center of earth)
    #                            if FAC is pos the gravity decreases (further from center of earth)
    
    # necessary modules 
    import numpy as np
    
    # constants
    a = 0.3087691 # first term
    b = 0.0004398 # second term w/o sin
    c = 7.2125e-8 # thrid term 
    
    h_diff = h-h_base # elevation difference between point and the base 
    
    free_air_cor = -(a-b*(np.sin(lat*np.pi/180))**2)*h_diff + (c*(h_diff**2))
    
    return free_air_cor

def sph_cap(lat,h,h_base,rho):
    
    # This is the spherical cap bouger correction sometimes called the Bullard A+B
    
    # necessary modules
    import numpy as np
    
    # constants (there's a lot)
    latrads = lat*np.pi/180
    G = 6.67408e-11 # gravitational constant
    requator = 6378.1e3 # radius at the equator in meters
    rpole = 6356.752e3 # radius at pole in meters
    S = 166735 # thickness of slab in meters
    h_diff = h-h_base
    
    # calculate radius at current latitude
    Rtop = ((requator**2*np.cos(latrads))**2+(rpole**2*np.sin(latrads))**2)
    Rbottom = ((requator*np.cos(latrads))**2+(rpole*np.sin(latrads))**2)
    R = (Rtop/Rbottom)**0.5
    
    # terms made by constants
    alpha = S/R 
    ada = h_diff/(R+h_diff)
    delta = R/(R+h_diff)
    n = 2*(np.sin((alpha/2)*(np.pi/180))-(np.sin((alpha/2)*(np.pi/180))**2))
    m = -3*(np.sin(alpha*np.pi/180)**2)*np.cos(alpha*np.pi/180)
    p = -6*(np.cos(alpha*np.pi/180)**2)*np.sin((alpha/2)*(np.pi/180)) + 4*np.sin((alpha/2)*(np.pi/180))**3
    k = np.sin(alpha*np.pi/180)**2
    f = np.cos(alpha*np.pi/180)
    d = (3*np.cos(alpha*np.pi/180)**2) - 2
    
    mu = (1/3)*ada**2 - ada
    
    term1 = d+f*delta+delta**2
    term2 = ((f-delta)**2+k)**0.5
    term3 = f-delta+term2
    l = (1/3)*(term1*term2+p+m*np.log(n/term3))
    
    # calculate correction
    g = (2*np.pi*G*rho*((1+mu)*h_diff-l*(R+h_diff)))*1e5 # 10e5 converts to mGals
    
    
    return g


# Define the input and output files

# testing functions
infile='/home/mitch/Gravity/Potential_Fields/blkft_utep.utm'
outfile = '/home/mitch/Gravity/Potential_Fields/blkft_utep_reprocessed.dat'

f = open(infile, 'r')
f_new = open(outfile, 'w')
## 

#base station values
lat_base = 42.65466600 
h_base = 1741.132 # meters
cor_grav_base = 3208.897 # mGals

while True:
    # read a line at a time, do the corrections, and write to the new file \
    # read in the line and assign variables to values
    line = f.readline().strip()
    if line == '':
        print('break')
        break
    raw = line.split(' ')
    long = float(raw[0])
    lat = float(raw[1])
    utm_x = float(raw[2])
    utm_y = float(raw[3])
    elev = float(raw[5])
    grav = float(raw[4])
    
    # corrections
    tc = theoretical_cor(lat,lat_base)
    atm = atm_cor(elev,h_base)
    fc = FAC(lat,elev,h_base)
    bab = sph_cap(lat,elev,h_base,2670)
    
    # corrected gravity reading
    new_grav = grav-tc-fc+atm-bab
    bouger_anomaly = new_grav-cor_grav_base
    f_new.write("%f %f %f %f %f %f %f %f %f %f %f %f" % (long,lat,utm_x,utm_y,elev,grav,tc,atm,fc,bab,new_grav,bouger_anomaly))
    f_new.write("\n")
    
