#!/bin/bash

# ---- Get useful extra functions
source ../gmt_extras.sh

# ---- Set defaults
gmt_extras::set_gmt_defaults

# ---- Variables
out=magnitude
rgn=-R-5/155/0.6/1.2
proj=-JX1.5i
basedir="../../output/network/magnitude"
grps=("no_int_var_width" "rnd_no_int_var_width" "w_int_var_width" "rnd_w_int_var_width")
labels=("a" "b" "c" "d")
titles=("Uniform segment lengths" "Random segment lengths" "Unifom segment lengths" "Random segment lengths")

# ---- Initialise
gmt psbasemap $rgn $proj -B+n -X-1i -K > $out.ps

# ---- Plot
for i in ${!grps[@]} ; do

  if [ $i -eq 0 ] ; then
    W="W"
  else
    W="w"
  fi

  gmt psbasemap $rgn $proj -B+n -X1.65i -O -K >> $out.ps
  # gmt psxy $basedir/${grps[$i]}_full.dat $rgn $proj -Sc3p -W0.8p,steelblue -t70 -O -K >> $out.ps
  gmt psxy $basedir/m2-100_${grps[$i]}_full.dat $rgn $proj -Sc3p -W0.8p,tomato -t70 -O -K >> $out.ps
  if [ $i -eq 0 ] || [ $i -eq 3 ] ; then
    gmt psxy $basedir/m100-150_${grps[$i]}_full.dat $rgn $proj -Sc3p -W0.8p,tomato -t70 -O -K >> $out.ps
  fi
  gmt psxy $basedir/m40_${grps[$i]}_full.dat $rgn $proj -Sc3p -W0.8p,steelblue -t70 -O -K >> $out.ps
  gmt psxy $basedir/${grps[$i]}_bin.dat $rgn $proj -Sd3.5p -W1p,black -O -K >> $out.ps
  echo ${labels[$i]} | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
  # gmt psbasemap $rgn $proj -BnSe${W} -Bx50+l"Number of inlet segments, @%2%N@%%@-1@- [-]" -By0.1+l"@%2%L@-e@-@%% / @~\341@~@%2%L@%%@~\361@~ [-]" -O -K >> $out.ps
  gmt psbasemap $rgn $proj -BnSe${W} -Bx50+l"Number of inlet segments, @%2%N@%%@-1@- [-]" -By0.1+l"@[\widehat{\textit{L}}@[ / @[\langle\textit{L}\rangle@[ [-]" -O -K >> $out.ps
  echo "${titles[$i]}" | gmt pstext $rgn $proj -F+f8p+jCB+cCT -D0i/0.1i -N -O -K >> $out.ps

  if [ $i -eq 3 ] ; then
    gmt_extras::plot_key_symbol $rgn $proj 145 140 0.72 "-Sc3p -W0.8p,steelblue" "@%2%N@%%@-1@- = 40" $out
    gmt_extras::plot_key_symbol $rgn $proj 145 140 0.68 "-Sc3p -W0.8p,tomato" "@%2%N@%%@-1@- = [2..150]" $out
    gmt_extras::plot_key_symbol $rgn $proj 145 140 0.64 "-Sd3.5p -W1p,black" "Binned" $out
  fi

done

rgn=-R0/3.15/0/3.15
proj=-JX3.15i
gmt psbasemap $rgn $proj -B+n -X-4.95i -O -K >> $out.ps
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


# ---- Finalise
gmt psbasemap -R0/1/0/1 -JX2i -B+n -O >> $out.ps
gmt psconvert -A -E400 -Tf $out.ps
convert -density 600x600 -quality 100 -alpha remove $out.pdf $out.jpg
rm $out.ps
eog $out.jpg &