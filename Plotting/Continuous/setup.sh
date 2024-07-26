#!/bin/bash

# ---- Get useful extra functions
source ../gmt_extras.sh

# ---- Set defaults
gmt_extras::set_gmt_defaults


# ---- Variables
out=setup
rgn=-R-5/105/0/700
rgn_Qw=-R-5/105/0/60
rgn_Qs=-R-5/105/0/6
proj=-JX2.6i/2i

# ---- CPTs
gmt makecpt -T1.3/2.3/0.2 -Cplasma -D -G0/0.95 -I > p.cpt

# ---- Discharges
gmt psbasemap $rgn $proj -B+n -Y6i -K > $out.ps
gmt psxy ../../output/continuous/setup/constant.dq $rgn_Qw $proj -W0.8p,dimgrey,4_4 -O -K >> $out.ps
gmt psxy ../../output/continuous/setup/water.dq $rgn_Qw $proj -W0.8p -Cp.cpt -O -K >>  $out.ps
gmt psxy ../../output/continuous/setup/sediment.dq $rgn_Qs $proj -W0.8p,. -O -K >>  $out.ps
gmt_extras::plot_key_multi_line $rgn_Qw $proj 88 100 11 -W0.8p $out p.cpt "1.4 1.6 1.8 2 2.2"
gmt_extras::plot_key_line $rgn_Qw $proj 88 100 7 -W0.8p,. $out
gmt_extras::plot_key_line $rgn_Qw $proj 88 100 3 -W0.8p,dimgrey,4_4 $out
echo "88 11 @%2%Q@-w@-@%%(@%2%x@%%)
88 7 @%2%Q@-s@-@%%(@%2%x@%%)
88 3 @~\341@~@%2%Q@-w@-@%%@~\361@~, @~\341@~@%2%Q@-s@-@%%@~\361@~" | gmt pstext $rgn_Qw $proj -F+f7p,Helvetica,black+jRM -D-0.05i/0i -O -K >> $out.ps
gmt psscale $rgn $proj -Dx1.3i/1.85i+w1i/0.07i+jMC+h -Bx0.2+1+l"@%2%p@-x,Qw@-     p@-x,Qs@-@%%" -Cp.cpt --MAP_LABEL_OFFSET=3.5p -O -K >> $out.ps
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
gmt psxy ../../output/continuous/setup/numerical_profile.de $rgn $proj -W0.8p -Cp.cpt -O -K >> $out.ps
gmt psxy ../../output/continuous/setup/analytical_profile.de $rgn $proj -W0.8p,dimgrey,4_4 -O -K >> $out.ps
gmt psbasemap $rgn $proj \
  -BnSeW \
  -Bx20+l"Downstream distance, @%2%x@%% [km]"\
  -By100+l"Elevation, @%2%z@%% [m]" -O -K >> $out.ps
gmt_extras::plot_key_multi_line $rgn $proj 88 100 650 -W0.8p $out p.cpt "1.4 1.6 1.8 2 2.2"
gmt_extras::plot_key_line $rgn $proj 88 100 590 -W0.8p,dimgrey,4_4 $out
echo "88 650 Continuous supply
88 590 Upstream supply" | gmt pstext $rgn $proj -F+f7p,Helvetica,black+jRM -D-0.05i/0i -O -K >> $out.ps
echo "b" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jLT+cLT -D0.05i/-0.08i -O >> $out.ps

# ---- Show
# gv $out.ps &
gmt psconvert -A -E400 -Tj $out.ps
eog $out.jpg &
rm $out.ps