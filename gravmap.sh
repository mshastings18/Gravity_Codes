#!/bin/sh
# this line tells the os that it is receiving a bash script

################ DEFINE VARIABLES, CHANGE GLOBAL DEFAULTS, CREATE COLOR PALETTE
PROJ="-JM6i"
LIMS="-R-121.7/-121.5/41.55/41.65"
PSFILE="Medicine_Lake.ps"
GRID="-I0.001"

# set the map border to plain (default is "fancy" and looks outdated) and set axes to
# decimal degrees instead of degrees minutes seconds
gmt set FORMAT_GEO_MAP ddd.xx
gmt set MAP_FRAME_TYPE plain

# make the color palette, once it is created you can comment out the command
# because you don't need to keep remaking it, I have 2 because I was playing with different cpts

# using gmtinfo for full dataset: LIMS = -123/-121/41/43
#gmt makecpt -Chaxby -T-180/-55/1 -Z -V > grav2.cpt
# making based on visual inspection of gravity data for LIMS: = -122.3/-121/41/43
#gmt makecpt -Chaxby -T-180/-90/1 -Z -V > grav3.cpt
# zoom in on medicine lake for possible intrusion LIMS = -122/-121.25/41.25/41.8
gmt makecpt -Chaxby -T-160/-135/1 -Z -V > grav4.cpt
# defining the color palette as a variable because I am a lazy programmer
CPT="grav4.cpt"

################## CREATE THE GRID

# awk is a powerful UNIX tool that allows you to manipulate data files
# the -F"," tells it that the file you are piping the command to is a csv
# the '{print $1, $2, $3}' tells it to only use columns 1, 2, and 3 as the
# input for gmt blockmean. 
# reading this line in english reads:
# awk print columns 1, 2, and 3 from pot_field_data.dat and pipe into gmt blockmean
awk -F"," '{print $1, $2, $3}' pot_field_data.dat |\
	gmt blockmean $GRID $LIMS -V > surf.in
# gmt surface is used with blockmean to create the interpolation from your data
# and create a NetCDF file
gmt surface surf.in $GRID $LIMS -Gsurf.grd -V

################### PLOTTING

# plots the NetCDF over the projection
gmt grdimage surf.grd $PROJ -C$CPT -K -n+c -V > $PSFILE

# creates teh contours from the grid file
gmt grdcontour surf.grd $PROJ $LIMS -L-185/-55 -A- -C$CPT -Wthinnest,50 -K -V -O >> $PSFILE

# plots the locations of vents (this isn't important to our maping area so ignore this line
#gmt psxy bfv_loc_latlon.dat $PROJ $LIMS -St0.25 -Gblack  -W0.5p,black -K -V -O >> $PSFILE

# awk! 
# this time I'm taking the xyz data that we used to make the interpolation
# and piping it into a gmt command to plot them as colored points
# I did this to check our interpolation to make sure there aren't large
# gaps in our data and that the interpolation is reasonable. 
# (I could hear Rocco's voice in my head telling me to check the constraints on our
# interpolation)
awk -F"," '{print $1, $2, $3}' pot_field_data.dat  |\
	gmt psxy $PROJ $LIMS -Sc0.1 -C$CPT -W0.25p,black -K -V -O >> $PSFILE

# plot a triangle for the approximate location of the Medicine Lake volcano
gmt psxy $PROJ $LIMS -St0.3 -Gblack -W0.5p,black -K -V -O >> $PSFILE << EOF
-121.553 41.611 
EOF

# creates the underlying basemap
gmt psbasemap $PROJ $LIMS -Ba0.05WeSn -K -O >> $PSFILE

# creates the scale
gmt psscale -Dx6.5i/2.25i/3.5i/0.2i -Ba5+l"Bouger Anomaly (mGals)" -C$CPT -O >> $PSFILE

#################### CONVERT FILE AND VIEW PRODUCT

# converts your postscript file to a pdf so you can view it instead of looking at 
# printer language
ps2pdf $PSFILE

