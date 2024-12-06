#!/bin/bash

# ---- Get useful extra functions
source ../gmt_extras.sh

# ---- Set defaults
gmt_extras::set_gmt_defaults

# ---- Inputs / Output
basedir="../../Output/Network/Figure_13_Network_Spatial_Gain_Lag"
out="../../Figures/Figure_13_Network_Spatial_Gain_Lag"

# ---- Variables
proj=-JX1.5i
rgn=-R-10/110/0.1/0.8
rgn_lag=-R-10/110/0.025/0.325
nets=("UUU" "NUU" "UAU" "NAU")
axes=("eW" "ew" "ew" "ew")
g_lab=("a" "b" "c" "d")
l_lab=("e" "f" "g" "h")
titles=("Uniform segment lengths" "Non-uniform segment lengths" "Unifom segment lengths" "Non-uniform segment lengths")

# ---- Initiate
gmt psbasemap $rgn $proj -B+n -Y6i -X-0.65i -K > $out.ps

# CPT
gmt makecpt -Cviridis -T0.5/4.5/1 -I > order.cpt

for i in ${!nets[@]} ; do

  indir=$basedir/${nets[$i]}

  # ---- Gain_z
  gmt psbasemap $rgn $proj -B+n -X1.65i -Y1.65i -O -K >> $out.ps
  gmt psxy $indir/single_seg_U_gain.dg $rgn $proj -W0.8p,black,3_2 -O -K >> $out.ps
  gmt psxy $indir/single_seg_A_gain.dg $rgn $proj -W0.8p,dimgrey,3_3_0.8_3 -O -K >> $out.ps
  gmt psxy $indir/gain.dg $rgn $proj -W0.8p -Corder.cpt -O -K >> $out.ps
  echo ${g_lab[$i]} | \
    gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jLT+cLT -D0.05i/-0.08i -O -K >> $out.ps
  echo "${titles[$i]}" | gmt pstext $rgn $proj -F+f8p+jCB+cCT -D0i/0.1i -N -O -K >> $out.ps
  gmt psbasemap $rgn $proj -Bns${axes[$i]} \
      -Bx20+l"Downstream distance [km]" \
      -By0.1+l"Gain, @%2%G@-z@-@%%" \
      -O -K >> $out.ps
      
  if [ $i -eq 0 ] ; then
    gmt_extras::plot_key_multi_line $rgn $proj 105 90.5 0.76 -W0.8p "Network" $out order.cpt "4 3 2 1"
    gmt_extras::plot_key_line $rgn $proj 105 90.5 0.72 -W0.8p,3_2 "Upstream supply" $out
    gmt_extras::plot_key_line $rgn $proj 105 90.5 0.68 -W0.8p,dimgrey,3_3.1_0.8_3.1_3 "Along stream supply" $out
  fi

  if [ ${nets[$i]} == "NAU" ] ; then
    gmt psscale $rgn $proj \
      -Corder.cpt \
      -Dx0.7i/1.35i+w0.7i/0.07i+h \
      -B1+l"Stream order, @~\167@~" \
      --MAP_LABEL_OFFSET=-8p \
      --MAP_ANNOT_OFFSET=5p \
      --MAP_TICK_LENGTH=7p \
      --MAP_DEFAULT_PEN=7p \
      --MAP_TICK_PEN=1.5p \
      --FONT=16p \
      -O -K >> $out.ps
  fi

  # ---- Lag_z
  gmt psbasemap $rgn_lag $proj -B+n -Y-1.65i -O -K >> $out.ps
  gmt psxy $indir/single_seg_U_lag.dl $rgn_lag $proj -W0.8p,black,3_3 -O -K >> $out.ps
  gmt psxy $indir/single_seg_A_lag.dl $rgn_lag $proj -W0.8p,dimgrey,3_3_0.8_3 -O -K >> $out.ps
  gmt psxy $indir/lag.dl $rgn_lag $proj -W0.8p -Corder.cpt -O -K >> $out.ps
  echo ${l_lab[$i]} | \
    gmt pstext $rgn_lag $proj -F+f11p,Helvetica-Bold,black+jLT+cLT -D0.05i/-0.08i -O -K >> $out.ps
  gmt psbasemap $rgn_lag $proj -BnS${axes[$i]} \
      -Bx20+l"Downstream distance [km]" \
      -By0.05+l"Lag, @~\152@~@%2%@-z@-@%% / @%2%P@%%" \
      -O -K >> $out.ps
      
done

rgn=-R0/3.15/0/3.15
proj=-JX3.15i
gmt psbasemap $rgn $proj -B+n -Y1.65i -X-4.95i -O -K >> $out.ps
echo "0.75 1.72
0.75 1.79
2.4 1.79
2.4 1.72" | gmt psxy $rgn $proj -W0.8p -O -K >> $out.ps
echo "Upstream supply" | gmt pstext $rgn $proj -F+f8p+jCM+cCB -D0i/1.79i -Gwhite -N -O -K >> $out.ps

gmt psbasemap $rgn $proj -B+n -X3.3i -O -K >> $out.ps
echo "0.75 1.72
0.75 1.79
2.4 1.79
2.4 1.72" | gmt psxy $rgn $proj -W0.8p -O -K >> $out.ps
echo "Along stream supply" | gmt pstext $rgn $proj -F+f8p+jCM+cCB -D0i/1.79i -Gwhite -N -O -K >> $out.ps

# ---- Show
gmt psbasemap $rgn $proj -B+n -O >> $out.ps
# gv $out.ps &
gmt psconvert -A -E400 -Tj $out.ps
rm $out.ps order.cpt
eog $out.jpg &