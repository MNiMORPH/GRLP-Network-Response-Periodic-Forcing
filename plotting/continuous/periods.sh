#!/bin/bash -i

# ---- Set defaults
# set_gmt_defaults
source setup_gmt.sh

# ---- Inputs / Output
basedir="../../output/continuous/periods"
out="periods"

# ---- Variables
proj=-JX2il/2i
pmin=0.003
pmax=300

# ---- CPTs
gmt makecpt -T1.2/2.8/0.4 -Cplasma -D -G0/0.95 > p.cpt

# ---- G_z
rgn=-R${pmin}/${pmax}/-0.1/1.3
gmt psbasemap $rgn $proj -B+n -X0.5i -Y6i -K > $out.ps
gmt psxy $basedir/G_z_rng_lin.pg $rgn $proj -Glightgrey -O -K >> $out.ps 
gmt psxy $basedir/G_z_out_lin.pg $rgn $proj -W0.8p -O -K >> $out.ps 
# gmt psxy $basedir/G_z_num.pg $rgn $proj -Cp.cpt -W0.8p -O -K >> $out.ps
# gmt psxy $basedir/G_z_in_num.pg $rgn $proj -Cp.cpt -W0.8p,4_4 -O -K >> $out.ps
gmt psxy $basedir/G_z_num.pg $rgn $proj -Cp.cpt -Ey+a+cf+w3p+p0.8p -O -K >> $out.ps
gmt psxy $basedir/G_z_num.pg $rgn $proj -Sc4.5p -Gblack -O -K >> $out.ps
gmt psxy $basedir/G_z_num.pg $rgn $proj -Sc3p -Cp.cpt -O -K >> $out.ps
echo a | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jLT+cLT -D0.05i/-0.08i -O -K >> $out.ps
echo 1 1.3 "@~\144@~@%2%z@%%" | \
  gmt pstext $rgn $proj -F+f10p,Helvetica,black+jMC -D0i/0.2i -N -O -K >> $out.ps
echo "> -W0.8p
0.0015 1.05
0.004 1.05
> -W3p,lightgrey
0.0015 0.95
0.004 0.95" | gmt psxy $rgn $proj -O -K >> $out.ps
echo "0.0024494897427831787 0.85 0.5" | gmt psxy $rgn $proj -Sc4.5p -Gblack -O -K >> $out.ps
echo "0.0024494897427831787 0.85 0.5" | gmt psxy $rgn $proj -Sc3p -Cp.cpt -O -K >> $out.ps
echo "0.004 1.05 Upstream supply (outlet)
0.004 0.95 Upstream supply (range)
0.004 0.85 Continuous supply" | gmt pstext $rgn $proj -F+f6p,Helvetica,black+jLM -D0.02i/0i -O -K >> $out.ps
# echo "0.1 0.4
# 1 0.4
# 10 0.92" | gmt psxy $rgn $proj -Si3p -W0.8p -Gblack -O -K >> $out.ps
gmt psbasemap $rgn $proj -BnseW -Bx1f3p+l"Period, @%2%P@%% / @%2%T@-eq@-@%%" -By0.2+l"Gain, @%2%G@-z@-@%%" -O -K >> $out.ps

# ---- lag_z
rgn=-R${pmin}/${pmax}/-0.05/0.45
gmt psbasemap $rgn $proj -B+n -Y-2.2i -O -K >> $out.ps
gmt psxy $basedir/lag_z_rng_lin.pg $rgn $proj -Glightgrey -O -K >> $out.ps 
gmt psxy $basedir/lag_z_out_lin.pg $rgn $proj -W0.8p -O -K >> $out.ps 
gmt psxy $basedir/lag_z_num.pg $rgn $proj -Cp.cpt -Ey+a+cf+w3p+p0.8p -O -K >> $out.ps
gmt psxy $basedir/lag_z_num.pg $rgn $proj -Sc4.5p -Gblack -O -K >> $out.ps
gmt psxy $basedir/lag_z_num.pg $rgn $proj -Sc3p -Cp.cpt -O -K >> $out.ps
echo d | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jLT+cLT -D0.05i/-0.08i -O -K >> $out.ps
gmt psbasemap $rgn $proj -BnSeW -Bx1f3p+l"Period, @%2%P@%% / @%2%T@-eq@-@%%" -By0.1+l"Lag, @~\152@~@%2%@-z@-@%% / @%2%P@%%" -O -K >> $out.ps

