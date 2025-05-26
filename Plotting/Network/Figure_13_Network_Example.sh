#!/bin/bash

# ---- Get useful extra functions
source ../gmt_extras.sh

# ---- Define extra functions
label_stream () {
  x1=$1
  y1=$2
  x2=$3
  y2=$4
  lab=$5
  echo "$x1 $y1
$x2 $y2" | gmt psxy $rgn $proj -W1p,grey -O -K >> $out.ps
  echo $x1 $y1 $lab | gmt pstext $rgn $proj -F+f7p,Helvetica-Bold,grey -Gwhite -C12%+tO -O -K >> $out.ps
}

label_time_series() {
  y1=$1
  y2=$2
  lab=$3
  off=$4
  
  rgnx=-R0/3/0/700
  projx=-JX3i/2i
  
  echo "2.025 $y1
2.06 $y1
2.06 $y2
2.025 $y2" | gmt psxy $rgnx $projx -W1p -O -K >> $out.ps
  
  echo 2.06 $(echo $y1 $y2 | awk '{print ($1+$2)/2}') $lab | gmt pstext $rgnx $projx -F+f7p,Helvetica-Bold -Gwhite -C10% -D$off/0i -O -K >> $out.ps
}

# ---- Set defaults
gmt_extras::set_gmt_defaults

# ---- Variables
out=../../Figures/Figure_13_Network_Example
basedir=../../Output/Network/Figure_13_Network_Example

# ---- CPTs
gmt makecpt -T0.2/0.6/0.01 -Cplasma -D -Z > gain.cpt
gmt makecpt -T0/0.25/0.01 -Cocean -D -Z -G-6000/-500 -I > lag.cpt
gmt makecpt -Cviridis -T0.5/4.5/1 -I -D > order.cpt

# ---- Plot planforms

rgn=-R-5/105/0/21
proj=-JX2i

gmt psbasemap $rgn $proj -B+n -Y4i -K > $out.ps
gmt psxy $basedir/planform_select.d $rgn $proj -W4p,grey -O -K >> $out.ps
gmt psxy $basedir/planform.d $rgn $proj -W1.2p -Corder.cpt -O -K >> $out.ps
gmt psxy $basedir/planform_nodes.d $rgn $proj -Sc2.5p -W0.8p,black -O -K >> $out.ps
echo a | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jLT+cLT -D0.05i/-0.08i -O -K >> $out.ps
gmt psscale $rgn $proj -Dx1i/2.15i+w1.5i/0.07i+jMC+h+m -Corder.cpt -B1+l"Stream order, @~\167@~ [-]" \
  --MAP_LABEL_OFFSET=2p \
  --MAP_ANNOT_OFFSET=5p \
  --MAP_TICK_LENGTH=6p \
  --MAP_DEFAULT_PEN=5p \
  --MAP_TICK_PEN=1p \
  --FONT=12p \
  -O -K >> $out.ps
label_stream 17 1.5 12 2.5 i
label_stream 12.5 8 12.5 6.5 ii
label_stream 30 18 37.5 18.5 iii
label_stream 98 1.25 91 1.75 iv
label_stream 36 11.5 31.5 10.3 v
label_stream 62 1 68 1 vi
label_stream 76 18.5 83.5 19 vii
gmt psbasemap $rgn $proj -BnSlr -Bx20+l"Downstream distance, @%2%x@%% [km]" -O -K >> $out.ps

gmt psbasemap $rgn $proj -B+n -X2.25i -O -K >> $out.ps
gmt psxy $basedir/planform_select.d $rgn $proj -W4p,grey -O -K >> $out.ps
gmt psxy $basedir/planform_gain.dg $rgn $proj -W1.2p -Cgain.cpt -O -K >> $out.ps
echo b | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jLT+cLT -D0.05i/-0.08i -O -K >> $out.ps
gmt psscale $rgn $proj -Dx1i/2.15i+w1.5i/0.07i+jMC+e+h+m -Cgain.cpt -B0.1+l"Gain, @%2%G@-z@-@%% [-]" \
  --MAP_LABEL_OFFSET=2p \
  --MAP_ANNOT_OFFSET=5p \
  --MAP_TICK_LENGTH=6p \
  --MAP_DEFAULT_PEN=5p \
  --MAP_TICK_PEN=1p \
  --FONT=12p \
  -O -K >> $out.ps
label_stream 17 1.5 12 2.5 i
label_stream 12.5 8 12.5 6.5 ii
label_stream 30 18 37.5 18.5 iii
label_stream 98 1.25 91 1.75 iv
label_stream 36 11.5 31.5 10.3 v
label_stream 62 1 68 1 vi
label_stream 76 18.5 83.5 19 vii
gmt psbasemap $rgn $proj -BnSlr -Bx20+l"Downstream distance, @%2%x@%% [km]" -O -K >> $out.ps

