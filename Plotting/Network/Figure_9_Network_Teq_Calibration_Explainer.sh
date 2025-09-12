#!/bin/bash

# ---- Get useful extra functions
source ../gmt_extras.sh

# ---- Set defaults
gmt_extras::set_gmt_defaults

# variables
out="../../Figures/Figure_9_Network_Teq_Calibration_Explainer"
rgn=-R0.003/300/-0.05/1.1
proj=-JX1.5il/1.5i
rgnx=-R0/100/0/100
projx=-JX1.5i/1.5i
basedir="../../Output/Network/Figure_9_Network_Teq_Calibration_Explainer"

# plot
gmt psbasemap $rgn $proj -B+n -K > $out.ps

gmt psxy $basedir/linear_gain.pg $rgn $proj -W0.8p -O -K >> $out.ps
gmt psxy $basedir/gain_connect.pg $rgn $proj -W0.8p,steelblue -O -K >> $out.ps
gmt psxy $basedir/gain_L.pg $rgn $proj -Sc3.5p -W0.6p,dimgrey -Glightgrey -O -K >> $out.ps
gmt psxy $basedir/gain_Le.pg $rgn $proj -Sc3.5p -Gwhite -O -K >> $out.ps
gmt psxy $basedir/gain_Le.pg $rgn $proj -Sc3.5p -W0.6p,steelblue -Gsteelblue@40 -O -K >> $out.ps
echo "(a)" | gmt pstext $rgn $proj -F+f10p,Helvetica-Bold,black+jTL+cTL -D0.04i/-0.06i -O -K >> $out.ps
gmt psbasemap $rgn $proj -BtSrW -Bx1f3p+l"Period, @%2%P@%% / @%2%T@-eq@-@%% [-]" -By0.2+l"Gain, @[\textit{G\textsubscript{Q\textsubscript{s},L}}@[ [-]" --MAP_LABEL_OFFSET=4p -O -K >> $out.ps
gmt_extras::plot_key_symbol $rgnx $projx 94 91 6 "-Sc3.5p -W0.6p,dimgrey -Glightgrey" "Network, @[\textit{T\textsubscript{eq,max}}@[" $out
gmt_extras::plot_key_symbol $rgnx $projx 94 91 14 "-Sc3.5p -W0.6p,steelblue -Gsteelblue@40" "Network, @[\widehat{\textit{T\textsubscript{eq}}}@[" $out
gmt_extras::plot_key_line $rgnx $projx 97 91 22 -W0.8p "Upstream" $out


rgn=-R0/150/0/0.4
proj=-JX1i/1.5i
gmt psbasemap $rgn $proj -B+n -X2i -O -K >> $out.ps
gmt psxy $basedir/misfit_rng.dat $rgn $proj -W1p -O -K >> $out.ps
gmt psxy $basedir/misfit_L.dat $rgn $proj -Sc3.5p -W0.6p,dimgrey -Glightgrey -O -K >> $out.ps
gmt psxy $basedir/misfit_Le.dat $rgn $proj -Sc3.5p -Gwhite -O -K >> $out.ps
gmt psxy $basedir/misfit_Le.dat $rgn $proj -Sc3.5p -W0.6p,steelblue -Gsteelblue@40 -O -K >> $out.ps
echo "(b)" | gmt pstext $rgn $proj -F+f10p,Helvetica-Bold,black+jTL+cTL -D0.04i/-0.06i -O -K >> $out.ps
gmt psbasemap $rgn $proj -BtSrW -Bx50+l"Network @%2%T@-eq@-@%% [kyr]" -By0.1+l"RMS Misfit [-]" --MAP_LABEL_OFFSET=4p -O -K >> $out.ps
gmt_extras::plot_key_symbol $rgnx $projx 60.6 57.6 94 "-Sc3.5p -W0.6p,dimgrey -Glightgrey" "@[\textit{T\textsubscript{eq,max}}@[" $out
gmt_extras::plot_key_symbol $rgnx $projx 60.6 57.6 86 "-Sc3.5p -W0.6p,steelblue -Gsteelblue@40" "@[\widehat{\textit{T\textsubscript{eq}}}@[" $out


# Finalise, show
gmt psbasemap -R0/1/0/1 -JX2i -B+n -O >> $out.ps
gmt psconvert -A -E300 -Tf $out.ps
convert -density 400x400 -quality 100 -alpha remove $out.pdf $out.jpg
rm $out.ps
eog $out.jpg &