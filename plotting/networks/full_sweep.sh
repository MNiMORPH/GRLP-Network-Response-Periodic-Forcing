#!/bin/bash

# ---- Get useful extra functions
source ../gmt_extras.sh

# ---- Set defaults
gmt_extras::set_gmt_defaults

# variables
out=sweep
proj=-JX1.5il/1.5i
basedir="../../output/network/full_sweep"
sweepdirs=("m40_fix_seg_length_no_internal" "m40_rnd_seg_length_no_internal" "m40_fix_seg_length_w_internal" "m40_rnd_seg_length_w_internal")
G_z_labels=("a" "b" "c" "d")
lag_z_labels=("e" "f" "g" "h")
G_Qs_labels=("i" "j" "k" "l")
lag_Qs_labels=("m" "n" "o" "p")
G_Qs_Qw_labels=("q" "r" "s" "t")
lag_Qs_Qw_labels=("u" "v" "w" "x")
titles=("Uniform segment lengths" "Random segment lengths" "Unifom segment lengths" "Random segment lengths")


# CPT
gmt makecpt -Cviridis -T0/100/1 -Z -D > mag.cpt

gmt psbasemap -R1/10/1/10 $proj -B+n -X-1i -K > $out.ps

for i in ${!sweepdirs[@]} ; do

  if [ $i -eq 0 ] ; then
    W="W"
  else
    W="w"
  fi
  
  rgn=-R0.003/300/-0.05/1.05
  gmt psbasemap $rgn $proj -B+n -X1.65i -Y8.25i -O -K >> $out.ps
  gmt psxy $basedir/z_continuous_gain.pg $rgn $proj -G197.12/64.125/125.88 -t70 -O -K >> $out.ps
  gmt psxy $basedir/z_linear_gain_rng.pg $rgn $proj -Gdimgrey -t70 -O -K >> $out.ps
  gmt psxy $basedir/z_linear_gain.pg $rgn $proj -W0.8p -O -K >> $out.ps
  # gmt psxy $basedir/${sweepdirs[$i]}/z_gain.pg $rgn $proj -Sc3p -W0.8p+cl -Cmag.cpt -Ey+a+p0.8p+w2p+cl -t95 -O -K >> $out.ps
  # awk ' { print $1, $2, $4, $5 } ' $basedir/${sweepdirs[$i]}/z_gain.pg | \
  #   gmt psxy $rgn $proj -Sc3p -W0.8p,steelblue -Ey+a+p0.8p,steelblue+w2p -t92 -O -K >> $out.ps
  awk ' { print $1, $2, $4, $5 } ' $basedir/${sweepdirs[$i]}_var_width/z_gain.pg | \
    gmt psxy $rgn $proj -Sc3p -W0.8p,steelblue -Ey+a+p0.8p,steelblue+w2p -t92 -O -K >> $out.ps
  echo "${G_z_labels[$i]}" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
  gmt psbasemap $rgn $proj -Bnse${W} -Bx1f3p+l"Period, @%2%P@%% / @%2%T@-eq@-@%% [-]" -By0.2+l"Gain, @%2%G@-z@-@%% [-]" -O -K >> $out.ps
  echo "${titles[$i]}" | gmt pstext $rgn $proj -F+f8p+jCB+cCT -D0i/0.1i -N -O -K >> $out.ps

  rgn_l=-R0.003/300/-0.05/1.05
  gmt psbasemap $rgn_l $proj -B+n -Y-1.65i -O -K >> $out.ps
  gmt psxy $basedir/z_continuous_lag.pl $rgn_l $proj -G197.12/64.125/125.88 -t70 -O -K >> $out.ps
  gmt psxy $basedir/z_linear_lag_rng.pl $rgn_l $proj -Gdimgrey -t70 -O -K >> $out.ps
  gmt psxy $basedir/z_linear_lag.pl $rgn $proj -W0.8p -O -K >> $out.ps
  # gmt psxy $basedir/${sweepdirs[$i]}/z_lag.pl $rgn_l $proj -Sc3p -W0.8p+cl -Cmag.cpt -Ey+a+p0.8p+w2p+cl -t95 -O -K >> $out.ps
  # awk ' { print $1, $2, $4, $5 } ' $basedir/${sweepdirs[$i]}/z_lag.pl | \
  #   gmt psxy $rgn $proj -Sc3p -W0.8p,steelblue -Ey+a+p0.8p,steelblue+w2p -t92 -O -K >> $out.ps
  awk ' { print $1, $2, $4, $5 } ' $basedir/${sweepdirs[$i]}_var_width/z_lag.pl | \
    gmt psxy $rgn $proj -Sc3p -W0.8p,steelblue -Ey+a+p0.8p,steelblue+w2p -t92 -O -K >> $out.ps
  echo "${lag_z_labels[$i]}" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
  gmt psbasemap $rgn_l $proj -Bnse${W} -Bx1f3p+l"Period, @%2%P@%% / @%2%T@-eq@-@%% [-]" -By0.2+l"Lag, @~\152@~@%2%@-z@-@%% / @%2%P@%% [-]" -O -K >> $out.ps
  
  rgn=-R0.003/300/-0.05/1.05
  gmt psbasemap $rgn $proj -B+n -Y-1.65i -O -K >> $out.ps
  gmt psxy $basedir/Qs_continuous_gain.pg $rgn $proj -G197.12/64.125/125.88 -t70 -O -K >> $out.ps
  gmt psxy $basedir/Qs_linear_gain.pg $rgn $proj -W0.8p -O -K >> $out.ps
  # gmt psxy $basedir/${sweepdirs[$i]}/Qs_gain.pg $rgn $proj -Sc3p -W0.8p,steelblue -t92 -O -K >> $out.ps
  gmt psxy $basedir/${sweepdirs[$i]}_var_width/Qs_gain.pg $rgn $proj -Sc3p -W0.8p,steelblue -t92 -O -K >> $out.ps
  echo "${G_Qs_labels[$i]}" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
  gmt psbasemap $rgn $proj -Bnse${W} -Bx1f3p+l"Period, @%2%P@%% / @%2%T@-eq@-@%% [-]" -By0.2+l"Gain, @%2%G@-Qs,L@-@%% [-]" -O -K >> $out.ps
  
  rgn_l=-R0.003/300/-0.05/1.05
  gmt psbasemap $rgn_l $proj -B+n -Y-1.65i -O -K >> $out.ps
  gmt psxy $basedir/Qs_continuous_lag.pl $rgn_l $proj -G197.12/64.125/125.88 -t70 -O -K >> $out.ps
  gmt psxy $basedir/Qs_linear_lag.pl $rgn_l $proj -W0.8p -O -K >> $out.ps
  # gmt psxy $basedir/${sweepdirs[$i]}/Qs_lag.pl $rgn_l $proj -Sc3p -W0.8p,steelblue -t92 -O -K >> $out.ps
  gmt psxy $basedir/${sweepdirs[$i]}_var_width/Qs_lag.pl $rgn_l $proj -Sc3p -W0.8p,steelblue -t92 -O -K >> $out.ps
  echo "${lag_Qs_labels[$i]}" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
  gmt psbasemap $rgn_l $proj -Bnse${W} -Bx1f3p+l"Period, @%2%P@%% / @%2%T@-eq@-@%% [-]" -By0.2+l"Lag, @~\152@~@%2%@-Qs,L@-@%% / @%2%P@%% [-]" -O -K >> $out.ps

  rgn=-R0.003/300/-0.05/1.25
  gmt psbasemap $rgn $proj -B+n -Y-1.65i -O -K >> $out.ps
  gmt psxy $basedir/Qs_Qw_continuous_gain.pg $rgn $proj -G197.12/64.125/125.88 -t70 -O -K >> $out.ps
  gmt psxy $basedir/Qs_Qw_linear_gain.pg $rgn $proj -W0.8p -O -K >> $out.ps
  # gmt psxy $basedir/${sweepdirs[$i]}/Qs_Qw_gain.pg $rgn $proj -Sc3p -W0.8p,steelblue -t92 -O -K >> $out.ps
  gmt psxy $basedir/${sweepdirs[$i]}_var_width/Qs_Qw_gain.pg $rgn $proj -Sc3p -W0.8p,steelblue -t92 -O -K >> $out.ps
  echo "${G_Qs_Qw_labels[$i]}" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
  gmt psbasemap $rgn $proj -Bnse${W} -Bx1f3p+l"Period, @%2%P@%% / @%2%T@-eq@-@%% [-]" -By0.2+l"Gain, @%2%G@-Qs,L@-@%% [-]" -O -K >> $out.ps

  rgn_l=-R0.003/300/-0.275/0.025
  gmt psbasemap $rgn_l $proj -B+n -Y-1.65i -O -K >> $out.ps
  gmt psxy $basedir/Qs_Qw_continuous_lag.pl $rgn_l $proj -G197.12/64.125/125.88 -t70 -O -K >> $out.ps
  gmt psxy $basedir/Qs_Qw_linear_lag.pl $rgn_l $proj -W0.8p -O -K >> $out.ps
  # gmt psxy $basedir/${sweepdirs[$i]}/Qs_Qw_lag.pl $rgn_l $proj -Sc3p -W0.8p,steelblue -t92 -O -K >> $out.ps
  gmt psxy $basedir/${sweepdirs[$i]}_var_width/Qs_Qw_lag.pl $rgn_l $proj -Sc3p -W0.8p,steelblue -t92 -O -K >> $out.ps
  echo "${lag_Qs_Qw_labels[$i]}" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jBL+cBL -D0.05i/0.08i -O -K >> $out.ps
  gmt psbasemap $rgn_l $proj -BnSe${W} -Bx1f3p+l"Period, @%2%P@%% / @%2%T@-eq@-@%% [-]" -By0.05+l"Lag, @~\152@~@%2%@-Qs,L@-@%% / @%2%P@%% [-]" -O -K >> $out.ps

done

rgn=-R0/3.15/0/3.15
proj=-JX3.15i
gmt psbasemap $rgn $proj -B+n -Y8.25i -X-4.95i -O -K >> $out.ps
echo "0.75 1.72
0.75 1.79
2.4 1.79
2.4 1.72" | gmt psxy $rgn $proj -W0.8p -O -K >> $out.ps
echo "No internal supply" | gmt pstext $rgn $proj -F+f8p+jCM+cCB -D0i/1.79i -Gwhite -N -O -K >> $out.ps

gmt psbasemap $rgn $proj -B+n -X3.3i -O -K >> $out.ps
echo "0.75 1.72
0.75 1.79
2.4 1.79
2.4 1.72" | gmt psxy $rgn $proj -W0.8p -O -K >> $out.ps
echo "With internal supply" | gmt pstext $rgn $proj -F+f8p+jCM+cCB -D0i/1.79i -Gwhite -N -O -K >> $out.ps


# Finalise, show
gmt psbasemap -R0/1/0/1 -JX2i -B+n -O >> $out.ps
gmt psconvert -A -E400 -Tf $out.ps
convert -density 600x600 -quality 100 -alpha remove $out.pdf $out.jpg
rm $out.ps
eog $out.jpg &