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
  gmt psxy $indir/${periods[$i]}/profile.te $rgn $proj -W1p,black -O -K >> $out.ps
  gmt psbasemap $rgn $proj \
    -BS${axes[$i]}${forcing_axes[$i]} \
    -Bx${time_ticks[$i]}+l"Time, @%2%t@%% [kyr]" \
    -By250+l"Elevation, @%2%z@%% [m]" \
    -O -K >> $out.ps

  # Elevation(x)
  rgn=-R-10/110/0/750
  proj=-JX2i/1.5i
  gmt psbasemap $rgn $proj -B+n -Y-2.1i -O -K >> $out.ps

  gmt psbasemap $rgn $proj \
    -BS${axes[$i]}${forcing_axes[$i]} \
    -Bx20+l"Downstream distance, @%2%x@%% [km]" \
    -By250+l"Elevation, @%2%z@%% [m]" \
    -O -K >> $out.ps

done

# ---- Finalise
gmt psbasemap -R -J -B+n -O >> $out.ps

# ---- Show
gmt psconvert -A -E400 -Tj $out.ps
eog $out.jpg &