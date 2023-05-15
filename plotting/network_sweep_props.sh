#!/bin/bash -i

plot_hist () {
  infile=$1
  col=$2
  fill=$3
  trans=$4
  x1=$(awk ' { print $'$col' } ' $infile | gmt gmtinfo -C | awk ' { print $1 } ')
  x2=$(awk ' { print $'$col' } ' $infile | gmt gmtinfo -C | awk ' { print $2 } ')
  awk ' { print $'$col' } ' $infile | \
    gmt pshistogram $rgn $proj -T$x1/$x2/25+n -G$fill -t$trans -O -K >> $out.ps
}


# Defaults
set_gmt_defaults

# Files
m20="../output/network_sweep_m20/props.dat"
m40="../output/network_sweep_m40/props.dat"
m2_m60="../output/network_sweep_m2-m60/props.dat"
out="sweep_props"

# Variables
proj=-JX1.8i

# Bifurcation ratio
rgn=-R2/5/0/140
gmt psbasemap $rgn $proj -B+n -Y6i -K > $out.ps
plot_hist $m20 1 "red" 60
# plot_hist $m40 1 "dodgerblue" 60
# plot_hist $m2_m60 1 "black" 60
gmt psbasemap $rgn $proj -BnSeW -Bx1+l"Bifurcation ratio, @%2%R@-B@-@%%" -By20+l"Count" -O -K >> $out.ps

# Length ratio
rgn=-R0.5/5.5/0/50
gmt psbasemap $rgn $proj -B+n -X2.2i -O -K >> $out.ps
plot_hist $m20 2 "red" 60
# plot_hist $m40 2 "dodgerblue" 60
# plot_hist $m2_m60 2 "black" 60
gmt psbasemap $rgn $proj -BnSeW -Bx1+l"Length ratio, @%2%R@-L@-@%%" -By10 -O -K >> $out.ps

# Discharge ratio
rgn=-R1.8/4.7/0/50
gmt psbasemap $rgn $proj -B+n -X2.2i -O -K >> $out.ps
plot_hist $m20 3 "red" 60
# plot_hist $m40 3 "dodgerblue" 60
# echo "4.7 50" | gmt psxy $rgn $proj -Ss10p -Gred -t60 -D-0.12i/-0.12i -O -K >> $out.ps
# echo "4.7 50 @%2%N@%%@-1@- = 20" | gmt pstext $rgn $proj -F+f8p+jRM -D-0.2i/-0.12i -O -K >> $out.ps
# echo "4.7 50" | gmt psxy $rgn $proj -Ss10p -Gdodgerblue -t60 -D-0.12i/-0.28i -O -K >> $out.ps
# echo "4.7 50 @%2%N@%%@-1@- = 40" | gmt pstext $rgn $proj -F+f8p+jRM -D-0.2i/-0.28i -O -K >> $out.ps
# echo "4.7 50" | gmt psxy $rgn $proj -Ss10p -Gblack -t60 -D-0.12i/-0.44i -O -K >> $out.ps
# echo "4.7 50 @%2%N@%%@-1@- = [2..60]" | gmt pstext $rgn $proj -F+f8p+jRM -D-0.2i/-0.44i -O -K >> $out.ps
# plot_hist $m2_m60 3 "black" 60
gmt psbasemap $rgn $proj -BnSeW -Bx0.5+l"Discharge ratio, @%2%R@-Q@-@%%" -By10 -O -K >> $out.ps

# Topological length
rgn=-R0/30/0/50
gmt psbasemap $rgn $proj -B+n -X-4.4i -Y-2.4i -O -K >> $out.ps
# echo "5 0
# 5 50
# 20 50
# 20 0" | gmt psxy $rgn $proj -Glightgrey -O -K >> $out.ps
plot_hist $m20 4 "red" 60
# plot_hist $m40 4 "dodgerblue" 60
echo "10.9177 0
10.9177 50" | gmt psxy $rgn $proj -W1p,red,4_4 -O -K >> $out.ps
# echo "17.1852 0
# 17.1852 50" | gmt psxy $rgn $proj -W1p,dodgerblue,4_4 -O -K >> $out.ps
# plot_hist $m2_m60 4 "black" 60
gmt psbasemap $rgn $proj -BnSeW -Bx5+l"Topological length, @~\154@~" -By10+l"Count" -O -K >> $out.ps

# Hack
rgn=-R0.4/1.6/0/50
gmt psbasemap $rgn $proj -B+n -X2.2i -O -K >> $out.ps
plot_hist $m20 5 "red" 60
# plot_hist $m40 5 "dodgerblue" 60
# plot_hist $m2_m60 5 "black" 60
gmt psbasemap $rgn $proj -BnSeW -Bx0.2+l"Hack exponent, @%2%h@%%" -By10 -O -K >> $out.ps

# eff length
rgn=-R0.45/0.85/0/50
gmt psbasemap $rgn $proj -B+n -X2.2i -O -K >> $out.ps
plot_hist $m20 6 "red" 60
# plot_hist $m40 6 "dodgerblue" 60
# plot_hist $m2_m60 6 "black" 60
gmt psbasemap $rgn $proj -BnSeW -Bx0.1+l"Mean length / Maximum length, @~\341@~@%2%L@%%@~\361@~ / @%2%L@%%" -By10 -O >> $out.ps


# ---- Show
# gmt psconvert -A -E400 -Tj $out.ps
# eog $out.jpg &
gmt psconvert -A -E400 -Tf $out.ps
# evince $out.pdf &
convert -density 400 -quality 100 -alpha remove $out.pdf $out.jpg
eog $out.jpg &