#!/bin/bash -i

# Set defaults
set_gmt_defaults

# variables
rgn=-R0.003/300/-0.05/1.05
proj=-JX3il/2i
basedir="../../output/network/calibration"
sweepdir="m40_fix_seg_length_no_internal"

out=simple_calibration_blank
gmt psbasemap $rgn $proj -B+n -K > $out.ps
gmt psxy $basedir/linear_gain.pg $rgn $proj -W0.8p -O -K >> $out.ps
gmt psbasemap $rgn $proj -BnSeW -Bx1f3p+l"Period, @%2%P@%% / @%2%T@-eq@-@%% [-]" -By0.2+l"Gain, @%2%G@-Qs,L@-@%% [-]" -O -K >> $out.ps

# Finalise, show
gmt psbasemap -R0/1/0/1 -JX2i -B+n -O >> $out.ps
gmt psconvert -A -E300 -Tf $out.ps
convert -density 300x300 -quality 100 -alpha remove $out.pdf $out.jpg
rm $out.ps
eog $out.jpg

# plot single
out=simple_calibration_single_L
gmt psbasemap $rgn $proj -B+n -K > $out.ps
gmt psxy $basedir/linear_gain.pg $rgn $proj -W0.8p -O -K >> $out.ps
head -n7 $basedir/$sweepdir/gain_L.pg | \
  gmt psxy $rgn $proj -Sc4p -G31/119/180 -t25 -O -K >> $out.ps
head -n7 $basedir/$sweepdir/gain_L.pg | \
  gmt psxy $rgn $proj -Sc4p -W0.8p,31/119/180 -O -K >> $out.ps
gmt psbasemap $rgn $proj -BnSeW -Bx1f3p+l"Period, @%2%P@%% / @%2%T@-eq@-@%% [-]" -By0.2+l"Gain, @%2%G@-Qs,L@-@%% [-]" -O -K >> $out.ps

# Finalise, show
gmt psbasemap -R0/1/0/1 -JX2i -B+n -O >> $out.ps
gmt psconvert -A -E300 -Tf $out.ps
convert -density 300x300 -quality 100 -alpha remove $out.pdf $out.jpg
rm $out.ps
eog $out.jpg

# plot single
out=simple_calibration_single_Le
gmt psbasemap $rgn $proj -B+n -K > $out.ps
gmt psxy $basedir/linear_gain.pg $rgn $proj -W0.8p -O -K >> $out.ps
head -n7 $basedir/$sweepdir/gain_L.pg | \
  gmt psxy $rgn $proj -Sc4p -Glightgrey -t25 -O -K >> $out.ps
head -n7 $basedir/$sweepdir/gain_L.pg | \
  gmt psxy $rgn $proj -Sc4p -W0.8p,lightgrey -O -K >> $out.ps
head -n7 $basedir/$sweepdir/gain_Le.pg | \
  gmt psxy $rgn $proj -Sc4p -G31/119/180 -t25 -O -K >> $out.ps
head -n7 $basedir/$sweepdir/gain_Le.pg | \
  gmt psxy $rgn $proj -Sc4p -W0.8p,31/119/180 -O -K >> $out.ps
gmt psbasemap $rgn $proj -BnSeW -Bx1f3p+l"Period, @%2%P@%% / @%2%T@-eq@-@%% [-]" -By0.2+l"Gain, @%2%G@-Qs,L@-@%% [-]" -O -K >> $out.ps

# Finalise, show
gmt psbasemap -R0/1/0/1 -JX2i -B+n -O >> $out.ps
gmt psconvert -A -E300 -Tf $out.ps
convert -density 300x300 -quality 100 -alpha remove $out.pdf $out.jpg
rm $out.ps
eog $out.jpg

# plot all
out=simple_calibration_all_L
gmt psbasemap $rgn $proj -B+n -K > $out.ps
gmt psxy $basedir/linear_gain.pg $rgn $proj -W0.8p -O -K >> $out.ps
gmt psxy $basedir/$sweepdir/gain_L.pg $rgn $proj -Sc4p -G31/119/180 -t85 -O -K >> $out.ps
gmt psxy $basedir/$sweepdir/gain_L.pg $rgn $proj -Sc4p -W0.8p,31/119/180 -t80 -O -K >> $out.ps
gmt psbasemap $rgn $proj -BnSeW -Bx1f3p+l"Period, @%2%P@%% / @%2%T@-eq@-@%% [-]" -By0.2+l"Gain, @%2%G@-Qs,L@-@%% [-]" -O -K >> $out.ps

# Finalise, show
gmt psbasemap -R0/1/0/1 -JX2i -B+n -O >> $out.ps
gmt psconvert -A -E300 -Tf $out.ps
convert -density 300x300 -quality 100 -alpha remove $out.pdf $out.jpg
rm $out.ps
eog $out.jpg


# plot all
out=simple_calibration_all_Le
gmt psbasemap $rgn $proj -B+n -K > $out.ps
gmt psxy $basedir/linear_gain.pg $rgn $proj -W0.8p -O -K >> $out.ps
gmt psxy $basedir/$sweepdir/gain_L.pg $rgn $proj -Sc4p -Glightgrey -t85 -O -K >> $out.ps
gmt psxy $basedir/$sweepdir/gain_L.pg $rgn $proj -Sc4p -W0.8p,lightgrey -t80 -O -K >> $out.ps
gmt psxy $basedir/$sweepdir/gain_Le.pg $rgn $proj -Sc4p -G31/119/180 -t85 -O -K >> $out.ps
gmt psxy $basedir/$sweepdir/gain_Le.pg $rgn $proj -Sc4p -W0.8p,31/119/180 -t80 -O -K >> $out.ps
gmt psbasemap $rgn $proj -BnSeW -Bx1f3p+l"Period, @%2%P@%% / @%2%T@-eq@-@%% [-]" -By0.2+l"Gain, @%2%G@-Qs,L@-@%% [-]" -O -K >> $out.ps

# Finalise, show
gmt psbasemap -R0/1/0/1 -JX2i -B+n -O >> $out.ps
gmt psconvert -A -E300 -Tf $out.ps
convert -density 300x300 -quality 100 -alpha remove $out.pdf $out.jpg
rm $out.ps
eog $out.jpg