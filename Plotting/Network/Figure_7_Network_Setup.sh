#!/bin/bash

# ---- Get useful extra functions
source ../gmt_extras.sh

# ---- Set defaults
gmt_extras::set_gmt_defaults
gmt gmtset MAP_TICK_LENGTH_PRIMARY 3.5p
gmt gmtset MAP_ANNOT_OFFSET_PRIMARY 2p
gmt gmtset MAP_LABEL_OFFSET 3.5p

# Variables
basedir="../../Output/Network/Figure_7_Network_Setup"
netdirs=("UUU" "NUU" "UAU" "NAU")
plan_labs=("a" "b" "c" "d")
discharge_labs=("e" "f" "g" "h")
prof_labs=("i" "j" "k" "l")
ratio_labs=("m" "n" "o" "p")
hack_off=(0.41 0.42 0.41 0.41)
titles=("Uniform segment lengths" "Non-uniform segment lengths" "Uniform segment lengths" "Non-uniform segment lengths")
out="../../Figures/Figure_7_Network_Setup"

# CPT
gmt makecpt -Cviridis -T0.5/4.5/1 -I > order.cpt

# Initialise
gmt psbasemap -R0/1/0/1 -JX2i -B+n -X-1i -K > $out.ps

# Loop, plot
for i in ${!netdirs[@]} ; do
  
  netdir=$basedir/${netdirs[$i]}
  read Rb Rl Rq h <<< $(awk ' NR==1 { printf "%.2f %.2f %.2f %.2f", $1, $2, $3, $4 } ' $netdir/info.i)
  
  if [ $i -eq 0 ] ; then
    W="W"
  else
    W="w"
  fi
  
  # Planform
  ymax=$(gmt gmtinfo -C $netdir/planform.d | awk ' { print $4*1.05 } ')
  rgn=-R-10/110/0/$ymax
  proj=-JX1.5i
  gmt psbasemap $rgn $proj -B+n -Y5.2i -X1.65i -O -K >> $out.ps
  gmt psxy $netdir/planform.d $rgn $proj -W1p -Corder.cpt -O -K >> $out.ps
  gmt psbasemap $rgn $proj -Btslr -Bx20+l"Downstream distance [km]" -O -K >> $out.ps
  echo "${plan_labs[$i]}" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jLT+cLT -D0.05i/-0.08i -O -K >> $out.ps
  echo "${titles[$i]}" | gmt pstext $rgn $proj -F+f8p+jCB+cCT -D0i/0.08i -N -O -K >> $out.ps
  
  # Discharge
  qmin=$(gmt gmtinfo -C $netdir/discharge.dq | awk ' { print -$4*0.05 } ')
  qmax=$(gmt gmtinfo -C $netdir/discharge.dq | awk ' { print $4*1.05 } ')
  rgn=-R-10/110/$qmin/$qmax
  proj=-JX1.5i
  gmt psbasemap $rgn $proj -B+n -Y-1.65i -O -K >> $out.ps
  gmt psxy $netdir/discharge.dq $rgn $proj -W1p -Corder.cpt -O -K >> $out.ps
  echo "${discharge_labs[$i]}" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jRB+cRB -D-0.05i/0.08i -O -K >> $out.ps
  gmt psbasemap $rgn $proj \
    -Bnse${W} \
    -Bx20+l"Downstream distance, @%2%x@%% [km]" \
    -By40+l"Discharge, @%2%Q@-w@-@%% [m@+3@+ s@+-1@+]" \
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
  echo "@%2%p@%% = $h" | \
    gmt pstext $rgn $proj_in -F+f6p,Helvetica,dimgrey+jML+cBL -D${hack_off[$i]}i/0.25i -N -O -K >> $out.ps
  gmt psbasemap $rgn $proj_in \
    -Bsw -Bx20 -By40 \
    --MAP_TICK_LENGTH_PRIMARY=2p \
    --MAP_FRAME_PEN=1p \
    -O -K >> $out.ps
  
  # Profile
  rgn=-R-10/110/0/700
  gmt psbasemap $rgn $proj -B+n -X-0.1i -Y-2.55i -O -K >> $out.ps
  gmt psxy $netdir/profile.de $rgn $proj -W1p -Corder.cpt -O -K >> $out.ps  
  echo "${prof_labs[$i]}" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jLB+cLB -D0.05i/0.08i -O -K >> $out.ps
  if [ $i -eq 3 ] ; then
    gmt psscale $rgn $proj \
      -Corder.cpt \
      -Dx0.72i/1.35i+w0.7i/0.07i+h \
      -B1+l"Stream order, @~\167@~" \
      --MAP_LABEL_OFFSET=-8p \
      --MAP_ANNOT_OFFSET=5p \
      --MAP_TICK_LENGTH=7p \
      --MAP_DEFAULT_PEN=7p \
      --MAP_TICK_PEN=1.5p \
      --FONT=16p \
      -O -K >> $out.ps
  fi
  gmt psbasemap $rgn $proj \
    -BnSe${W} \
    -Bx20+l"Downstream distance, @%2%x@%% [km]" \
    -By200+l"Elevation, @%2%z@%% [m]" \
    -O -K >> $out.ps

  # Ratios
  Rb_colour=187/85/102
  Rl_colour=221/170/51
  Rq_colour=0/68/136
  rgn=-R0.5/4.5/0.7/500
  proj=-JX1.5i/1.5il
  gmt psbasemap $rgn $proj -B+n -Y-1.9i -O -K >> $out.ps
  gmt psxy $netdir/count_fit.oc $rgn $proj -W0.8p,$Rb_colour,4p_4p -O -K >> $out.ps
  gmt psxy $netdir/length_fit.oc $rgn $proj -W0.8p,$Rl_colour,4p_4p -O -K >> $out.ps
  gmt psxy $netdir/discharge_fit.oc $rgn $proj -W0.8p,$Rq_colour,4p_4p -O -K >> $out.ps
  gmt psxy $netdir/counts.oc $rgn $proj -Sc3.5p -G$Rb_colour -O -K >> $out.ps
  gmt psxy $netdir/lengths.oc $rgn $proj -Sc3.5p -G$Rl_colour -O -K >> $out.ps
  gmt psxy $netdir/discharges.oc $rgn $proj -Sc3.5p -G$Rq_colour -O -K >> $out.ps
  echo "@%2%R@-B@-@%% = $Rb" | \
    gmt pstext $rgn $proj -F+f7p,$Rb_colour+jTL+cTL -D0.04i/-0.05i -O -K >> $out.ps
  echo "@%2%R@-L@-@%% = $Rl" | \
    gmt pstext $rgn $proj -F+f7p,$Rl_colour+jCT+cCT -D0i/-0.05i -O -K >> $out.ps
  echo "@%2%R@-Q@-@%% = $Rq" | \
    gmt pstext $rgn $proj -F+f7p,$Rq_colour+jTR+cTR -D-0.04i/-0.05i -O -K >> $out.ps
  echo "${ratio_labs[$i]}" | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jLB+cLB -D0.05i/0.08i -O -K >> $out.ps
  gmt psbasemap $rgn $proj \
    -BtS \
    -Bx1+l"Stream order, @~\167@~ [-]" \
    -O -K >> $out.ps
  gmt psbasemap $rgn $proj \
    -Be${W} \
    -By1f3p+l"@%2%@;$Rb_colour;N@-@~\167@~@-@%% [-]@;;     @%2%@;$Rl_colour;L@-@~\167@~@-@%% [km]@;;     @%2%@;$Rq_colour;Q@-w,@~\167@~@-@%% [m@+3@+ s@+-1@+]@;;" \
    --MAP_LABEL_OFFSET=4p \
    -O -K >> $out.ps

done

rgn=-R0/3.15/0/3.15
proj=-JX3.15i
gmt psbasemap $rgn $proj -B+n -Y5.2i -X-4.95i -O -K >> $out.ps
echo "0.75 1.72
0.75 1.79
2.4 1.79
2.4 1.72" | gmt psxy $rgn $proj -W0.8p -O -K >> $out.ps
echo "Upstream supply" | gmt pstext $rgn $proj -F+f8p+jCM+cCB -D0i/1.79i -Gwhite -N -O -K >> $out.ps

gmt psbasemap $rgn $proj -B+n -X3.3i -O -K >> $out.ps
echo "0.75 1.72
0.75 1.79
2.4 1.79
2.4 1.72" | gmt psxy $rgn $proj -W0.8p -O -K >> $out.ps
echo "Along-stream supply" | gmt pstext $rgn $proj -F+f8p+jCM+cCB -D0i/1.79i -Gwhite -N -O -K >> $out.ps

# Finalise, show
gmt psbasemap -R0/1/0/1 -JX2i -B+n -O >> $out.ps
gmt psconvert -A -E400 -Tj $out.ps
rm $out.ps *.cpt
eog $out.jpg &