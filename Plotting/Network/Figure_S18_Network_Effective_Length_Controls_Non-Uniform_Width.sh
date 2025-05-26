#!/bin/bash

# ---- Get useful extra functions
source ../gmt_extras.sh

# ---- Set defaults
gmt_extras::set_gmt_defaults

# ---- Variables
out=../../Figures/Figure_S18_Network_Effective_Length_Controls_Non-Uniform_Width
vars=("@%2%R@-B@-@%%" "@%2%R@-L@-@%%" "@%2%R@-Q@-@%%" "@%2%K@%%" "@%2%l@%%@-max@-" "@~\341@~@%2%l@%%@~\361@~" "@~\341@~@%2%l@-I @-@%%@~\361@~" "@%2%L@%%@-max@-" "@~\341@~@%2%L@%%@~\361@~" "@~\341@~@%2%L@-I @-@%%@~\361@~" "@%2%w@%%" "@~\341@~@%2%w@%%@~\361@~" "@%2%p@%%")
offs=(0.15 0.25 0.15 0.25 0.15 0.25 0.15 0.25 0.15 0.25 0.15 0.25 0.15)
basedir="../../Output/Network/Figure_S18_S19_S20_Network_Effective_Length_Controls_Non-Uniform_Width"
cases=("UUN" "NUN" "UAN" "NAN")
corr_labels=("a" "b" "c" "d")
Le_labels=("e" "f" "g" "h")
Le2_labels=("i" "j" "k" "l")
titles=("Uniform segment lengths" "Non-uniform segment lengths" "Uniform segment lengths" "Non-uniform segment lengths")

# ---- Plot
rgn=-R0/1/0/1
proj=-JX1.5i
gmt psbasemap $rgn $proj -B+n -Y2i -K > $out.ps

