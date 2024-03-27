#!/bin/bash -i

# ---- Set defaults
set_gmt_defaults


# ---- Inputs / Output
basedir="../../output/network/spatial"
out="spatial"

# ---- Variables
proj=-JX2i
rgn=-R-10/110/-0.05/0.75
rgn_lag=-R-10/110/-0.025/0.325
periods=("m20_fix_seg_length" "m40_fix_seg_length" "m40_rnd_seg_length")
axes=("eW" "ew" "ew")
g_lab=("a" "b" "c")
l_lab=("d" "e" "f")
title=("@~\155@~ = 20, fixed segment length" "@~\155@~ = 40, fixed segment length" "@~\155@~ = 40, random segment length")

# ---- Initiate
gmt psbasemap $rgn $proj -B+n -Y6i -X-1.5i -K > $out.ps

# CPT
gmt makecpt -Cviridis -T0.5/4.5/1 -I > order.cpt

for i in ${!periods[@]} ; do

  indir=$basedir/${periods[$i]}

  # ---- Gain_z
  gmt psbasemap $rgn $proj -B+n -X2.3i -Y2.2i -O -K >> $out.ps
  gmt psxy $indir/lin_gain.dg $rgn $proj -W0.8p,dimgrey,4_4 -O -K >> $out.ps
  gmt psxy $indir/gain.dg $rgn $proj -W0.8p -Corder.cpt -O -K >> $out.ps
  echo ${g_lab[$i]} | \
    gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jLT+cLT -D0.05i/-0.08i -O -K >> $out.ps
  echo 50 0.75 ${title[$i]} | \
    gmt pstext $rgn $proj -F+f11p,Helvetica,black -N -D0i/0.22i -O -K >> $out.ps
  gmt psbasemap $rgn $proj -Bns${axes[$i]} \
      -Bx20+l"Downstream distance [km]" \
      -By0.1+l"Gain, @%2%G@-z@-@%%" \
      -O -K >> $out.ps
      
#   if [ ${periods[$i]} == "slow" ] ; then
#     echo "> -Z0.4
# 83.5 0
# 87.6 0
# > -Z0.5
# 87.6 0
# 91.7 0
# > -Z0.6
# 91.7 0
# 95.8 0
# > -Z0.7
# 95.8 0
# 100 0" | gmt psxy $rgn $proj -W0.8p -Cp.cpt -O -K >> $out.ps
#     echo "83.5 0.09
# 100 0.09" | gmt psxy $rgn $proj -W0.8p,dimgrey,4_4 -O -K >> $out.ps
#     echo "83.5 0.09 Upstream supply
# 83.5 0 Continuous supply" | gmt pstext $rgn $proj -F+f7p,Helvetica,black+jRM -D-0.05i/0i -O -K >> $out.ps
#   fi

  # ---- Lag_z
  gmt psbasemap $rgn_lag $proj -B+n -Y-2.2i -O -K >> $out.ps
  gmt psxy $indir/lin_lag.dl $rgn_lag $proj -W0.8p,dimgrey,4_4 -O -K >> $out.ps
  gmt psxy $indir/lag.dl $rgn_lag $proj -W0.8p -Corder.cpt -O -K >> $out.ps
  echo ${l_lab[$i]} | \
    gmt pstext $rgn_lag $proj -F+f11p,Helvetica-Bold,black+jLT+cLT -D0.05i/-0.08i -O -K >> $out.ps
  gmt psbasemap $rgn_lag $proj -BnS${axes[$i]} \
      -Bx20+l"Downstream distance [km]" \
      -By0.05+l"Lag, @~\152@~@%2%@-z@-@%% / @%2%P@%%" \
      -O -K >> $out.ps
    
  if [ ${periods[$i]} == "m40_rnd_seg_length" ] ; then
    gmt psscale $rgn $proj \
      -Corder.cpt \
      -Dx0.1i/0.1i+w0.7i/0.07i+h+m \
      -B1+l"Stream order, @%2%O@%%" \
      -O -K >> $out.ps
  fi
  
done

# ---- Show
gmt psbasemap $rgn $proj -B+n -O >> $out.ps
# gv $out.ps &
gmt psconvert -A -E400 -Tj $out.ps
eog $out.jpg &