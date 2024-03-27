#!/bin/bash -i

# Set defaults
set_gmt_defaults

# Variables
out=controls
proj=-JX1.15i
proj_hist=-JX1.15i/0.15i
basedir="../../output/network/controls"
sweepfiles=("m20_fix_seg_length.dat" "m40_fix_seg_length.dat" "m2-100_fix_seg_length.dat" "m40_rnd_seg_length.dat" "m2-100_rnd_seg_length.dat")
# Rb_ticks=(100 150 25 150)
# Rl_ticks=(50 100 30 80)
# Rq_ticks=(50 100 40 30)
# h_ticks=(40 40 20 30)
# L_ticks=(60 60 30 25)
# Le_ticks=(70 60 40 30)

Rb_just=("TL" "TL" "BL" "TL" "TL")
Rb_off=("0.05i/0i" "0.05i/0i" "0i/0.01i" "0.05i/0i" "0.05i/0i")
Rl_just=("BL" "TL" "TR" "TR" "TR")
Rl_off=("0i/0.01i" "0.05i/0i" "-0.01i/0i" "-0.01i/0i" "-0.01i/0i")
Rq_just=("TR" "TL" "BL" "ML" "ML")
Rq_off=("-0.01i/0i" "0.05i/0i" "0i/0.01i" "0.05i/0i" "0.05i/0i")
h_just=("BL" "BL" "BL" "ML" "ML")
h_off=("0i/0.01i" "0i/0.01i" "0i/0.01i" "0.05i/0i" "0.05i/0i")
L_just=("BL" "BL" "BL" "ML" "ML")
L_off=("0i/0.01i" "0i/0.01i" "0i/0.01i" "0.05i/0i" "0.05i/0i")
Le_just=("BL" "BL" "BL" "BL" "BL")
Le_off=("-0.01i/0i" "-0.01i/0i" "-0.01i/0i" "-0.01i/0i" "-0.01i/0i")

Rb_labs=("a" "f" "k" "p" "u")
Rl_labs=("b" "g" "l" "q" "v")
Rq_labs=("c" "h" "m" "r" "w")
h_labs=("d" "i" "n" "s" "x")
L_labs=("e" "j" "o" "t" "y")

