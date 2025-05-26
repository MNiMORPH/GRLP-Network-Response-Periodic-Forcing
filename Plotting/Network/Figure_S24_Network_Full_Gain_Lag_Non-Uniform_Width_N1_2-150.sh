#!/bin/bash

# ---- Get useful extra functions
source ../gmt_extras.sh

# ---- Set defaults
gmt_extras::set_gmt_defaults
gmt set MAP_LABEL_OFFSET 3p

# variables
out="../../Figures/Figure_S24_Network_Full_Gain_Lag_Non-Uniform_Width_N1_2-150"
proj=-JX1.5il/1.1i
basedir="../../Output/Network/Figure_S22_S23_S24_S25_Network_Full_Gain_Lag_Non-Uniform_Width"
sweepdirs=("UUN" "NUN" "UAN" "NAN")
G_z_labels=("a" "b" "c" "d")
lag_z_labels=("e" "f" "g" "h")
G_Qs_labels=("i" "j" "k" "l")
lag_Qs_labels=("m" "n" "o" "p")
G_Qs_Qw_labels=("q" "r" "s" "t")
lag_Qs_Qw_labels=("u" "v" "w" "x")
titles=("Uniform segment lengths" "Non-uniform segment lengths" "Uniform segment lengths" "Non-uniform segment lengths")


gmt psbasemap -R1/10/1/10 $proj -B+n -X-1i -K > $out.ps

