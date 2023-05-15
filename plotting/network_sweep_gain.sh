#!/bin/bash -i

# ---- Defaults
set_gmt_defaults

# ---- Files & Directories
m20="../output/network_sweep_m20"
m40="../output/network_sweep_m40"
m2_m60="../output/network_sweep_m2-m60"
out=sweep_gain

# ---- Variables
proj=-JX3il/2i
rgn=-R0.00316/316/-0.1/1.1

# ---- z: uncorrected
gmt psbasemap $rgn $proj -B+n -Y6i -K > $out.ps
gmt psxy $m20/z_gain_poly.pg $rgn $proj -Glightgrey -O -K >> $out.ps
gmt psxy $m20/z_gain_out.pg $rgn $proj -W0.8p,black -O -K >> $out.ps
awk ' { print $1, $3, $4, $5 } ' $m20/net_z_gain_out.pg | \
  gmt psxy $rgn $proj -Ey+a+w2p+p0.8p,red -t80 -O -K >> $out.ps
awk ' { print $1, $3 } ' $m20/net_z_gain_out.pg | \
  gmt psxy $rgn $proj -Sc3p -Gred -W0.8p -t80 -O -K >> $out.ps
awk ' { print $1, $3, $4, $5 } ' $m40/net_z_gain_out.pg | \
  gmt psxy $rgn $proj -Ey+a+w2p+p0.8p,dodgerblue -t80 -O -K >> $out.ps
awk ' { print $1, $3 } ' $m40/net_z_gain_out.pg | \
  gmt psxy $rgn $proj -Sc3p -Gdodgerblue -W0.8p -t80 -O -K >> $out.ps
awk ' { print $1, $3, $4, $5 } ' $m2_m60/net_z_gain_out.pg | \
  gmt psxy $rgn $proj -Ey+a+w2p+p0.8p,black -t90 -O -K >> $out.ps
awk ' { print $1, $3 } ' $m2_m60/net_z_gain_out.pg | \
  gmt psxy $rgn $proj -Sc3p -Gblack -W0.8p -t90 -O -K >> $out.ps

# ---- Key  
echo "0.005 1.02
0.02 1.02" | gmt psxy $rgn $proj -W4p,lightgrey -O -K >> $out.ps
echo "0.02 1.02 Linear valley range" | \
  gmt pstext $rgn $proj -F+f8p,Helvetica,black+jLM -D0.05i/0i -O -K >> $out.ps
echo "0.005 1.02
0.02 1.02" | gmt psxy $rgn $proj -W0.8p,black -D0i/-0.15i -O -K >> $out.ps
echo "0.02 1.02 Linear valley outlet" | \
  gmt pstext $rgn $proj -F+f8p,Helvetica,black+jLM -D0.05i/-0.15i -O -K >> $out.ps
echo "0.01 1.02 0.03" | \
  gmt psxy $rgn $proj -Ey+w2p+p0.8p -D0i/-0.3i -O -K >> $out.ps
echo "0.02 1.02 Network range" | \
  gmt pstext $rgn $proj -F+f8p,Helvetica,black+jLM -D0.05i/-0.3i -O -K >> $out.ps
echo "0.01 1.02" | \
  gmt psxy $rgn $proj -Sc3p -W0.8p,black -D0i/-0.45i -O -K >> $out.ps
echo "0.02 1.02 Network outlet" | \
  gmt pstext $rgn $proj -F+f8p,Helvetica,black+jLM -D0.05i/-0.45i -O -K >> $out.ps
echo "1 1.1 @%3%T@-eq@-@%% @~\272@~ @%3%L@%%@+2@+ / @~\153@~" | \
  gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black -D0i/0.25i -N -O -K >> $out.ps
gmt psbasemap $rgn $proj -BnseW -Bxa1f3p+l"@%2%P@%% / @%2%T@-eq@-@%%" -By0.2+l"@%2%G@-z@-@%%" -O -K >> $out.ps

# ---- z: corrected
gmt psbasemap $rgn $proj -B+n -X3.2i -O -K >> $out.ps
gmt psxy $m20/z_gain_poly.pg $rgn $proj -Glightgrey -O -K >> $out.ps
gmt psxy $m20/z_gain_out.pg $rgn $proj -W0.8p,black -O -K >> $out.ps
awk ' { print $2, $3, $4, $5 } ' $m20/net_z_gain_out.pg | \
  gmt psxy $rgn $proj -Ey+a+w2p+p0.8p,red -t80 -O -K >> $out.ps
awk ' { print $2, $3 } ' $m20/net_z_gain_out.pg | \
  gmt psxy $rgn $proj -Sc3p -Gred -t80 -W0.8p -O -K >> $out.ps
awk ' { print $2, $3, $4, $5 } ' $m40/net_z_gain_out.pg | \
  gmt psxy $rgn $proj -Ey+a+w2p+p0.8p,dodgerblue -t80 -O -K >> $out.ps
awk ' { print $2, $3 } ' $m40/net_z_gain_out.pg | \
  gmt psxy $rgn $proj -Sc3p -Gdodgerblue -t80 -W0.8p -O -K >> $out.ps
awk ' { print $2, $3, $4, $5 } ' $m2_m60/net_z_gain_out.pg | \
  gmt psxy $rgn $proj -Ey+a+w2p+p0.8p,black -t90 -O -K >> $out.ps
