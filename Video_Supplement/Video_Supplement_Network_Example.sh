#!/bin/bash

# ---- Get useful extra functions
source ../Plotting/gmt_extras.sh

# ---- Set defaults
gmt_extras::set_gmt_defaults

# ---- Variables
basedir=./Output

# ---- CPTs
gmt makecpt -T-0.17/0.17/0.01 -Croma -D -Z -I > dz_fast.cpt
gmt makecpt -T-0.17/0.17/0.01 -Croma -D -Z -I > dz_medium.cpt
gmt makecpt -T-0.17/0.17/0.01 -Croma -D -Z -I > dz_slow.cpt

# ---- Plot initial set up
echo "Plotting initial set up."

out=init

rgn=-R-5/105/0/21
proj=-JX2i

gmt psbasemap $rgn $proj -B+n -Y4i -K > $out.ps
echo "(d)" | gmt pstext $rgn $proj -F+f10p,Helvetica-Bold,black+jLT+cLT -D0.04i/-0.07i -O -K >> $out.ps
gmt psscale $rgn $proj -Dx0.1i/1.4i+w0.5i/0.05i+jMC+e -Cdz_fast.cpt \
  -B0.17+l"@[\delta\textit{z}~/~\overline{\textit{z}}@[ [-]" \
  --MAP_LABEL_OFFSET=6p \
  --MAP_ANNOT_OFFSET=4p \
  --MAP_TICK_LENGTH=5p \
  --MAP_DEFAULT_PEN=5p \
  --MAP_TICK_PEN=1p \
  --FONT=16p \
  -O -K >> $out.ps
gmt psbasemap $rgn $proj -BtSlr -Bx20+l"Downstream distance, @%2%x@%% [km]" -O -K >> $out.ps

gmt psbasemap $rgn $proj -B+n -X2.25i -O -K >> $out.ps
echo "(e)" | gmt pstext $rgn $proj -F+f10p,Helvetica-Bold,black+jLT+cLT -D0.04i/-0.07i -O -K >> $out.ps
gmt psscale $rgn $proj -Dx0.1i/1.4i+w0.5i/0.05i+jMC+e -Cdz_medium.cpt \
  -B0.17+l"@[\delta\textit{z}~/~\overline{\textit{z}}@[ [-]" \
  --MAP_LABEL_OFFSET=6p \
  --MAP_ANNOT_OFFSET=4p \
  --MAP_TICK_LENGTH=5p \
  --MAP_DEFAULT_PEN=5p \
  --MAP_TICK_PEN=1p \
  --FONT=16p \
  -O -K >> $out.ps
gmt psbasemap $rgn $proj -BtSlr -Bx20+l"Downstream distance, @%2%x@%% [km]" -O -K >> $out.ps

gmt psbasemap $rgn $proj -B+n -X2.25i -O -K >> $out.ps
echo "(f)" | gmt pstext $rgn $proj -F+f10p,Helvetica-Bold,black+jLT+cLT -D0.04i/-0.07i -O -K >> $out.ps
gmt psscale $rgn $proj -Dx0.1i/1.4i+w0.5i/0.05i+jMC+e -Cdz_slow.cpt \
  -B0.17+l"@[\delta\textit{z}~/~\overline{\textit{z}}@[ [-]" \
  --MAP_LABEL_OFFSET=6p \
  --MAP_ANNOT_OFFSET=4p \
  --MAP_TICK_LENGTH=5p \
  --MAP_DEFAULT_PEN=5p \
  --MAP_TICK_PEN=1p \
  --FONT=16p \
  -O -K >> $out.ps
gmt psbasemap $rgn $proj -BtSlr -Bx20+l"Downstream distance, @%2%x@%% [km]" -O -K >> $out.ps

proj=-JX2i/0.6i

