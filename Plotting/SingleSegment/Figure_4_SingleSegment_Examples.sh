#!/bin/bash

# ---- Get useful extra functions
source ../gmt_extras.sh

# ---- Set defaults
gmt_extras::set_gmt_defaults

# ---- Variables
out=../../Figures/Figure_4_SingleSegment_Examples
indir=../../Output/SingleSegment/Figure_4_S1_SingleSegment_Examples
periods=("fast" "medium" "slow")
min_times=(-2.5 -25 -250)
max_times=(32.5 325 3250)
time_ticks=(10 100 1000)
axes=("ne" "ne" "nE")
forcing_axes=("W" "w" "w")
elevation_axes=("neW" "new" "new")
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
  rgn=-R${min_times[$i]}/${max_times[$i]}/0.7/1.39
  proj=-JX2i/0.75i
  gmt psbasemap $rgn $proj -B+n -X2.2i -Y4.65i -O -K >> $out.ps
  gmt psxy $indir/${periods[$i]}/force_tps_ref.te $rgn $proj -W0.8p,lightgrey -O -K >> $out.ps
  if [ $i -eq 2 ] ; then
    echo "${min_times[$i]} 1.39
${max_times[$i]} 1.39
${max_times[$i]} 1.2
${min_times[$i]} 1.2" | gmt psxy $rgn $proj -Gwhite -O -K >> $out.ps
  fi
  gmt psxy $indir/${periods[$i]}/Qs_scale.tq $rgn $proj -W1p,lightred -O -K >> $out.ps
  gmt psxy $indir/${periods[$i]}/force_tps.tq $rgn $proj -Sc3p -Glightred -O -K >> $out.ps
  gmt psxy $indir/${periods[$i]}/ref_Qs_out.tq $rgn $proj -W1p,dimgrey,3p_2p -O -K >> $out.ps
  gmt psxy $indir/${periods[$i]}/ref_Qs_out_tps.tq $rgn $proj -Sc3p -Gdimgrey -O -K >> $out.ps
  gmt psxy $indir/${periods[$i]}/Qs_out.tq $rgn $proj -W1p,black -O -K >> $out.ps
  gmt psxy $indir/${periods[$i]}/Qs_out_tps.tq $rgn $proj -Sc3p -Gblack -O -K >> $out.ps
  gmt psxy $indir/${periods[$i]}/scale_circles.ts $rgn $proj -Sc4p -W0.8p -Ct.cpt -O -K >> $out.ps
  echo ${Qs_labels[$i]} | \
    gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
  echo ${titles[$i]} | \
    gmt pstext $rgn $proj -F+f11p,Helvetica,black+jBC+cTC -D0i/0.16i -N -O -K >> $out.ps
  if [ $i -eq 2 ] ; then
    gmt_extras::plot_key_line $rgn $proj 720 400 1.3 -W1p,lightred "@%2%Q@-s,0@-@%%" $out
    gmt_extras::plot_key_line $rgn $proj 1820 1500 1.3 -W1p,dimgrey,3p_2p "@%2%Q@-s,L@-@%% (Up')" $out
    gmt_extras::plot_key_line $rgn $proj 3150 2830 1.3 -W1p,black "@%2%Q@-s,L@-@%% (Along')" $out
  fi
  gmt psbasemap $rgn $proj \
    -B${forcing_axes[$i]} \
    -By0.2+l"@[\textit{Q\textsubscript{s,0}}~/~\overline{\textit{Q\textsubscript{s,0}}}@[ [-]" \
    --FONT=lightred \
    --MAP_FRAME_PEN=lightred \
    --MAP_TICK_PEN_PRIMARY=lightred \
    --MAP_LABEL_OFFSET=4p \
    -O -K >> $out.ps
  gmt psbasemap $rgn $proj \
    -Bs${axes[$i]} \
    -Bx${time_ticks[$i]}+l"Time, @%2%t@%% [kyr]" \
    -By0.2+l"@[\textit{Q\textsubscript{s,L}}~/~\overline{\textit{Q\textsubscript{s,L}}}@[ [-]" \
    --MAP_LABEL_OFFSET=4p \
    -O -K >> $out.ps  

  # Water supply forcing, sediment output
  rgn=-R${min_times[$i]}/${max_times[$i]}/0.7/1.39
  proj=-JX2i/0.75i
  gmt psbasemap $rgn $proj -B+n -Y-0.95i -O -K >> $out.ps
  gmt psxy $indir/${periods[$i]}/force_tps_ref.te $rgn $proj -W0.8p,lightgrey -O -K >> $out.ps
  if [ $i -eq 2 ] ; then
    echo "${min_times[$i]} 1.39