gmt psbasemap $rgn $proj -B+n -X2.25i -O -K >> $out.ps
gmt psxy $basedir/planform_select.d $rgn $proj -W4p,grey -O -K >> $out.ps
gmt psxy $basedir/planform_lag.dl $rgn $proj -W1.2p -Clag.cpt -O -K >> $out.ps
echo c | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jLT+cLT -D0.05i/-0.08i -O -K >> $out.ps
gmt psscale $rgn $proj -Dx1i/2.15i+w1.5i/0.07i+jMC+e+h+m -Clag.cpt -B0.05+l"Lag, @~\152@~@%2%@-z@-@%% / @%2%P@%% [-]" \
  --MAP_LABEL_OFFSET=2p \
  --MAP_ANNOT_OFFSET=5p \
  --MAP_TICK_LENGTH=6p \
  --MAP_DEFAULT_PEN=5p \
  --MAP_TICK_PEN=1p \
  --FONT=12p \
  -O -K >> $out.ps
label_stream 17 1.5 12 2.5 i
label_stream 12.5 8 12.5 6.5 ii
label_stream 30 18 37.5 18.5 iii
label_stream 98 1.25 91 1.75 iv
label_stream 36 11.5 31.5 10.3 v
label_stream 62 1 68 1 vi
label_stream 76 18.5 83.5 19 vii
gmt psbasemap $rgn $proj -BnSlr -Bx20+l"Downstream distance, @%2%x@%% [km]" -O -K >> $out.ps

# ---- Plot time series

rgn=-R0/260/0/700

gmt psbasemap $rgn $proj -B+n -X-4.5i -Y-2.6i -O -K >> $out.ps
gmt psxy $basedir/force_tps.te $rgn $proj -W0.8p,lightgrey -O -K >> $out.ps
gmt psxy $basedir/panel0.te $rgn $proj -W1p -Corder.cpt -O -K >> $out.ps
gmt psxy $basedir/panel_tps0.te $rgn $proj -Sc2p -Corder.cpt -O -K >> $out.ps
echo d | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jLT+cLT -D0.05i/-0.07i -Gwhite -C30%/40% -O -K >> $out.ps
gmt psbasemap $rgn $proj -BnSrW -Bx50+l"Time, @%2%t@%% [kyr]" -By100+l"Elevation, @%2%z@%% [m]" -O -K >> $out.ps
label_time_series 10 610 i 0i

gmt psbasemap $rgn $proj -B+n -X2.25i -O -K >> $out.ps
gmt psxy $basedir/force_tps.te $rgn $proj -W0.6p,lightgrey -O -K >> $out.ps
gmt psxy $basedir/panel1.te $rgn $proj -W1p -Corder.cpt -O -K >> $out.ps
gmt psxy $basedir/panel_tps1.te $rgn $proj -Sc2p -Corder.cpt -O -K >> $out.ps
echo e | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jLT+cLT -D0.05i/-0.07i -Gwhite -C30%/40% -O -K >> $out.ps
gmt psbasemap $rgn $proj -BnSrw -Bx50+l"Time, @%2%t@%% [kyr]" -By100+l"Elevation, @%2%z@%% [m]" -O -K >> $out.ps
label_time_series 460 540 ii 0i
label_time_series 155 400 iii 0i
label_time_series 50 100 iv 0i

gmt psbasemap $rgn $proj -B+n -X2.25i -O -K >> $out.ps
gmt psxy $basedir/force_tps.te $rgn $proj -W0.6p,lightgrey -O -K >> $out.ps
gmt psxy $basedir/panel2.te $rgn $proj -W1p -Corder.cpt -O -K >> $out.ps
gmt psxy $basedir/panel_tps2.te $rgn $proj -Sc2p -Corder.cpt -O -K >> $out.ps
echo f | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jLT+cLT -D0.05i/-0.07i -Gwhite -C30%/40% -O -K >> $out.ps
gmt psbasemap $rgn $proj -BnSrw -Bx50+l"Time, @%2%t@%% [kyr]" -By100+l"Elevation, @%2%z@%% [m]" -O -K >> $out.ps
label_time_series 350 480 v 0i
label_time_series 110 180 vi 0i
label_time_series 20 90 vii 0.02i

# ---- Show
gmt psbasemap $rgn $proj -B+n -O >> $out.ps
gmt psconvert -A -E400 -Tj $out.ps
rm $out.ps *.cpt
eog $out.jpg &