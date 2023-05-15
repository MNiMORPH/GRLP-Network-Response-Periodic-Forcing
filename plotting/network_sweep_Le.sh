#!/bin/bash -i

# ---- Defaults
set_gmt_defaults

# Files
m20="../output/network_sweep_m20"
m40="../output/network_sweep_m40"
m2_m60="../output/network_sweep_m2-m60"
m20props="$m20/props.dat"
m40props="$m40/props.dat"
m2_m60props="$m2_m60/props.dat"
out="sweep_Le"

# Variables
proj=-JX1.8i

# Bifurcation ratio
rgn=-R2/5/0.6/1.16
gmt psbasemap $rgn $proj -B+n -Y6i -K > $out.ps
awk ' { print $1, $7 } ' $m20props | \
  gmt psxy $rgn $proj -Sc3p -Gred -t60 -O -K >> $out.ps
# awk ' { print $1, $7 } ' $m40props | \
#   gmt psxy $rgn $proj -Sc3p -Gdodgerblue -t60 -O -K >> $out.ps
# awk ' { print $1, $7 } ' $m2_m60props | \
#   gmt psxy $rgn $proj -Sc3p -Gblack -t60 -O -K >> $out.ps
gmt psbasemap $rgn $proj -BnSeW -Bx1+l"Bifurcation ratio, @%2%R@-B@-@%%" -By0.1+l"Effective length / Maximum length, @%2%L@-e@-@%% / @%2%L@%%" -O -K >> $out.ps

# Length ratio
rgn=-R0.5/5.5/0.6/1.16
gmt psbasemap $rgn $proj -B+n -X2.2i -O -K >> $out.ps
awk ' { print $2, $7 } ' $m20props | \
  gmt psxy $rgn $proj -Sc3p -Gred -t60 -O -K >> $out.ps
# awk ' { print $2, $7 } ' $m40props | \
#   gmt psxy $rgn $proj -Sc3p -Gdodgerblue -t60 -O -K >> $out.ps
# awk ' { print $2, $7 } ' $m2_m60props | \
#   gmt psxy $rgn $proj -Sc3p -Gblack -t60 -O -K >> $out.ps
gmt psbasemap $rgn $proj -BnSew -Bx1+l"Length ratio, @%2%R@-L@-@%%" -By0.1 -O -K >> $out.ps

# Discharge ratio
rgn=-R1.8/4.7/0.6/1.16
gmt psbasemap $rgn $proj -B+n -X2.2i -O -K >> $out.ps
awk ' { print $3, $7 } ' $m20props | \
  gmt psxy $rgn $proj -Sc3p -Gred -t60 -O -K >> $out.ps
# awk ' { print $3, $7 } ' $m40props | \
#   gmt psxy $rgn $proj -Sc3p -Gdodgerblue -t60 -O -K >> $out.ps
# awk ' { print $3, $7 } ' $m2_m60props | \
#   gmt psxy $rgn $proj -Sc3p -Gblack -t60 -O -K >> $out.ps
gmt psbasemap $rgn $proj -BnSew -Bx0.5+l"Discharge ratio, @%2%R@-Q@-@%%" -By0.1 -O -K >> $out.ps

# Topological length
rgn=-R0/30/0.6/1.16
gmt psbasemap $rgn $proj -B+n -X-4.4i -Y-2.4i -O -K >> $out.ps
awk ' { print $4, $7 } ' $m20props | \
  gmt psxy $rgn $proj -Sc3p -Gred -t60 -O -K >> $out.ps
# awk ' { print $4, $7 } ' $m40props | \
#   gmt psxy $rgn $proj -Sc3p -Gdodgerblue -t60 -O -K >> $out.ps
# awk ' { print $4, $7 } ' $m2_m60props | \
#   gmt psxy $rgn $proj -Sc3p -Gblack -t60 -O -K >> $out.ps
gmt psbasemap $rgn $proj -BnSeW -Bx5+l"Topological length, @~\154@~" -By0.1+l"Effective length / Maximum length, @%2%L@-e@-@%% / @%2%L@%%" -O -K >> $out.ps

