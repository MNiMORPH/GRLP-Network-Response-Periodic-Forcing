#!/bin/bash -i

plot_hist () {
  infile=$1
  col1=$2
  col2=$3
  fill=$4
  trans=$5
  x1=$(awk ' { print $'$col1'/$'$col2' } ' $infile | gmt gmtinfo -C | awk ' { print $1 } ')
  x2=$(awk ' { print $'$col1'/$'$col2' } ' $infile | gmt gmtinfo -C | awk ' { print $2 } ')
  awk ' { print $'$col1'/$'$col2' } ' $infile | \
    gmt pshistogram $rgn $proj -T${x1}/${x2}/30+n -G$fill -t$trans -O -K >> $out.ps
}

# ---- Defaults
set_gmt_defaults

# ---- Files
m20="../output/network_sweep_m20"
m40="../output/network_sweep_m40"
m2_m60="../output/network_sweep_m2-m60"
m20props="$m20/props.dat"
m40props="$m40/props.dat"
m2_m60props="$m2_m60/props.dat"
out="sweep_Le_Lm"

# ---- Histogram
rgn=-R1/1.5/0/60
proj=-JX2.4i
gmt psbasemap $rgn $proj -B+n -Y6i -K > $out.ps
plot_hist $m20props 7 6 "red" 80
plot_hist $m40props 7 6 "dodgerblue" 80
plot_hist $m2_m60props 7 6 "black" 60
gmt psbasemap $rgn $proj -BnSeW -Bx0.1+l"Effective length / Mean length,  @%2%L@-e@-@%% / @~\341@~@%2%L@%%@~\361@~" -By10+l"Count" -O -K >> $out.ps

# ---- f(N1)
rgn=-R-5/65/0.95/1.55
gmt psbasemap $rgn $proj -B+n -X3.2i -O -K >> $out.ps
awk ' { print $8, $7/$6 } ' $m20props | \
  gmt psxy $rgn $proj -Sc3p -Gred -t95 -O -K >> $out.ps
awk ' { print $8, $7/$6 } ' $m40props | \
  gmt psxy $rgn $proj -Sc3p -Gdodgerblue -t95 -O -K >> $out.ps
awk ' { print $8, $7/$6 } ' $m2_m60props | \
  gmt psxy $rgn $proj -Sc3p -Gblack -t60 -O -K >> $out.ps
echo "1 1" | gmt psxy $rgn $proj -Sa7p -W0.8p -O -K >> $out.ps

# key
echo "65 0.95" | gmt psxy $rgn $proj -Sc3p -Gred -t60 -D-0.12i/0.6i -O -K >> $out.ps
echo "65 0.95 @%2%N@%%@-1@- = 20" | gmt pstext $rgn $proj -F+f8p+jRM -D-0.2i/0.6i -O -K >> $out.ps
echo "65 0.95" | gmt psxy $rgn $proj -Sc3p -Gdodgerblue -t60 -D-0.12i/0.44i -O -K >> $out.ps
echo "65 0.95 @%2%N@%%@-1@- = 40" | gmt pstext $rgn $proj -F+f8p+jRM -D-0.2i/0.44i -O -K >> $out.ps
echo "65 0.95" | gmt psxy $rgn $proj -Sc3p -Gblack -t60 -D-0.12i/0.28i -O -K >> $out.ps
echo "65 0.95 @%2%N@%%@-1@- = [2..60]" | gmt pstext $rgn $proj -F+f8p+jRM -D-0.2i/0.28i -O -K >> $out.ps
echo "65 0.95" | gmt psxy $rgn $proj -Sa7p -W0.8p -D-0.12i/0.12i -O -K >> $out.ps
echo "65 0.95 Linear" | gmt pstext $rgn $proj -F+f8p+jRM -D-0.2i/0.12i -O -K >> $out.ps

gmt psbasemap $rgn $proj -BnSeW -Bx10+l"Number of sources, @%2%N@%%@-1@-" -By0.1+l"Effective length / Mean length,  @%2%L@-e@-@%% / @~\341@~@%2%L@%%@~\361@~" -O >> $out.ps


# ---- Show
# gmt psconvert -A -E400 -Tj $out.ps
# eog $out.jpg &
gmt psconvert -A -E400 -Tf $out.ps
# evince $out.pdf &
convert -density 400 -quality 100 -alpha remove $out.pdf $out.jpg
eog $out.jpg &