#!/bin/bash
#SBATCH --nodes=10
#SBATCH --ntasks=10
#SBATCH --cpus-per-task=10
#SBATCH --time=4-00:0

# Load python
module load Python

# Activate virtual environment
source /home/mcnab/network/bin/activate

# Define parameters
setup_file="./Setup_N1_40.yaml"
nruns=5
nnets_per_run=10

# Loop over runs, submitting jobs
for run in $(seq $nruns) ; do
  net0=$(echo $run $nnets_per_run | awk ' { print ($1-1)*$2 } ')
  netn=$(echo $net0 $nnets_per_run | awk ' { print $1+$2-1 } ')
  srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=4-00:0 \
    python Network_MC.py \
    $net0 $netn $setup_file &
done
  
wait
deactivate