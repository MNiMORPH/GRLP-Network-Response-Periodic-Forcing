#!/bin/bash

out=../../Figures/Figure_2_Cartoon
height=3.5i

# PANEL A
pic=../../Cartoon/Figure_2a_Upstream_Supply.png
width_pix=$(file $pic | awk ' { print $5 } ')
height_pix=$(file $pic | awk ' { print $7 } ' | sed s/","//)
width=$(echo $height $height_pix $width_pix | awk ' { print $1/$2*$3 } ')i
rgn=-R0/$width_pix/0/$height_pix
proj=-JX$width/$height
gmt psimage $pic $rgn $proj -Dg0/0+w$width -K > $out.ps
echo "a" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jLM+cLT -W0.8p -N -C20%/20% -D0i/0.25i -O -K >> $out.ps
echo "Upstream supply" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jCM+cCT -N -D0i/0.25i -O -K >> $out.ps

# PANEL B
pic=../../Cartoon/Figure_2b_Along_Stream_Supply.png
width_pix=$(file $pic | awk ' { print $5 } ')
height_pix=$(file $pic | awk ' { print $7 } ' | sed s/","//)
width=$(echo $height $height_pix $width_pix | awk ' { print $1/$2*$3 } ')i
rgn=-R0/$width_pix/0/$height_pix
proj=-JX$width/$height
gmt psimage $pic $rgn $proj -Dg0/0+w$width -X2.5i -O -K >> $out.ps
echo "b" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jLM+cLT -W0.8p -N -C20%/20% -D0i/0.25i -O -K >> $out.ps
echo "Along-stream supply" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jCM+cCT -N -D0i/0.25i -O >> $out.ps

# SHOW
gmt psconvert -A -E600 -Tj $out.ps
rm $out.ps
eog $out.jpg &