#!/bin/bash -i

# ---- Defaults
set_gmt_defaults

# ---- CPTs
gmt makecpt -Cviridis -T0.5/4.5/1 -I > order.cpt

# ---- Output
out=example

# ---- Info
read -e ymax Qmax mag len <<< $(head -n1 ../output/network_example/info.txt)
read -e k h Rb Rl Rq <<< $(head -n1 ../output/network_example/flt_info.txt)

# ---- Planform
rgn=-R0/100/0/$ymax
proj=-JX1.5i/1.8i
gmt psbasemap $rgn $proj -B+n -K > $out.ps
gmt psxy ../output/network_example/planform.d $rgn $proj -W1p -Corder.cpt -O -K >> $out.ps
echo 0 0 "@%2%N@%%@-1@- = $mag" | \
  gmt pstext $rgn $proj -F+f8p,Helvetica,black+jBL -D0i/0.07i -N -O -K >> $out.ps
echo 0 0 "@~\154@~ = $len" | \
  gmt pstext $rgn $proj -F+f8p,Helvetica,black+jBL -D0i/0.22i -N -O -K >> $out.ps
gmt psscale $rgn $proj -Corder.cpt -Dx0.8i/1.7i+w0.7i/0.08i+h -B1+l"Stream order" -O -K >> $out.ps
gmt psbasemap $rgn $proj -BS -Bx20+l"Downstream distance [km]" -O -K >> $out.ps

# ---- Discharge
rgn=-R-10/110/0/$Qmax
proj=-JX1.8i
gmt psbasemap $rgn $proj -B+n -X2.1i -O -K >> $out.ps
echo "-5 $(echo $Qmax | awk ' { print $1*0.93 } ')
15 $(echo $Qmax | awk ' { print $1*0.93 } ')" | gmt psxy $rgn $proj -W0.8p,dimgrey,4_4 -O -K >> $out.ps
echo 15 $(echo $Qmax | awk ' { print $1*0.93 } ') "@%2%L@%% @~\265@~ @%2%Q@-w@-@%%@+$h@+" | \
  gmt pstext $rgn $proj -F+f8p,Helvetica,black+jLM -D0.05i/0i -O -K >> $out.ps
gmt psxy ../output/network_example/discharge_fit.dq $rgn $proj -W0.8p,dimgrey,4_4 -O -K >> $out.ps
gmt psxy ../output/network_example/discharge.dq $rgn $proj -Sc4p -W0.8p -Corder.cpt -O -K >> $out.ps
gmt psbasemap $rgn $proj -BnSW -Bx20+l"Distance from source [km]" -By10+l"@%2%Q@-w@-@%% [m@+3@+ s@+-1@+]" -O -K >> $out.ps
rgn=-R-10/110/0/$(echo $Qmax | awk ' { print $1/10 } ')
gmt psbasemap $rgn $proj -BE -Bx20+l"Downstream distance [km]" -By1+l"@%2%Q@-s@-@%% [x10@+-3@+ m@+3@+ s@+-1@+]" -O -K >> $out.ps

# # ---- Profile
# rgn=-R-10/110/0/650
# proj=-JX1.8i
# gmt psbasemap $rgn $proj -B+n -X2.8i -O -K >> $out.ps
# gmt psxy ../output/network_example/profile.de $rgn $proj -W1.6p -Corder.cpt -O -K >> $out.ps
# gmt psxy ../output/setup/analytical_profile.de $rgn $proj -W0.8p,lightgrey,4_4 -O -K >> $out.ps
# gmt psbasemap $rgn $proj -BnSeW -Bx20+l"Downstream distance [km]" -By200+l"Elevation [m]" -O >> $out.ps

# ---- Ratios
rgn=-R0.5/4.5/0.6/100
proj=-JX1.8i/1.8il
gmt psbasemap $rgn $proj -B+n -X2.7i -O -K >> $out.ps

awk ' { print $1, $3 } ' ../output/network_example/bifurcation.on | \
  gmt psxy $rgn $proj -W0.8p,lightred,- -O -K >> $out.ps
awk ' { print $1, $3 } ' ../output/network_example/length.ol | \
  gmt psxy $rgn $proj -W0.8p,lightblue,- -O -K >> $out.ps
  awk ' { print $1, $3 } ' ../output/network_example/discharge.oq | \
    gmt psxy $rgn $proj -W0.8p,100/200/100,- -O -K >> $out.ps


awk ' { print $1, $2 } ' ../output/network_example/bifurcation.on | \
  gmt psxy $rgn $proj -SC3.5p -Gred -O -K >> $out.ps
awk ' { print $1, $2 } ' ../output/network_example/length.ol | \
  gmt psxy $rgn $proj -ST3.5p -Gblue -O -K >> $out.ps
awk ' { print $1, $2 } ' ../output/network_example/discharge.oq | \
  gmt psxy $rgn $proj -SS3.5p -G0/125/0 -O -K >> $out.ps

echo "0.7 0.6
1.5 0.6" | gmt psxy $rgn $proj -W0.8p,lightred,- -D0i/0.1i -O -K >> $out.ps
echo 1.1 0.6 | gmt psxy $rgn $proj -SC3.5p -Gred -D0i/0.1i -O -K >> $out.ps
echo 1.5 0.6 "@%2%R@-B@-@%% = $Rb" | \
  gmt pstext $rgn $proj -F+f7p,Helvetica,black+jLM -D0.02i/0.1i -O -K >> $out.ps
echo "0.7 0.6
1.5 0.6" | gmt psxy $rgn $proj -W0.8p,lightblue,- -D0i/0.22i -O -K >> $out.ps
echo 1.1 0.6 | gmt psxy $rgn $proj -ST3.5p -Gblue -D0i/0.22i -O -K >> $out.ps
echo 1.5 0.6 "@%2%R@-L@-@%% = $Rl" | \
  gmt pstext $rgn $proj -F+f7p,Helvetica,black+jLM -D0.02i/0.22i -O -K >> $out.ps
echo "0.7 0.6
1.5 0.6" | gmt psxy $rgn $proj -W0.8p,100/200/100,- -D0i/0.34i -O -K >> $out.ps
echo 1.1 0.6 | gmt psxy $rgn $proj -SS3.5p -G0/125/0 -D0i/0.34i -O -K >> $out.ps
echo 1.5 0.6 "@%2%R@-Q@-@%% = $Rq" | \
  gmt pstext $rgn $proj -F+f7p,Helvetica,black+jLM -D0.02i/0.34i -O -K >> $out.ps
  
gmt psbasemap $rgn $proj -BnSeW \
  -Bx1+l"Stream order, @~\167@~" \
  -Bya1f3p+l"@;red;@%2%N@%%@-@~\167@~@-@;;    @;blue;@%2%L@%%@-@~\167@~@- [km]@;;    @;0/125/0;@%2%Q@%%@-@%2%w@%%,@~\167@~@- [m@+3@+ s@+-1@+]@;;" -O >> $out.ps

# ---- Show
# gv $out.ps &
gmt psconvert -A -E300 -Tj $out.ps
eog $out.jpg &