#!/bin/bash -i

# ---- Defaults
set_gmt_defaults

# ---- CPTs
gmt makecpt -Cviridis -T0.5/4.5/1 -I > order.cpt
gmt makecpt -Cviridis -T0/100/1 -I > x.cpt

# ---- Set up
# basedir="../output/network_example/gif"
basedir="../output/linear/gif"

# # labels=("Qw_fast" "Qw_medium" "Qw_slow")
# labels=("fast" "medium" "slow")
# titles=("@%3%P@%% = @%3%T@-eq@-@%% / 5" "@%3%P@%% = @%3%T@-eq@-@%%" "@%3%P@%% = @%3%T@-eq@-@%% x 5")
# profile_grds=("nSeW" "nSew" "nSEw")
# scale_grds=("nsW" "nsw" "nsw")
# scale_grds2=("e" "e" "E")
# elev_grds=("nSeW" "nSew" "nSEw")

# labels=("Qw_fast")
# # labels=("fast")
# titles=("@%3%P@%% = @%3%T@-eq@-@%% / 5")
# profile_grds=("nSEW")
# scale_grds=("nsW")
# scale_grds2=("E")
# elev_grds=("nSEW")

labels=("Qw_fast" "Qw_medium")
# labels=("fast" "medium")
titles=("@%3%P@%% = @%3%T@-eq@-@%% / 5" "@%3%P@%% = @%3%T@-eq@-@%%")
profile_grds=("nSeW" "nSEw")
scale_grds=("nsW" "nsw")
scale_grds2=("e" "E")
elev_grds=("nSeW" "nSEw")


# ---- Make individual scenes

