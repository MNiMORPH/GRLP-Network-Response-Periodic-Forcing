#!/bin/bash -i

# Set defaults
set_gmt_defaults

# variables
out=calibration
rgn=-R0.003/300/-0.05/1.05
proj=-JX1.5il/1.5i
basedir="../../output/network/calibration"
sweepdirs=("m20_fix_seg_length" "m40_fix_seg_length" "m2-100_fix_seg_length" "m40_rnd_seg_length")
L_labs=("a" "c" "e" "g")
Le_labs=("b" "d" "f" "h")

# CPT
gmt makecpt -Cviridis -T0/100/1 -Z -D > mag.cpt

# plot
gmt psbasemap $rgn $proj -B+n -X3i -Y8i -K > $out.ps

for i in ${!sweepdirs[@]} ; do

  if [ $i -eq 3 ] ; then
    S="S"
  else
    S="s"
  fi

  gmt psbasemap $rgn $proj -B+n -X-1.7i -Y-1.7i -O -K >> $out.ps
  gmt psxy $basedir/continuous_gain.pg $rgn $proj -Glightgrey -W0.8p,lightgrey -O -K >> $out.ps
  gmt psxy $basedir/linear_gain.pg $rgn $proj -W0.8p -O -K >> $out.ps
  gmt psxy $basedir/${sweepdirs[$i]}/gain_L.pg $rgn $proj -Sc3p -W0.8p+cl -Cmag.cpt -t95 -O -K >> $out.ps
  echo "${L_labs[$i]}" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
  gmt psbasemap $rgn $proj -Bn${S}eW -Bx1f3p+l"Period, @%2%P@%% / @%2%T@-eq@-@%% [-]" -By0.2+l"Gain, @%2%G@-Qs,L@-@%% [-]" -O -K >> $out.ps

  if [ $i -eq 0 ] ; then
    echo "1 1.1 @%2%T@-eq@-@%% = @%2%L@%%@+2@+ / @~\341\153\361@~" | \
      gmt pstext $rgn $proj -F+f9p+jBC -N -D0i/0.05i -O -K >> $out.ps
  fi

  if [ $i -eq 3 ] ; then
    gmt psscale $rgn $proj \
      -Cmag.cpt \
      -Dx0.85i/0.08i+w0.5i/0.06i+h+m+ef \
      -B50+l"Magnitude, @~\155@~ [-]" \
      --FONT_LABEL=6p \
      --FONT_ANNOT_PRIMARY=6p \
      --MAP_LABEL_OFFSET=4p \
      -O -K >> $out.ps
  fi

  gmt psbasemap $rgn $proj -B+n -X1.7i -O -K >> $out.ps
  gmt psxy $basedir/continuous_gain.pg $rgn $proj -Glightgrey -W0.8p,lightgrey -O -K >> $out.ps
  gmt psxy $basedir/linear_gain.pg $rgn $proj -W0.8p -O -K >> $out.ps
  gmt psxy $basedir/${sweepdirs[$i]}/gain_Le.pg $rgn $proj -Sc3p -W0.8p+cl -Cmag.cpt -t95 -O -K >> $out.ps
  echo "${Le_labs[$i]}" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
  gmt psbasemap $rgn $proj -Bn${S}ew -Bx1f3p+l"Period, @%2%P@%% / @%2%T@-eq@-@%% [-]" -By0.2+l"Gain, @%2%G@-Qs,L@-@%% [-]" -O -K >> $out.ps

  if [ $i -eq 0 ] ; then
    echo "1 1.1 @%2%T@-eq@-@%% = @%2%L@-e@-@%%@+2@+ / @~\341\153\361@~" | \
      gmt pstext $rgn $proj -F+f9p+jBC -N -D0i/0.05i -O -K >> $out.ps
  fi

  if [ $i -eq 3 ] ; then
    echo "> -W0.8p
100 0.12
200 0.12
> -W4p,lightgrey
100 0.03
200 0.03" | gmt psxy $rgn $proj -O -K >> $out.ps
    echo "141 0.21 50" | gmt psxy $rgn $proj -Sc3p -W0.8p+cl -Cmag.cpt -O -K >> $out.ps
    echo "100 0.12 Upstream supply
100 0.03 Continuous supply
100 0.21 Network" | gmt pstext $rgn $proj -F+f6p+jRM -D-0.02i/0i -O -K >> $out.ps
  fi

done

# Finalise, show
gmt psbasemap -R0/1/0/1 -JX2i -B+n -O >> $out.ps
gmt psconvert -A -E400 -Tf $out.ps
convert -density 600x600 -quality 100 -alpha remove $out.pdf $out.jpg
rm $out.ps
eog $out.jpg &