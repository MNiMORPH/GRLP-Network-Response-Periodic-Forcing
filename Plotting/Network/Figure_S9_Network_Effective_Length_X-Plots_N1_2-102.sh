#!/bin/bash

# ---- Get useful extra functions
source ../gmt_extras.sh

# ---- Set defaults
gmt_extras::set_gmt_defaults

# ---- Variables
out=../../Figures/Figure_S9_Network_Effective_Length_X-Plots_N1_2-102
basedir="../../Output/Network/Figure_10_S8_S9_Network_Effective_Length_Controls"
cases=("UUU" "NUU" "UAU" "NAU")
p_labs=("a" "g" "m" "s")
R_B_labs=("b" "h" "n" "t")
R_L_labs=("c" "i" "o" "u")
R_Q_labs=("d" "j" "p" "v")
K_labs=("e" "k" "q" "w")
L_labs=("f" "l" "r" "x")
titles=("Uniform segment lengths" "Random segment lengths" "Unifom segment lengths" "Random segment lengths")

# ---- Plot
proj=-JX1i
gmt psbasemap -R0/1/0/1 $proj -B+n -Y8i -X6.95i -K > $out.ps

for i in ${!cases[@]} ; do
  
  if [ $i -eq 3 ] ; then
    S="S"
  else
    S="s"
  fi
  
  rgn=-R0/3/35/115
  gmt psbasemap $rgn $proj -B+n -Y-1.15i -X-5.75i -O -K >> $out.ps
  awk ' { print $1, $8 } ' $basedir/N1_2-102_${cases[$i]}.dat | \
    gmt psxy $rgn $proj -Sc2.5p -W0.8p,steelblue -t70 -O -K >> $out.ps
  echo "${p_labs[$i]}" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
  gmt psbasemap $rgn $proj \
    -Bn${S}eW \
    -Bpx1+l"@%2%p@-d,Qw@-@%% [-]" \
    -By10+l"Effective length, @[\widehat{\textit{L}}@[ [km]" \
    -O -K >> $out.ps
    
  rgn=-R2/7/35/115
  gmt psbasemap $rgn $proj -B+n -X1.15i -O -K >> $out.ps
  awk ' { print $2, $8 } ' $basedir/N1_2-102_${cases[$i]}.dat | \
    gmt psxy $rgn $proj -Sc2.5p -W0.8p,steelblue -t70 -O -K >> $out.ps
  echo "${R_B_labs[$i]}" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
  gmt psbasemap $rgn $proj \
    -Bn${S}ew \
    -Bpx1+l"@%2%R@-B@-@%% [-]" \
    -By10+l"Effective length, @[\widehat{\textit{L}}@[ [km]" \
    -O -K >> $out.ps
    
  rgn=-R0/6/35/115
  gmt psbasemap $rgn $proj -B+n -X1.15i -O -K >> $out.ps
  awk ' { print $3, $8 } ' $basedir/N1_2-102_${cases[$i]}.dat | \
    gmt psxy $rgn $proj -Sc2.5p -W0.8p,steelblue -t70 -O -K >> $out.ps
  echo "${R_L_labs[$i]}" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
  gmt psbasemap $rgn $proj \
    -Bn${S}ew \
    -Bpx1+l"@%2%R@-L@-@%% [-]" \
    -By10+l"Effective length, @[\widehat{\textit{L}}@[ [km]" \
    -O -K >> $out.ps
    
  rgn=-R0/12/35/115
  gmt psbasemap $rgn $proj -B+n -X1.15i -O -K >> $out.ps
  awk ' { print $4, $8 } ' $basedir/N1_2-102_${cases[$i]}.dat | \
    gmt psxy $rgn $proj -Sc2.5p -W0.8p,steelblue -t70 -O -K >> $out.ps
  echo "${R_Q_labs[$i]}" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
  gmt psbasemap $rgn $proj \
    -Bn${S}ew \
    -Bpx2+l"@%2%R@-Q@-@%% [-]" \
    -By10+l"Effective length, @[\widehat{\textit{L}}@[ [km]" \
    -O -K >> $out.ps
    
  rgn=-R0/12/35/115
  gmt psbasemap $rgn $proj -B+n -X1.15i -O -K >> $out.ps
  awk ' { print $5, $8 } ' $basedir/N1_2-102_${cases[$i]}.dat | \
    gmt psxy $rgn $proj -Sc2.5p -W0.8p,steelblue -t70 -O -K >> $out.ps
  echo "${K_labs[$i]}" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
  gmt psbasemap $rgn $proj \
    -Bn${S}ew \
    -Bpx2+l"@%2%K@%% [-]" \
    -By10+l"Effective length, @[\widehat{\textit{L}}@[ [km]" \
    -O -K >> $out.ps
    
  rgn=-R30/100/35/115
  gmt psbasemap $rgn $proj -B+n -X1.15i -O -K >> $out.ps
  awk ' { print $7, $8 } ' $basedir/N1_2-102_${cases[$i]}.dat | \
    gmt psxy $rgn $proj -Sc2.5p -W0.8p,steelblue -t70 -O -K >> $out.ps
  echo "${L_labs[$i]}" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
  gmt psbasemap $rgn $proj \
    -Bn${S}ew \
    -Bpx20+l"@~\341@~@%2%L@%%@~\361@~@-50@- [km]" \
    -By10+l"Effective length, @[\widehat{\textit{L}}@[ [km]" \
    -O -K >> $out.ps

done

# Finalise, show
gmt psbasemap -R0/1/0/1 $proj -B+n -O >> $out.ps
gmt psconvert -A -E400 -Tf $out.ps
convert -density 600x600 -quality 100 -alpha remove $out.pdf $out.jpg
rm $out.ps $out.pdf
eog $out.jpg &