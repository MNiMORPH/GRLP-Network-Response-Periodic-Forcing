#!/bin/bash

# ---- Define catchments to process and colours for plotting.
catches=(South_Platte Niobara Bighorn Arkansas Big_Blue)
colours=(213/094/000 000/158/115 086/180/233 204/121/167 000/114/178)

# ---- Loop over catchments.
for i in ${!catches[@]} ; do
  catch=${catches[$i]}
  colour=${colours[$i]}
  echo Working on: $catch
  
  # ---- Create temporary data file with inverted commas removed.
  sed 's/"//g' $catch.csv > streams.tmp

  # ---- Extract minimum and maximum drainage areas for the catchment.
  # Sometimes there are a few points from the downstream catchment, which can
  # swamp the remaining drainage areas. So we ignore the last couple of points.
  # The $9 condition ignores endorheic segments.
  Amin=$(awk ' BEGIN {FS=","} NR>1 && $9!=1 {print $8}' streams.tmp | \
            head -n-2 | \
            gmt gmtinfo -C | \
            awk '{print $1}')
  Amax=$(awk ' BEGIN {FS=","} NR>1 && $9!=1 {print $8}' streams.tmp | \
            head -n-2 | \
            gmt gmtinfo -C | \
            awk '{print $2}')

  # ---- Initialise output file.
  echo -e > ${catch}.gmt
  
  # ---- Loop over segments.
  for stream in $(awk ' BEGIN {FS=","} NR>1 {print $1}' streams.tmp | uniq | head -n-1) ; do

    # ---- Get area and use to write segment header.
    # Scale line width by area, and use colour specified above.
    A=$(awk ' BEGIN {FS=","} $1=='$stream' {print $8}' streams.tmp | head -n1)
    W=$(echo $A $Amin $Amax | awk '{print 0.2 + ($1-$2)/($3-$2)*1}')
    echo "> -W${W}p,$colour" >> ${catch}.gmt
    
    # ---- Write the stream x,y data.
    # The $9 condition ignores endorheic segments.
    awk ' BEGIN {FS=","} $1=='$stream' && $9!=1 {print $20, $21}' streams.tmp >> ${catch}.gmt

  done

done

# ---- Tidy up
rm streams.tmp