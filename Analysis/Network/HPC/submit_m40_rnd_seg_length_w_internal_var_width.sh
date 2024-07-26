#!/bin/bash
#SBATCH --nodes=10
#SBATCH --ntasks=10
#SBATCH --cpus-per-task=10
#SBATCH --time=4-00:0

module load Python
source /home/mcnab/network/bin/activate

setup_file="./setup_m40_rnd_seg_length_w_internal_var_width.yaml"
nruns=10
nnets_per_run=20
for run in $(seq $nruns) ; do
  net0=$(echo $run $nnets_per_run | awk ' { print ($1-1)*$2 } ')
  netn=$(echo $net0 $nnets_per_run | awk ' { print $1+$2-1 } ')
  srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=4-00:0 \
    python network_sweep_seg_length.py \
    $net0 $netn $setup_file &
done
  
wait
deactivate