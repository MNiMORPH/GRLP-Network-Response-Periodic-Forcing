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
nruns=50

# Loop over runs, submitting jobs
for run in $(seq $nruns) ; do
  srun --exclusive --nodes=1 --ntasks=1 --cpus-per-task=8  \
    python Network_MC.py \
    $run 20 "/home/mcnab/grlp_network_analysis/Output/Network/MC_N1_20/" &
done
  
wait
deactivate