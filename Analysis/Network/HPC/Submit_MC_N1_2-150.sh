#!/bin/bash
#SBATCH --nodes=20
#SBATCH --ntasks=100
#SBATCH --cpus-per-task=8
#SBATCH --time=20-00:0

# Load python
module load Python

# Activate virtual environment
source /home/mcnab/network/bin/activate

# Define variables
N1_min=2
N1_max=150
i=0

# Loop over N1s
for N1 in $(seq $N1_min 1 $N1_max) ; do

  # Four runs per N1
  for j in $(seq 0 3) ; do
    
    # Submit the job
    srun --exclusive --nodes=1 --ntasks=1 --cpus-per-task=8 \
      python Network_MC.py \
      $i $N1 "/home/mcnab/grlp_network_analysis/Output/Network/MC_N1_2-150/" &
    
    # Every 100th job, wait for jobs to finish before continuing
    if [ $i -eq 99 ] || [ $i -eq 199 ] || [ $i -eq 299 ] || [ $i -eq 399 ] || [ $i -eq 499 ] ; then
      wait
    fi
    
    # Increment
    i=$[$i+1]
    
  done
  
done
  
wait
deactivate