#!/bin/bash -i

# Set defaults
set_gmt_defaults
gmt set PS_PAGE_ORIENTATION landscape

# variables
out=sweep
proj=-JX1.3il/1.3i
basedir="../../output/network/full_sweep"
sweepdirs=("m20_fix_seg_length" "m40_fix_seg_length" "m2-100_fix_seg_length" "m40_rnd_seg_length")

# CPT
gmt makecpt -Cviridis -T0/100/1 -Z -D > mag.cpt

gmt psbasemap -R1/10/1/10 $proj -B+n -X9.7i -Y8i -K > $out.ps

for i in ${!sweepdirs[@]} ; do

  if [ $i -eq 3 ] ; then
    S="S"
  else
    S="s"
  fi
  
  rgn=-R0.003/300/-0.05/1.25
  gmt psbasemap $rgn $proj -B+n -X-8.95i -Y-1.45i -O -K >> $out.ps
  gmt psxy $basedir/z_continuous_gain.pg $rgn $proj -Glightgrey -W0.8p,lightgrey -O -K >> $out.ps
  gmt psxy $basedir/z_linear_gain.pg $rgn $proj -W0.8p -O -K >> $out.ps
  gmt psxy $basedir/${sweepdirs[$i]}/z_gain.pg $rgn $proj -Sc3p -W0.8p+cl -Cmag.cpt -Ey+a+p0.8p+w2p+cl -t95 -O -K >> $out.ps
  gmt psbasemap $rgn $proj -Bn${S}eW -Bx1f3p+l"Period, @%2%P@%% / @%2%T@-eq@-@%% [-]" -By0.2+l"Gain, @%2%G@-z@-@%% [-]" -O -K >> $out.ps

  rgn_l=-R0.003/300/-0.05/1.05
  gmt psbasemap $rgn_l $proj -B+n -X1.45i -O -K >> $out.ps
  gmt psxy $basedir/z_continuous_lag.pl $rgn_l $proj -Glightgrey -W0.8p,lightgrey -O -K >> $out.ps
  gmt psxy $basedir/z_linear_lag.pl $rgn_l $proj -W0.8p -O -K >> $out.ps
  gmt psxy $basedir/${sweepdirs[$i]}/z_lag.pl $rgn_l $proj -Sc3p -W0.8p+cl -Cmag.cpt -Ey+a+p0.8p+w2p+cl -t95 -O -K >> $out.ps
  gmt psbasemap $rgn_l $proj -Bn${S}Ew -Bx1f3p+l"Period, @%2%P@%% / @%2%T@-eq@-@%% [-]" -By0.2+l"Lag, @~\152@~@%2%@-z@-@%% / @%2%P@%% [-]" -O -K >> $out.ps

  gmt psbasemap $rgn $proj -B+n -X2.3i -O -K >> $out.ps
  gmt psxy $basedir/Qs_continuous_gain.pg $rgn $proj -Glightgrey -W0.8p,lightgrey -O -K >> $out.ps
  gmt psxy $basedir/Qs_linear_gain.pg $rgn $proj -W0.8p -O -K >> $out.ps
  gmt psxy $basedir/${sweepdirs[$i]}/Qs_gain.pg $rgn $proj -Sc3p -W0.8p+cl -Cmag.cpt -t95 -O -K >> $out.ps
  gmt psbasemap $rgn $proj -Bn${S}eW -Bx1f3p+l"Period, @%2%P@%% / @%2%T@-eq@-@%% [-]" -By0.2+l"Gain, @%2%G@-Qs,L@-@%% [-]" -O -K >> $out.ps

  rgn_l=-R0.003/300/-0.05/1.05
  gmt psbasemap $rgn_l $proj -B+n -X1.45i -O -K >> $out.ps
  gmt psxy $basedir/Qs_continuous_lag.pl $rgn_l $proj -Glightgrey -W0.8p,lightgrey -O -K >> $out.ps
  gmt psxy $basedir/Qs_linear_lag.pl $rgn_l $proj -W0.8p -O -K >> $out.ps
  gmt psxy $basedir/${sweepdirs[$i]}/Qs_lag.pl $rgn_l $proj -Sc3p -W0.8p+cl -Cmag.cpt -t95 -O -K >> $out.ps
  gmt psbasemap $rgn_l $proj -Bn${S}Ew -Bx1f3p+l"Period, @%2%P@%% / @%2%T@-eq@-@%% [-]" -By0.2+l"Lag, @~\152@~@%2%@-Qs,L@-@%% / @%2%P@%% [-]" -O -K >> $out.ps

  gmt psbasemap $rgn $proj -B+n -X2.3i -O -K >> $out.ps
  gmt psxy $basedir/Qs_Qw_continuous_gain.pg $rgn $proj -Glightgrey -W0.8p,lightgrey -O -K >> $out.ps
  gmt psxy $basedir/Qs_Qw_linear_gain.pg $rgn $proj -W0.8p -O -K >> $out.ps
  if [ $i -eq 3 ] ; then
    gmt psxy $basedir/${sweepdirs[$i]}/Qs_Qw_gain.pg $rgn $proj -Sc3p -W0.8p+cl -Cmag.cpt -t95 -O -K >> $out.ps
  fi
  gmt psbasemap $rgn $proj -Bn${S}eW -Bx1f3p+l"Period, @%2%P@%% / @%2%T@-eq@-@%% [-]" -By0.2+l"Gain, @%2%G@-Qs,L@-@%% [-]" -O -K >> $out.ps

  rgn_l=-R0.003/300/-0.275/0.025
  gmt psbasemap $rgn_l $proj -B+n -X1.45i -O -K >> $out.ps
  gmt psxy $basedir/Qs_Qw_continuous_lag.pl $rgn_l $proj -Glightgrey -W0.8p,lightgrey -O -K >> $out.ps
  gmt psxy $basedir/Qs_Qw_linear_lag.pl $rgn_l $proj -W0.8p -O -K >> $out.ps
  if [ $i -eq 3 ] ; then
    gmt psxy $basedir/${sweepdirs[$i]}/Qs_Qw_lag.pl $rgn_l $proj -Sc3p -W0.8p+cl -Cmag.cpt -t95 -O -K >> $out.ps
  fi
  gmt psbasemap $rgn_l $proj -Bn${S}Ew -Bx1f3p+l"Period, @%2%P@%% / @%2%T@-eq@-@%% [-]" -By0.05+l"Lag, @~\152@~@%2%@-Qs,L@-@%% / @%2%P@%% [-]" -O -K >> $out.ps

done

# Finalise, show
gmt psbasemap -R0/1/0/1 -JX2i -B+n -O >> $out.ps
gmt psconvert -A -E400 -Tf $out.ps
convert -density 600x600 -quality 100 -alpha remove $out.pdf $out.jpg
rm $out.ps
eog $out.jpg &