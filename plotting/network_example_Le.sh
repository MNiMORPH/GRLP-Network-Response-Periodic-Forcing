#!/bin/bash -i

# ---- Defaults
set_gmt_defaults

# ---- Files & Directories
m20="../output/network_sweep_m20"
example="../output/network_example"
out=example_Le

# ---- Variables
proj=-JX3il/2i
rgn=-R0.00316/316/-0.1/1.1

# ---- z: uncorrected
gmt psbasemap $rgn $proj -B+n -Y6i -K > $out.ps
gmt psxy $m20/z_gain_poly.pg $rgn $proj -Glightgrey -O -K >> $out.ps
gmt psxy $m20/z_gain_out.pg $rgn $proj -W0.8p,black -O -K >> $out.ps
awk ' NR>=0 && NR<=6 { print $1, $3, $4, $5 } ' $m20/net_z_gain_out.pg | \
  gmt psxy $rgn $proj -Ey+a+w2p+p0.8p,lightred -O -K >> $out.ps
awk ' NR>=0 && NR<=6 { print $1, $3 } ' $m20/net_z_gain_out.pg | \
  gmt psxy $rgn $proj -Sc3p -Glightred -O -K >> $out.ps
awk ' NR>=0 && NR<=6 { print $2, $3, $4, $5 } ' $m20/net_z_gain_out.pg | \
  gmt psxy $rgn $proj -Ey+a+w2p+p0.8p,black -O -K >> $out.ps
awk ' NR>=0 && NR<=6 { print $2, $3 } ' $m20/net_z_gain_out.pg | \
  gmt psxy $rgn $proj -Sc3p -Gred -W0.8p -O -K >> $out.ps
echo "0.00316 1.1 0.04" | gmt psxy $rgn $proj -Ey+w2p+p0.8p,lightred -D0.1i/-0.15i -O -K >> $out.ps
echo "0.00316 1.1 0.04" | gmt psxy $rgn $proj -Sc3p -Glightred -D0.1i/-0.15i -O -K >> $out.ps
echo "0.00316 1.1 @%2%T@-eq@-@%% = @%2%L@%%@+2@+ / @~\153@~" | \
  gmt pstext $rgn $proj -F+f8p+jLM -D0.15i/-0.15i -O -K >> $out.ps
echo "0.00316 1.1 0.04" | gmt psxy $rgn $proj -Ey+w2p+p0.8p,black -D0.1i/-0.35i -O -K >> $out.ps
echo "0.00316 1.1 0.04" | gmt psxy $rgn $proj -Sc3p -Gred -W0.8p -D0.1i/-0.35i -O -K >> $out.ps
echo "0.00316 1.1 @%2%T@-eq@-@%% = @%2%L@-e@-@%%@+2@+ / @~\153@~" | \
  gmt pstext $rgn $proj -F+f8p+jLM -D0.15i/-0.35i -O -K >> $out.ps
gmt psbasemap $rgn $proj -BnSeW -Bxa1f3p+l"@%2%P@%% / @%2%T@-eq@-@%%" -By0.2+l"@%2%G@-z@-@%%" -O >> $out.ps

# ---- Show
# gmt psconvert -A -E400 -Tj $out.ps
# eog $out.jpg &
gmt psconvert -A -E400 -Tf $out.ps
# evince $out.pdf &
convert -density 400 -quality 100 -alpha remove $out.pdf $out.jpg
eog $out.jpg &