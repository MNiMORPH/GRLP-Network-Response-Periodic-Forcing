#!/bin/bash

# ---- Get useful extra functions
source ../gmt_extras.sh

# ---- Set defaults
gmt_extras::set_gmt_defaults

# ---- Inputs / Output
basedir="../../Output/Network/Figure_14_Network_Spatial_Gain_Lag"
out="../../Figures/Figure_14_Network_Spatial_Gain_Lag"

# ---- Variables
proj=-JX1.5i/1.1i
rgn=-R-10/110/-0.05/1.05
rgn_lag=-R-10/110/-0.025/0.425
nets=("UUU" "NUU" "UAU" "NAU")
axes=("eW" "ew" "ew" "ew")
titles=("Uniform segment lengths" "Non-uniform segment lengths" "Uniform segment lengths" "Non-uniform segment lengths")

# ---- Initiate
gmt psbasemap $rgn $proj -B+n -Y9i -X5.6i -K > $out.ps

# CPT
gmt makecpt -Cviridis -T0.5/4.5/1 -I > order.cpt

# for p in $(seq 0 2) ; do
for p in "fast" "medium" "slow" ; do

  gmt psbasemap $rgn $proj -B+n -X-6.6i -Y-2.4i -O -K >> $out.ps

  if [ $p == "fast" ] ; then
    g_lab=("a" "b" "c" "d")
    l_lab=("e" "f" "g" "h")
  elif [ $p == "medium" ] ; then
    g_lab=("i" "j" "k" "l")
    l_lab=("m" "n" "o" "p")
  else
    g_lab=("q" "r" "s" "t")
    l_lab=("u" "v" "w" "x")
  fi

  for i in ${!nets[@]} ; do

    indir=$basedir/${nets[$i]}

    # ---- Gain_z
    gmt psbasemap $rgn $proj -B+n -X1.65i -Y1.2i -O -K >> $out.ps
    gmt psxy $indir/$p/single_seg_U_gain.dg $rgn $proj -W0.8p,black,3_2 -O -K >> $out.ps
    gmt psxy $indir/$p/single_seg_A_gain.dg $rgn $proj -W0.8p,dimgrey,3_3_0.8_3 -O -K >> $out.ps
    gmt psxy $indir/$p/gain.dg $rgn $proj -W0.8p -Corder.cpt -O -K >> $out.ps
    echo ${g_lab[$i]} | \
      gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jLT+cLT -D0.05i/-0.08i -O -K >> $out.ps
    gmt psbasemap $rgn $proj -Bts${axes[$i]} \
        -Bx20+l"Downstream distance [km]" \
        -By0.2+l"Gain, @%2%G@-z@-@%% [-]" \
        -O -K >> $out.ps

    if [ $p == "fast" ] ; then
      echo "${titles[$i]}" | gmt pstext $rgn $proj -F+f8p+jCB+cCT -D0i/0.07i -N -O -K >> $out.ps   
    fi 
    if [ $p == "slow" ] && [ $i -eq 3 ] ; then
      gmt_extras::plot_key_multi_line $rgn $proj 105 90.5 0.25 -W0.8p "Network" $out order.cpt "4 3 2 1"
      gmt_extras::plot_key_line $rgn $proj 105 90.5 0.15 -W0.8p,3_2 "Upstream supply" $out
      gmt_extras::plot_key_line $rgn $proj 105 90.5 0.05 -W0.8p,dimgrey,3_3.1_0.8_3.1_3 "Along-stream supply" $out
    fi


    # ---- Lag_z
    gmt psbasemap $rgn_lag $proj -B+n -Y-1.2i -O -K >> $out.ps
    gmt psxy $indir/$p/single_seg_U_lag.dl $rgn_lag $proj -W0.8p,black,3_3 -O -K >> $out.ps
    gmt psxy $indir/$p/single_seg_A_lag.dl $rgn_lag $proj -W0.8p,dimgrey,3_3_0.8_3 -O -K >> $out.ps
    gmt psxy $indir/$p/lag.dl $rgn_lag $proj -W0.8p -Corder.cpt -O -K >> $out.ps
    echo ${l_lab[$i]} | \
      gmt pstext $rgn_lag $proj -F+f11p,Helvetica-Bold,black+jLT+cLT -D0.05i/-0.08i -O -K >> $out.ps
      
    if [ $p == "slow" ] ; then
      S="S"
    else
      S="s"
    fi
    gmt psbasemap $rgn_lag $proj -Bt${S}${axes[$i]} \
      -Bx20+l"Downstream distance, @%2%x@%% [km]" \
      -By0.1+l"Lag, @~\152@~@%2%@-z@-@%% / @%2%P@%% [-]" \
      -O -K >> $out.ps
        
    if [ $p == "slow" ] && [ ${nets[$i]} == "NAU" ] ; then
      gmt psscale $rgn $proj \
        -Corder.cpt \
        -Dx0.7i/0.95i+w0.7i/0.07i+h \
        -B1+l"Stream order, @~\167@~" \
        --MAP_LABEL_OFFSET=-8p \
        --MAP_ANNOT_OFFSET=5p \
        --MAP_TICK_LENGTH=7p \
        --MAP_DEFAULT_PEN=7p \
        --MAP_TICK_PEN=1.5p \
        --FONT=16p \
        -O -K >> $out.ps
    fi

  done