${max_times[$i]} 1.39
${max_times[$i]} 1.2
${min_times[$i]} 1.2" | gmt psxy $rgn $proj -Gwhite -O -K >> $out.ps
  fi
  gmt psxy $indir/${periods[$i]}/Qw_scale.tq $rgn $proj -W1p,dodgerblue -O -K >> $out.ps
  gmt psxy $indir/${periods[$i]}/force_tps.tq $rgn $proj -Sc3p -Gdodgerblue -O -K >> $out.ps
  gmt psxy $indir/${periods[$i]}/Qw_ref_Qs_out.tq $rgn $proj -W1p,dimgrey,3p_2p -O -K >> $out.ps
  gmt psxy $indir/${periods[$i]}/Qw_ref_Qs_out_tps.tq $rgn $proj -Sc3p -Gdimgrey -O -K >> $out.ps
  gmt psxy $indir/${periods[$i]}/Qw_Qs_out.tq $rgn $proj -W1p,black -O -K >> $out.ps
  gmt psxy $indir/${periods[$i]}/Qw_Qs_out_tps.tq $rgn $proj -Sc3p -Gblack -O -K >> $out.ps
  echo ${Qw_labels[$i]} | \
    gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
  if [ $i -eq 2 ] ; then
    gmt_extras::plot_key_line $rgn $proj 720 400 1.3 -W1p,dodgerblue "@%2%Q@-w,0@-@%%" $out
    gmt_extras::plot_key_line $rgn $proj 1820 1500 1.3 -W1p,dimgrey,3p_2p "@%2%Q@-s,L@-@%% (Up')" $out
    gmt_extras::plot_key_line $rgn $proj 3150 2830 1.3 -W1p,black "@%2%Q@-s,L@-@%% (Along')" $out
  fi
  gmt psbasemap $rgn $proj \
    -B${forcing_axes[$i]} \
    -By0.2+l"@[\textit{Q\textsubscript{w,0}}~/~\overline{\textit{Q\textsubscript{w,0}}}@[ [-]" \
    --FONT=dodgerblue \
    --MAP_FRAME_PEN=dodgerblue \
    --MAP_TICK_PEN_PRIMARY=dodgerblue \
    --MAP_LABEL_OFFSET=4p \
    -O -K >> $out.ps
  gmt psbasemap $rgn $proj \
    -Bs${axes[$i]} \
    -Bx${time_ticks[$i]}+l"Time, @%2%t@%% [kyr]" \
    -By0.2+l"@[\textit{Q\textsubscript{s,L}}~/~\overline{\textit{Q\textsubscript{s,L}}}@[ [-]" \
    --MAP_LABEL_OFFSET=4p \
    -O -K >> $out.ps

    
  # Elevation(t)
  rgn=-R${min_times[$i]}/${max_times[$i]}/0/800
  proj=-JX2i/1.5i
  gmt psbasemap $rgn $proj -B+n -Y-1.7i -O -K >> $out.ps
  gmt psxy $indir/${periods[$i]}/force_tps_ref.te $rgn $proj -W0.8p,lightgrey -O -K >> $out.ps
  if [ $i -eq 2 ] ; then
    echo "1000 800