rgn=-R0/26/0.7/1.3
gmt psbasemap $rgn $proj -B+n -Y2.5i -X-4.5i -O -K >> $out.ps
gmt psxy $basedir/fast/force_tps.te $rgn $proj -W0.8p,lightgrey -O -K >> $out.ps
gmt psxy $basedir/fast/force.tq $rgn $proj -W0.8p,lightred -O -K >> $out.ps
echo "(a)" | gmt pstext $rgn $proj -F+f10p,Helvetica-Bold,black+jLB+cLB -D0.04i/0.08i -Gwhite -C30%/30% -O -K >> $out.ps
echo "@%2%P@%% = @%2%T@-eq@-@%% / 10" | \
  gmt pstext $rgn $proj -F+f11p,Helvetica,black+jBC+cTC -D0i/0.12i -N -O -K >> $out.ps

rgn=-R0/260/0.7/1.3
gmt psbasemap $rgn $proj -B+n -X2.25i -O -K >> $out.ps
gmt psxy $basedir/medium/force_tps.te $rgn $proj -W0.8p,lightgrey -O -K >> $out.ps
gmt psxy $basedir/medium/force.tq $rgn $proj -W0.8p,lightred -O -K >> $out.ps
echo "(b)" | gmt pstext $rgn $proj -F+f10p,Helvetica-Bold,black+jLB+cLB -D0.04i/0.08i -Gwhite -C30%/30% -O -K >> $out.ps
echo "@%2%P@%% = @%2%T@-eq@-@%%" | \
  gmt pstext $rgn $proj -F+f11p,Helvetica,black+jBC+cTC -D0i/0.12i -N -O -K >> $out.ps

rgn=-R0/2600/0.7/1.3
gmt psbasemap $rgn $proj -B+n -X2.25i -O -K >> $out.ps
gmt psxy $basedir/slow/force_tps.te $rgn $proj -W0.8p,lightgrey -O -K >> $out.ps
gmt psxy $basedir/slow/force.tq $rgn $proj -W0.8p,lightred -O -K >> $out.ps
echo "(c)" | gmt pstext $rgn $proj -F+f10p,Helvetica-Bold,black+jLB+cLB -D0.04i/0.08i -Gwhite -C30%/30% -O -K >> $out.ps
echo "@%2%P@%% = @%2%T@-eq@-@%% @~\264@~ 10" | \
  gmt pstext $rgn $proj -F+f11p,Helvetica,black+jBC+cTC -D0i/0.12i -N -O -K >> $out.ps

# ---- Plot time dependent bits
echo "Plotting individual frames:"

