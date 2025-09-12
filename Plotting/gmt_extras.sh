#!/bin/bash

gmt_extras::set_gmt_defaults () {
  gmt set FONT_ANNOT_PRIMARY 7p
  gmt set FONT_LABEL 7p
  gmt set MAP_ANNOT_OFFSET_PRIMARY 2p
  gmt set MAP_LABEL_OFFSET 6p
  gmt set PS_LINE_JOIN round
  gmt set MAP_FRAME_TYPE plain
  gmt set PS_PAGE_ORIENTATION portrait
  gmt set PS_MEDIA a4
  gmt set GMT_VERBOSE n
  gmt set PS_CHAR_ENCODING Standard+
}

gmt_extras::plot_key_line () {
  local rgn=$1
  local proj=$2
  local x1=$3
  local x2=$4
  local y=$5
  local fmt=$6
  local label=$7
  local out=$8
  echo "$x1 $y
$x2 $y" | gmt psxy $rgn $proj $fmt -O -K >> $out.ps

  local just=$(echo $x1 $x2 | awk ' { if ($2>$1) print "LM" ; else print "RM" } ')
  local xoff=$(echo $x1 $x2 | awk ' { if ($2>$1) print 0.02 ; else print -0.02 } ')
  echo "$x2 $y $label" | \
    gmt pstext $rgn $proj -F+f6p+j$just -D${xoff}i/0i -O -K >> $out.ps
}

gmt_extras::plot_key_symbol () {
  local rgn=$1
  local proj=$2
  local x1=$3
  local x2=$4
  local y=$5
  local fmt=$6
  local label=$7
  local out=$8
  echo $x1 $y | gmt psxy $rgn $proj $fmt -O -K >> $out.ps

  local just=$(echo $x1 $x2 | awk ' { if ($2>$1) print "LM" ; else print "RM" } ')
  local xoff=$(echo $x1 $x2 | awk ' { if ($2>$1) print 0.02 ; else print -0.02 } ')
  echo "$x2 $y $label" | \
    gmt pstext $rgn $proj -F+f6p+j$just -D${xoff}i/0i -O -K >> $out.ps
}

gmt_extras::plot_key_error_symbol () {
  local rgn=$1
  local proj=$2
  local x1=$3
  local x2=$4
  local y=$5
  local err=$6
  local fmt=$7
  local label=$8
  local out=$9
  echo $x1 $y $err | gmt psxy $rgn $proj $fmt -O -K >> $out.ps

  local just=$(echo $x1 $x2 | awk ' { if ($2>$1) print "LM" ; else print "RM" } ')
  local xoff=$(echo $x1 $x2 | awk ' { if ($2>$1) print 0.02 ; else print -0.02 } ')
  echo "$x2 $y $label" | \
    gmt pstext $rgn $proj -F+f6p+j$just -D${xoff}i/0i -O -K >> $out.ps
}


gmt_extras::plot_key_multi_line () {
  local rgn=$1
  local proj=$2
  local x1=$3
  local x2=$4
  local y=$5
  local fmt=$6
  local label=$7
  local out=$8
  local cpt=$9
  shift 9
  local values=($@)  
  
  local dx=$(echo $x1 $x2 ${#values[@]} | awk ' { print ($2-$1)/$3 } ')
  local x1s=($(seq $x1 $dx $(echo $x2 $dx | awk ' { print $1-$2 } ')))
  local x2s=($(seq $(echo $x1 $dx | awk ' { print $1+$2 } ') $dx $x2))
  
  local i
  for i in ${!x1s[@]} ; do
    echo "> -Z${values[$i]}
${x1s[$i]} $y
${x2s[$i]} $y" | gmt psxy $rgn $proj $fmt -C$cpt -O -K >> $out.ps
  done
  
  local just=$(echo $x1 $x2 | awk ' { if ($2>$1) print "LM" ; else print "RM" } ')
  local xoff=$(echo $x1 $x2 | awk ' { if ($2>$1) print 0.02 ; else print -0.02 } ')
  echo "$x2 $y $label" | \
    gmt pstext $rgn $proj -F+f6p+j$just -D${xoff}i/0i -O -K >> $out.ps
}

gmt_extras::plot_discharge_key () {
  local rgn=$1
  local proj=$2
  local x=$3
  local y1=$4
  local y2=$5
  local out=$6
  local w1=0.8
  local w2=2.2
  local nx=20
  local dy=$(echo $y1 $y2 $nx | awk ' { print ($2-$1)/$3 }')
  for y in $(seq $y1 $dy $y2) ; do
    local yplus=$(echo $y $dy | awk ' { print $1+$2 }')
    local w=$(echo $w1 $w2 $y1 $y2 $y | awk ' { print $1 + ($5-$3)/($4-$3)*($2-$1) } ')
    echo "$x $y
$x $yplus" | gmt psxy $rgn $proj -W${w}p -O -K >> $out.ps
  done
  echo "$x $y1 min(@%2%Q@-w@-@%%)" | \
    gmt pstext $rgn $proj -F+f6p+jRM -D-0.04i/0i -O -K >> $out.ps
  echo $x $y2 "max(@%2%Q@-w@-@%%)" | \
    gmt pstext $rgn $proj -F+f6p+jRM -D-0.04i/0i -O -K >> $out.ps
}
