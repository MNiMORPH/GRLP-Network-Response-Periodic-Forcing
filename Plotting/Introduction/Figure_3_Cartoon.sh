#!/bin/bash

out=../../Figures/Figure_3_Cartoon
height=3.25i

# PANEL A
pic=Cartoon_Drawings/Figure_3a_Upstream_Supply.png
width_pix=$(file $pic | awk ' { print $5 } ')
height_pix=$(file $pic | awk ' { print $7 } ' | sed s/","//)
width=$(echo $height $height_pix $width_pix | awk ' { print $1/$2*$3 } ')i
rgn=-R0/$width_pix/0/$height_pix
proj=-JX$width/$height
gmt psimage $pic $rgn $proj -Dg0/0+w$width -K > $out.ps
echo "(a)" | gmt pstext $rgn $proj -F+f9p,Helvetica-Bold,black+jCT+cCT -N -D-0.65i/-0.075i -O -K >> $out.ps
echo "Single segment" | gmt pstext $rgn $proj -F+f9p,Helvetica-Bold,black+jCT+cCT -D0i/0i -N -O -K >> $out.ps
echo "Upstream supply" | gmt pstext $rgn $proj -F+f9p,Helvetica-Bold,black+jCT+cCT -D0i/-0.15i -N -O -K >> $out.ps
echo "M@+c@+Nab et al. (2023)" | gmt pstext $rgn $proj -F+f7p,Helvetica-Bold,grey+jCT+cCT -N -D0i/-0.34i -O -K >> $out.ps

# PANEL B
pic=Cartoon_Drawings/Figure_3b_Along_Stream_Supply.png
width_pix=$(file $pic | awk ' { print $5 } ')
height_pix=$(file $pic | awk ' { print $7 } ' | sed s/","//)
width=$(echo $height $height_pix $width_pix | awk ' { print $1/$2*$3 } ')i
rgn=-R0/$width_pix/0/$height_pix
proj=-JX$width/$height
gmt psimage $pic $rgn $proj -Dg0/0+w$width -X1.55i -O -K >> $out.ps
echo "(b)" | gmt pstext $rgn $proj -F+f9p,Helvetica-Bold,black+jCT+cCT -N -D-0.75i/-0.075i -O -K >> $out.ps
echo "Single segment" | gmt pstext $rgn $proj -F+f9p,Helvetica-Bold,black+jCT+cCT -D0i/0i -N -O -K >> $out.ps
echo "Along-stream supply" | gmt pstext $rgn $proj -F+f9p,Helvetica-Bold,black+jCT+cCT -D0i/-0.15i -N -O -K >> $out.ps
echo "This study" | gmt pstext $rgn $proj -F+f7p,Helvetica-Bold,grey+jCT+cCT -N -D0i/-0.34i -O -K >> $out.ps

# PANEL C
pic=Cartoon_Drawings/Figure_3c_Network.png
width_pix=$(file $pic | awk ' { print $5 } ')
height_pix=$(file $pic | awk ' { print $7 } ' | sed s/","//)
width=$(echo $height $height_pix $width_pix | awk ' { print $1/$2*$3 } ')i
rgn=-R0/$width_pix/0/$height_pix
proj=-JX$width/$height
gmt psimage $pic $rgn $proj -Dg0/0+w$width -X2.25i -O -K >> $out.ps
echo "(c)" | gmt pstext $rgn $proj -F+f9p,Helvetica-Bold,black+jCT+cCT -N -D-1.5i/-0.075i -O -K >> $out.ps
echo "Network" | gmt pstext $rgn $proj -F+f9p,Helvetica-Bold,black+jCT+cCT -D-0.8i/0i -N -O -K >> $out.ps
echo "Upstream supply" | gmt pstext $rgn $proj -F+f9p,Helvetica-Bold,black+jCT+cCT -D-0.8i/-0.15i -N -O -K >> $out.ps
echo "This study" | gmt pstext $rgn $proj -F+f7p,Helvetica-Bold,grey+jCT+cCT -N -D-0.8i/-0.32i -O -K >> $out.ps
echo "Network" | gmt pstext $rgn $proj -F+f9p,Helvetica-Bold,black+jCT+cCT -D0.65i/0i -N -O -K >> $out.ps
echo "Along-stream supply" | gmt pstext $rgn $proj -F+f9p,Helvetica-Bold,black+jCT+cCT -D0.65i/-0.15i -N -O -K >> $out.ps
echo "This study" | gmt pstext $rgn $proj -F+f7p,Helvetica-Bold,grey+jCT+cCT -N -D0.65i/-0.34i -O >> $out.ps

# SHOW
gmt psconvert -A -E600 -Tj $out.ps
gmt psconvert -A -E300 -Tf $out.ps
rm $out.ps
eog $out.jpg &