# for t in {000..199} ; do
for t in 199 ; do
  echo "Plotting scene $t."

  out=$basedir/scene$t
  gmt psbasemap -R0/1/0/1 -JX1i -B+n -X-1.75i -Y4i -K > $out.ps

  for i in ${!labels[@]} ; do

    # Profile
    rgn=-R-10/110/0/700
    proj=-JX2i/1.5i
    gmt psbasemap $rgn $proj -B+n -X2.4i -Y3i -O -K >> $out.ps
    gmt psxy $basedir/steady_profile.de $rgn $proj -W0.8p,dimgrey,3_2 -O -K >> $out.ps
    gmt psxy $basedir/${labels[$i]}/lin_z${t}.de $rgn $proj -W0.8p -O -K >> $out.ps    
    gmt psxy $basedir/${labels[$i]}/lin_z${t}_circles.de $rgn $proj -Sc3p -W0.8p -Cx.cpt -O -K >> $out.ps
    # gmt psxy $basedir/${labels[$i]}/z${t}.de $rgn $proj -W0.8p -Corder.cpt -O -K >> $out.ps
    # gmt psxy $basedir/${labels[$i]}/z${t}_circles.de $rgn $proj -Sc3p -W0.8p -Corder.cpt -O -K >> $out.ps
    echo 50 700 ${titles[$i]} | \
      gmt pstext $rgn $proj -F+f10p,Helvetica-Bold -D0i/0.2i -N -O -K >> $out.ps
    gmt psbasemap $rgn $proj -B${profile_grds[$i]} -Bx20+l"Downstream distance [km]" -By200+l"Elevation [m]" -O -K >> $out.ps

    # Scale
    rgn=-R0/500/0.7/1.3
    proj=-JX2i/0.7i
    gmt psbasemap $rgn $proj -B+n -Y-1.3i -O -K >> $out.ps
    # gmt psxy $basedir/${labels[$i]}/scale${t}_tps_refs.ts $rgn $proj -W0.8p,grey,1_2 -O -K >> $out.ps
    gmt psxy $basedir/${labels[$i]}/scale.ts $rgn $proj -W0.8p,grey -O -K >> $out.ps
    gmt psxy $basedir/${labels[$i]}/scale${t}.ts $rgn $proj -W0.8p,black -O -K >> $out.ps
    gmt psxy $basedir/${labels[$i]}/scale${t}_tps.ts $rgn $proj -Sc2.5p -Gblack -O -K >> $out.ps
    # gmt psxy $basedir/${labels[$i]}/Qs${t}.ts $rgn $proj -W0.8p,red -O -K >> $out.ps
    gmt psxy $basedir/${labels[$i]}/lin_Qs${t}.ts $rgn $proj -W0.8p,red -O -K >> $out.ps
    if [ $i -gt 0 ] ; then
      gmt psxy $basedir/${labels[$i]}/lin_Qs${t}_tps.ts $rgn $proj -Sc2.5p -Gred -O -K >> $out.ps
    fi
    # gmt psbasemap $rgn $proj -B${scale_grds[$i]} -Bx100 -By0.2+l"Norm. @%2%Q@-s,0@-@%%" -O -K >> $out.ps
    gmt psbasemap $rgn $proj -B${scale_grds[$i]} -Bx100 -By0.2+l"Norm. @%2%Q@-w@-@%%" -O -K >> $out.ps
    gmt psbasemap $rgn $proj -B${scale_grds2[$i]} -By0.2+l"Norm. @%2%Q@-s,L@-@%%" --MAP_DEFAULT_PEN="+red" --FONT="red" -O -K >> $out.ps
    # rgn=-R0/100/0.7/1.3
    # proj=-JX0.4i/0.7i
    # gmt psbasemap $rgn $proj -Bnsew --MAP_DEFAULT_PEN="+,blue" -O -K >> $out.ps

    # Time series
    rgn=-R0/500/0/700
    proj=-JX2i/1.5i
    gmt psbasemap $rgn $proj -B+n -Y-1.7i -O -K >> $out.ps
    # gmt psxy $basedir/${labels[$i]}/scale${t}_tps_refs.te $rgn $proj -W0.8p,grey,1_2 -O -K >> $out.ps
    # gmt psxy $basedir/z_refs.te $rgn $proj -W0.8p,. -Corder.cpt -O -K >> $out.ps
    # gmt psxy $basedir/${labels[$i]}/z${t}.te $rgn $proj -W0.8p -Corder.cpt -O -K >> $out.ps
    gmt psxy $basedir/lin_z_refs.te $rgn $proj -W0.8p,. -Cx.cpt -O -K >> $out.ps
    gmt psxy $basedir/${labels[$i]}/lin_z${t}.te $rgn $proj -W0.8p -Cx.cpt -O -K >> $out.ps
    if [ $i -gt 0 ] ; then
      gmt psxy $basedir/${labels[$i]}/lin_z${t}_tps.te $rgn $proj -Sc2.5p -Cx.cpt -O -K >> $out.ps
    fi
    gmt psbasemap $rgn $proj -B${elev_grds[$i]} -Bx100+l"Time [kyr]" -By200+l"Elevation [m]" -O -K >> $out.ps
    # rgn=-R0/100/0/700
    # proj=-JX0.4i/1.5i
    # gmt psbasemap $rgn $proj -Bnsew --MAP_DEFAULT_PEN="+,blue" -O -K >> $out.ps

    # # Scale
    # rgn=-R0/100/0.7/1.3
    # proj=-JX3.5i/0.7i
    # gmt psbasemap $rgn $proj -B+n -Y1.7i -X3.2i -O -K >> $out.ps
    # # gmt psxy $basedir/${labels[$i]}/scale${t}_tps_refs.ts $rgn $proj -W0.8p,grey,1_2 -O -K >> $out.ps
    # gmt psxy $basedir/${labels[$i]}/scale.ts $rgn $proj -W0.8p,grey -O -K >> $out.ps
    # gmt psxy $basedir/${labels[$i]}/scale${t}.ts $rgn $proj -W0.8p,black -O -K >> $out.ps
    # gmt psxy $basedir/${labels[$i]}/scale${t}_tps.ts $rgn $proj -Sc2.5p -Gblack -O -K >> $out.ps
    # # gmt psxy $basedir/${labels[$i]}/Qs${t}.ts $rgn $proj -W0.8p,red -O -K >> $out.ps
    # gmt psxy $basedir/${labels[$i]}/lin_Qs${t}.ts $rgn $proj -W0.8p,red -O -K >> $out.ps
    # gmt psxy $basedir/${labels[$i]}/lin_Qs${t}_tps.ts $rgn $proj -Sc2.5p -Gred -O -K >> $out.ps
    # gmt psbasemap $rgn $proj -B${scale_grds[$i]} -Bx20 -By0.2+l"Norm. @%2%Q@-s,0@-@%%" -O -K >> $out.ps
    # gmt psbasemap $rgn $proj -B${scale_grds2[$i]} -By0.2+l"Norm. @%2%Q@-s,L@-@%%" --MAP_DEFAULT_PEN="+red" --FONT="red" -O -K >> $out.ps
    # 
    # # Time series
    # rgn=-R0/100/0/700
    # proj=-JX3.5i/1.5i
    # gmt psbasemap $rgn $proj -B+n -Y-1.7i -O -K >> $out.ps
    # # gmt psxy $basedir/${labels[$i]}/scale${t}_tps_refs.te $rgn $proj -W0.8p,grey,1_2 -O -K >> $out.ps
    # # gmt psxy $basedir/z_refs.te $rgn $proj -W0.8p,. -Corder.cpt -O -K >> $out.ps
    # # gmt psxy $basedir/${labels[$i]}/z${t}.te $rgn $proj -W0.8p -Corder.cpt -O -K >> $out.ps
    # gmt psxy $basedir/lin_z_refs.te $rgn $proj -W0.8p,. -Cx.cpt -O -K >> $out.ps
    # gmt psxy $basedir/${labels[$i]}/lin_z${t}.te $rgn $proj -W0.8p -Cx.cpt -O -K >> $out.ps
    # gmt psxy $basedir/${labels[$i]}/lin_z${t}_tps.te $rgn $proj -Sc2.5p -Cx.cpt -O -K >> $out.ps
    # gmt psbasemap $rgn $proj -B${elev_grds[$i]} -Bx20+l"Time [kyr]" -By200+l"Elevation [m]" -O -K >> $out.ps

  done

  # Show
  gmt psbasemap -R0/1/0/1 -JX1i -B+n -O >> $out.ps
  gmt psconvert -A -E400 -Tj $out.ps
  eog $out.jpg &

done

# ---- Create gif
# convert -loop 0 $basedir/scene*.jpg $basedir/periodic.gif
# ffmpeg -framerate 10 -pattern_type glob -i "$basedir/scene*.jpg" -final_delay 500 -vf "scale=1024:-1" -y $basedir/periodic.gif
# eog $basedir/periodic.gif &