for i in ${!cases[@]} ; do
  echo "Plotting ${cases[$i]}."
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

  rgn=-R-0.5/12.5/-0.9/1.1
  gmt psbasemap $rgn $proj -B+n -X0.45i -Y3.8i -O -K >> $out.ps
  for j in ${!vars[@]} ; do
    echo $j -0.9 "${vars[$j]}" | \
      gmt pstext $rgn $proj -F+f7p+jBC -D0i/-${offs[$j]}i -N -O -K >> $out.ps
  done
  for k in $(seq 0 1 $(wc -l $basedir/N1_40_${cases[$i]}_corr.dat | awk ' { print $1-1 } ')) ; do
    x1=$(echo $k | awk ' { print $1-0.3 } ')
    x2=$(echo $k | awk ' { print $1+0.3 } ')
    y1=$(awk ' { if ($1=='$k') print $2 } ' $basedir/N1_40_${cases[$i]}_corr.dat)
    y2=$(awk ' { if ($1=='$k') print $2 } ' $basedir/N1_2-150_${cases[$i]}_corr.dat)
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

  rgn=-R0/180/-10/260
  gmt psbasemap $rgn $proj -B+n -Y-2i -O -K >> $out.ps
  awk ' { print $11, $1 } ' $basedir/N1_40_${cases[$i]}.dat | \
    gmt psxy $rgn $proj -Sc2.5p -W0.8p,steelblue -t70 -O -K >> $out.ps
  gmt psxy $basedir/N1_40_${cases[$i]}_fit.dat $rgn $proj -W1p,black,3p_2p -O -K >> $out.ps
  gmt psbasemap $rgn $proj \
    -Btsr${W} -Bpx45+l"Mean inlet length, @~\341@~@%2%L@-I @-@%%@~\361@~ [km]" \
    -By50+l"Effective length, @[\widehat{\textit{L}}@[ [km]" \
    -O -K >> $out.ps
  echo "${Le_labels[$i]}" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
  grad=$(awk ' { printf "%.2f", $1 } ' $basedir/N1_40_${cases[$i]}_grad.dat)
  gmt_extras::plot_key_line $rgn $proj 48 70 238 -W0.8p,3p_2p "@[\widehat{\textit{L}}@[ / @[\langle\textit{L\textsubscript{I}}\rangle@[ = $grad" $out


  proj_hist=-JX1.5i/0.3i
  rgn_hist=-R0/180/0/60
  awk ' { print $11 } ' $basedir/N1_40_${cases[$i]}.dat | \
    gmt pshistogram $rgn_hist $proj_hist -Ggrey -T30+n -O -K >> $out.ps
  gmt psbasemap $rgn_hist $proj_hist -Bb${E} -By30 -O -K >> $out.ps
  if [ $i -eq 3 ] ; then
    echo "Count:" | gmt pstext $rgn_hist $proj_hist -F+f7p+jBL+cBR -D0.08i/0.4i -N -O -K >> $out.ps
  fi
    
  proj_hist2=-JX-0.3i/1.5i
  rgn_hist2=-R-10/260/0/60
  awk ' { print $1 } ' $basedir/N1_40_${cases[$i]}.dat | \
    gmt pshistogram $rgn_hist2 $proj_hist2 -Ggrey -T30+n -X1.2i -A -O -K >> $out.ps
  echo "Count:" | gmt pstext $rgn_hist2 $proj_hist2 -F+f7p+jBR+cTR -D-0.4i/0.08i -N -O -K >> $out.ps
  gmt psbasemap -R0/60/-10/260 $proj_hist2 -BrN -Bx30 -O -K >> $out.ps

  rgn=-R0/180/-10/260
  gmt psbasemap $rgn $proj -B+n -Y-1.8i -X-1.2i -O -K >> $out.ps
  awk ' { print $11, $1 } ' $basedir/N1_2-150_${cases[$i]}.dat | \
    gmt psxy $rgn $proj -Sc2.5p -W0.8p,tomato -t70 -O -K >> $out.ps
  gmt psxy $basedir/N1_2-150_${cases[$i]}_fit.dat $rgn $proj -W1p,black,3p_3p -O -K >> $out.ps
  gmt psbasemap $rgn $proj \
    -BtSr${W} -Bpx45+l"Mean inlet length, @~\341@~@%2%L@-I @-@%%@~\361@~ [km]" \
    -By50+l"Effective length, @[\widehat{\textit{L}}@[ [km]" \
    -O -K >> $out.ps
  echo "${Le2_labels[$i]}" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
  grad=$(awk ' { printf "%.2f", $1 } ' $basedir/N1_2-150_${cases[$i]}_grad.dat)
  gmt_extras::plot_key_line $rgn $proj 48 70 238 -W0.8p,3p_2p "@[\widehat{\textit{L}}@[ / @[\langle\textit{L\textsubscript{I}}\rangle@[ = $grad" $out

  proj_hist=-JX1.5i/0.3i
  rgn_hist=-R0/180/0/80
  awk ' { print $11 } ' $basedir/N1_2-150_${cases[$i]}.dat | \
    gmt pshistogram $rgn_hist $proj_hist -Ggrey -T30+n -O -K >> $out.ps
  gmt psbasemap $rgn_hist $proj_hist -Bb${E} -By40 -O -K >> $out.ps
  if [ $i -eq 3 ] ; then
    echo "Count:" | gmt pstext $rgn_hist $proj_hist -F+f7p+jBL+cBR -D0.08i/0.4i -N -O -K >> $out.ps
  fi
    
  proj_hist2=-JX-0.3i/1.5i
  rgn_hist2=-R-10/260/0/80
  gmt psbasemap $rgn $proj -B+n -X1.2i -O -K >> $out.ps
  awk ' { print $1 } ' $basedir/N1_2-150_${cases[$i]}.dat | \
    gmt pshistogram $rgn_hist2 $proj_hist2 -Ggrey -T30+n -A -O -K >> $out.ps
  echo "Count:" | gmt pstext $rgn_hist2 $proj_hist2 -F+f7p+jBR+cTR -D-0.4i/0.08i -N -O -K >> $out.ps
  gmt psbasemap -R0/80/-10/260 $proj_hist2 -BrN -Bx40 -O -K >> $out.ps


done

rgn=-R0/3.15/0/3.15
proj=-JX3.15i
gmt psbasemap $rgn $proj -B+n -X-6.15i -Y3.8i -O -K >> $out.ps
echo "0.75 1.72
0.75 1.79
2.4 1.79
2.4 1.72" | gmt psxy $rgn $proj -W0.8p -O -K >> $out.ps
echo "Upstream supply" | gmt pstext $rgn $proj -F+f8p+jCM+cCB -D0i/1.79i -Gwhite -N -O -K >> $out.ps

gmt psbasemap $rgn $proj -B+n -X3.3i -O -K >> $out.ps
echo "0.75 1.72
0.75 1.79
2.4 1.79
2.4 1.72" | gmt psxy $rgn $proj -W0.8p -O -K >> $out.ps
echo "Along-stream supply" | gmt pstext $rgn $proj -F+f8p+jCM+cCB -D0i/1.79i -Gwhite -N -O -K >> $out.ps


# Finalise, show
gmt psbasemap -R0/1/0/1 -JX2i -B+n -O >> $out.ps
gmt psconvert -A -E400 -Tf $out.ps
convert -density 600x600 -quality 100 -alpha remove $out.pdf $out.jpg
rm $out.ps $out.pdf
eog $out.jpg &