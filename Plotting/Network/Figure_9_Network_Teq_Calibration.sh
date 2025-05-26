#!/bin/bash

# ---- Get useful extra functions
source ../gmt_extras.sh

# ---- Set defaults
gmt_extras::set_gmt_defaults

# variables
out="../../Figures/Figure_9_Network_Teq_Calibration"
rgn=-R0.003/300/-0.05/1.05
proj=-JX1.5il/1.5i
rgnx=-R0/100/0/100
projx=-JX1.5i/1.5i
basedir="../../Output/Network/Figure_9_S4_Network_Teq_Calibration"
sweepdirs=("UUU" "NUU" "UAU" "NAU")
L_labs=("a" "b" "c" "d")
Le_labs=("e" "f" "g" "h")
titles=("Uniform segment lengths" "Non-uniform segment lengths" "Uniform segment lengths" "Non-uniform segment lengths")

# plot
gmt psbasemap $rgn $proj -B+n -K > $out.ps

for i in ${!sweepdirs[@]} ; do

  if [ $i -eq 0 ] ; then
    W="W"
  else
    W="w"
  fi

  gmt psbasemap $rgn $proj -B+n -X0.6i -Y1.72i -O -K >> $out.ps
  gmt psxy $basedir/continuous_gain.pg $rgn $proj -Glightgrey -W0.8p,lightgrey -O -K >> $out.ps
  gmt psxy $basedir/linear_gain.pg $rgn $proj -W0.8p -O -K >> $out.ps
  gmt psxy $basedir/MC_N1_40/${sweepdirs[$i]}/gain_L.pg $rgn $proj -Sc3.5p -W0.6p,steelblue -t75 -O -K >> $out.ps
  echo "${L_labs[$i]}" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
  gmt psbasemap $rgn $proj -BtSe${W} -Bx1f3p+l"Period, @%2%P@%% / @%2%T@-eq,max@-@%% [-]" -By0.2+l"Gain, @[\textit{G\textsubscript{Q\textsubscript{s},L}}@[ [-]" -O -K >> $out.ps
  echo "${titles[$i]}" | gmt pstext $rgn $proj -F+f8p+jCB+cCT -D0i/0.07i -N -O -K >> $out.ps

  if [ $i -eq 0 ] ; then
    gmt_extras::plot_key_line $rgnx $projx 3 9 77 -W4p,lightgrey "Along-stream" $out
    gmt_extras::plot_key_line $rgnx $projx 3 9 69 -W0.8p "Upstream" $out
    gmt_extras::plot_key_symbol $rgnx $projx 6 9 61 "-Sc3p -W0.8p,steelblue" "Network" $out
  fi

  proj_in=-JX0.35i
  rgn_in=-R0/200/0/50
  gmt psbasemap $rgn_in $proj_in -B+n -Y0.28i -X1.05i -O -K >> $out.ps
  gmt pshistogram $basedir/MC_N1_40/${sweepdirs[$i]}/Teq_max.t $rgn_in $proj_in -Gsteelblue -W0.1p,steelblue -T15+n -O -K >> $out.ps
  gmt psbasemap $rgn_in $proj_in \
    -BSW -Bx100+l"@[\textit{T\textsubscript{eq,max}}@[ [kyr]" -By25 \
    --MAP_TICK_LENGTH_PRIMARY=2p \
    --MAP_FRAME_PEN=0.8p \
    --FONT_LABEL=5p \
    --FONT_ANNOT_PRIMARY=5p \
    --MAP_LABEL_OFFSET=2p \
    -O -K >> $out.ps

  gmt psbasemap $rgn $proj -B+n -Y-2.28i -X-1.05i -O -K >> $out.ps
  gmt psxy $basedir/continuous_gain.pg $rgn $proj -Glightgrey -W0.8p,lightgrey -O -K >> $out.ps
  gmt psxy $basedir/linear_gain.pg $rgn $proj -W0.8p -O -K >> $out.ps
  gmt psxy $basedir/MC_N1_40/${sweepdirs[$i]}/gain_Le.pg $rgn $proj -Sc3.5p -W0.6p,steelblue -t75 -O -K >> $out.ps
  echo "${Le_labs[$i]}" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
  gmt psbasemap $rgn $proj -BtSe${W} -Bx1f3p+l"Period, \textit{P} / @[\widehat{\textit{T\textsubscript{eq}}}@[ [-]" -By0.2+l"Gain, @[\textit{G\textsubscript{Q\textsubscript{s},L}}@[ [-]" -O -K >> $out.ps

  proj_in=-JX0.35i
  rgn_in=-R0/200/0/50
  gmt psbasemap $rgn_in $proj_in -B+n -Y0.28i -X1.05i -O -K >> $out.ps
  gmt pshistogram $basedir/MC_N1_40/${sweepdirs[$i]}/Teq.t $rgn_in $proj_in -Gsteelblue -W0.1p,steelblue -T15+n -O -K >> $out.ps
  gmt psbasemap $rgn_in $proj_in \
    -BSW -Bx100+l"@[\widehat{\textit{T\textsubscript{eq}}}@[ [kyr]" -By25 \
    --MAP_TICK_LENGTH_PRIMARY=2p \
    --MAP_FRAME_PEN=0.8p \
    --FONT_LABEL=5p \
    --FONT_ANNOT_PRIMARY=5p \
    --MAP_LABEL_OFFSET=2p \
    -O -K >> $out.ps
done

rgn=-R0/3.15/0/3.15
proj=-JX3.15i
gmt psbasemap $rgn $proj -B+n -Y1.72i -X-6i -O -K >> $out.ps
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


# Finalise, show
gmt psbasemap -R0/1/0/1 -JX2i -B+n -O >> $out.ps
gmt psconvert -A -E400 -Tf $out.ps
convert -density 600x600 -quality 100 -alpha remove $out.pdf $out.jpg
rm $out.ps $out.pdf
eog $out.jpg &