#!/bin/bash

# ---- Get useful extra functions
source ../gmt_extras.sh

# ---- Set defaults
gmt_extras::set_gmt_defaults

# ---- Define some functions

plot_catch () {
  
  # Define input file
  to_plot=./Planform_Data/${catch}.gmt
  
  # Get min/max lat/lon and define region
  y1=$(awk ' $1!=">" {print $2}' $to_plot | gmt gmtinfo -C | awk '{print $1}')
  y2=$(awk ' $1!=">" {print $2}' $to_plot | gmt gmtinfo -C | awk '{print $2}')
  x1=$(awk ' $1!=">" {print $1}' $to_plot | gmt gmtinfo -C | awk '{print $1}')
  x2=$(awk ' $1!=">" {print $1}' $to_plot | gmt gmtinfo -C | awk '{print $2}')
  rgn=-R$x1/$x2/$y1/$y2
  
  # Define projection
  proj=-Jm0.48i
  
  # Plot streams
  gmt psxy $to_plot $rgn $proj -O -K >> $out.ps
  
  # Plot label
  echo $xlab $ylab $lab | \
    gmt pstext $rgn $proj -F+f8p,Helvetica-Bold,$col -N -O -K >> $out.ps

}

plot_scl () {

    # Derive second two y-levels from input
    y2=$(echo $y1 | awk ' { print $1+0.05 } ')
    y3=$(echo $y1 | awk ' { print $1+0.1 } ')
    
    # Project eastwards from input x/y to get x-levels
    x10=$(gmt project -C$x1/$y1 -A90 -L0/10 -G1 -Q | tail -n1 | awk '{print $1}')
    x25=$(gmt project -C$x1/$y1 -A90 -L0/25 -G1 -Q | tail -n1 | awk '{print $1}')
    x50=$(gmt project -C$x1/$y1 -A90 -L0/50 -G1 -Q | tail -n1 | awk '{print $1}')
    x100=$(gmt project -C$x1/$y1 -A90 -L0/100 -G1 -Q | tail -n1 | awk '{print $1}')
    
    # Draw black boxes
    echo "$x1 $y2
$x10 $y2
$x10 $y3
$x1 $y3
>
$x25 $y2
$x50 $y2
$x50 $y3
$x25 $y3
>
$x10 $y1
$x25 $y1
$x25 $y2
$x10 $y2
>
$x50 $y1
$x100 $y1
$x100 $y2
$x50 $y2" | gmt psxy $rgn $proj -Gblack -O -K >> $out.ps

    # Draw outline
    echo "$x1 $y1
$x100 $y1
$x100 $y3
$x1 $y3" | gmt psxy $rgn $proj -W0.2p -L -O -K >> $out.ps

    # Plot labels
    echo $x100 $y2 "km" | gmt pstext $rgn $proj -F+f6p,Helvetica-Bold,black+jLM -D0.025i/0i -N -O -K >> $out.ps
    echo "$x1 $y3 0
$x25 $y3 25
$x100 $y3 100"| gmt pstext $rgn $proj -F+f6p,Helvetica-Bold,black+jCB -D0i/0.025i -N -O -K >> $out.ps
    echo "$x10 $y1 10
$x50 $y1 50"| gmt pstext $rgn $proj -F+f6p,Helvetica-Bold,black+jCT -D0i/-0.025i -N -O -K >> $out.ps

}

# ---- Plot

# Define output
out=../../Figures/Figure_1_Planforms

# Initialise
gmt psbasemap -R0/1/0/1 -JX2i -B+n -Y6i -K > $out.ps

# Plot first catchment
catch=South_Platte
lab="South Platte"
xlab=-101.5
ylab=41.35
col=213/094/000
plot_catch

# Plot next catchment
gmt psbasemap -R0/1/0/1 -JX2i -X1.5i -B+n -O -K >> $out.ps
catch=Big_Blue
lab="Big Blue"
xlab=-98.5
ylab=40.1
col=000/114/178
plot_catch

# Plot next catchment
gmt psbasemap -R0/1/0/1 -JX2i -B+n -Y-0.65i -X-1.75i -O -K >> $out.ps
catch=Niobara
lab="Niobrara"
xlab=-103.3
ylab=42.8
col=000/158/115
plot_catch

# Plot next catchment
gmt psbasemap -R0/1/0/1 -JX2i -B+n -Y-1.2i -O -K >> $out.ps
catch=Arkansas
lab="Arkansas"
xlab=-103.8
ylab=39.15
col=204/121/167
plot_catch

# Plot last catchment
gmt psbasemap -R0/1/0/1 -JX2i -B+n -X1.7i -O -K >> $out.ps
catch=Bighorn
lab="Bighorn"
xlab=-109.4
ylab=44.5
col=086/180/233
plot_catch

# Plot scale bar
gmt psbasemap -R0/1/0/1 -JX2i -B+n -X-0.85i -Y-0.35i -O -K >> $out.ps
x1=-109
y1=43
plot_scl

# Finalise
gmt psbasemap $rgn $proj -B+n -O >> $out.ps
gmt psconvert -A -E300 -Tj $out.ps
gmt psconvert -A -E300 -Tf $out.ps
rm $out.ps
eog $out.jpg &