done

rgn=-R0/3.15/0/3.15
proj=-JX3.15i
gmt psbasemap $rgn $proj -B+n -Y6i -X-4.95i -O -K >> $out.ps
echo "0.75 1.3
0.75 1.35
2.4 1.35
2.4 1.3" | gmt psxy $rgn $proj -W0.8p -O -K >> $out.ps
echo "Upstream supply" | gmt pstext $rgn $proj -F+f8p+jCM+cCB -D0i/1.35i -Gwhite -N -O -K >> $out.ps

gmt psbasemap $rgn $proj -B+n -X3.3i -O -K >> $out.ps
echo "0.75 1.3
0.75 1.35
2.4 1.35
2.4 1.3" | gmt psxy $rgn $proj -W0.8p -O -K >> $out.ps
echo "Along-stream supply" | gmt pstext $rgn $proj -F+f8p+jCM+cCB -D0i/1.35i -Gwhite -N -O -K >> $out.ps

gmt psbasemap $rgn $proj -B+n -Y-1.2i -X3.15i -O -K >> $out.ps
echo "0.1 2.05
0.17 2.05
0.17 0.25
0.1 0.25" | gmt psxy $rgn $proj -W0.8p -O -K >> $out.ps
echo "0.17 1.15 @%2%P@%% = @%2%T@-eq@-@%% / 10" | gmt pstext $rgn $proj -F+f8p+a270 -Gwhite -N -O -K >> $out.ps

gmt psbasemap $rgn $proj -B+n -Y-2.4i -O -K >> $out.ps
echo "0.1 2.05
0.17 2.05
0.17 0.25
0.1 0.25" | gmt psxy $rgn $proj -W0.8p -O -K >> $out.ps
echo "0.17 1.15 @%2%P@%% = @%2%T@-eq@-@%%" | gmt pstext $rgn $proj -F+f8p+a270 -Gwhite -N -O -K >> $out.ps

gmt psbasemap $rgn $proj -B+n -Y-2.4i -O -K >> $out.ps
echo "0.1 2.05
0.17 2.05
0.17 0.25
0.1 0.25" | gmt psxy $rgn $proj -W0.8p -O -K >> $out.ps
echo "0.17 1.15 @%2%P@%% = @%2%T@-eq@-@%% x 10" | gmt pstext $rgn $proj -F+f8p+a270 -Gwhite -N -O -K >> $out.ps

# ---- Show
gmt psbasemap $rgn $proj -B+n -O >> $out.ps
# gv $out.ps &
gmt psconvert -A -E400 -Tj $out.ps
rm $out.ps order.cpt
eog $out.jpg &