for frame in {000..160} ; do
  
  echo "    - $frame"

  outf=$frame
  cp $out.ps $outf.ps
  
  rgn=-R-5/105/0/21
  proj=-JX2i

  gmt psbasemap $rgn $proj -B+n -Y-2.5i -X-4.5i -O -K >> $outf.ps
  gmt psxy $basedir/fast/frame${frame}_dz.de $rgn $proj -W1.2p -Cdz_fast.cpt -O -K >> $outf.ps

  gmt psbasemap $rgn $proj -B+n -X2.25i -O -K >> $outf.ps
  gmt psxy $basedir/medium/frame${frame}_dz.de $rgn $proj -W1.2p -Cdz_medium.cpt -O -K >> $outf.ps

  gmt psbasemap $rgn $proj -B+n -X2.25i -O -K >> $outf.ps
  gmt psxy $basedir/slow/frame${frame}_dz.de $rgn $proj -W1.2p -Cdz_slow.cpt -O -K >> $outf.ps

  proj=-JX2i/0.6i
  
  rgn=-R0/26/0.7/1.3
  gmt psbasemap $rgn $proj -B+n -Y2.5i -X-4.5i -O -K >> $outf.ps
  gmt psxy $basedir/fast/frame${frame}_force.tq $rgn $proj -W0.8p,red -O -K >> $outf.ps
  gmt psxy $basedir/fast/frame${frame}_force_tps.tq $rgn $proj -Sc2p -Gred -O -K >> $outf.ps
  gmt psxy $basedir/fast/frame${frame}_Qs_out.tq $rgn $proj -W0.8p,black -O -K >> $outf.ps
  gmt psxy $basedir/fast/frame${frame}_Qs_out_tps.tq $rgn $proj -Sc2p -Gblack -O -K >> $outf.ps
  gmt psbasemap $rgn $proj -BW -Bx5+l"Time, @%2%t@%% [kyr]" \
    -By0.2+l"@[\textit{Q\textsubscript{s,0}}~/~\overline{\textit{Q\textsubscript{s,0}}}@[ [-]" \
    --FONT=red \
    --MAP_FRAME_PEN=red \
    --MAP_TICK_PEN_PRIMARY=red \
    --MAP_LABEL_OFFSET=4p \
    -O -K >> $outf.ps
  gmt psbasemap $rgn $proj -BtSe -Bx5+l"Time, @%2%t@%% [kyr]" -By0.2 -O -K >> $outf.ps

  rgn=-R0/260/0.7/1.3
  gmt psbasemap $rgn $proj -B+n -X2.25i -O -K >> $outf.ps
  gmt psxy $basedir/medium/frame${frame}_force.tq $rgn $proj -W0.8p,red -O -K >> $outf.ps
  gmt psxy $basedir/medium/frame${frame}_force_tps.tq $rgn $proj -Sc2p -Gred -O -K >> $outf.ps
  gmt psxy $basedir/medium/frame${frame}_Qs_out.tq $rgn $proj -W0.8p,black -O -K >> $outf.ps
  gmt psxy $basedir/medium/frame${frame}_Qs_out_tps.tq $rgn $proj -Sc2p -Gblack -O -K >> $outf.ps
  gmt psbasemap $rgn $proj -Bw -Bx50+l"Time, @%2%t@%% [kyr]" \
    -By0.2+l"@[\textit{Q\textsubscript{s,0}}~/~\overline{\textit{Q\textsubscript{s,0}}}@[ [-]" \
    --FONT=red \
    --MAP_FRAME_PEN=red \
    --MAP_TICK_PEN_PRIMARY=red \
    --MAP_LABEL_OFFSET=4p \
    -O -K >> $outf.ps
  gmt psbasemap $rgn $proj -BtSe -Bx50+l"Time, @%2%t@%% [kyr]" -By0.2 -O -K >> $outf.ps

  rgn=-R0/2600/0.7/1.3
  gmt psbasemap $rgn $proj -B+n -X2.25i -O -K >> $outf.ps
  gmt psxy $basedir/slow/frame${frame}_force.tq $rgn $proj -W0.8p,red -O -K >> $outf.ps
  gmt psxy $basedir/slow/frame${frame}_force_tps.tq $rgn $proj -Sc2p -Gred -O -K >> $outf.ps
  gmt psxy $basedir/slow/frame${frame}_Qs_out.tq $rgn $proj -W0.8p,black -O -K >> $outf.ps
  gmt psxy $basedir/slow/frame${frame}_Qs_out_tps.tq $rgn $proj -Sc2p -Gblack -O -K >> $outf.ps
  gmt psbasemap $rgn $proj -Bw -Bx500+l"Time, @%2%t@%% [kyr]" \
    -By0.2+l"@[\textit{Q\textsubscript{s,0}}~/~\overline{\textit{Q\textsubscript{s,0}}}@[ [-]" \
    --FONT=red \
    --MAP_FRAME_PEN=red \
    --MAP_TICK_PEN_PRIMARY=red \
    --MAP_LABEL_OFFSET=4p \
    -O -K >> $outf.ps
  gmt psbasemap $rgn $proj -BtSE -Bx500+l"Time, @%2%t@%% [kyr]" \
    -By0.2+l"@[\textit{Q\textsubscript{s,L}}~/~\overline{\textit{Q\textsubscript{s,L}}}@[ [-]" \
    --MAP_LABEL_OFFSET=4p \
    -O -K >> $outf.ps

  # ---- Convert
  gmt psbasemap $rgn $proj -B+n -O >> $outf.ps
  gmt psconvert -A -E180 -Tj $outf.ps

done

# ---- GIF
echo "Creating final GIF."
convert -delay 10 -loop 0 ???.jpg -delay 100 160.jpg 000.jpg Video_Supplement_Network_Example.gif
atom Video_Supplement_Network_Example.gif

# ---- Tidy up
rm *.ps *.jpg *.cpt gmt.*