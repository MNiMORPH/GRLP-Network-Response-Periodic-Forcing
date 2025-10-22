#!/bin/bash

out=../../Figures/Key_Figure
height=3.25i

# PANEL C
pic=Cartoon_Drawings/Figure_3c_Network.png
width_pix=$(file $pic | awk ' { print $5 } ')
height_pix=$(file $pic | awk ' { print $7 } ' | sed s/","//)
width=$(echo $height $height_pix $width_pix | awk ' { print $1/$2*$3 } ')i
rgn=-R0/$width_pix/0/$height_pix
proj=-JX$width/$height
gmt psimage $pic $rgn $proj -Dg0/0+w$width -K > $out.ps
echo "Network" | gmt pstext $rgn $proj -F+f9p,Helvetica-Bold,black+jCT+cCT -D-0.8i/-0.05i -N -O -K >> $out.ps
echo "Upstream supply" | gmt pstext $rgn $proj -F+f9p,Helvetica-Bold,black+jCT+cCT -D-0.8i/-0.22i -N -O -K >> $out.ps
echo "Network" | gmt pstext $rgn $proj -F+f9p,Helvetica-Bold,black+jCT+cCT -D0.65i/-0.05i -N -O -K >> $out.ps
echo "Along-stream supply" | gmt pstext $rgn $proj -F+f9p,Helvetica-Bold,black+jCT+cCT -D0.65i/-0.22i -N -O >> $out.ps

# SHOW
gmt psconvert -A -E600 -Tj $out.ps
rm $out.ps
eog $out.jpg &