# Hack
rgn=-R0.4/1.6/0.6/1.16
gmt psbasemap $rgn $proj -B+n -X2.2i -O -K >> $out.ps
awk ' { print $5, $7 } ' $m20props | \
  gmt psxy $rgn $proj -Sc3p -Gred -t60 -O -K >> $out.ps
# awk ' { print $5, $7 } ' $m40props | \
#   gmt psxy $rgn $proj -Sc3p -Gdodgerblue -t60 -O -K >> $out.ps
# awk ' { print $5, $7 } ' $m2_m60props | \
#   gmt psxy $rgn $proj -Sc3p -Gblack -t60 -O -K >> $out.ps
gmt psbasemap $rgn $proj -BnSew -Bx0.2+l"Hack exponent, @%2%h@%%" -By0.1 -O -K >> $out.ps

# Mean length
rgn=-R0.45/0.85/0.6/1.16
gmt psbasemap $rgn $proj -B+n -X2.2i -O -K >> $out.ps
echo "0.47 1.12
0.555 1.12" | gmt psxy $rgn $proj -W0.8p,dimgrey,- -O -K >> $out.ps
echo "0.555 1.12 @%2%L@-e@-@%% @~\273@~ 1.4 @~\264@~ @~\341@~@%2%L@%%@~\361@~" | \
  gmt pstext $rgn $proj -F+f8p,Helvetica,black+jLM -D0i/0i -O -K >> $out.ps
gmt psxy $m20/Le_fit.dat $rgn $proj -W0.8p,dimgrey,- -O -K >> $out.ps
awk ' { print $6, $7 } ' $m20props | \
  gmt psxy $rgn $proj -Sc3p -Gred -t60 -O -K >> $out.ps
# awk ' { print $6, $7 } ' $m40props | \
#   gmt psxy $rgn $proj -Sc3p -Gdodgerblue -t60 -O -K >> $out.ps
# awk ' { print $6, $7 } ' $m2_m60props | \
#   gmt psxy $rgn $proj -Sc3p -Gblack -t60 -O -K >> $out.ps
# echo "0.85 0.6" | gmt psxy $rgn $proj -Sc3p -Gred -t60 -D-0.12i/0.28i -O -K >> $out.ps
# echo "0.85 0.6 @%2%N@%%@-1@- = 20" | gmt pstext $rgn $proj -F+f8p+jRM -D-0.18i/0.28i -O -K >> $out.ps
# echo "0.85 0.6" | gmt psxy $rgn $proj -Sc3p -Gdodgerblue -t60 -D-0.12i/0.12i -O -K >> $out.ps
# echo "0.85 0.6 @%2%N@%%@-1@- = 40" | gmt pstext $rgn $proj -F+f8p+jRM -D-0.18i/0.12i -O -K >> $out.ps
# echo "0.85 0.6" | gmt psxy $rgn $proj -Sc3p -Gblack -t60 -D-0.12i/0.12i -O -K >> $out.ps
# echo "0.85 0.6 @%2%N@%%@-1@- = [2..60]" | gmt pstext $rgn $proj -F+f8p+jRM -D-0.18i/0.12i -O -K >> $out.ps
gmt psbasemap $rgn $proj -BnSew -Bx0.1+l"Mean length / Maximum length, @~\341@~@%2%L@%%@~\361@~ / @%2%L@%%" -By0.1 -O >> $out.ps


# Show
# gv $out.ps &
# gmt psconvert -A -E400 -Tj $out.ps
# eog $out.jpg &
gmt psconvert -A -E400 -Tf $out.ps
# evince $out.pdf &
convert -density 400 -quality 100 -alpha remove $out.pdf $out.jpg
eog $out.jpg &