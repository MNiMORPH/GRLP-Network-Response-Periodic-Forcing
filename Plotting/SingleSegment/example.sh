#!/bin/bash

# ---- Get useful extra functions
source ../gmt_extras.sh

# ---- Set defaults
gmt_extras::set_gmt_defaults

# ---- Variables
out=example
indir=../../output/continuous/example
periods=("fast" "medium" "slow")
min_times=(-2.5 -25 -250)
max_times=(32.5 325 3250)
time_ticks=(10 100 1000)
axes=("ne" "ne" "nE")
forcing_axes=("W" "w" "w")
profile_axes=("nSrW" "nSrw" "nSrw")
profile_axes2=("e" "e" "E")
Qs_labels=("a" "b" "c")
Qw_labels=("d" "e" "f")
z_labels=("g" "h" "i")
prof_labels=("j" "k" "l")
titles=("@%2%P@%% = @%2%T@-eq@-@%% / 10" "@%2%P@%% = @%2%T@-eq@-@%%" "@%2%P@%% = @%2%T@-eq@-@%% x 10")

# ---- CPTs
gmt makecpt -Cviridis -T0/100/1 -Z -D -I > x.cpt
gmt makecpt -Cgray -T2000/2250/1 -Z -I -G0.3/0.9 > t.cpt
gmt makecpt -T2000/2250/1 -Z -Cwhite,dodgerblue -D -G0.3/0.9 > t2.cpt


# ---- Initialise
gmt psbasemap -R -J -B+n -X-1i -K > $out.ps

# ---- Loop over periods, plot
for i in ${!periods[@]} ; do
  
  # Sediment supply forcing, sediment output
  rgn=-R${min_times[$i]}/${max_times[$i]}/0.7/1.3
  proj=-JX2i/0.75i
  gmt psbasemap $rgn $proj -B+n -X2.2i -Y4.75i -O -K >> $out.ps
  gmt psxy $indir/${periods[$i]}/Qs_scale.tq $rgn $proj -W1p,lightred -O -K >> $out.ps
  gmt psxy $indir/${periods[$i]}/ref_Qs_out.tq $rgn $proj -W1p,dimgrey,3p_2p -O -K >> $out.ps
  gmt psxy $indir/${periods[$i]}/Qs_out.tq $rgn $proj -W1p,black -O -K >> $out.ps
  gmt psxy $indir/${periods[$i]}/scale_circles.ts $rgn $proj -Sc4p -W0.8p -Ct.cpt -O -K >> $out.ps
  echo ${Qs_labels[$i]} | \
    gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jBL+cBL -D0.05i/0.08i -O -K >> $out.ps
  echo ${titles[$i]} | \
    gmt pstext $rgn $proj -F+f11p,Helvetica,black+jBC+cTC -D0i/0.16i -N -O -K >> $out.ps
  gmt psbasemap $rgn $proj \
    -B${forcing_axes[$i]} \
    -By0.2+l"@%2%Q@-s,0@-@%%\047 [-]" \
    --FONT=lightred \
    --MAP_FRAME_PEN=lightred \
    --MAP_TICK_PEN_PRIMARY=lightred \
    -O -K >> $out.ps
  gmt psbasemap $rgn $proj \
    -Bs${axes[$i]} \
    -Bx${time_ticks[$i]}+l"Time, @%2%t@%% [kyr]" \
    -By0.2+l"@%2%Q@-s,L@-@%%\047 [-]" \
    -O -K >> $out.ps
    

  # Water supply forcing, sediment output
  rgn=-R${min_times[$i]}/${max_times[$i]}/0.7/1.3
  proj=-JX2i/0.75i
  gmt psbasemap $rgn $proj -B+n -Y-0.95i -O -K >> $out.ps
  gmt psxy $indir/${periods[$i]}/Qw_scale.tq $rgn $proj -W1p,dodgerblue -O -K >> $out.ps
  gmt psxy $indir/${periods[$i]}/Qw_ref_Qs_out.tq $rgn $proj -W1p,dimgrey,3p_2p -O -K >> $out.ps
  gmt psxy $indir/${periods[$i]}/Qw_Qs_out.tq $rgn $proj -W1p,black -O -K >> $out.ps
  echo ${Qw_labels[$i]} | \
    gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jBL+cBL -D0.05i/0.08i -O -K >> $out.ps
  gmt psbasemap $rgn $proj \
    -B${forcing_axes[$i]} \
    -By0.2+l"@%2%Q@-w@-@%%\047 [-]" \
    --FONT=dodgerblue \
    --MAP_FRAME_PEN=dodgerblue \
    --MAP_TICK_PEN_PRIMARY=dodgerblue \
    -O -K >> $out.ps
  gmt psbasemap $rgn $proj \
    -Bs${axes[$i]} \
    -Bx${time_ticks[$i]}+l"Time, @%2%t@%% [kyr]" \
    -By0.2+l"@%2%Q@-s,L@-@%%\047 [-]" \
    -O -K >> $out.ps

    
  # Elevation(t)
  rgn=-R${min_times[$i]}/${max_times[$i]}/0/750
  proj=-JX2i/1.5i
  gmt psbasemap $rgn $proj -B+n -Y-1.7i -O -K >> $out.ps
  gmt psxy $indir/${periods[$i]}/ref_profile.te $rgn $proj -W1p,dimgrey,3p_3p -O -K >> $out.ps
  gmt psxy $indir/${periods[$i]}/profile.te $rgn $proj -W1p -Cx.cpt -O -K >> $out.ps
  echo ${z_labels[$i]} | \
    gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
  gmt psbasemap $rgn $proj \
    -BS${axes[$i]}${forcing_axes[$i]} \
    -Bx${time_ticks[$i]}+l"Time, @%2%t@%% [kyr]" \
    -By250+l"Elevation, @%2%z@%% [m]" \
    -O -K >> $out.ps


  # Elevation(x)
  rgn=-R-10/110/-100/750
  proj=-JX2i/1.5i
  rgn2=-R-10/110/-100/100
  proj2=-JX2i/0.35294117647058826i
  gmt psbasemap $rgn $proj -B+n -Y-2.1i -O -K >> $out.ps
  gmt psxy $indir/${periods[$i]}/profile_pert.de $rgn2 $proj2 -W1p -Ct2.cpt -O -K >> $out.ps
  gmt psxy $indir/${periods[$i]}/profile.de $rgn $proj -W1p -Ct.cpt -O -K >> $out.ps
  echo ${prof_labels[$i]} | \
    gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
  gmt psbasemap $rgn $proj \
    -B${profile_axes[$i]} \
    -Bx20+l"Downstream distance, @%2%x@%% [km]" \
    -By250+l"Elevation, @%2%z@%% [m]" \
    -O -K >> $out.ps
  gmt psbasemap $rgn2 $proj2 \
    -B${profile_axes2[$i]} \
    -By100+l"@~\144@~@%2%z@%% [m]" \
    --FONT=dodgerblue \
    --MAP_FRAME_PEN=dodgerblue \
    --MAP_TICK_PEN_PRIMARY=dodgerblue \
    -O -K >> $out.ps
done


# ---- Finalise
gmt psbasemap -R -J -B+n -O >> $out.ps


# ---- Show
gmt psconvert -A -E400 -Tj $out.ps
eog $out.jpg &