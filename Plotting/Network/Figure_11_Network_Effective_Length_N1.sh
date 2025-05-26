#!/bin/bash

# ---- Get useful extra functions
source ../gmt_extras.sh

# ---- Set defaults
gmt_extras::set_gmt_defaults

# ---- Variables
out="../../Figures/Figure_11_Network_Effective_Length_N1"
rgn=-R-5/155/1/1.6
proj=-JX1.5i
basedir="../../Output/Network/Figure_11_Network_Effective_Length_N1"
cases=("UUU" "NUU" "UAU" "NAU")
eff_labels=("a" "b" "c" "d")
mean_labels=("e" "f" "g" "h")
ratio_labels=("i" "j" "k" "l")
titles=("Uniform segment lengths" "Non-uniform segment lengths" "Uniform segment lengths" "Non-uniform segment lengths")

# ---- Initialise
gmt psbasemap $rgn $proj -B+n -X-1i -K > $out.ps

# ---- Plot
for i in ${!cases[@]} ; do

  if [ $i -eq 0 ] ; then
    W="W"
  else
    W="w"
  fi

  rgn=-R-5/155/0/275
  gmt psbasemap $rgn $proj -B+n -X1.65i -Y3.3i -O -K >> $out.ps
  awk ' { print $1, $2 } ' $basedir/N1_2-150_${cases[$i]}_full.dat | \
    gmt psxy  $rgn $proj -Sc3p -W0.8p,tomato -t70 -O -K >> $out.ps
  awk ' { print $1, $2 } ' $basedir/N1_40_${cases[$i]}_full.dat | \
    gmt psxy $rgn $proj -Sc3p -W0.8p,steelblue -t70 -O -K >> $out.ps
  awk ' { print $1, $2 } ' $basedir/N1_2-150_${cases[$i]}_bin.dat | \
    gmt psxy $rgn $proj -Sd3.5p -W1p,black -O -K >> $out.ps
  echo ${eff_labels[$i]} | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
  gmt psbasemap $rgn $proj -Btse${W} -Bx50+l"Number of inlet segments, @%2%N@%%@-1@- [-]" -By50+l"Effective length, @[\widehat{\textit{L}}@[ [km]" -O -K >> $out.ps
  echo "${titles[$i]}" | gmt pstext $rgn $proj -F+f8p+jCB+cCT -D0i/0.07i -N -O -K >> $out.ps

  rgn=-R-5/155/0/180
  gmt psbasemap $rgn $proj -B+n -Y-1.65i -O -K >> $out.ps
  awk ' { print $1, $3 } ' $basedir/N1_2-150_${cases[$i]}_full.dat | \
    gmt psxy  $rgn $proj -Sc3p -W0.8p,tomato -t70 -O -K >> $out.ps
  awk ' { print $1, $3 } ' $basedir/N1_40_${cases[$i]}_full.dat | \
    gmt psxy $rgn $proj -Sc3p -W0.8p,steelblue -t70 -O -K >> $out.ps
  awk ' { print $1, $3 } ' $basedir/N1_2-150_${cases[$i]}_bin.dat | \
    gmt psxy $rgn $proj -Sd3.5p -W1p,black -O -K >> $out.ps
  echo ${mean_labels[$i]} | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
  gmt psbasemap $rgn $proj -Bnse${W} -Bx50+l"Number of inlet segments, @%2%N@%%@-1@- [-]" -By40+l"Mean inlet length, @[\langle\textit{L\textsubscript{I}}\rangle@[ [km]" -O -K >> $out.ps

  rgn=-R-5/155/1/1.6
  gmt psbasemap $rgn $proj -B+n -Y-1.65i -O -K >> $out.ps
  awk ' { print $1, $2/$3 } ' $basedir/N1_2-150_${cases[$i]}_full.dat | \
    gmt psxy  $rgn $proj -Sc3p -W0.8p,tomato -t70 -O -K >> $out.ps
  awk ' { print $1, $2/$3 } ' $basedir/N1_40_${cases[$i]}_full.dat | \
    gmt psxy $rgn $proj -Sc3p -W0.8p,steelblue -t70 -O -K >> $out.ps
  awk ' { print $1, $2/$3 } ' $basedir/N1_2-150_${cases[$i]}_bin.dat | \
    gmt psxy $rgn $proj -Sd3.5p -W1p,black -O -K >> $out.ps
  echo ${ratio_labels[$i]} | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
  gmt psbasemap $rgn $proj -BnSe${W} -Bx50+l"Number of inlet segments, @%2%N@%%@-1@- [-]" -By0.1+l"@[\widehat{\textit{L}}@[ / @[\langle\textit{L\textsubscript{I}}\rangle@[ [-]" -O -K >> $out.ps

  if [ $i -eq 3 ] ; then
    gmt_extras::plot_key_symbol $rgn $proj 145 140 1.13 "-Sc3p -W0.8p,steelblue" "@%2%N@%%@-1@- = 40" $out
    gmt_extras::plot_key_symbol $rgn $proj 145 140 1.085 "-Sc3p -W0.8p,tomato" "@%2%N@%%@-1@- = [2..150]" $out
    gmt_extras::plot_key_symbol $rgn $proj 145 140 1.04 "-Sd3.5p -W1p,black" "Binned" $out
  fi

done

rgn=-R0/3.15/0/3.15
proj=-JX3.15i
gmt psbasemap $rgn $proj -B+n -X-4.95i -Y3.3i -O -K >> $out.ps
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

# ---- Finalise
gmt psbasemap -R0/1/0/1 -JX2i -B+n -O >> $out.ps
gmt psconvert -A -E400 -Tf $out.ps
convert -density 600x600 -quality 100 -alpha remove $out.pdf $out.jpg
rm $out.ps $out.pdf
eog $out.jpg &