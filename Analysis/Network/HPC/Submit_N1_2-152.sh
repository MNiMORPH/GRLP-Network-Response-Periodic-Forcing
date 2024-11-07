#!/bin/bash
#SBATCH --nodes=10
#SBATCH --ntasks=50
#SBATCH --cpus-per-task=8
#SBATCH --time=10-00:0

# Load python
module load Python

# Activate virtual environment
source /home/mcnab/network/bin/activate

# Define variables
min_N1_min=2
max_N1_min=142
i=1

for N1_min in $(seq $min_N1_min 10 $max_N1_min) ; do

  for N1 in $(seq $N1_min 2 $(echo $N1_min | awk ' {print $1 + 8} ')) ; do
    
    for j in $(seq 0 1) ; do
      srun --exclusive --nodes=1 --ntasks=1 --cpus-per-task=8 \
        python Network_MC.py \
        $i $N1 "/home/mcnab/grlp_network_analysis/Output/Network/MC_N1_2-152/" &
      if [ $i -eq 50 ] || [ $i -eq 100 ]; then
        wait
      fi
      i=$[$i+1]
    done
    
  done
  
done
  
wait
deactivate