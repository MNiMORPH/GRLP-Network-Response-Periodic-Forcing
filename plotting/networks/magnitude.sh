#!/bin/bash -i

# ---- Defaults
set_gmt_defaults

# ---- Variables
out=magnitude
basedir="../../output/network/magnitude"
rgn=-R-5/105/0.5/0.9
proj=-JX1.5i

# CPT
gmt makecpt -Cviridis -T0/100/1 -Z -D > mag.cpt

# ---- Fixed segment length
gmt psbasemap $rgn $proj -B+n -K > $out.ps
gmt psxy $basedir/fixed_segment_lengths.dat $rgn $proj -Sc3p -W0.8p+cl -Cmag.cpt -t50 -O -K >> $out.ps
echo "a" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
gmt psbasemap $rgn $proj -BnSeW -Bx20+l"Magnitude, @~\155@~ [-]" -By0.1+l"@%2%L@-e@-@%% / @~\341@~@%2%L@%%@~\361@~ [-]" -O -K >> $out.ps

# ---- Variable segment length
gmt psbasemap $rgn $proj -B+n -X1.7i -O -K >> $out.ps
gmt psxy $basedir/variable_segment_lengths.dat $rgn $proj -Sc3p -W0.8p+cl -Cmag.cpt -t50 -O -K >> $out.ps
echo "b" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
gmt psbasemap $rgn $proj -BnSew -Bx20+l"Magnitude, @~\155@~ [-]" -By0.1+ -O -K >> $out.ps

# ---- Finalise
gmt psbasemap -R0/1/0/1 -JX2i -B+n -O >> $out.ps
gmt psconvert -A -E400 -Tf $out.ps
convert -density 600x600 -quality 100 -alpha remove $out.pdf $out.jpg
rm $out.ps
eog $out.jpg &