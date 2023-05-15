#!/bin/bash -i

# ---- Defaults
set_gmt_defaults

# ---- Variables
out=setup
rgn=-R-10/110/0/700
rgn_Qw=-R-10/110/0/40
rgn_Qs=-R-10/110/0/4
proj=-JX2.6i/2i

# ---- CPTs
gmt makecpt -T0/3/0.1 -Cplasma -D -Z > p.cpt

# ---- Discharges
gmt psbasemap $rgn $proj -B+n -Y6i -K > $out.ps
gmt psxy output/setup/water.dq $rgn_Qw $proj -W0.8p -Cp.cpt -O -K >>  $out.ps
gmt psxy output/setup/sediment.dq $rgn_Qs $proj -W0.8p,. -O -K >>  $out.ps
# gmt psxy output/setup/constant.dq $rgn_Qw $proj -W0.8p,dimgrey,4_4 -O -K >> $out.ps
echo "> -Z2
-5 600
8 600" | gmt psxy $rgn $proj -W0.8p -Cp.cpt -O -K >> $out.ps
echo "-5 550
8 550" | gmt psxy $rgn $proj -W0.8p,. -O -K >> $out.ps
echo "8 600 @%2%Q@-w@-@%%
8 550 @%2%Q@-s@-@%%" | gmt pstext $rgn $proj -F+f8p,Helvetica,black+jLM -D0.05i/0i -O -K >> $out.ps
gmt psscale $rgn $proj -Dx1.3i/1.85i+w0.8i/0.08i+jMC+h -Bx1+l"Discharge exponent, @%2%p@%%" -Cp.cpt --MAP_LABEL_OFFSET=3.5p -O -K >> $out.ps
echo "a" | gmt pstext $rgn $proj -F+f10p,Helvetica-Bold,black+jLT+cLT -D0.05i/-0.08i -O -K >> $out.ps
gmt psbasemap $rgn_Qw $proj \
  -BnSW \
  -Bx20+l"Downstream distance, @%2%x@%% [km]" \
  -By10+l"Water discharge, @%2%Q@-w@-@%% [m@+3@+ s@+-1@+]" -O -K >> $out.ps
gmt psbasemap $rgn_Qs $proj \
  -BE \
  -By1+l"Sediment discharge, @%2%Q@-s@-@%% [x10@+-3@+ m@+3@+ s@+-1@+]" -O -K >> $out.ps

# ----- Profile
gmt psbasemap $rgn_Qw $proj -B+n -X3.7i -O -K >> $out.ps
gmt psxy output/setup/numerical_profile.de $rgn $proj -W0.8p -Cp.cpt -O -K >> $out.ps
gmt psxy output/setup/analytical_profile.de $rgn $proj -W0.8p,dimgrey,4_4 -O -K >> $out.ps
gmt psbasemap $rgn $proj \
  -BnSeW \
  -Bx20+l"Downstream distance, @%2%x@%% [km]"\
  -By200+l"Elevation, @%2%z@%% [m]" -O -K >> $out.ps
echo "> -Z2
105 650
92 650" | gmt psxy $rgn $proj -W0.8p -Cp.cpt -O -K >> $out.ps
echo "105 600
92 600" | gmt psxy $rgn $proj -W0.8p,dimgrey,4_4 -O -K >> $out.ps
echo "92 650 Numerical (@%2%p@%% = 2)
92 600 Analytical (@%2%p@%% = 0)" | gmt pstext $rgn $proj -F+f8p,Helvetica,black+jRM -D-0.05i/0i -O -K >> $out.ps
echo "b" | gmt pstext $rgn $proj -F+f10p,Helvetica-Bold,black+jLT+cLT -D0.05i/-0.08i -O >> $out.ps



# ---- Show
# gv $out.ps &
gmt psconvert -A -E400 -Tj $out.ps
eog $out.jpg &