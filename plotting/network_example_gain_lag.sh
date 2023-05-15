#!/bin/bash -i

# ---- Defaults
set_gmt_defaults

# ---- CPTs
gmt makecpt -Cviridis -T0.5/4.5/1 -I > order.cpt

# ---- Output
out=example_gain

# ---- Gain fast
rgn=-R-10/110/-0.1/0.9
proj=-JX2i/2i
gmt psbasemap $rgn $proj -B+n -Y6i -K > $out.ps
awk ' { print $1, $2 } ' ../output/network_example/lin_gain.dg | \
  gmt psxy $rgn $proj -W1p,dimgrey,. -O -K >> $out.ps
gmt psxy ../output/network_example/gain_fast.dg $rgn $proj -W1p -Corder.cpt -O -K >> $out.ps
echo "50 0.9 @%3%P@%% = @%3%T@-eq@-@%% / 5" | \
  gmt pstext $rgn $proj -F+f10p,Helvetica-Bold -D0i/0.2i -N -O -K >> $out.ps
gmt psbasemap $rgn $proj -BnseW -Bx20+l"Downstream distance [km]" -By0.2+l"@%2%G@-z@-@%%" -O -K >> $out.ps

# ---- Lag fast
rgn=-R-10/110/-0.1/0.9
gmt psbasemap $rgn $proj -B+n -Y-2.2i -O -K >> $out.ps
awk ' { print $1, $2 } ' ../output/network_example/lin_lag.dl | \
  gmt psxy $rgn $proj -W1p,dimgrey,. -O -K >> $out.ps
gmt psxy ../output/network_example/lag_fast.dl $rgn $proj -W1p -Corder.cpt -O -K >> $out.ps
gmt psbasemap $rgn $proj -BnSeW -Bx20+l"Downstream distance [km]" -By0.2+l"@~\152@~@%2%@-z@-@%% / @%2%P@%%" -O -K >> $out.ps

# ---- Gain medium
rgn=-R-10/110/-0.1/0.9
proj=-JX2i/2i
gmt psbasemap $rgn $proj -B+n -X2.2i -Y2.2i -O -K >> $out.ps
awk ' { print $1, $3 } ' ../output/network_example/lin_gain.dg | \
  gmt psxy $rgn $proj -W1p,dimgrey,. -O -K >> $out.ps
gmt psxy ../output/network_example/gain_medium.dg $rgn $proj -W1p -Corder.cpt -O -K >> $out.ps
echo "50 0.9 @%3%P@%% = @%3%T@-eq@-@%%" | \
  gmt pstext $rgn $proj -F+f10p,Helvetica-Bold -D0i/0.2i -N -O -K >> $out.ps
gmt psbasemap $rgn $proj -Bnsew -Bx20+l"Downstream distance [km]" -By0.2+l"@%2%G@-z@-@%%" -O -K >> $out.ps

# ---- Lag medium
rgn=-R-10/110/-0.1/0.9
gmt psbasemap $rgn $proj -B+n -Y-2.2i -O -K >> $out.ps
awk ' { print $1, $3 } ' ../output/network_example/lin_lag.dl | \
  gmt psxy $rgn $proj -W1p,dimgrey,. -O -K >> $out.ps
gmt psxy ../output/network_example/lag_medium.dl $rgn $proj -W1p -Corder.cpt -O -K >> $out.ps
gmt psbasemap $rgn $proj -BnSew -Bx20+l"Downstream distance [km]" -By0.2+l"@~\152@~@%2%@-z@-@%% / @%2%P@%%" -O -K >> $out.ps

# ---- Gain slow
rgn=-R-10/110/-0.1/0.9
proj=-JX2i/2i
gmt psbasemap $rgn $proj -B+n -X2.2i -Y2.2i -O -K >> $out.ps
awk ' { print $1, $4 } ' ../output/network_example/lin_gain.dg | \
  gmt psxy $rgn $proj -W1p,dimgrey,. -O -K >> $out.ps
gmt psxy ../output/network_example/gain_slow.dg $rgn $proj -W1p -Corder.cpt -O -K >> $out.ps
echo "50 0.9 @%3%P@%% = @%3%T@-eq@-@%% x 5" | \
  gmt pstext $rgn $proj -F+f10p,Helvetica-Bold -D0i/0.2i -N -O -K >> $out.ps
gmt psbasemap $rgn $proj -Bnsew -Bx20+l"Downstream distance [km]" -By0.2+l"@%2%G@-z@-@%%" -O -K >> $out.ps

# ---- Lag slow
rgn=-R-10/110/-0.1/0.9
gmt psbasemap $rgn $proj -B+n -Y-2.2i -O -K >> $out.ps
awk ' { print $1, $4 } ' ../output/network_example/lin_lag.dl | \
  gmt psxy $rgn $proj -W1p,dimgrey,. -O -K >> $out.ps
gmt psxy ../output/network_example/lag_slow.dl $rgn $proj -W1p -Corder.cpt -O -K >> $out.ps
gmt psbasemap $rgn $proj -BnSew -Bx20+l"Downstream distance [km]" -By0.2+l"@~\152@~@%2%@-z@-@%% / @%2%P@%%" -O >> $out.ps

# ---- Show
gmt psconvert -A -E400 -Tj $out.ps
eog $out.jpg &