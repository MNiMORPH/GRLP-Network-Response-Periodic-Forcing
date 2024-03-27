#!/bin/bash -i

# Set defaults
set_gmt_defaults
gmt gmtset MAP_TICK_LENGTH_PRIMARY 3.5p
gmt gmtset MAP_ANNOT_OFFSET_PRIMARY 2p
gmt gmtset MAP_LABEL_OFFSET 3.5p

# Variables
basedir="../../output/network/examples"
netdirs=("m20_fix_seg_length" "m40_fix_seg_length" "m40_rnd_seg_length")
plan_labs=("a" "e" "i")
discharge_labs=("b" "f" "j")
prof_labs=("c" "g" "k")
ratio_labs=("d" "h" "l")
hack_off=(0.3 0.34 0.37)
out=examples

# CPT
gmt makecpt -Cviridis -T0.5/4.5/1 -I > order.cpt

# Initialise
gmt psbasemap -R0/1/0/1 -JX2i -B+n -Y8i -X6.2i -K > $out.ps

# Loop, plot
for i in ${!netdirs[@]} ; do
  
  netdir=$basedir/${netdirs[$i]}
  read Rb Rl Rq h <<< $(awk ' NR==1 { printf "%.2f %.2f %.2f %.2f", $1, $2, $3, $4 } ' $netdir/info.i)
  
  if [ $i -eq 2 ] ; then
    S="S"
  else
    S="s"
  fi
  
  # Planform
  ymax=$(gmt gmtinfo -C $netdir/planform.d | awk ' { print $4*1.05 } ')
  rgn=-R0/100/0/$ymax
  proj=-JX1.25i
  gmt psbasemap $rgn $proj -B+n -Y-1.65i -X-5.75i -O -K >> $out.ps
  gmt psxy $netdir/planform.d $rgn $proj -W1p -Corder.cpt -O -K >> $out.ps
  gmt psbasemap $rgn $proj -B${S} -Bx20+l"Downstream distance [km]" -O -K >> $out.ps
  echo "${plan_labs[$i]}" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jRB+cRB -D-0.05i/0.08i -O -K >> $out.ps

  # Discharge
  qmin=$(gmt gmtinfo -C $netdir/discharge.dq | awk ' { print -$4*0.05 } ')
  qmax=$(gmt gmtinfo -C $netdir/discharge.dq | awk ' { print $4*1.05 } ')
  rgn=-R-10/110/$qmin/$qmax
  proj=-JX1.5i
  gmt psbasemap $rgn $proj -B+n -X1.7i -O -K >> $out.ps
  gmt psxy $netdir/discharge.dq $rgn $proj -W1p -Corder.cpt -O -K >> $out.ps
  echo "${discharge_labs[$i]}" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jRB+cRB -D-0.05i/0.08i -O -K >> $out.ps
  gmt psbasemap $rgn $proj \
    -Bn${S}eW \
    -Bx20+l"Downstream distance, @%2%x@%% [km]" \
    -By10+l"Discharge, @%2%Q@-w@-@%% [m@+3@+ s@+-1@+]" \
    -O -K >> $out.ps
  
  # Hack
  proj_in=-JX0.5i
  gmt psbasemap $rgn $proj_in -B+n -X0.1i -Y0.9i -O -K >> $out.ps
  gmt psxy $netdir/hack.dq $rgn $proj_in -Sc2p -Corder.cpt -O -K >> $out.ps  
  gmt psxy $netdir/hack_fit.dq $rgn $proj_in -W0.6p,dimgrey,2p_2p -O -K >> $out.ps
  echo "@%2%d@%%" | \
    gmt pstext $rgn $proj_in -F+f7p,Helvetica+jRB+cRB -D0i/0.03i -O -K >> $out.ps
  echo "@%2%Q@-w@-@%%" | \
    gmt pstext $rgn $proj_in -F+f7p,Helvetica+jTL+cTL -D0.02i/0i -O -K >> $out.ps
  echo "@%2%h@%% = $h" | \
    gmt pstext $rgn $proj_in -F+f6p,Helvetica,dimgrey+jML+cBL -D${hack_off[$i]}i/0.25i -N -O -K >> $out.ps
  gmt psbasemap $rgn $proj_in \
    -Bsw -Bx20 -By10 \
    --MAP_TICK_LENGTH_PRIMARY=2p \
    --MAP_FRAME_PEN=1p \
    -O -K >> $out.ps
  
  # Profile
  rgn=-R-10/110/0/700
  gmt psbasemap $rgn $proj -B+n -X1.95i -Y-0.9i -O -K >> $out.ps
  gmt psxy $netdir/profile.de $rgn $proj -W1p -Corder.cpt -O -K >> $out.ps  
  echo "${prof_labs[$i]}" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jLB+cLB -D0.05i/0.08i -O -K >> $out.ps
  if [ $i -eq 0 ] ; then
    gmt psscale $rgn $proj \
      -Corder.cpt \
      -Dx0.72i/1.35i+w0.7i/0.07i+h \
      -B1+l"Stream order, @%2%O@%%" \
      -O -K >> $out.ps
  fi
  gmt psbasemap $rgn $proj \
    -Bn${S}eW \
    -Bx20+l"Downstream distance, @%2%x@%% [km]" \
    -By200+l"Elevation, @%2%z@%% [m]" \
    -O -K >> $out.ps

  # Ratios
  rgn=-R0.5/4.5/0.7/143
  proj=-JX1.5i/1.5il
  gmt psbasemap $rgn $proj -B+n -X2i -O -K >> $out.ps
  gmt psxy $netdir/count_fit.oc $rgn $proj -W0.8p,red,4p_4p -O -K >> $out.ps
  gmt psxy $netdir/counts.oc $rgn $proj -Sc3.5p -Gred -O -K >> $out.ps
  gmt psxy $netdir/length_fit.oc $rgn $proj -W0.8p,blue,4p_4p -O -K >> $out.ps
  gmt psxy $netdir/lengths.oc $rgn $proj -Sc3.5p -Gblue -O -K >> $out.ps
  gmt psxy $netdir/discharge_fit.oc $rgn $proj -W0.8p,0/125/0,4p_4p -O -K >> $out.ps
  gmt psxy $netdir/discharges.oc $rgn $proj -Sc3.5p -G0/125/0 -O -K >> $out.ps
  echo "4.5 10 @%2%R@-b@-@%% = $Rb" | \
    gmt pstext $rgn $proj -F+f6p,red+jRM -D-0.03i/0.14i -O -K >> $out.ps
  echo "4.5 10 @%2%R@-l@-@%% = $Rl" | \
    gmt pstext $rgn $proj -F+f6p,blue+jRM -D-0.03i/0i -O -K >> $out.ps
  echo "4.5 10 @%2%R@-Q@-@%% = $Rq" | \
    gmt pstext $rgn $proj -F+f6p,0/125/0+jRM -D-0.03i/-0.14i -O -K >> $out.ps
  echo "${ratio_labs[$i]}" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jLB+cLB -D0.05i/0.08i -O -K >> $out.ps
  gmt psbasemap $rgn $proj \
    -Bn${S} \
    -Bx1+l"Stream order, @%2%O@%% [-]" \
    -O -K >> $out.ps
  gmt psbasemap $rgn $proj \
    -BeW \
    -By1f3p+l"@%2%@;red;N@-o@-@%% [-]@;;     @%2%@;blue;L@-o@-@%% [km]@;;     @%2%@;0/125/0;Q@-w,o@-@%% [m@+3@+ s@+-1@+]@;;" \
    --MAP_LABEL_OFFSET=2p \
    -O -K >> $out.ps

done

# Finalise, show
gmt psbasemap -R0/1/0/1 -JX2i -B+n -O >> $out.ps
gmt psconvert -A -E400 -Tj $out.ps
rm $out.ps
eog $out.jpg &