${max_times[$i]} 800
${max_times[$i]} 680
1000 680" | gmt psxy $rgn $proj -Gwhite -O -K >> $out.ps
  fi
  gmt psxy $indir/${periods[$i]}/ref_profile.te $rgn $proj -W1p,dimgrey,3p_3p -O -K >> $out.ps
  gmt psxy $indir/${periods[$i]}/ref_profile_tps.te $rgn $proj -Sc3p -Gdimgrey -O -K >> $out.ps
  gmt psxy $indir/${periods[$i]}/profile.te $rgn $proj -W1p -Cx.cpt -O -K >> $out.ps
  gmt psxy $indir/${periods[$i]}/profile_tps.te $rgn $proj -Sc3p -Cx.cpt -O -K >> $out.ps
  echo ${z_labels[$i]} | \
    gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
  if [ $i -eq 2 ] ; then
    gmt_extras::plot_key_line $rgn $proj 1820 1500 750 -W1p,dimgrey,3p_2p "@%2%z@%% (Up')" $out
    gmt_extras::plot_key_multi_line $rgn $proj 3150 2830 750 -W1p,black "@%2%z@%% (Along')" $out x.cpt "80 60 40 20 0"
    gmt psbasemap $rgn $proj \
      -BSnwr \
      -Bx${time_ticks[$i]}+l"Time, @%2%t@%% [kyr]" \
      -By200+l"Elevation, @%2%z@%% [m]" \
      -O -K >> $out.ps
    gmt psscale $rgn $proj \
      -Cx.cpt \
      -Dx2.12i/0i+w1.33i/0.07i+r \
      -Bx20+l"Downstream distance, @%2%x@%% [km]" \
      --MAP_LABEL_OFFSET=6p \
      --MAP_ANNOT_OFFSET=5p \
      --FONT=14.5p \
      -O -K >> $out.ps
  else
    gmt psbasemap $rgn $proj \
      -BS${elevation_axes[$i]} \
      -Bx${time_ticks[$i]}+l"Time, @%2%t@%% [kyr]" \
      -By200+l"Elevation, @%2%z@%% [m]" \
      -O -K >> $out.ps

  fi

  # Elevation(x)
  rgn=-R-10/110/-100/800
  proj=-JX2i/1.5i
  rgn2=-R-10/110/-100/100
  proj2=-JX2i/0.35294117647058826i
  gmt psbasemap $rgn $proj -B+n -Y-2i -O -K >> $out.ps
  gmt psxy $indir/${periods[$i]}/profile_pert.de $rgn2 $proj2 -W1p -Ct2.cpt -O -K >> $out.ps
  gmt psxy $indir/${periods[$i]}/profile.de $rgn $proj -W1p -Ct.cpt -O -K >> $out.ps
  echo ${prof_labels[$i]} | \
    gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jTL+cTL -D0.05i/-0.08i -O -K >> $out.ps
  gmt psbasemap $rgn $proj \
    -B${profile_axes[$i]} \
    -Bx20+l"Downstream distance, @%2%x@%% [km]" \
    -By200+l"Elevation, @%2%z@%% [m]" \
    -O -K >> $out.ps
  gmt psbasemap $rgn2 $proj2 \
    -B${profile_axes2[$i]} \
    -By100+l"@~\144@~@%2%z@%% [m]" \
    --FONT=dodgerblue \
    --MAP_FRAME_PEN=dodgerblue \
    --MAP_TICK_PEN_PRIMARY=dodgerblue \
    -O -K >> $out.ps
    
    if [ $i -eq 2 ] ; then
      gmt_extras::plot_key_multi_line $rgn $proj 60.97 50 743.75 -W1p "@%2%z@%% (Along')" $out t.cpt "2250 2177.5 2125 2062.5 2000"
      gmt_extras::plot_key_multi_line $rgn $proj 106.57 95.6 743.75 -W1p "@~\144@~@%2%z@%% (Along')" $out t2.cpt "2250 2177.5 2125 2062.5 2000"
    fi
done


# ---- Finalise
gmt psbasemap -R -J -B+n -O >> $out.ps


# ---- Show
gmt psconvert -A -E400 -Tj $out.ps
eog $out.jpg &
rm $out.ps *.cpt