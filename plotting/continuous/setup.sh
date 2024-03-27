#!/bin/bash -i

overbar () {
  x=$1
  y=$2
  p=$3
  r=$4
  yoff=$(echo $p | awk ' { print $1/2 } ')
  x1=$(echo $x | awk ' { print $1-1.2 } ')
  x2=$(echo $x | awk ' { print $1+1.2 } ')
  echo "$x1 $y
  $x2 $y" | gmt psxy $r $proj -W0.4p -D0p/${yoff}p -O -K >> $out.ps
}

# ---- Defaults
set_gmt_defaults

# ---- Variables
out=setup
rgn=-R-5/105/0/700
rgn_Qw=-R-5/105/0/35
rgn_Qs=-R-5/105/0/3.5
proj=-JX2.6i/2i

# ---- CPTs
gmt makecpt -T1.2/2.8/0.4 -Cplasma -D -G0/0.95 -I > p.cpt

# ---- Discharges
gmt psbasemap $rgn $proj -B+n -Y6i -K > $out.ps
gmt psxy ../../output/continuous/setup/constant.dq $rgn_Qw $proj -W0.8p,dimgrey,4_4 -O -K >> $out.ps
gmt psxy ../../output/continuous/setup/water.dq $rgn_Qw $proj -W0.8p -Cp.cpt -O -K >>  $out.ps
gmt psxy ../../output/continuous/setup/sediment.dq $rgn_Qs $proj -W0.8p,. -O -K >>  $out.ps
echo "> -Z0.4
88 7
91 7
>
> -Z0.5
91 7
94 7
> -Z0.6
94 7
97 7
> -Z0.7
97 7
100 7" | gmt psxy $rgn_Qw $proj -W0.8p -Cp.cpt -O -K >> $out.ps
echo "100 4.5
88 4.5" | gmt psxy $rgn_Qw $proj -W0.8p,. -O -K >> $out.ps
echo "100 2
88 2" | gmt psxy $rgn_Qw $proj -W0.8p,dimgrey,4_4 -O -K >> $out.ps
echo "88 7 @%2%Q@-w@-@%%(@%2%x@%%)
88 4.5 @%2%Q@-s@-@%%(@%2%x@%%)
88 2 @~\341@~@%2%Q@-w@-@%%@~\361@~, @~\341@~@%2%Q@-s@-@%%@~\361@~" | gmt pstext $rgn_Qw $proj -F+f7p,Helvetica,black+jRM -D-0.05i/0i -O -K >> $out.ps
# overbar 83.5 2 7 $rgn_Qw
# overbar 76 2 7 $rgn_Qw
gmt psscale $rgn $proj -Dx1.3i/1.85i+w0.8i/0.08i+jMC+h -Bx0.4+1+l"@%2%p@-x,Qw@-     p@-x,Qs@-@%%" -Cp.cpt --MAP_LABEL_OFFSET=3.5p -O -K >> $out.ps
# gmt psscale $rgn $proj -Dx0.12i/1.2i+w0.8i/0.08i+jMC -Bx0.1+l"Hack exponent, @%2%h@%%" -Cp.cpt --MAP_LABEL_OFFSET=3.5p -O -K >> $out.ps
echo "a" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jLT+cLT -D0.05i/-0.08i -O -K >> $out.ps
gmt psbasemap $rgn_Qw $proj \
  -BnsW \
  -Bx20+l"Downstream distance, @%2%x@%% [km]" \
  -By5+l"Water discharge, @%2%Q@-w@-@%% [m@+3@+ s@+-1@+]" -O -K >> $out.ps
gmt psbasemap $rgn_Qs $proj \
  -BE \
  -By0.5+l"Sediment discharge, @%2%Q@-s@-@%% [x10@+-3@+ m@+3@+ s@+-1@+]" -O -K >> $out.ps

# ----- Profile
gmt psbasemap $rgn_Qw $proj -B+n -Y-2.2i -O -K >> $out.ps
gmt psxy ../../output/continuous/setup/numerical_profile.de $rgn $proj -W0.8p -Cp.cpt -O -K >> $out.ps
gmt psxy ../../output/continuous/setup/analytical_profile.de $rgn $proj -W0.8p,dimgrey,4_4 -O -K >> $out.ps
gmt psbasemap $rgn $proj \
  -BnSeW \
  -Bx20+l"Downstream distance, @%2%x@%% [km]"\
  -By100+l"Elevation, @%2%z@%% [m]" -O -K >> $out.ps
echo "> -Z0.4
88 650
91 650
>
> -Z0.5
91 650
94 650
> -Z0.6
94 650
97 650
> -Z0.7
97 650
100 650" | gmt psxy $rgn $proj -W0.8p -Cp.cpt -O -K >> $out.ps
echo "100 590
88 590" | gmt psxy $rgn $proj -W0.8p,dimgrey,4_4 -O -K >> $out.ps
echo "88 650 Continuous supply
88 590 Upstream supply" | gmt pstext $rgn $proj -F+f7p,Helvetica,black+jRM -D-0.05i/0i -O -K >> $out.ps
echo "b" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jLT+cLT -D0.05i/-0.08i -O >> $out.ps

# ---- Show
# gv $out.ps &
gmt psconvert -A -E400 -Tj $out.ps
eog $out.jpg &