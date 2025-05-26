#!/bin/bash

cross_plot () {
  case=$1
  col=$2
  lab=$3
  dx=$4
  off=$5
  axes=$6
  panel=$7
  
  Lmin=25
  Lmax=150
  
  xmin=$(cat $basedir/N1_40_???.dat | awk ' { print $'$col'} ' | gmt gmtinfo -C | awk ' {print $1 } ')
  xmax=$(cat $basedir/N1_40_???.dat | awk ' { print $'$col'} ' | gmt gmtinfo -C | awk ' {print $2 } ')

  xext=$(echo $xmin $xmax | awk ' { print ($2-$1)/10 } ')
  
  xmin_ext=$(echo $xmin $xext | awk ' { print $1-$2 } ')
  xmax_ext=$(echo $xmax $xext | awk ' { print $1+$2 } ')

  rgn=-R${xmin_ext}/${xmax_ext}/${Lmin}/${Lmax}

  gmt psbasemap $rgn $proj -B+n $off -O -K >> $out.ps
  awk ' { print $'$col', $1 } ' $basedir/N1_40_${case}.dat | \
    gmt psxy $rgn $proj -Sc2.5p -W0.8p,steelblue -t70 -O -K >> $out.ps
  echo $panel | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
  gmt psbasemap $rgn $proj \
    -Bn$axes \
    -Bx$dx+l"$lab" \
    -By25+l"Effective length, @[\widehat{\textit{L}}@[ [km]" \
    -O -K >> $out.ps  
}

# ---- Get useful extra functions
source ../gmt_extras.sh

# ---- Set defaults
gmt_extras::set_gmt_defaults

# ---- Variables
basedir="../../Output/Network/Figure_S18_S19_S20_Network_Effective_Length_Controls_Non-Uniform_Width"
cases=("UUN" "NUN" "UAN" "NAN")
titles=("Uniform segment lengths" "Non-uniform segment lengths" "Uniform segment lengths" "Non-uniform segment lengths")
proj=-JX1i


# ---- Plot Part A
out=../../Figures/Figure_S19a_Network_Effective_Length_X-Plots_Non-Uniform_Width_N1_40
R_B_labs=("a" "g" "m" "s")
R_L_labs=("b" "h" "n" "t")
R_Q_labs=("c" "i" "o" "u")
K_labs=("d" "j" "p" "v")
l_labs=("e" "k" "q" "w")
l_mean_labs=("f" "l" "r" "x")

gmt psbasemap -R0/1/0/1 $proj -B+n -Y8i -X6.95i -K > $out.ps

for i in ${!cases[@]} ; do
  
  if [ $i -eq 3 ] ; then
    S="S"
  else
    S="s"
  fi
  
  cross_plot ${cases[$i]} 2 "@%2%R@-B@-@%% [-]" 1 "-Y-1.15i -X-5.75i" ${S}eW "${R_B_labs[$i]}"
  cross_plot ${cases[$i]} 3 "@%2%R@-L@-@%% [-]" 1 "-X1.15i" ${S}ew "${R_L_labs[$i]}"
  cross_plot ${cases[$i]} 4 "@%2%R@-Q@-@%% [-]" 1 "-X1.15i" ${S}ew "${R_Q_labs[$i]}"
  cross_plot ${cases[$i]} 5 "@%2%K@%% [-]" 4 "-X1.15i" ${S}ew "${K_labs[$i]}"
  cross_plot ${cases[$i]} 6 "@%2%l@%% [-]" 5 "-X1.15i" ${S}ew "${l_labs[$i]}"
  cross_plot ${cases[$i]} 7 "@~\341@~@%2%l@%%@~\361@~ [-]" 2 "-X1.15i" ${S}ew "${l_mean_labs[$i]}"

done

# Finalise, show
gmt psbasemap -R0/1/0/1 $proj -B+n -O >> $out.ps
gmt psconvert -A -E400 -Tf $out.ps
convert -density 600x600 -quality 100 -alpha remove $out.pdf $out.jpg
rm $out.ps $out.pdf
eog $out.jpg

# ---- Plot Part B
out=../../Figures/Figure_S19b_Network_Effective_Length_X-Plots_Non-Uniform_Width_N1_40
l_mean_head_labs=("y" "ar" "ak" "aq")
L_labs=("z" "af" "al" "ar")
L_mean_head_labs=("aa" "ag" "am" "as")
w_labs=("ab" "ah" "an" "at")
w_mean_labs=("ac" "ai" "ao" "au")
p_labs=("ad" "aj" "ap" "av")
gmt psbasemap -R0/1/0/1 $proj -B+n -Y8i -X6.95i -K > $out.ps

for i in ${!cases[@]} ; do
  
  if [ $i -eq 3 ] ; then
    S="S"
  else
    S="s"
  fi
  
  cross_plot ${cases[$i]} 8 "@~\341@~@%2%l@-I@-@%%@~\361@~ [-]" 2 "-Y-1.15i -X-5.75i" ${S}eW "${l_mean_head_labs[$i]}"
  cross_plot ${cases[$i]} 9 "@%2%L@%% [km]" 50 "-X1.15i" ${S}ew "${L_labs[$i]}"
  cross_plot ${cases[$i]} 10 "@~\341@~@%2%L@%%@~\361@~ [km]" 25 "-X1.15i" ${S}ew "${L_mean_head_labs[$i]}"
  cross_plot ${cases[$i]} 12 "@%2%w@%% [-]" 4 "-X1.15i" ${S}ew "${w_labs[$i]}"
  cross_plot ${cases[$i]} 13 "@~\341@~@%2%w@%%@~\361@~ [-]" 2 "-X1.15i" ${S}ew "${w_mean_labs[$i]}"
  cross_plot ${cases[$i]} 14 "@%2%p@%% [-]" 0.4 "-X1.15i" ${S}ew "${p_labs[$i]}"

done

# Finalise, show
gmt psbasemap -R0/1/0/1 $proj -B+n -O >> $out.ps
gmt psconvert -A -E400 -Tf $out.ps
convert -density 600x600 -quality 100 -alpha remove $out.pdf $out.jpg
rm $out.ps $out.pdf
eog $out.jpg &