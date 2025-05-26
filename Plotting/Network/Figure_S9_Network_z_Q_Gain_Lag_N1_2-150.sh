#!/bin/bash

# ---- Get useful extra functions
source ../gmt_extras.sh

# ---- Set defaults
gmt_extras::set_gmt_defaults
gmt set MAP_LABEL_OFFSET 3p

# variables
out="../../Figures/Figure_S9_Network_z_Q_Gain_Lag_N1_2-150"
proj=-JX1.5il/1.5i
basedir="../../Output/Network/Figure_11_S7_S8_S9_Network_Full_Gain_Lag"
sweepdirs=("UUU" "NUU" "UAU" "NAU")
G_z_labels=("a" "b" "c" "d")
lag_z_labels=("e" "f" "g" "h")
titles=("Uniform segment lengths" "Non-uniform segment lengths" "Uniform segment lengths" "Non-uniform segment lengths")


gmt psbasemap -R1/10/1/10 $proj -B+n -X-1i -K > $out.ps

for i in ${!sweepdirs[@]} ; do

  if [ $i -eq 0 ] ; then
    W="W"
  else
    W="w"
  fi
  
  rgn=-R0.003/300/-0.05/1.05
  gmt psbasemap $rgn $proj -B+n -X1.65i -Y1.65i -O -K >> $out.ps
  gmt psxy $basedir/z_Q_continuous_gain.pg $rgn $proj -G197.12/64.125/125.88 -t70 -O -K >> $out.ps
  gmt psxy $basedir/z_linear_gain_rng.pg $rgn $proj -Gdimgrey -t70 -O -K >> $out.ps
  gmt psxy $basedir/z_linear_gain.pg $rgn $proj -W0.8p -O -K >> $out.ps
  gmt psxy $basedir/MC_N1_2-150/${sweepdirs[$i]}/z_Q_gain.pg $rgn $proj -Ey+a+p0.6p,tomato+w2p -t95 -O -K >> $out.ps
  gmt psxy $basedir/MC_N1_2-150/${sweepdirs[$i]}/z_Q_gain.pg $rgn $proj -Sc3.5p -W0.6p,tomato -t75 -O -K >> $out.ps
  echo "${G_z_labels[$i]}" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
  gmt psbasemap $rgn $proj -Btse${W} -Bx1f3p+l"Period, \textit{P} / @[\widehat{\textit{T\textsubscript{eq}}}@[ [-]" -By0.2+l"Gain, @[\textit{G\textsubscript{z}}@[ [-]" -O -K >> $out.ps
  echo "${titles[$i]}" | gmt pstext $rgn $proj -F+f8p+jCB+cCT -D0i/0.07i -N -O -K >> $out.ps

  rgn_l=-R0.003/300/-0.05/1.05
  gmt psbasemap $rgn_l $proj -B+n -Y-1.65i -O -K >> $out.ps
  gmt psxy $basedir/z_Q_continuous_lag.pl $rgn_l $proj -G197.12/64.125/125.88 -t70 -O -K >> $out.ps
  gmt psxy $basedir/z_linear_lag_rng.pl $rgn_l $proj -Gdimgrey -t70 -O -K >> $out.ps
  gmt psxy $basedir/z_linear_lag.pl $rgn $proj -W0.8p -O -K >> $out.ps
  gmt psxy $basedir/MC_N1_2-150/${sweepdirs[$i]}/z_Q_lag.pl $rgn $proj -Ey+a+p0.6p,tomato+w2p -t95 -O -K >> $out.ps
  gmt psxy $basedir/MC_N1_2-150/${sweepdirs[$i]}/z_Q_lag.pl $rgn $proj -Sc3.5p -W0.6p,tomato -t75 -O -K >> $out.ps
  echo "${lag_z_labels[$i]}" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
  gmt psbasemap $rgn_l $proj -BnSe${W} -Bx1f3p+l"Period, \textit{P} / @[\widehat{\textit{T\textsubscript{eq}}}@[ [-]" -By0.2+l"Lag, @~\152@~@%2%@-z@-@%% / @%2%P@%% [-]" -O -K >> $out.ps

done

rgn=-R0/3.15/0/3.15
proj=-JX3.15i
gmt psbasemap $rgn $proj -B+n -Y1.65i -X-4.95i -O -K >> $out.ps
echo "0.75 1.7
0.75 1.75
2.4 1.75
2.4 1.7" | gmt psxy $rgn $proj -W0.8p -O -K >> $out.ps
echo "Upstream supply" | gmt pstext $rgn $proj -F+f8p+jCM+cCB -D0i/1.75i -Gwhite -N -O -K >> $out.ps

gmt psbasemap $rgn $proj -B+n -X3.3i -O -K >> $out.ps
echo "0.75 1.7
0.75 1.75
2.4 1.75
2.4 1.7" | gmt psxy $rgn $proj -W0.8p -O -K >> $out.ps
echo "Along-stream supply" | gmt pstext $rgn $proj -F+f8p+jCM+cCB -D0i/1.75i -Gwhite -N -O -K >> $out.ps

gmt psbasemap $rgn $proj -B+n -Y-1.65i -X3.15i -O -K >> $out.ps
echo "0.1 2.4
0.17 2.4
0.17 0.75
0.1 0.75" | gmt psxy $rgn $proj -W0.8p -O -K >> $out.ps
echo "0.17 1.575 @~\144@~@%2%z@%%: Varying water supply" | gmt pstext $rgn $proj -F+f8p+a270 -Gwhite -N -O -K >> $out.ps

# Finalise, show
gmt psbasemap -R0/1/0/1 -JX2i -B+n -O >> $out.ps
gmt psconvert -A -E400 -Tf $out.ps
convert -density 600x600 -quality 100 -alpha remove $out.pdf $out.jpg
rm $out.ps $out.pdf
eog $out.jpg &