# ---- G_Qs (Qs)
rgn=-R${pmin}/${pmax}/-0.1/1.3
gmt psbasemap $rgn $proj -B+n -Y2.2i -X2.6i -O -K >> $out.ps
gmt psxy $basedir/G_Qs_out_lin.pg $rgn $proj -W0.8p -O -K >> $out.ps 
gmt psxy $basedir/G_Qs_num.pg $rgn $proj -Sc4.5p -Gblack -O -K >> $out.ps
gmt psxy $basedir/G_Qs_num.pg $rgn $proj -Sc3p -Cp.cpt -O -K >> $out.ps
echo b | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jLT+cLT -D0.05i/-0.08i -O -K >> $out.ps
echo 1 1.3 "@~\144@~@%2%Q@-s@-@%%: Varying sediment supply" | \
  gmt pstext $rgn $proj -F+f10p,Helvetica,black+jMC -D0i/0.2i -N -O -K >> $out.ps
gmt psbasemap $rgn $proj -BnseW -Bx1f3p+l"Period, @%2%P@%% / @%2%T@-eq@-@%%" -By0.2+l"Gain, @%2%G@-Qs@-@%%" -O -K >> $out.ps

# ---- lag_Qs (Qs)
rgn=-R${pmin}/${pmax}/-0.05/0.45
gmt psbasemap $rgn $proj -B+n -Y-2.2i -O -K >> $out.ps
gmt psxy $basedir/lag_Qs_out_lin.pg $rgn $proj -W0.8p -O -K >> $out.ps 
gmt psxy $basedir/lag_Qs_num.pg $rgn $proj -Sc4.5p -Gblack -O -K >> $out.ps
gmt psxy $basedir/lag_Qs_num.pg $rgn $proj -Sc3p -Cp.cpt -O -K >> $out.ps
echo e | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jLT+cLT -D0.05i/-0.08i -O -K >> $out.ps
gmt psbasemap $rgn $proj -BnSeW -Bx1f3p+l"Period, @%2%P@%% / @%2%T@-eq@-@%%" -By0.1+l"Lag, @~\152@~@%2%@-Qs@-@%% / @%2%P@%%" -O -K >> $out.ps

# ---- G_Qs (Qw)
rgn=-R${pmin}/${pmax}/-0.1/1.3
gmt psbasemap $rgn $proj -B+n -Y2.2i -X2.25i -O -K >> $out.ps
gmt psxy $basedir/G_Qs_Qw_out_lin.pg $rgn $proj -W0.8p -O -K >> $out.ps 
gmt psxy $basedir/G_Qs_Qw_num.pg $rgn $proj -Sc4.5p -Gblack -O -K >> $out.ps
gmt psxy $basedir/G_Qs_Qw_num.pg $rgn $proj -Sc3p -Cp.cpt -O -K >> $out.ps
echo c | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jRT+cRT -D-0.05i/-0.08i -O -K >> $out.ps
echo 1 1.3 "@~\144@~@%2%Q@-s@-@%%: Varying water supply" | \
  gmt pstext $rgn $proj -F+f10p,Helvetica,black+jMC -D0i/0.2i -N -O -K >> $out.ps
gmt psbasemap $rgn $proj -BnsEw -Bx1f3p+l"Period, @%2%P@%% / @%2%T@-eq@-@%%" -By0.2+l"Gain, @%2%G@-Qs@-@%%" -O -K >> $out.ps

# ---- lag_Qs (Qw)
rgn=-R${pmin}/${pmax}/-0.275/0.025
gmt psbasemap $rgn $proj -B+n -Y-2.2i -O -K >> $out.ps
gmt psxy $basedir/lag_Qs_Qw_out_lin.pg $rgn $proj -W0.8p -O -K >> $out.ps 
gmt psxy $basedir/lag_Qs_Qw_num.pg $rgn $proj -Sc4.5p -Gblack -O -K >> $out.ps
gmt psxy $basedir/lag_Qs_Qw_num.pg $rgn $proj -Sc3p -Cp.cpt -O -K >> $out.ps
echo f | gmt pstext $rgn $proj -F+f11p,Helvetica-Bold,black+jRT+cRT -D-0.05i/-0.08i -O -K >> $out.ps
gmt psscale $rgn $proj -Dx0.5i/0.15i+w0.8i/0.08i+jMC+h+m -Bx0.4+1+l"@%2%p@-x,Qw@-     p@-x,Qs@-@%%" -Cp.cpt --MAP_LABEL_OFFSET=3.5p -O -K >> $out.ps
gmt psbasemap $rgn $proj -BnSEw -Bx1f3p+l"Period, @%2%P@%% / @%2%T@-eq@-@%%" -By0.05+l"Lag, @~\152@~@%2%@-Qs@-@%% / @%2%P@%%" -O >> $out.ps

# ---- Show
gmt psconvert -A -E400 -Tj $out.ps
eog $out.jpg &