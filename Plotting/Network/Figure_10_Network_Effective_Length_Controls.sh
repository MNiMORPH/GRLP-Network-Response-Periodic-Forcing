#!/bin/bash

# ---- Get useful extra functions
source ../gmt_extras.sh

# ---- Set defaults
gmt_extras::set_gmt_defaults

# ---- Variables
out=../../Figures/Figure_10_Network_Effective_Length_Controls
vars=("@%2%p@-d,Qw@-@%%" "@%2%R@-B@-@%%" "@%2%R@-L@-@%%" "@%2%R@-Q@-@%%" "@%2%K@%%" "@~\341@~@%2%L@%%@~\361@~" "@~\341@~@%2%L@%%@~\361@~@-50@-")
# vars=("@[p_{d,Q_w}@[" "@[R_B@[" "@[R_L@[" "@[R_Q@[" "@[K@[" "@[\langle L \rangle@[" "@[\langle L \rangle_{50}@[")
basedir="../../Output/Network/Figure_10_Network_Effective_Length_Controls"
cases=("UUU" "NUU" "UAU" "NAU")
corr_labels=("a" "b" "c" "d")
Le_labels=("e" "f" "g" "h")
Le2_labels=("i" "j" "k" "l")
titles=("Uniform segment lengths" "Random segment lengths" "Unifom segment lengths" "Random segment lengths")

# ---- Plot
rgn=-R-0.5/6.5/-1.1/1.1
proj=-JX1.5i
gmt psbasemap $rgn $proj -B+n -Y2i -K > $out.ps

for i in ${!cases[@]} ; do
echo $i
  if [ $i -eq 0 ] ; then
    W="W"
  else
    W="w"
  fi

  if [ $i -eq 3 ] ; then
    E="E"
  else
    E="e"
  fi

  rgn=-R-0.5/6.5/-0.5/1.1
  gmt psbasemap $rgn $proj -B+n -X0.45i -Y3.8i -O -K >> $out.ps
  for j in ${!vars[@]} ; do
    echo $j -0.5 "${vars[$j]}" | \
      gmt pstext $rgn $proj -F+f7p+jBC -D0i/-0.16i -N -O -K >> $out.ps
  done
  for k in $(seq 0 1 $(wc -l $basedir/N1_40_${cases[$i]}_corr.dat | awk ' { print $1-1 } ')) ; do
    x1=$(echo $k | awk ' { print $1-0.3 } ')
    x2=$(echo $k | awk ' { print $1+0.3 } ')
    y1=$(awk ' { if ($1=='$k') print $2 } ' $basedir/N1_40_${cases[$i]}_corr.dat)
    y2=$(awk ' { if ($1=='$k') print $2 } ' $basedir/N1_2-102_${cases[$i]}_corr.dat)
    echo "$x1 0
$x1 $y1
$k $y1
$k 0" | gmt psxy $rgn $proj -Gsteelblue -W0.1p,steelblue -O -K >> $out.ps
  echo "$x2 0
