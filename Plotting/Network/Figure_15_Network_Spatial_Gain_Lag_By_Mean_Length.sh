#!/bin/bash

# ---- Get useful extra functions
source ../gmt_extras.sh

# ---- Set defaults
gmt_extras::set_gmt_defaults

# ---- Inputs / Output
basedir="../../Output/Network/Figure_15_Network_Spatial_Gain_Lag_By_Mean_Length"
out="../../Figures/Figure_15_Network_Spatial_Gain_Lag_By_Mean_Length"

# ---- Variables
proj=-JX1.5i
rgn=-R-10/110/0.2/0.6
# rgn_lag=-R-10/110/0.025/0.325
nets=("0" "66" "132" "199")
axes=("eW" "ew" "ew" "ew")
plan_lab=("a" "b" "c" "d")
g_lab=("e" "f" "g" "h")
l_lab=("i" "j" "k" "l")
x_max=("55" "85" "105" "130")
x_off=("1.65" "0.98" "1.44" "1.74")
projx=("0.83" "1.29" "1.59" "1.97")
titles=("1@+st@+ percentile" "33@+rd@+ percentile" "66@+th@+ percentile" "99@+th@+ percentile")

# ---- Planform domain
ymax0=$(gmt gmtinfo -C $basedir/${nets[0]}/planform.d | awk ' { print $4*1.05 } ')

# ---- Initiate
gmt psbasemap $rgn $proj -B+n -Y6i -X-0.65i -K > $out.ps

# CPT
gmt makecpt -Cviridis -T0.5/4.5/1 -I > order.cpt

