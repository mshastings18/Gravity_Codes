#!/usr/bin/env python3
# Based on xcess_mass.pl by Dr. Connor. Calculate the excess mass from a gravity
# anomaly. 

# Author: Mitchell Hastings

############################################# SCAFFOLD #############################################
## have the functions call each other
## make gmtinterp(datafile) have arguments for grid spacing and region
## add option to write latlon2UTM output to a file 
## write a better code description


####################################################################################################


def gmtinterp(datafile):
    # GMTINERP(datafile) calls gmt blockmean, gmt surface, and gmt grd2xyz to 
    # create an interpolated surface of the datafile given
    
    # SCAFFOLD: build so that the region and grid spacing are part of the function
    
    # modules
    from subprocess import call
    
    # these lines call gmt to do a block average smooth curve interpolation of the data then
    # convert it to an xyz grid
    call("gmt blockmean %s -I0.001 -R-121.7/-121.5/41.55/41.65 > surf.in" %(datafile), shell = True)
    call("gmt surface surf.in -I0.001 -R-121.7/-121.5/41.55/41.65 -Gsurf.grd", shell = True)
    call("gmt grd2xyz surf.grd > surf.xyz", shell = True)
    
def latlon2UTM(xyzgrd,UTMZONE):
    # LATLON2UTM(xyzgrd, UTMZONE) converts lat long coordinates into utm 
    # coordinates. the xyzgrd format should be tab delimited and should be 
    # long, lat, z-value. the function returns utmx, utmy, and z-values at each
    # value. Currently the if -statement restricting the lat long is for use in
    # the project, however, I may change this later to be more versitile. 
    
    # modules
    # import pyproj to use commands from Proj4
    from pyproj import Proj,transform
    
    # open file for reading
    infile = xyzgrd
    f = open(infile,'r')
    
    # Define the projections
    inProj = Proj(init='epsg:4326')    # WGS84 lat/long
    outProj = Proj(proj='utm', zone=UTMZONE, ellps='WGS84')       # input UTMZONE
    
    # initialize arrays for utm coordinates
    utmx = []
    utmy = []
    grav = []
    
    # Convert inProj to outProj
    while True:
        line = f.readline().strip()
        if line == '':
            print('break')
            break
        raw = line.split('\t')
        long = float(raw[0])    # Longitude
        lat = float(raw[1])     # Latitude
        z = float(raw[2])       # Gravity, but can be other types of z-values
        if (-121.625 <= long <= -121.550 and 41.575 <= lat <= 41.620): # restrict lat/long
            utm_x, utm_y = transform(inProj, outProj, long,lat)
            utmx.append(utm_x)
            utmy.append(utm_y)
            grav.append(z)
        
    # return the arrays
    return utmx, utmy, grav

def xcessmass_calc(grav, background_grav, utmx):
    # Maths to do the excess mass calculation, returns the excess mass of the anomaly you 
    # separated
    
    # modules 
    import numpy as np
    
    # sum all of the elements in gravity after reduction for background gravity
    grav_sum = 0
    for gravity in grav:
        reduced_grav = gravity - background_grav
        grav_sum = grav_sum + reduced_grav
    
    # Convert mGals to m/s^2 for calculations
    grav_sum = grav_sum/1e5
    
    # constants 
    G = 6.674e-11# gravitational constant [m^3][kg^-1][s^-2]
    pi = np.pi # pi (3.14159...)

    # use the x-array from latlon2UTM to get the x and y spacing (its the same so just use one array)
    deltax = utmx[2]-utmx[1] # x grid spacing
    deltay = deltax # y grid spacing
    
    # excess mass calculation
    term1 = 1/(2*pi*G) # consolidating terms

    xcess = term1*grav_sum*deltax*deltay # calculation for excess mass 
    
    return xcess
    
def xcess_mass(datafile, UTMZONE, background_grav):
    # Description
    
    # Do the interpolation with gmt's blockmean and surface to generate the grid file 'surf.xyz'
    gmtinterp(datafile)
    
    # extract the anomaly and convert to utm
    utmx, utmy, grav = latlon2UTM('surf.xyz', UTMZONE)
    
    # Do the excess mass calculation 
    excess_mass = xcessmass_calc(grav, background_grav,utmx)
    
    print('Excess Mass: ', excess_mass,' kg')
    
    return excess_mass


# Test line
excess_mass = xcess_mass('MLgrav.dat', 10, -148) 