$x2 $y2
$k $y2
$k 0" | gmt psxy $rgn $proj -Gtomato -W0.1p,tomato -O -K >> $out.ps
  done
  # gmt psxy $basedir/${corrfiles[$i]} $rgn $proj -Sc3.5p -Gsteelblue -W0.8p -O -K >> $out.ps
  gmt psbasemap $rgn $proj -Bnse${W} -Bx1 -By0.2+l"Correlation coefficient, @%2%r@%%" -O -K >> $out.ps
  echo "${corr_labels[$i]}" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
  echo "${titles[$i]}" | gmt pstext $rgn $proj -F+f8p+jCB+cCT -D0i/0.1i -N -O -K >> $out.ps

  rgn=-R35/105/35/115
  gmt psbasemap $rgn $proj -B+n -Y-2i -O -K >> $out.ps
  awk ' { print $5, $7 } ' $basedir/N1_40_${cases[$i]}.dat | \
    gmt psxy $rgn $proj -Sc2.5p -W0.8p,steelblue -t70 -O -K >> $out.ps
  gmt psxy $basedir/N1_40_${cases[$i]}_fit.dat $rgn $proj -W1p,black,3p_3p -O -K >> $out.ps
  gmt psbasemap $rgn $proj \
    -Btsr${W} -Bpx10+l"Mean length, @%2%@~\341@~L@~\361@~@%% [km]" \
    -By10+l"Effective length, @[\widehat{\textit{L}}@[ [km]" \
    -O -K >> $out.ps
  echo "${Le_labels[$i]}" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps

  proj_hist=-JX1.5i/0.3i
  rgn_hist=-R35/105/0/40
  awk ' { print $5 } ' $basedir/N1_40_${cases[$i]}.dat | \
    gmt pshistogram $rgn_hist $proj_hist -Ggrey -T30+n -O -K >> $out.ps
  gmt psbasemap $rgn_hist $proj_hist -Bb${E} -By20 -O -K >> $out.ps
  if [ $i -eq 3 ] ; then
    echo "Count:" | gmt pstext $rgn_hist $proj_hist -F+f7p+jBL+cBR -D0.08i/0.4i -N -O -K >> $out.ps
  fi
    
  proj_hist2=-JX-0.3i/1.5i
  rgn_hist2=-R35/115/0/40
  awk ' { print $7 } ' $basedir/N1_40_${cases[$i]}.dat | \
    gmt pshistogram $rgn_hist2 $proj_hist2 -Ggrey -T30+n -X1.2i -A -O -K >> $out.ps
  echo "Count:" | gmt pstext $rgn_hist2 $proj_hist2 -F+f7p+jBR+cTR -D-0.4i/0.08i -N -O -K >> $out.ps
  gmt psbasemap -R0/40/35/115 $proj_hist2 -BrN -Bx20 -O -K >> $out.ps

  rgn=-R35/105/35/115
  gmt psbasemap $rgn $proj -B+n -Y-1.8i -X-1.2i -O -K >> $out.ps
  awk ' $8<40 { print $5, $7 } ' $basedir/N1_2-102_${cases[$i]}.dat | \
    gmt psxy $rgn $proj -Sc2.5p -W0.8p,dimgrey -t70 -O -K >> $out.ps
  awk ' $8>=40 { print $5, $7 } ' $basedir/N1_2-102_${cases[$i]}.dat | \
    gmt psxy $rgn $proj -Sc2.5p -W0.8p,tomato -t70 -O -K >> $out.ps
  gmt psxy $basedir/N1_2-102_${cases[$i]}_fit.dat $rgn $proj -W1p,black,3p_3p -O -K >> $out.ps
  gmt psbasemap $rgn $proj \
    -BtSr${W} -Bpx10+l"Mean length, @~\341@~@%2%L@%%@~\361@~ [km]"\
    -By10+l"Effective length, @[\widehat{\textit{L}}@[ [km]" \
    -O -K >> $out.ps
  echo "${Le2_labels[$i]}" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps

  proj_hist=-JX1.5i/0.3i
  rgn_hist=-R35/105/0/120
  awk ' { print $5 } ' $basedir/N1_2-102_${cases[$i]}.dat | \
    gmt pshistogram $rgn_hist $proj_hist -Ggrey -T30+n -O -K >> $out.ps
  gmt psbasemap $rgn_hist $proj_hist -Bb${E} -By60 -O -K >> $out.ps
  if [ $i -eq 3 ] ; then
    echo "Count:" | gmt pstext $rgn_hist $proj_hist -F+f7p+jBL+cBR -D0.08i/0.4i -N -O -K >> $out.ps
  fi
    
  proj_hist2=-JX-0.3i/1.5i
  rgn_hist2=-R35/115/0/120
  awk ' { print $7 } ' $basedir/N1_2-102_${cases[$i]}.dat | \
    gmt pshistogram $rgn_hist2 $proj_hist2 -Ggrey -T30+n -X1.2i -A -O -K >> $out.ps
  echo "Count:" | gmt pstext $rgn_hist2 $proj_hist2 -F+f7p+jBR+cTR -D-0.4i/0.08i -N -O -K >> $out.ps
  gmt psbasemap -R0/120/35/115 $proj_hist2 -BrN -Bx60 -O -K >> $out.ps


done

rgn=-R0/3.15/0/3.15
proj=-JX3.15i
gmt psbasemap $rgn $proj -B+n -X-6.15i -Y3.8i -O -K >> $out.ps
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
rm $out.ps $out.pdf
eog $out.jpg &