for i in ${!nets[@]} ; do
  
  proj=-JX${projx[$i]}i/1.5i
  
  indir=$basedir/${nets[$i]}
  
  # ---- Planform
  ymax=$(gmt gmtinfo -C $basedir/${nets[$i]}/planform.d | awk ' { print $4*1.05 } ')
  yoff=$(echo $ymax0 $ymax | awk ' { print ($1-$2)/2 } ')
  rgn=-R-5/${x_max[$i]}/0/$ymax0
  gmt psbasemap $rgn $proj -B+n -X${x_off[$i]}i -Y3.2i -O -K >> $out.ps
  awk ' { if ($1!=">") print $1, $2+'$yoff' ; else print $0 } ' $indir/planform.d | \
    gmt psxy $rgn $proj -W1p -Corder.cpt -O -K >> $out.ps
  gmt psbasemap $rgn $proj -Btslr -Bx20+l"Downstream distance [km]" -O -K >> $out.ps
  echo "${plan_lab[$i]}" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jLT+cLT -D0.05i/-0.08i -O -K >> $out.ps
  echo "${titles[$i]}" | gmt pstext $rgn $proj -F+f8p+jCB+cCT -D0i/0.08i -N -O -K >> $out.ps

  if [ ${nets[$i]} == "199" ] ; then
    gmt psscale $rgn $proj \
      -Corder.cpt \
      -Dx1.2i/1.35i+w0.7i/0.07i+h \
      -B1+l"Stream order, @~\167@~" \
      --MAP_LABEL_OFFSET=-8p \
      --MAP_ANNOT_OFFSET=5p \
      --MAP_TICK_LENGTH=7p \
      --MAP_DEFAULT_PEN=7p \
      --MAP_TICK_PEN=1.5p \
      --FONT=16p \
      -O -K >> $out.ps
  fi

  # ---- Gain_z
  rgn=-R-5/${x_max[$i]}/0.2/0.6
  gmt psbasemap $rgn $proj -B+n -Y-1.6i -O -K >> $out.ps
  gmt psxy $indir/single_seg_U_gain.dg $rgn $proj -W0.8p,black,3_2 -O -K >> $out.ps
  gmt psxy $indir/single_seg_A_gain.dg $rgn $proj -W0.8p,dimgrey,3_3_0.8_3 -O -K >> $out.ps
  gmt psxy $indir/gain.dg $rgn $proj -W0.8p -Corder.cpt -O -K >> $out.ps
  echo ${g_lab[$i]} | \
    gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jLT+cLT -D0.05i/-0.08i -O -K >> $out.ps
  gmt psbasemap $rgn $proj -Bts${axes[$i]} \
    -Bx20+l"Downstream distance, @%2%x@%% [km]" \
    -By0.1+l"Gain, @%2%G@-z@-@%% [-]" \
    -O -K >> $out.ps
  
  # ---- Lag_z
  rgn=-R-5/${x_max[$i]}/0.025/0.325
  gmt psbasemap $rgn $proj -B+n -Y-1.6i -O -K >> $out.ps
  gmt psxy $indir/single_seg_U_lag.dl $rgn $proj -W0.8p,black,3_3 -O -K >> $out.ps
  gmt psxy $indir/single_seg_A_lag.dl $rgn $proj -W0.8p,dimgrey,3_3_0.8_3 -O -K >> $out.ps
  gmt psxy $indir/lag.dl $rgn $proj -W0.8p -Corder.cpt -O -K >> $out.ps
  echo ${l_lab[$i]} | \
    gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jLT+cLT -D0.05i/-0.08i -O -K >> $out.ps
  if [ ${nets[$i]} == "0" ] ; then
    gmt psbasemap $rgn $proj -BnS${axes[$i]} \
      -Bx20+l"@%2%x@%% [km]" \
      -By0.05+l"Lag, @~\152@~@%2%@-z@-@%% / @%2%P@%% [-]" \
      -O -K >> $out.ps
  else
    gmt psbasemap $rgn $proj -BtS${axes[$i]} \
      -Bx20+l"Downstream distance, @%2%x@%% [km]" \
      -By0.05+l"Lag, @~\152@~@%2%@-z@-@%% / @%2%P@%% [-]" \
      -O -K >> $out.ps
    # gmt psbasemap $rgn $proj -BnS${axes[$i]} \
    #   -Bx20+l"Downstream distance, @%2%x@%% [km]" \
    #   -By0.05+l"Lag, @~\152@~@%2%@-z@-@%% / @%2%P@%% [-]" \
    #   --FONT=dimgrey \
    #   --MAP_FRAME_PEN=dimgrey \
    #   --MAP_TICK_PEN_PRIMARY=dimgrey \
    #   -O -K >> $out.ps 
  fi

  if [ $i -eq 3 ] ; then
    gmt_extras::plot_key_multi_line $rgn $proj 0 12.5 0.085 -W0.8p "Network" $out order.cpt "4 3 2 1"
    gmt_extras::plot_key_line $rgn $proj 0 12.5 0.065 -W0.8p,3_2 "Upstream supply" $out
    gmt_extras::plot_key_line $rgn $proj 0 12.5 0.045 -W0.8p,dimgrey,3_3.1_0.8_3.1_3 "Along stream supply" $out
  fi

done

rgn=-R0/600/0/100
proj=-JX6i/1i
gmt psbasemap $rgn $proj -B+n -Y4.8i -X-4.16i -O -K >> $out.ps
echo "5 37.5
45 37.5
>
10 34.5
5 37.5
10 40.5" | gmt psxy $rgn $proj -W1p -O -K >> $out.ps
echo "45 45 Shorter mean length" | gmt pstext $rgn $proj -F+f8p,Helvetica-Bold+jLM -D0.03i/0i -O -K >> $out.ps
echo "45 30 More compact" | gmt pstext $rgn $proj -F+f8p,Helvetica-Bold+jLM -D0.03i/0i -O -K >> $out.ps

gmt psbasemap $rgn $proj -B+n -X4.13i -O -K >> $out.ps
echo "195 37.5
155 37.5
>
190 34.5
195 37.5
190 40.5" | gmt psxy $rgn $proj -W1p -O -K >> $out.ps
echo "155 45 Longer mean length" | gmt pstext $rgn $proj -F+f8p,Helvetica-Bold+jRM -D-0.03i/0i -O -K >> $out.ps
echo "155 30 More elongate" | gmt pstext $rgn $proj -F+f8p,Helvetica-Bold+jRM -D-0.03i/0i -O -K >> $out.ps

# ---- Show
gmt psbasemap $rgn $proj -B+n -O >> $out.ps
# gv $out.ps &
gmt psconvert -A -E400 -Tj $out.ps
rm $out.ps order.cpt
eog $out.jpg &