awk ' { print $2, $3 } ' $m2_m60/net_z_gain_out.pg | \
  gmt psxy $rgn $proj -Sc3p -Gblack -W0.8p -t90 -O -K >> $out.ps
echo "1 1.1 @%3%T@-eq@-@%% @~\272@~ @%3%L@-e@-@%%@+2@+ / @~\153@~" | \
  gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black -D0i/0.25i -N -O -K >> $out.ps
gmt psbasemap $rgn $proj -Bnsew -Bxa1f3p+l"@%2%P@%% / @%2%T@-eq@-@%%" -By0.2 -O -K >> $out.ps

# ---- Qs: uncorrected
gmt psbasemap $rgn $proj -B+n -X-3.2i -Y-2.2i -O -K >> $out.ps
gmt psxy $m20/Qs_gain_poly.pg $rgn $proj -Glightgrey -O -K >> $out.ps
gmt psxy $m20/Qs_gain_out.pg $rgn $proj -W0.8p,black -O -K >> $out.ps
awk ' { print $1, $3, $4, $5 } ' $m20/net_Qs_gain_out.pg | \
  gmt psxy $rgn $proj -Ey+a+w2p+p0.8p,red -t80 -O -K >> $out.ps
awk ' { print $1, $3 } ' $m20/net_Qs_gain_out.pg | \
  gmt psxy $rgn $proj -Sc3p -Gred -W0.8p,black -t80 -O -K >> $out.ps
awk ' { print $1, $3, $4, $5 } ' $m40/net_Qs_gain_out.pg | \
  gmt psxy $rgn $proj -Ey+a+w2p+p0.8p,dodgerblue -t80 -O -K >> $out.ps
awk ' { print $1, $3 } ' $m40/net_Qs_gain_out.pg | \
  gmt psxy $rgn $proj -Sc3p -Gdodgerblue -W0.8p,black -t80 -O -K >> $out.ps
awk ' { print $1, $3, $4, $5 } ' $m2_m60/net_Qs_gain_out.pg | \
  gmt psxy $rgn $proj -Ey+a+w2p+p0.8p,black -t90 -O -K >> $out.ps
awk ' { print $1, $3 } ' $m2_m60/net_Qs_gain_out.pg | \
  gmt psxy $rgn $proj -Sc3p -Gblack -W0.8p -t90 -O -K >> $out.ps
gmt psbasemap $rgn $proj -BnSeW -Bxa1f3p+l"@%2%P@%% / @%2%T@-eq@-@%%" -By0.2+l"@%2%G@-Qs@-@%%" -O -K >> $out.ps

# ---- Qs: corrected
gmt psbasemap $rgn $proj -B+n -X3.2i -O -K >> $out.ps
gmt psxy $m20/Qs_gain_poly.pg $rgn $proj -Glightgrey -O -K >> $out.ps
gmt psxy $m20/Qs_gain_out.pg $rgn $proj -W0.8p,black -O -K >> $out.ps
awk ' { print $2, $3, $4, $5 } ' $m20/net_Qs_gain_out.pg | \
  gmt psxy $rgn $proj -Ey+a+w2p+p0.8p,red -t80 -O -K >> $out.ps
awk ' { print $2, $3 } ' $m20/net_Qs_gain_out.pg | \
  gmt psxy $rgn $proj -Sc3p -Gred -W0.8p,black -t80 -O -K >> $out.ps
awk ' { print $2, $3, $4, $5 } ' $m40/net_Qs_gain_out.pg | \
  gmt psxy $rgn $proj -Ey+a+w2p+p0.8p,dodgerblue -t80 -O -K >> $out.ps
awk ' { print $2, $3 } ' $m40/net_Qs_gain_out.pg | \
  gmt psxy $rgn $proj -Sc3p -Gdodgerblue -W0.8p,black -t80 -O -K >> $out.ps
awk ' { print $2, $3, $4, $5 } ' $m2_m60/net_Qs_gain_out.pg | \
  gmt psxy $rgn $proj -Ey+a+w2p+p0.8p,black -t90 -O -K >> $out.ps
awk ' { print $2, $3 } ' $m2_m60/net_Qs_gain_out.pg | \
  gmt psxy $rgn $proj -Sc3p -Gblack -W0.8p -t90 -O -K >> $out.ps

# Key
echo "316 -0.1 @%2%N@%%@-1@- = 20" | \
  gmt pstext $rgn $proj -F+f8p,red+jRM -D-0.1i/0.45i -O -K >> $out.ps 
echo "316 -0.1 @%2%N@%%@-1@- = 40" | \
  gmt pstext $rgn $proj -F+f8p,dodgerblue+jRM -D-0.1i/0.3i -O -K >> $out.ps 
echo "316 -0.1 @%2%N@%%@-1@- = [2..60]" | \
  gmt pstext $rgn $proj -F+f8p,black+jRM -D-0.1i/0.15i -O -K >> $out.ps 
gmt psbasemap $rgn $proj -BnSew -Bxa1f3p+l"@%2%P@%% / @%2%T@-eq@-@%%" -By0.2 -O >> $out.ps


# ---- Show
# gmt psconvert -A -E400 -Tj $out.ps
# eog $out.jpg &
gmt psconvert -A -E400 -Tf $out.ps
# evince $out.pdf &
convert -density 400 -quality 100 -alpha remove $out.pdf $out.jpg
eog $out.jpg &