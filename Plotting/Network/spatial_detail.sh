#!/bin/bash

# ---- Get useful extra functions
source ../gmt_extras.sh

# ---- Set defaults
gmt_extras::set_gmt_defaults

# ---- Inputs / Output
basedir="../../output/network/spatial/m40_fix_seg_length_no_internal"
out="spatial_detail"

# ---- CPTs
gmt makecpt -T0.2/0.4/0.01 -Cplasma -D -Z > gain.cpt
gmt makecpt -T0.1/0.25/0.01 -Cocean -D -Z -G-6000/-500 > lag.cpt
gmt makecpt -Cviridis -T0.5/4.5/1 -I > order.cpt

# ---- Planforms
rgn=-R-10/110/0/31
proj=-JX1.5i
gmt psbasemap $rgn $proj -B+n -Y4i -K > $out.ps
echo "85 4
95 2.5
>
10 6.25
5 4.5
>
32 19
22 19
>
75 27.75
85 27
>
88 11.25
100 12" | gmt psxy $rgn $proj -W0.8p,darkgrey -O -K >> $out.ps
echo "95 2.5 T
5 4.5 i
22 19 ii
85 27 iii
102 12 iv" | gmt pstext $rgn $proj -F+f7p,Helvetica-Bold,darkgrey -Gwhite -O -K >> $out.ps
gmt psxy $basedir/plan_select.d $rgn $proj -W3p,darkgrey -O -K >> $out.ps
gmt psxy $basedir/plan_gain.dg $rgn $proj -W1p -Cgain.cpt -O -K >> $out.ps
echo a | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jLT+cLT -D0.05i/-0.08i -O -K >> $out.ps
gmt psscale $rgn $proj -Dx1.6i/0.75i+w1i/0.07i+jMC+e -Cgain.cpt -B0.05+l"Gain, @%2%G@-z@-@%% [-]" --MAP_LABEL_OFFSET=4p --FONT_ANNOT_PRIMARY=6p --FONT_LABEL=6p -O -K >> $out.ps
gmt psbasemap $rgn $proj -Bnslr -Bx20+l"Downstream distance [km]" -O -K >> $out.ps

gmt psbasemap $rgn $proj -B+n -Y-1.65i -O -K >> $out.ps
echo "85 4
95 2.5
>
10 6.25
5 4.5
>
32 19
22 19
>
75 27.75
85 27
>
88 11.25
102 12" | gmt psxy $rgn $proj -W0.8p,darkgrey -O -K >> $out.ps
echo "95 2.5 T
5 4.5 i
22 19 ii
85 27 iii
102 12 iv" | gmt pstext $rgn $proj -F+f7p,Helvetica-Bold,darkgrey -Gwhite -O -K >> $out.ps
gmt psxy $basedir/plan_select.d $rgn $proj -W3p,darkgrey -O -K >> $out.ps
gmt psxy $basedir/plan_lag.dl $rgn $proj -W1p -Clag.cpt -O -K >> $out.ps
echo b | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jLT+cLT -D0.05i/-0.08i -O -K >> $out.ps
gmt psscale $rgn $proj -Dx1.6i/0.75i+w1i/0.07i+jMC+e -Clag.cpt -B0.05+l"Lag, @~\152@~@%2%@-z@-@%% / @%2%P@%% [-]" --MAP_LABEL_OFFSET=4p --FONT_ANNOT_PRIMARY=6p --FONT_LABEL=6p -O -K >> $out.ps
gmt psbasemap $rgn $proj -BnSlr -Bx20+l"Downstream distance [km]" -O -K >> $out.ps


# ---- Trunk time series
rgn=-R0/160/0/675
proj=-JX1.5i/3.15i
gmt psbasemap $rgn $proj -B+n -X2.6i -O -K >> $out.ps
gmt psxy $basedir/scl_tp_grid.te $rgn $proj -W0.5p,darkgrey,0.5p_1.5p -O -K >> $out.ps
gmt psxy $basedir/trunk.te $rgn $proj -W0.8p -Corder.cpt -O -K >> $out.ps
gmt psxy $basedir/trunk_tps.te $rgn $proj -Sc2p -Corder.cpt -O -K >> $out.ps
echo c | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jLT+cLT -D0.05i/-0.08i -O -K >> $out.ps
gmt psbasemap $rgn $proj -BnSeW -Bx40+l"Time [kyr]" -By100+l"Elevation [m]" -O -K >> $out.ps


# ---- Tributary time series
rgn=-R0/160/0/675
proj=-JX1.5i/3.15i
gmt psbasemap $rgn $proj -B+n -X1.65i -O -K >> $out.ps
gmt psxy $basedir/scl_tp_grid.te $rgn $proj -W0.5p,darkgrey,0.5p_1.5p -O -K >> $out.ps
gmt psxy $basedir/trib.te $rgn $proj -W0.8p -Corder.cpt -O -K >> $out.ps
gmt psxy $basedir/trib_tps.te $rgn $proj -Sc2p -Corder.cpt -O -K >> $out.ps
echo d | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jLT+cLT -D0.05i/-0.08i -O -K >> $out.ps
gmt psscale $rgn $proj \
  -Corder.cpt \
  -Dx0.72i/3.02i+w0.7i/0.07i+h \
  -B1+l"Stream order, @%2%O@%%" \
  --MAP_LABEL_OFFSET=4p --FONT_ANNOT_PRIMARY=6p --FONT_LABEL=6p \
  -F+gwhite+c0p/0p/4p/4p \
  -O -K >> $out.ps
gmt psbasemap $rgn $proj -BnSrw -Bx40+l"Time [kyr]" -By100+l"Elevation [m]" -O -K >> $out.ps

# ---- Tributary labels
rgn=-R0/320/0/650
proj=-JX3i/3.15i
x1=163
x2=168
echo "$x1 75
$x2 75
$x2 126
$x1 126
>
$x1 146
$x2 146
$x2 294
$x1 294
>
$x1 291
$x2 291
$x2 415
$x1 415
>
$x1 445
$x2 445
$x2 570
$x1 570" | gmt psxy $rgn $proj -W1p -O -K >> $out.ps
echo "168 100.5 iv
168 219.5 iii
168 353 ii
168 507.5 i" | gmt pstext $rgn $proj -F+f7p -Gwhite -O -K >> $out.ps

# ---- Show
gmt psbasemap $rgn $proj -B+n -O >> $out.ps
# gv $out.ps &
gmt psconvert -A -E400 -Tj $out.ps
eog $out.jpg &