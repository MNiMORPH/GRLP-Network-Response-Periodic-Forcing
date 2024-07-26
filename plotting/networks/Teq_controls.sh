#!/bin/bash -i

# Set defaults
set_gmt_defaults

rgn=-R45/85/31.76/113.3
proj=-JX3i
basedir="../../output/network/Teq_controls"
out=Teq_controls

# gmt psbasemap $rgn $proj -B+n -K > $out.ps
# gmt psxy $basedir/Teq_vs_Le_fit.txt $rgn $proj -W1p,255/127/14,3p_2p -O -K >> $out.ps
# gmt psxy $basedir/Teq_vs_Le.txt $rgn $proj -Sc3.5p -G31/119/180 -t60 -O -K >> $out.ps
# gmt psxy $basedir/Teq_vs_Le.txt $rgn $proj -Sc3.5p -W0.8p,31/119/180 -t50 -O -K >> $out.ps
# gmt psbasemap $rgn $proj -BnSeW -Bx5+l"Mean downstream distance, @~\341@~@%2%L@%%@~\361@~ [km]" -By10+l"Equilibration time, @%2%T@-eq@-@%% [kyr]" -O >> $out.ps
# 
# gmt psconvert -A -E400 -Tf $out.ps
# convert -density 600x600 -quality 100 -alpha remove $out.pdf $out.jpg
# rm $out.ps $out.pdf
# eog $out.jpg


out=planforms
proj=-JX2i
gmt psbasemap $rgn $proj -X-2i -Y3i -B+n -K > $out.ps

for i in $(seq 0 1 5) ; do

  if [ $i -eq 3 ] ; then
    x_off=-4.8i
    y_off=-2.5i
  else
    x_off=2.4i
    y_off=0i
  fi

  ymax=$(gmt gmtinfo -C $basedir/planform_${i}.d | awk ' { print $4*1.05 } ')
  rgn=-R0/100/0/$ymax
  gmt psbasemap $rgn $proj -B+n -Y$y_off -X$x_off -O -K >> $out.ps
  gmt psxy $basedir/planform_${i}.d $rgn $proj -W1.4p -Corder.cpt -O -K >> $out.ps
  gmt psbasemap $rgn $proj -BS -Bx20+l"Downstream distance [km]" -O -K >> $out.ps

done

gmt psscale $rgn $proj \
  -Corder.cpt \
  -Dx2i/1.5i+w1i/0.07i+jMC+m \
  -B1+l"Stream order" \
  -O -K >> $out.ps

gmt psbasemap $rgn $proj -B+n -O >> $out.ps
gmt psconvert -A -E400 -Tf $out.ps
convert -density 600x600 -quality 100 -alpha remove $out.pdf $out.jpg
rm $out.ps $out.pdf
eog $out.jpg
