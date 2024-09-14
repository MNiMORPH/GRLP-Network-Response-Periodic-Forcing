#!/bin/bash
#SBATCH --nodes=5
#SBATCH --ntasks=50
#SBATCH --cpus-per-task=4
#SBATCH --time=10-00:0

# Load python
module load Python

# Activate virtual environment
source /home/mcnab/network/bin/activate

# # Define parameters
# setup_file="./test.yaml"
# nruns=4
# # nnets_per_run=10

# # Loop over runs, submitting jobs
# for run in $(seq $nruns) ; do
#   net0=$(echo $run $nnets_per_run | awk ' { print ($1-1)*$2 } ')
#   netn=$(echo $net0 $nnets_per_run | awk ' { print $1+$2-1 } ')
#   srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=4-00:0 \
#     python Network_MC.py \
#     $net0 $netn $setup_file &
# done

# for i in $(seq $nruns) ; do
#   srun --exclusive --nodes=1 --ntasks=1 --cpus-per-task=4 \
#     python Network_MC_2.py \
#     $i $setup_file &
# done

min_N1_min=5
max_N1_min=95
i=0

for N1_min in $(seq $min_N1_min 10 $max_N1_min) ; do

  for N1 in $(seq $N1_min 2 $(echo $N1_min | awk ' {print $1 + 8} ')) ; do
    
    for j in $(seq 0 1) ; do
      srun --exclusive --nodes=1 --ntasks=1 --cpus-per-task=4 \
        python Network_MC_2.py \
        $i $N1 "/home/mcnab/grlp_network_analysis/Output/Network/MC_N1_5-105/" &
      i=$[$i+1]
      if [ $i -eq 49 ] ; then
        wait
      fi
    done
    
  done
  
done
  
wait
deactivate