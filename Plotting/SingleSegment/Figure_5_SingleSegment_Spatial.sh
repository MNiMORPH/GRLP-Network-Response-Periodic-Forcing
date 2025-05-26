#!/bin/bash

# ---- Get useful extra functions
source ../gmt_extras.sh

# ---- Set defaults
gmt_extras::set_gmt_defaults


# ---- Inputs / Output
basedir="../../Output/SingleSegment/Figure_5_SingleSegment_Spatial"
out="../../Figures/Figure_5_SingleSegment_Spatial"

# ---- Variables
proj=-JX2i
rgn=-R-10/110/-0.1/1.1
rgn_lag=-R-10/110/-0.05/0.45
periods=("fast" "medium" "slow")
axes=("eW" "ew" "ew")
g_lab=("a" "b" "c")
l_lab=("d" "e" "f")
title=("@%2%P@%% = @%2%T@-eq@-@%% / 10" "@%2%P@%% = @%2%T@-eq@-@%%" "@%2%P@%% = @%2%T@-eq@-@%% x 10")

# ---- Initiate
gmt psbasemap $rgn $proj -B+n -Y6i -X-1.5i -K > $out.ps

# ---- CPTs
gmt makecpt -T0.6/2.6/0.4 -Cplasma -D -G0/0.95 -I > p.cpt

for i in ${!periods[@]} ; do

  indir=$basedir/${periods[$i]}

  # ---- Gain_z
  gmt psbasemap $rgn $proj -B+n -X2.3i -Y2.2i -O -K >> $out.ps
  gmt psxy $indir/G_z_lin.dg $rgn $proj -W0.8p,dimgrey,4_4 -O -K >> $out.ps
  gmt psxy $indir/G_z.dg $rgn $proj -W0.8p -Cp.cpt -O -K >> $out.ps
  echo ${g_lab[$i]} | \
    gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jLT+cLT -D0.05i/-0.08i -O -K >> $out.ps
  echo ${title[$i]} | \
    gmt pstext $rgn $proj -F+f11p,Helvetica,black+jCB+cCT -N -D0i/0.16i -O -K >> $out.ps
  gmt psbasemap $rgn $proj -Bns${axes[$i]} \
      -Bx20+l"Downstream distance [km]" \
      -By0.2+l"Gain, @%2%G@-z@-@%%" \
      -O -K >> $out.ps
      
  if [ ${periods[$i]} == "slow" ] ; then
    gmt_extras::plot_key_line $rgn $proj 104 87.5 0.05 -W0.8p,dimgrey,4_4 "Upstream supply" $out
    gmt_extras::plot_key_multi_line $rgn $proj 104 87.5 -0.03 -W0.8p "Along-stream supply" $out p.cpt "1.4 1.6 1.8 2 2.2"
  fi

  # ---- Lag_z
  gmt psbasemap $rgn_lag $proj -B+n -Y-2.2i -O -K >> $out.ps
  gmt psxy $indir/Lag_z_lin.dl $rgn_lag $proj -W0.8p,dimgrey,4_4 -O -K >> $out.ps
  gmt psxy $indir/Lag_z.dl $rgn_lag $proj -W0.8p -Cp.cpt -O -K >> $out.ps
  echo ${l_lab[$i]} | \
    gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jLT+cLT -D0.05i/-0.08i -O -K >> $out.ps
  gmt psbasemap $rgn_lag $proj -BnS${axes[$i]} \
      -Bx20+l"Downstream distance [km]" \
      -By0.1+l"Lag, @~\152@~@%2%@-z@-@%% / @%2%P@%%" \
      -O -K >> $out.ps
  
  if [ ${periods[$i]} == "slow" ] ; then
    gmt psscale $rgn $proj \
      -Dx1.35i/1.85i+w1i/0.07i+jMC+h \
      -Bx0.4+l"@%2%p@-x,Qw@-     p@-x,Qs@-@%%" \
      -Cp.cpt \
      --MAP_LABEL_OFFSET=0p \
      --MAP_ANNOT_OFFSET=5p \
      --MAP_TICK_LENGTH=7p \
      --MAP_DEFAULT_PEN=5p \
      --MAP_TICK_PEN=1p \
      --FONT=14p \
      -O -K >> $out.ps
  fi
  
done

# ---- Show
gmt psbasemap $rgn $proj -B+n -O >> $out.ps
gmt psconvert -A -E400 -Tj $out.ps
eog $out.jpg &
rm $out.ps *.cpt