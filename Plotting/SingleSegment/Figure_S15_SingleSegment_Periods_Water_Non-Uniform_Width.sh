#!/bin/bash

# ---- Get useful extra functions
source ../gmt_extras.sh

# ---- Set defaults
gmt_extras::set_gmt_defaults

# ---- Inputs / Output
basedir="../../Output/SingleSegment/Figure_S14_S15_SingleSegment_Periods_Non-Uniform_Width"
out="../../Figures/Figure_S15_SingleSegment_Periods_Water"

# ---- Variables
proj=-JX2il/2i
projx=-JX2i
rgnx=-R0/100/0/100
pmin=0.01
pmax=100

# ---- CPTs
gmt makecpt -T0.6/2.6/0.4 -Cplasma -D -G0/0.95 -I --COLOR_NAN=white > p.cpt

# ---- G_z
rgn=-R${pmin}/${pmax}/-0.1/1.3
gmt psbasemap $rgn $proj -B+n -X0.5i -Y6i -K > $out.ps
gmt psxy $basedir/G_z_rng_lin.pg $rgn $proj -Glightgrey -O -K >> $out.ps 
gmt psxy $basedir/G_z_out_lin.pg $rgn $proj -W0.8p -O -K >> $out.ps 
awk ' { if ($1==">") print $0 ; else print $1, $3 } ' $basedir/G_z_num_Qw.pg | \
  gmt psxy $rgn $proj -Cp.cpt -W0.8p -O -K >> $out.ps
awk ' { if ($1==">") print $0 ; else print $1, $2 } ' $basedir/G_z_num_Qw.pg | \
  gmt psxy $rgn $proj -Cp.cpt -W0.8p,3_3 -O -K >> $out.ps
echo a | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jLT+cLT -D0.05i/-0.08i -O -K >> $out.ps
gmt psscale $rgn $proj -Dx1.4i/1.85i+w1i/0.07i+jMC+h -Bx0.4+l"@%2%p@-x,Qw@-     p@-x,Qs@-@%%" -Cp.cpt \
  --MAP_LABEL_OFFSET=0p \
  --MAP_ANNOT_OFFSET=5p \
  --MAP_TICK_LENGTH=7p \
  --MAP_DEFAULT_PEN=5p \
  --MAP_TICK_PEN=1p \
  --FONT=14p \
  -O -K >> $out.ps
gmt psbasemap $rgn $proj -BnseW -Bx1f3p+l"Period, @%2%P@%% / @%2%T@-eq@-@%%" -By0.2+l"Gain, @%2%G@-z@-@%%" -O -K >> $out.ps

# ---- lag_z
rgn=-R${pmin}/${pmax}/-0.025/0.525
gmt psbasemap $rgn $proj -B+n -Y-2.2i -O -K >> $out.ps
gmt psxy $basedir/lag_z_rng_lin.pl $rgn $proj -Glightgrey -O -K >> $out.ps 
gmt psxy $basedir/lag_z_out_lin.pl $rgn $proj -W0.8p -O -K >> $out.ps 
awk ' { if ($1==">") print $0 ; else print $1, $3 } ' $basedir/lag_z_num.pl | \
  gmt psxy $rgn $proj -Cp.cpt -W0.8p -O -K >> $out.ps
awk ' { if ($1==">") print $0 ; else print $1, $2 } ' $basedir/lag_z_num.pl | \
  gmt psxy $rgn $proj -Cp.cpt -W0.8p,3_3 -O -K >> $out.ps
awk ' { if ($1==">") print $0 ; else print $1, $4 } ' $basedir/lag_z_num.pl | \
  gmt psxy $rgn $proj -Cp.cpt -W0.8p,0.8_4 -O -K >> $out.ps
echo b | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jLT+cLT -D0.05i/-0.08i -O -K >> $out.ps
gmt_extras::plot_key_line $rgnx $projx 95 84.5 68 -W0.8p "Upstream: Outlet" $out
gmt_extras::plot_key_line $rgnx $projx 95 84.5 74 -W3p,lightgrey "Upstream: Range" $out
gmt_extras::plot_key_multi_line $rgnx $projx 95 84.5 88 -W0.8p "Along-stream: Outlet" $out p.cpt "2.2 2 1.8 1.6 1.4"
gmt_extras::plot_key_multi_line $rgnx $projx 95 84.5 94 -W0.8p "Along-stream: Inlet" $out p.cpt "2.2 nan 1.8 nan 1.4"
gmt_extras::plot_key_multi_line $rgnx $projx 95 84.5 82 -W0.8p "Along-stream: Max'" $out p.cpt "2.2 nan nan nan 2 nan nan nan 1.8 nan nan nan 1.6 nan nan nan 1.4"
gmt psbasemap $rgn $proj -BnSeW -Bx1f3p+l"Period, @%2%P@%% / @%2%T@-eq@-@%%" -By0.1+l"Lag, @~\152@~@%2%@-z@-@%% / @%2%P@%%" -O >> $out.ps

# ---- Show
gmt psconvert -A -E400 -Tj $out.ps
eog $out.jpg &
rm $out.ps *.cpt