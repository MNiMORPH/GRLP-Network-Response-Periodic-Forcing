#!/bin/bash -i

# ---- Set defaults
set_gmt_defaults


# ---- Inputs / Output
indir="./output/continuous_spatial"
out="continuous_spatial"

# ---- Variables
proj=-JX2i
rgn=-R-10/110/-0.25/2.75
rgn_lag=-R-10/110/-1.25/0.75

# ---- CPTs
gmt makecpt -T0/4/0.1 -Cplasma -D -Z > p.cpt


# ---- Gain_z
gmt psbasemap $rgn $proj -B+n -Y6i -K > $out.ps
gmt psxy $indir/G_z_lin.dg $rgn $proj -W0.8p,- -O -K >> $out.ps
gmt psxy $indir/G_z.dg $rgn $proj -W0.8p -Cp.cpt -O -K >> $out.ps
gmt psbasemap $rgn $proj -BnseW \
    -Bx20+l"Downstream distance [km]" \
    -By0.5+l"@%2%G@%%" \
    -O -K >> $out.ps

# ---- Lag_z
gmt psbasemap $rgn_lag $proj -B+n -Y-2.2i -O -K >> $out.ps
gmt psxy $indir/Lag_z_lin.dl $rgn_lag $proj -W0.8p,- -O -K >> $out.ps
gmt psxy $indir/Lag_z.dl $rgn_lag $proj -W0.8p -Cp.cpt -O -K >> $out.ps
gmt psbasemap $rgn_lag $proj -BnSeW \
    -Bx20+l"Downstream distance [km]" \
    -By0.5+l"@~\152@~@%2% / P@%%" \
    -O -K >> $out.ps

# ---- Gain_Qs(Qs)
gmt psbasemap $rgn $proj -B+n -Y2.2i -X2.2i -O -K >> $out.ps
gmt psxy $indir/G_Qs_lin.dg $rgn $proj -W0.8p,- -O -K >> $out.ps
gmt psxy $indir/G_Qs.dg $rgn $proj -W0.8p -Cp.cpt -O -K >> $out.ps
gmt psbasemap $rgn $proj -Bnsew \
    -Bx20+l"Downstream distance [km]" \
    -By0.5+l"@%2%G@%%" \
    -O -K >> $out.ps
    
# ---- Lag_Qs(Qs)
gmt psbasemap $rgn_lag $proj -B+n -Y-2.2i -O -K >> $out.ps
gmt psxy $indir/Lag_Qs_lin.dl $rgn_lag $proj -W0.8p,- -O -K >> $out.ps
gmt psxy $indir/Lag_Qs.dl $rgn_lag $proj -W0.8p -Cp.cpt -O -K >> $out.ps
gmt psbasemap $rgn_lag $proj -BnSew \
    -Bx20+l"Downstream distance [km]" \
    -By0.5+l"@~\152@~@%2% / P@%%" \
    -O -K >> $out.ps
        
# ---- Gain_Qs(Qw)
gmt psbasemap $rgn $proj -B+n -Y2.2i -X2.2i -O -K >> $out.ps
gmt psxy $indir/G_Qs_Qw_lin.dg $rgn $proj -W0.8p,- -O -K >> $out.ps
gmt psxy $indir/G_Qs_Qw.dg $rgn $proj -W0.8p -Cp.cpt -O -K >> $out.ps
gmt psbasemap $rgn $proj -Bnsew \
    -Bx20+l"Downstream distance [km]" \
    -By0.5+l"@%2%G@%%" \
    -O -K >> $out.ps
    
# ---- Lag_Qs(Qw)
gmt psbasemap $rgn_lag $proj -B+n -Y-2.2i -O -K >> $out.ps
gmt psxy $indir/Lag_Qs_Qw_lin.dl $rgn_lag $proj -W0.8p,- -O -K >> $out.ps
gmt psxy $indir/Lag_Qs_Qw.dl $rgn_lag $proj -W0.8p -Cp.cpt -O -K >> $out.ps
gmt psbasemap $rgn_lag $proj -BnSew \
    -Bx20+l"Downstream distance [km]" \
    -By0.5+l"@~\152@~@%2% / P@%%" \
    -O -K >> $out.ps
    
# ---- Show
gmt psbasemap $rgn $proj -B+n -O >> $out.ps
# gv $out.ps &
gmt psconvert -A -E400 -Tj $out.ps
eog $out.jpg &