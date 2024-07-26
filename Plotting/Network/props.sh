#!/bin/bash -i

# Set defaults
set_gmt_defaults

# Variables
out=props
proj=-JX1i
basedir="../../output/network/props"
sweepdir=("m20_fix_seg_length" "m40_fix_seg_length" "m2-100_fix_seg_length" "m40_rnd_seg_length")
Rb_counts=(300 500 100 500)
Rb_ticks=(100 100 25 100)
Rl_counts=(150 300 100 250)
Rl_ticks=(50 100 25 50)
Rq_counts=(200 250 150 100)
Rq_ticks=(50 50 50 25)
h_counts=(100 100 100 100)
h_ticks=(25 25 25 25)
Le_counts=(200 150 100 100)
Le_ticks=(50 50 25 25)
Rb_labs=("a" "f" "k" "p")
Rl_labs=("b" "g" "l" "q")
Rq_labs=("c" "h" "m" "r")
h_labs=("d" "i" "n" "s")
Le_labs=("e" "j" "o" "t")
sweep_labs=("@~\155@~ = 20" "@~\155@~ = 40" "@~\155@~ = 2-100" "@~\155@~ = 40")

gmt psbasemap -R0/1/0/1 $proj -B+n -Y9i -X6.4i -K > $out.ps
for i in ${!sweepdir[@]} ; do
  
  if [ $i -eq 3 ] ; then
    S="S"
  else
    S="s"
  fi

  # Rb
  rgn=-R0/10/0/${Rb_counts[$i]}
  gmt psbasemap $rgn $proj -B+n -X-5.2i -Y-1.15i -O -K >> $out.ps
  gmt pshistogram $basedir/${sweepdir[$i]}/Rb.c $rgn $proj -Ggrey -T20+n -O -K >> $out.ps
  echo ${Rb_labs[$i]} | gmt pstext $rgn $proj -F+f10p,Helvetica-Bold,black+jBR+cBR -D0i/0.06i -O -K >> $out.ps 
  gmt psbasemap $rgn $proj -B${S}W -Bpx2+l"@%2%R@-b@-@%% [-]" -By${Rb_ticks[$i]}+l"Count" -O -K >> $out.ps
  echo ${sweep_labs[$i]} | gmt pstext $rgn $proj -F+f11p+a90+cBL+jCM -N -D-0.6i/0.5i -O -K >> $out.ps

  # Rl
  rgn=-R0/10/0/${Rl_counts[$i]}
  gmt psbasemap $rgn $proj -B+n -X1.3i -O -K >> $out.ps
  gmt pshistogram $basedir/${sweepdir[$i]}/Rl.c $rgn $proj -Ggrey -T20+n -O -K >> $out.ps
  echo ${Rl_labs[$i]} | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jBR+cBR -D0i/0.06i -O -K >> $out.ps 
  gmt psbasemap $rgn $proj -B${S}W -Bx2+l"@%2%R@-l@-@%% [-]" -By${Rl_ticks[$i]} -O -K >> $out.ps

  # Rq
  rgn=-R0/10/0/${Rq_counts[$i]}
  gmt psbasemap $rgn $proj -B+n -X1.3i -O -K >> $out.ps
  gmt pshistogram $basedir/${sweepdir[$i]}/Rq.c $rgn $proj -Ggrey -T20+n -O -K >> $out.ps
  echo ${Rq_labs[$i]} | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jBR+cBR -D0i/0.06i -O -K >> $out.ps 
  gmt psbasemap $rgn $proj -B${S}W -Bx2+l"@%2%R@-Q@-@%% [-]" -By${Rq_ticks[$i]} -O -K >> $out.ps

  # h
  rgn=-R0.4/1.2/0/${h_counts[$i]}
  gmt psbasemap $rgn $proj -B+n -X1.3i -O -K >> $out.ps
  gmt pshistogram $basedir/${sweepdir[$i]}/h.c $rgn $proj -Ggrey -T20+n -O -K >> $out.ps
  echo ${h_labs[$i]} | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jBR+cBR -D0i/0.06i -O -K >> $out.ps 
  gmt psbasemap $rgn $proj -B${S}W -Bx0.2+l"@%2%h@%% [-]" -By${h_ticks[$i]} -O -K >> $out.ps

  # L
  rgn=-R20/120/0/${Le_counts[$i]}
  gmt psbasemap $rgn $proj -B+n -X1.3i -O -K >> $out.ps
  gmt pshistogram $basedir/${sweepdir[$i]}/Le.c $rgn $proj -Ggrey -T20+n -O -K >> $out.ps
  echo ${Le_labs[$i]} | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jBR+cBR -D0i/0.06i -O -K >> $out.ps 
  gmt psbasemap $rgn $proj -B${S}W -Bx20+l"@%2%L@-e@-@%% [km]" -By${Le_ticks[$i]} -O -K >> $out.ps

done

# Finalise, show
gmt psbasemap -R0/1/0/1 -JX2i -B+n -O >> $out.ps
gmt psconvert -A -E400 -Tj $out.ps
rm $out.ps
eog $out.jpg &