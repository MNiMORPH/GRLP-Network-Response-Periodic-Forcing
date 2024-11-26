#!/bin/bash
#SBATCH --nodes=10
#SBATCH --ntasks=50
#SBATCH --cpus-per-task=8
#SBATCH --time=10-00:0

# Load python
module load Python

# Activate virtual environment
source /home/mcnab/network/bin/activate

# Define parameters
nruns=200

# Loop over runs, submitting jobs
for run in $(seq $nruns) ; do
  
  # Submit the job
  srun --exclusive --nodes=1 --ntasks=1 --cpus-per-task=8  \
    python Network_MC.py \
    $run 40 "/home/mcnab/grlp_network_analysis/Output/Network/MC_N1_40/" &
    
  # Every 50th job, wait for jobs to finish before continuing
  if [ $i -eq 49 ] || [ $i -eq 99 ] || [ $i -eq 149 ] ; then
    wait
  fi

done
  
wait
deactivate