gmt psbasemap -R0/1/0/1 $proj -B+n -Y9i -X7i -K > $out.ps
for i in ${!sweepfiles[@]} ; do
  
  if [ $i -eq 4 ] ; then
    S="S"
  else
    S="s"
  fi
  # if [ $i -eq 0 ] ; then
  #   N="N"
  # else
  #   N="n"
  # fi

  # Rb
  rgn=-R0/8/10/80
  gmt psbasemap $rgn $proj -B+n -X-6.2i -Y-1.3i -O -K >> $out.ps
  awk ' { print $1, $6, $7 } ' $basedir/${sweepfiles[$i]} | \
    gmt psxy $rgn $proj -Sc2.5p -W0.8p+cl -Cmag.cpt -t80 -O -K >> $out.ps
  echo "${Rb_labs[$i]}" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
  gmt psbasemap $rgn $proj -Bt${S}rW -Bpx2+l"@%2%R@-b@-@%% [-]" -By20+l"@%2%L@-e@-@%% [km]" -O -K >> $out.ps
  max=$(awk ' { print $1 } ' $basedir/${sweepfiles[$i]} | gmt pshistogram -R0/8/0/500 $proj_hist -Gdimgrey -T30+n -I | awk ' { print $4 } ')
  max_x=$(awk ' { print $1 } ' $basedir/${sweepfiles[$i]} | gmt pshistogram -R0/8/0/500 -T30+n -Io | grep $max | awk ' { print $1 } ')
  rgn_hist=-R0/8/0/$max
  # min=$(awk ' { print $1 } ' $basedir/${sweepfiles[$i]} | gmt gmtinfo -C | awk ' { print $1 } ')
  # max=$(awk ' { print $1 } ' $basedir/${sweepfiles[$i]} | gmt gmtinfo -C | awk ' { print $2 } ')
  awk ' { print $1 } ' $basedir/${sweepfiles[$i]} | \
    gmt pshistogram $rgn_hist $proj_hist -Gdimgrey -T30+n -O -K >> $out.ps
  echo $max_x $max $max | gmt pstext $rgn_hist $proj_hist -F+f5p,dimgrey+j${Rb_just[$i]} -D${Rb_off[$i]} -N -O -K >> $out.ps
  gmt psbasemap $rgn_hist $proj_hist -Bb -Bpx2+l"@%2%R@-b@-@%% [-]" -By${Rb_ticks[$i]} --MAP_FRAME_TYPE=inside --FONT_ANNOT_PRIMARY=6p -O -K >> $out.ps

  # Rl
  gmt psbasemap $rgn $proj -B+n -X1.3i -O -K >> $out.ps
  awk ' { print $2, $6, $7 } ' $basedir/${sweepfiles[$i]} | \
    gmt psxy $rgn $proj -Sc2.5p -W0.8p+cl -Cmag.cpt -t80 -O -K >> $out.ps
  echo "${Rl_labs[$i]}" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
  gmt psbasemap $rgn $proj -Bt${S}rw -Bpx2+l"@%2%R@-l@-@%% [-]" -By20+l"@%2%L@-e@-@%% [km]" -O -K >> $out.ps
  max=$(awk ' { print $2 } ' $basedir/${sweepfiles[$i]} | gmt pshistogram -R0/8/0/500 $proj_hist -Gdimgrey -T30+n -I | awk ' { print $4 } ')
  max_x=$(awk ' { print $2 } ' $basedir/${sweepfiles[$i]} | gmt pshistogram -R0/8/0/500 -T30+n -Io | grep $max | awk ' NR==1 { print $1 } ')
  rgn_hist=-R0/8/0/$max
  awk ' { print $2 } ' $basedir/${sweepfiles[$i]} | \
    gmt pshistogram $rgn_hist $proj_hist -Gdimgrey -T30+n -O -K >> $out.ps
  echo $max_x $max $max | gmt pstext $rgn_hist $proj_hist -F+f5p,dimgrey+j${Rl_just[$i]} -D${Rl_off[$i]} -N -O -K >> $out.ps
  gmt psbasemap $rgn_hist $proj_hist -Bb -Bpx2+l"@%2%R@-l@-@%% [-]" -By${Rl_ticks[$i]} --MAP_FRAME_TYPE=inside --FONT_ANNOT_PRIMARY=6p -O -K >> $out.ps

  # Rq
  rgn=-R0/10/10/80
  gmt psbasemap $rgn $proj -B+n -X1.3i -O -K >> $out.ps
  awk ' { print $3, $6, $7 } ' $basedir/${sweepfiles[$i]} | \
    gmt psxy $rgn $proj -Sc2.5p -W0.8p+cl -Cmag.cpt -t80 -O -K >> $out.ps
  echo "${Rq_labs[$i]}" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
  gmt psbasemap $rgn $proj -Bt${S}rw -Bpx2+l"@%2%R@-Q@-@%% [-]" -By20+l"@%2%L@-e@-@%% [km]" -O -K >> $out.ps
  max=$(awk ' { print $3 } ' $basedir/${sweepfiles[$i]} | gmt pshistogram -R0/10/0/500 $proj_hist -Gdimgrey -T30+n -I | awk ' { print $4 } ')
  max_x=$(awk ' { print $3 } ' $basedir/${sweepfiles[$i]} | gmt pshistogram -R0/10/0/500 -T30+n -Io | grep -w $max | awk ' NR==1 { print $1 } ')
  rgn_hist=-R0/10/0/$max
  awk ' { print $3 } ' $basedir/${sweepfiles[$i]} | \
    gmt pshistogram $rgn_hist $proj_hist -Gdimgrey -T30+n -O -K >> $out.ps
  echo $max_x $max $max | gmt pstext $rgn_hist $proj_hist -F+f5p,dimgrey+j${Rq_just[$i]} -D${Rq_off[$i]} -N -O -K >> $out.ps
  gmt psbasemap $rgn_hist $proj_hist -Bb -Bpx2+l"@%2%R@-Q@-@%% [-]" -By${Rq_ticks[$i]} --MAP_FRAME_TYPE=inside --FONT_ANNOT_PRIMARY=6p -O -K >> $out.ps

  # h
  rgn=-R0.3/1.1/10/80
  gmt psbasemap $rgn $proj -B+n -X1.3i -O -K >> $out.ps
  awk ' { print $4, $6, $7 } ' $basedir/${sweepfiles[$i]} | \
    gmt psxy $rgn $proj -Sc2.5p -W0.8p+cl -Cmag.cpt -t80 -O -K >> $out.ps
  echo "${h_labs[$i]}" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
  gmt psbasemap $rgn $proj -Bt${S}rw -Bpx0.2+l"@%2%h@%% [-]" -By20+l"@%2%L@-e@-@%% [km]" -O -K >> $out.ps
  max=$(awk ' { print $4 } ' $basedir/${sweepfiles[$i]} | gmt pshistogram -R0.3/1.1/0/500 $proj_hist -Gdimgrey -T30+n -I | awk ' { print $4 } ')
  max_x=$(awk ' { print $4 } ' $basedir/${sweepfiles[$i]} | gmt pshistogram -R0.3/1.1/0/500 -T30+n -Io | grep -w $max | awk ' NR==1 { print $1 } ')
  rgn_hist=-R0.3/1.1/0/$max
  awk ' { print $4 } ' $basedir/${sweepfiles[$i]} | \
    gmt pshistogram $rgn_hist $proj_hist -Gdimgrey -T30+n -O -K >> $out.ps
  echo $max_x $max $max | gmt pstext $rgn_hist $proj_hist -F+f5p,dimgrey+j${h_just[$i]} -D${h_off[$i]} -N -O -K >> $out.ps
  gmt psbasemap $rgn_hist $proj_hist -Bb -Bpx0.2+l"@%2%h@%% [-]" -By${h_ticks[$i]} --MAP_FRAME_TYPE=inside --FONT_ANNOT_PRIMARY=6p -O -K >> $out.ps

  # <L>
  rgn=-R30/110/10/80
  gmt psbasemap $rgn $proj -B+n -X1.3i -O -K >> $out.ps
  awk ' { print $5, $6, $7 } ' $basedir/${sweepfiles[$i]} | \
    gmt psxy $rgn $proj -Sc2.5p -W0.8p+cl -Cmag.cpt -t80 -O -K >> $out.ps
  echo "${L_labs[$i]}" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
  gmt psbasemap $rgn $proj -Bt${S}rw -Bpx20+l"@~\341@~@%2%L@%%@~\361@~ [km]" -By20+l"@%2%L@-e@-@%% [km]" -O -K >> $out.ps
  max=$(awk ' { print $5 } ' $basedir/${sweepfiles[$i]} | gmt pshistogram -R30/110/0/500 $proj_hist -Gdimgrey -T30+n -I | awk ' { print $4 } ')
  max_x=$(awk ' { print $5 } ' $basedir/${sweepfiles[$i]} | gmt pshistogram -R30/110/0/500 -T30+n -Io | grep -w $max | awk ' NR==1 { print $1 } ')
  rgn_hist=-R30/110/0/$max
  awk ' { print $5 } ' $basedir/${sweepfiles[$i]} | \
    gmt pshistogram $rgn_hist $proj_hist -Gdimgrey -T30+n -O -K >> $out.ps
  echo $max_x $max $max | gmt pstext $rgn_hist $proj_hist -F+f5p,dimgrey+j${L_just[$i]} -D${L_off[$i]} -N -O -K >> $out.ps
  gmt psbasemap $rgn_hist $proj_hist -Bb -Bpx20+l"@~\341@~@%2%L@%%@~\361@~ [km]" -By${L_ticks[$i]} --MAP_FRAME_TYPE=inside --FONT_ANNOT_PRIMARY=6p -O -K >> $out.ps

  max=$(awk ' { print $6 } ' $basedir/${sweepfiles[$i]} | gmt pshistogram -R10/80/0/500 $proj_hist -Gdimgrey -T30+n -I | awk ' { print $4 } ')
  max_x=$(awk ' { print $6 } ' $basedir/${sweepfiles[$i]} | gmt pshistogram -R10/80/0/500 -T30+n -Io | grep -w $max | awk ' NR==1 { print $1 } ')
  proj_hist2=-JX-0.15i/1.15i
  rgn_hist2=-R10/80/0/$max
  awk ' { print $6 } ' $basedir/${sweepfiles[$i]} | \
    gmt pshistogram $rgn_hist2 $proj_hist2 -Gdimgrey -T30+n -X1i -A -O -K >> $out.ps
  echo $max $max_x $max | gmt pstext -R0/$max/10/80 $proj_hist2 -F+f5p,dimgrey+j${Le_just[$i]}+a90 -D${Le_off[$i]} -N -O -K >> $out.ps
  gmt psbasemap -R0/$max/10/80 $proj_hist2 -Br -Bx${Le_ticks[$i]} --MAP_FRAME_TYPE=inside --FONT_ANNOT_PRIMARY=6p --MAP_ANNOT_ORTHO=n -O -K >> $out.ps

done


# Finalise, show
gmt psbasemap -R0/1/0/1 -JX2i -B+n -O >> $out.ps
gmt psconvert -A -E400 -Tf $out.ps
convert -density 600x600 -quality 100 -alpha remove $out.pdf $out.jpg
rm $out.ps
eog $out.jpg &