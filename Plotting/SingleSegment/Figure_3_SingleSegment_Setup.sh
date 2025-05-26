#!/bin/bash

# ---- Get useful extra functions
source ../gmt_extras.sh

# ---- Set defaults
gmt_extras::set_gmt_defaults

# ---- Variables
out=../../Figures/Figure_3_SingleSegment_Setup
rgn=-R-5/105/0/700
rgn_Qw=-R-5/105/0/70
rgn_Qs=-R-5/105/0/7
proj=-JX2.6i/2i
basedir=../../Output/SingleSegment/Figure_3_SingleSegment_Setup

# ---- CPTs
gmt makecpt -T0.6/2.6/0.4 -Cplasma -D -G0/0.95 -I > p.cpt

# ---- Discharges
gmt psbasemap $rgn $proj -B+n -Y6i -K > $out.ps
gmt psxy $basedir/constant.dq $rgn_Qw $proj -W0.8p,dimgrey,4_4 -O -K >> $out.ps
gmt psxy $basedir/water.dq $rgn_Qw $proj -W0.8p -Cp.cpt -O -K >>  $out.ps
gmt psxy $basedir/sediment.dq $rgn_Qs $proj -W0.8p,. -O -K >>  $out.ps
gmt_extras::plot_key_multi_line $rgn_Qw $proj 100 88 14 -W0.8p "@%2%Q@-w@-@%%(@%2%x@%%)" $out p.cpt "1.4 1.6 1.8 2 2.2"
gmt_extras::plot_key_line $rgn_Qw $proj 100 88 9 -W0.8p,. "@%2%Q@-s@-@%%(@%2%x@%%)" $out
gmt_extras::plot_key_line $rgn_Qw $proj 100 88 4 -W0.8p,dimgrey,4_4 "@~\341@~@%2%Q@-w@-@%%@~\361@~, @~\341@~@%2%Q@-s@-@%%@~\361@~" $out
gmt psscale $rgn $proj \
  -Dx1.3i/1.85i+w1i/0.07i+jMC+h \
  -Bx0.4+l"@%2%p@-x,Qw@-     p@-x,Qs@-@%%" \
  -Cp.cpt \
  --MAP_LABEL_OFFSET=2p \
  --MAP_ANNOT_OFFSET=5p \
  --FONT=14p \
  -O -K >> $out.ps
echo "a" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jLT+cLT -D0.05i/-0.08i -O -K >> $out.ps
gmt psbasemap $rgn_Qw $proj \
  -BnsW \
  -Bx20+l"Downstream distance, @%2%x@%% [km]" \
  -By10+l"Water discharge, @%2%Q@-w@-@%% [m@+3@+ s@+-1@+]" -O -K >> $out.ps
gmt psbasemap $rgn_Qs $proj \
  -BE \
  -By1+l"Sediment discharge, @%2%Q@-s@-@%% [x10@+-3@+ m@+3@+ s@+-1@+]" -O -K >> $out.ps

# ----- Profile
gmt psbasemap $rgn $proj -B+n -Y-2.2i -O -K >> $out.ps
gmt psxy $basedir/numerical_profile.de $rgn $proj -W0.8p -Cp.cpt -O -K >> $out.ps
gmt psxy $basedir/analytical_profile.de $rgn $proj -W0.8p,dimgrey,4_4 -O -K >> $out.ps
gmt psbasemap $rgn $proj \
  -BnSeW \
  -Bx20+l"Downstream distance, @%2%x@%% [km]"\
  -By100+l"Elevation, @%2%z@%% [m]" -O -K >> $out.ps
gmt_extras::plot_key_multi_line $rgn $proj 100 88 650 -W0.8p "Along-stream supply" $out p.cpt "1.4 1.6 1.8 2 2.2"
gmt_extras::plot_key_line $rgn $proj 100 88 590 -W0.8p,dimgrey,4_4 "Upstream supply" $out
echo "b" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jLT+cLT -D0.05i/-0.08i -O >> $out.ps

# ---- Show
# gv $out.ps &
gmt psconvert -A -E400 -Tj $out.ps
eog $out.jpg &
rm $out.ps *.cpt