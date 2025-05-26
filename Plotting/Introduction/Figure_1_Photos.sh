#!/bin/bash

out=../../Figures/Figure_1_Photos

# Kyrgyz
photo=../../Photos/Kyrgyz_edit.jpg
rgn=-R0/2735/0/1564
proj=-JX3.5i/2i
gmt psbasemap $rgn $proj -B+n -Y4i -K > $out.ps
gmt psimage $photo $rgn $proj -Dg0/0+w0/2i -O -K >> $out.ps
echo "a" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jLT+cLT -D0.06i/-0.08i -O -K >> $out.ps
gmt psbasemap $rgn $proj -B0 -O -K >> $out.ps

# Toro
photo=../../Photos/Toro_edit.jpg
rgn=-R0/2542/0/1442
proj=-JX3.5i/2i
gmt psbasemap $rgn $proj -B+n -Y-2.15i -O -K >> $out.ps
gmt psimage $photo $rgn $proj -Dg0/0+w0/2i -O -K >> $out.ps
echo "b" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jLT+cLT -D0.06i/-0.08i -O -K >> $out.ps
gmt psbasemap $rgn $proj -B0 -O -K >> $out.ps

# France
photo=../../Photos/France_Edit.jpg
rgn=-R0/948/0/1422
proj=-JX2.7667i/4.15i
gmt psbasemap $rgn $proj -B+n -X3.65i -O -K >> $out.ps
gmt psimage $photo $rgn $proj -Dg0/0+w0/4.15i -O -K >> $out.ps
echo "c" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jLT+cLT -D0.06i/-0.08i -O -K >> $out.ps
gmt psbasemap $rgn $proj -B0 -O >> $out.ps

# gv $out.ps
gmt psconvert -A -E400 -Tj $out.ps
rm $out.ps
eog $out.jpg &