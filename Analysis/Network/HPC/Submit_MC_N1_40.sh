#!/bin/bash
#SBATCH --nodes=20
#SBATCH --ntasks=100
#SBATCH --cpus-per-task=8
#SBATCH --time=10-00:0

# Load python
module load Python

# Activate virtual environment
source /home/mcnab/network/bin/activate

# Define parameters
nruns=200

# Loop over runs, submitting jobs
for i in $(seq 0 $nruns) ; do
  
  # Submit the job
  srun --exclusive --nodes=1 --ntasks=1 --cpus-per-task=8  \
    python Network_MC.py \
    $i 40 "/home/mcnab/grlp_network_analysis/Output/Network/MC_N1_40/" &
    
  # After 100 jobs, wait for jobs to finish before continuing
  if [ $i -eq 99 ] ; then
    wait
  fi

done
  
wait
deactivate