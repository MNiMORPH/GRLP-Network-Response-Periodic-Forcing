#!/bin/bash

# ---- Get useful extra functions
source ../gmt_extras.sh

# ---- Set defaults
gmt_extras::set_gmt_defaults

# ---- Inputs / Output
basedir="../../Output/Network/Figure_17_Network_Short_Period_Lag"
out="../../Figures/Figure_17_Network_Short_Period_Lag"

# ---- CPTs
gmt makecpt -T10/20/1 -Cviridis -Z -D > inlet.cpt

proj=-JX1.5il/1.5i
rgn_l=-R0.007/4/0/1.05
gmt psbasemap $rgn_l $proj -B+n -K > $out.ps
gmt psxy $basedir/UUU_Qs_lag.pl $rgn_l $proj -Sc2.5p -t50 -Cinlet.cpt -O -K >> $out.ps
echo "(a)" | gmt pstext $rgn_l $proj -F+f10p,Helvetica-Bold,black+jTR+cTR -D-0.05i/-0.08i -O -K >> $out.ps
echo "Uniform segment lengths" | gmt pstext $rgn_l $proj -F+f8p+jCB+cCT -D0i/0.07i -N -O -K >> $out.ps
gmt psbasemap $rgn_l $proj \
  -BtSeW \
  -Bx1f3p+l"Period, \textit{P} / @[\widehat{\textit{T\textsubscript{eq}}}@[ [-]" \
  -By0.2+l"Lag, @[\varphi\textit{\textsubscript{Q\textsubscript{s},L} / P}@[ [-]" \
  --MAP_LABEL_OFFSET=3p \
  -O -K >> $out.ps

proj=-JX1.5il/1.5i
rgn_l=-R0.007/4/0/1.05
gmt psbasemap $rgn_l $proj -B+n -X1.65i -O -K >> $out.ps
gmt psxy $basedir/NUU_Qs_lag.pl $rgn_l $proj -Sc2.5p -t50 -Cinlet.cpt -O -K >> $out.ps
echo "(b)" | gmt pstext $rgn_l $proj -F+f10p,Helvetica-Bold,black+jTR+cTR -D-0.05i/-0.08i -O -K >> $out.ps
echo "Non-uniform segment lengths" | gmt pstext $rgn_l $proj -F+f8p+jCB+cCT -D0i/0.07i -N -O -K >> $out.ps
gmt psscale $rgn $proj \
  -Cinlet.cpt \
  -Dx0.75i/1.4i+w0.7i/0.07i+h+e+jMC \
  -B2+l"First inlet length [km]" \
  --MAP_LABEL_OFFSET=-8p \
  --MAP_ANNOT_OFFSET=5p \
  --MAP_TICK_LENGTH=7p \
  --MAP_DEFAULT_PEN=7p \
  --MAP_TICK_PEN=1.5p \
  --FONT=14p \
  -O -K >> $out.ps
  gmt psbasemap $rgn_l $proj \
    -BtSew \
    -Bx1f3p+l"Period, \textit{P} / @[\widehat{\textit{T\textsubscript{eq}}}@[ [-]" \
    -By0.2+l"Lag, @[\varphi\textit{\textsubscript{Q\textsubscript{s},L} / P}@[ [-]" \
    --MAP_LABEL_OFFSET=3p \
    -O -K >> $out.ps


rgn=-R0/3.15/0/3.15
proj=-JX3.15i
gmt psbasemap $rgn $proj -B+n -X-1.65i -O -K >> $out.ps
echo "0.75 1.7
0.75 1.75
2.4 1.75
2.4 1.7" | gmt psxy $rgn $proj -W0.8p -O -K >> $out.ps
echo "Upstream supply" | gmt pstext $rgn $proj -F+f8p+jCM+cCB -D0i/1.75i -Gwhite -N -O -K >> $out.ps

# Finalise, show
gmt psbasemap -R0/1/0/1 -JX2i -B+n -O >> $out.ps
gmt psconvert -A -E300 -Tf $out.ps
convert -density 300x300 -quality 90 -alpha remove $out.pdf $out.jpg
rm $out.ps *.cpt
eog $out.jpg &