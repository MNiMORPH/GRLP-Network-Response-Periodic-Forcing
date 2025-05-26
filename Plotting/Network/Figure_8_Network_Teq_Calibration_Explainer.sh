#!/bin/bash

# ---- Get useful extra functions
source ../gmt_extras.sh

# ---- Set defaults
gmt_extras::set_gmt_defaults

# variables
out="../../Figures/Figure_8_Network_Teq_Calibration_Explainer"
rgn=-R0.003/300/-0.05/1.1
proj=-JX1.5il/1.5i
rgnx=-R0/100/0/100
projx=-JX1.5i/1.5i
basedir="../../Output/Network/Figure_8_Network_Teq_Calibration_Explainer"

# plot
gmt psbasemap $rgn $proj -B+n -K > $out.ps

# gmt psxy $basedir/continuous_gain.pg $rgn $proj -Glightgrey -W0.8p,lightgrey -O -K >> $out.ps
gmt psxy $basedir/linear_gain.pg $rgn $proj -W0.8p -O -K >> $out.ps
gmt psxy $basedir/gain_connect.pg $rgn $proj -W0.8p,steelblue -O -K >> $out.ps
# gmt psxy $basedir/gain_connect.pg $rgn $proj -W0.8p,steelblue -S~n1:+skrtriangle/1.5p+p0.8p,steelblue -O -K >> $out.ps
gmt psxy $basedir/gain_L.pg $rgn $proj -Sc3.5p -W0.6p,dimgrey -Glightgrey -O -K >> $out.ps
gmt psxy $basedir/gain_Le.pg $rgn $proj -Sc3.5p -Gwhite -O -K >> $out.ps
gmt psxy $basedir/gain_Le.pg $rgn $proj -Sc3.5p -W0.6p,steelblue -Gsteelblue@40 -O -K >> $out.ps
echo a | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
gmt psbasemap $rgn $proj -BtSrW -Bx1f3p+l"Period, @%2%P@%% / @%2%T@-eq@-@%% [-]" -By0.2+l"Gain, @[\textit{G\textsubscript{Q\textsubscript{s},L}}@[ [-]" --MAP_LABEL_OFFSET=4p -O -K >> $out.ps
# gmt_extras::plot_key_line $rgnx $projx 3 9 77 -W4p,lightgrey "Along stream" $out
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
echo b | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
gmt psbasemap $rgn $proj -BtSrW -Bx50+l"Network @%2%T@-eq@-@%% [kyr]" -By0.1+l"RMS Misfit [-]" --MAP_LABEL_OFFSET=4p -O -K >> $out.ps
gmt_extras::plot_key_symbol $rgnx $projx 60.6 57.6 94 "-Sc3.5p -W0.6p,dimgrey -Glightgrey" "@[\textit{T\textsubscript{eq,max}}@[" $out
gmt_extras::plot_key_symbol $rgnx $projx 60.6 57.6 86 "-Sc3.5p -W0.6p,steelblue -Gsteelblue@40" "@[\widehat{\textit{T\textsubscript{eq}}}@[" $out



#   proj_in=-JX0.35i
#   rgn_in=-R0/200/0/50
#   gmt psbasemap $rgn_in $proj_in -B+n -Y0.28i -X1.05i -O -K >> $out.ps
#   gmt pshistogram $basedir/MC_N1_40/${sweepdirs[$i]}/Teq_max.t $rgn_in $proj_in -Gsteelblue -W0.1p,steelblue -T15+n -O -K >> $out.ps
#   gmt psbasemap $rgn_in $proj_in \
#     -BSW -Bx100+l"@[\textit{T\textsubscript{eq,max}}@[ [kyr]" -By25 \
#     --MAP_TICK_LENGTH_PRIMARY=2p \
#     --MAP_FRAME_PEN=0.8p \
#     --FONT_LABEL=5p \
#     --FONT_ANNOT_PRIMARY=5p \
#     --MAP_LABEL_OFFSET=2p \
#     -O -K >> $out.ps
# 
#   gmt psbasemap $rgn $proj -B+n -Y-2.28i -X-1.05i -O -K >> $out.ps
#   gmt psxy $basedir/continuous_gain.pg $rgn $proj -Glightgrey -W0.8p,lightgrey -O -K >> $out.ps
#   gmt psxy $basedir/linear_gain.pg $rgn $proj -W0.8p -O -K >> $out.ps
#   gmt psxy $basedir/MC_N1_40/${sweepdirs[$i]}/gain_Le.pg $rgn $proj -Sc3.5p -W0.6p,steelblue -t75 -O -K >> $out.ps
#   echo "${Le_labs[$i]}" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
#   gmt psbasemap $rgn $proj -BnSe${W} -Bx1f3p+l"Period, \textit{P} / @[\widehat{\textit{T\textsubscript{eq}}}@[ [-]" -By0.2+l"Gain, @[\textit{G\textsubscript{Q\textsubscript{s},L}}@[ [-]" -O -K >> $out.ps
# 
#   proj_in=-JX0.35i
#   rgn_in=-R0/200/0/50
#   gmt psbasemap $rgn_in $proj_in -B+n -Y0.28i -X1.05i -O -K >> $out.ps
#   gmt pshistogram $basedir/MC_N1_40/${sweepdirs[$i]}/Teq.t $rgn_in $proj_in -Gsteelblue -W0.1p,steelblue -T15+n -O -K >> $out.ps
#   gmt psbasemap $rgn_in $proj_in \
#     -BSW -Bx100+l"@[\widehat{\textit{T\textsubscript{eq}}}@[ [kyr]" -By25 \
#     --MAP_TICK_LENGTH_PRIMARY=2p \
#     --MAP_FRAME_PEN=0.8p \
#     --FONT_LABEL=5p \
#     --FONT_ANNOT_PRIMARY=5p \
#     --MAP_LABEL_OFFSET=2p \
#     -O -K >> $out.ps
# done
# 
# rgn=-R0/3.15/0/3.15
# proj=-JX3.15i
# gmt psbasemap $rgn $proj -B+n -Y1.72i -X-6i -O -K >> $out.ps
# echo "0.75 1.72
# 0.75 1.79
# 2.4 1.79
# 2.4 1.72" | gmt psxy $rgn $proj -W0.8p -O -K >> $out.ps
# echo "Upstream supply" | gmt pstext $rgn $proj -F+f8p+jCM+cCB -D0i/1.79i -Gwhite -N -O -K >> $out.ps
# 
# gmt psbasemap $rgn $proj -B+n -X3.3i -O -K >> $out.ps
# echo "0.75 1.72
# 0.75 1.79
# 2.4 1.79
# 2.4 1.72" | gmt psxy $rgn $proj -W0.8p -O -K >> $out.ps
# echo "Along-stream supply" | gmt pstext $rgn $proj -F+f8p+jCM+cCB -D0i/1.79i -Gwhite -N -O -K >> $out.ps


# Finalise, show
gmt psbasemap -R0/1/0/1 -JX2i -B+n -O >> $out.ps
gmt psconvert -A -E400 -Tf $out.ps
convert -density 600x600 -quality 100 -alpha remove $out.pdf $out.jpg
rm $out.ps $out.pdf
eog $out.jpg &