for i in ${!sweepdirs[@]} ; do

  if [ $i -eq 0 ] ; then
    W="W"
  else
    W="w"
  fi
  
  rgn=-R0.003/300/-0.05/1.05
  gmt psbasemap $rgn $proj -B+n -X1.65i -Y6i -O -K >> $out.ps
  gmt psxy $basedir/z_continuous_gain.pg $rgn $proj -G197.12/64.125/125.88 -t70 -O -K >> $out.ps
  gmt psxy $basedir/z_linear_gain_rng.pg $rgn $proj -Gdimgrey -t70 -O -K >> $out.ps
  gmt psxy $basedir/z_linear_gain.pg $rgn $proj -W0.8p -O -K >> $out.ps
  gmt psxy $basedir/MC_N1_2-150/${sweepdirs[$i]}/z_gain.pg $rgn $proj -Ey+a+p0.6p,tomato+w2p -t95 -O -K >> $out.ps
  gmt psxy $basedir/MC_N1_2-150/${sweepdirs[$i]}/z_gain.pg $rgn $proj -Sc3.5p -W0.6p,tomato -t75 -O -K >> $out.ps
  echo "${G_z_labels[$i]}" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
  gmt psbasemap $rgn $proj -Btse${W} -Bx1f3p+l"Period, \textit{P} / @[\widehat{\textit{T\textsubscript{eq}}}@[ [-]" -By0.2+l"Gain, @[\textit{G\textsubscript{z}}@[ [-]" -O -K >> $out.ps
  echo "${titles[$i]}" | gmt pstext $rgn $proj -F+f8p+jCB+cCT -D0i/0.07i -N -O -K >> $out.ps

  if [ $i -eq 3 ] ; then
    rgnx=-R0/100/0/100
    projx=-JX1.5i/1.5i
    gmt_extras::plot_key_error_symbol $rgnx $projx 94 91 13 2 "-Ey+p0.6p,tomato+w2p" "Network (range)" $out
    gmt_extras::plot_key_symbol $rgnx $projx 94 91 6 "-Sc3.5p -W0.6p,tomato" "Network (outlet)" $out
  fi

  rgn_l=-R0.003/300/-0.05/1.05
  gmt psbasemap $rgn_l $proj -B+n -Y-1.2i -O -K >> $out.ps
  gmt psxy $basedir/z_continuous_lag.pl $rgn_l $proj -G197.12/64.125/125.88 -t70 -O -K >> $out.ps
  gmt psxy $basedir/z_linear_lag_rng.pl $rgn_l $proj -Gdimgrey -t70 -O -K >> $out.ps
  gmt psxy $basedir/z_linear_lag.pl $rgn $proj -W0.8p -O -K >> $out.ps
  gmt psxy $basedir/MC_N1_2-150/${sweepdirs[$i]}/z_lag.pl $rgn $proj -Ey+a+p0.6p,tomato+w2p -t95 -O -K >> $out.ps
  gmt psxy $basedir/MC_N1_2-150/${sweepdirs[$i]}/z_lag.pl $rgn $proj -Sc3.5p -W0.6p,tomato -t75 -O -K >> $out.ps
  echo "${lag_z_labels[$i]}" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
  gmt psbasemap $rgn_l $proj -Btse${W} -Bx1f3p+l"Period, \textit{P} / @[\widehat{\textit{T\textsubscript{eq}}}@[ [-]" -By0.2+l"Lag, @[\varphi\textit{\textsubscript{z} / P}@[ [-]" -O -K >> $out.ps

  if [ $i -eq 3 ] ; then
    rgnx=-R0/100/0/100
    projx=-JX1.5i/1.5i
    gmt_extras::plot_key_line $rgnx $projx 97 91 67 "-W4p,197.12/64.125/125.88 -t70" "Along-stream (range)" $out
    gmt_extras::plot_key_line $rgnx $projx 97 91 60 "-W4p,dimgrey -t70" "Upstream (range)" $out
    gmt_extras::plot_key_line $rgnx $projx 97 91 53 -W0.8p "Upstream (outlet)" $out
  fi


  rgn=-R0.003/300/-0.05/1.05
  gmt psbasemap $rgn $proj -B+n -Y-1.2i -O -K >> $out.ps
  gmt psxy $basedir/Qs_continuous_gain.pg $rgn $proj -G197.12/64.125/125.88 -t70 -O -K >> $out.ps
  gmt psxy $basedir/Qs_linear_gain.pg $rgn $proj -W0.8p -O -K >> $out.ps
  gmt psxy $basedir/MC_N1_2-150/${sweepdirs[$i]}/Qs_gain.pg $rgn $proj -Sc3.5p -W0.6p,tomato -t90 -O -K >> $out.ps
  echo "${G_Qs_labels[$i]}" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
  gmt psbasemap $rgn $proj -Btse${W} -Bx1f3p+l"Period, \textit{P} / @[\widehat{\textit{T\textsubscript{eq}}}@[ [-]" -By0.2+l"Gain, @[\textit{G\textsubscript{Q\textsubscript{s},L}}@[ [-]" -O -K >> $out.ps
  
  rgn_l=-R0.003/300/-0.05/1.05
  gmt psbasemap $rgn_l $proj -B+n -Y-1.2i -O -K >> $out.ps
  gmt psxy $basedir/Qs_continuous_lag.pl $rgn_l $proj -G197.12/64.125/125.88 -t70 -O -K >> $out.ps
  gmt psxy $basedir/Qs_linear_lag.pl $rgn_l $proj -W0.8p -O -K >> $out.ps
  gmt psxy $basedir/MC_N1_2-150/${sweepdirs[$i]}/Qs_lag.pl $rgn_l $proj -Sc3.5p -W0.6p,tomato -t90 -O -K >> $out.ps
  echo "${lag_Qs_labels[$i]}" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
  gmt psbasemap $rgn_l $proj -Btse${W} -Bx1f3p+l"Period, \textit{P} / @[\widehat{\textit{T\textsubscript{eq}}}@[ [-]" -By0.2+l"Lag, @[\varphi\textit{\textsubscript{Q\textsubscript{s},L} / P}@[ [-]" -O -K >> $out.ps

  rgn=-R0.003/300/-0.05/1.25
  gmt psbasemap $rgn $proj -B+n -Y-1.2i -O -K >> $out.ps
  gmt psxy $basedir/Qs_Qw_continuous_gain.pg $rgn $proj -G197.12/64.125/125.88 -t70 -O -K >> $out.ps
  gmt psxy $basedir/Qs_Qw_linear_gain.pg $rgn $proj -W0.8p -O -K >> $out.ps
  gmt psxy $basedir/MC_N1_2-150/${sweepdirs[$i]}/Qs_Qw_gain.pg $rgn $proj -Sc3.5p -W0.6p,tomato -t90 -O -K >> $out.ps
  echo "${G_Qs_Qw_labels[$i]}" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jBL+cBL -D0.05i/0.08i -O -K >> $out.ps
  gmt psbasemap $rgn $proj -Btse${W} -Bx1f3p+l"Period, \textit{P} / @[\widehat{\textit{T\textsubscript{eq}}}@[ [-]" -By0.2+l"Gain, @[\textit{G\textsubscript{Q\textsubscript{s},L}}@[ [-]" -O -K >> $out.ps

  rgn_l=-R0.003/300/-0.275/0.025
  gmt psbasemap $rgn_l $proj -B+n -Y-1.2i -O -K >> $out.ps
  gmt psxy $basedir/Qs_Qw_continuous_lag.pl $rgn_l $proj -G197.12/64.125/125.88 -t70 -O -K >> $out.ps
  gmt psxy $basedir/Qs_Qw_linear_lag.pl $rgn_l $proj -W0.8p -O -K >> $out.ps
  gmt psxy $basedir/MC_N1_2-150/${sweepdirs[$i]}/Qs_Qw_lag.pl $rgn_l $proj -Sc3.5p -W0.6p,tomato -t90 -O -K >> $out.ps
  echo "${lag_Qs_Qw_labels[$i]}" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jBL+cBL -D0.05i/0.08i -O -K >> $out.ps
  gmt psbasemap $rgn_l $proj -BtSe${W} -Bx1f3p+l"Period, \textit{P} / @[\widehat{\textit{T\textsubscript{eq}}}@[ [-]" -By0.05+l"Lag, @[\varphi\textit{\textsubscript{Q\textsubscript{s},L} / P}@[ [-]" -O -K >> $out.ps

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
echo "0.17 1.15 @~\144@~@%2%z@%%: Varying sediment supply" | gmt pstext $rgn $proj -F+f8p+a270 -Gwhite -N -O -K >> $out.ps

gmt psbasemap $rgn $proj -B+n -Y-2.4i -O -K >> $out.ps
echo "0.1 2.05
0.17 2.05
0.17 0.25
0.1 0.25" | gmt psxy $rgn $proj -W0.8p -O -K >> $out.ps
echo "0.17 1.15 @~\144@~@%2%Q@-s@-@%%: Varying sediment supply" | gmt pstext $rgn $proj -F+f8p+a270 -Gwhite -N -O -K >> $out.ps

gmt psbasemap $rgn $proj -B+n -Y-2.4i -O -K >> $out.ps
echo "0.1 2.05
0.17 2.05
0.17 0.25
0.1 0.25" | gmt psxy $rgn $proj -W0.8p -O -K >> $out.ps
echo "0.17 1.15 @~\144@~@%2%Q@-s@-@%%: Varying water supply" | gmt pstext $rgn $proj -F+f8p+a270 -Gwhite -N -O -K >> $out.ps

# Finalise, show
gmt psbasemap -R0/1/0/1 -JX2i -B+n -O >> $out.ps
gmt psconvert -A -E400 -Tf $out.ps
convert -density 600x600 -quality 100 -alpha remove $out.pdf $out.jpg
rm $out.ps $out.pdf
eog $out.jpg &