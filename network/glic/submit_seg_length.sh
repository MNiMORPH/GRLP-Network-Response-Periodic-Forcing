#!/bin/bash
#SBATCH --nodes=10
#SBATCH --ntasks=10
#SBATCH --cpus-per-task=10
#SBATCH --time=3-00:0

module load Python
source /home/mcnab/network/bin/activate
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=3-00:0 python network_sweep_seg_length.py 0 19 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=3-00:0 python network_sweep_seg_length.py 20 39 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=3-00:0 python network_sweep_seg_length.py 40 59 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=3-00:0 python network_sweep_seg_length.py 60 79 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=3-00:0 python network_sweep_seg_length.py 80 99 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=3-00:0 python network_sweep_seg_length.py 100 119 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=3-00:0 python network_sweep_seg_length.py 120 139 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=3-00:0 python network_sweep_seg_length.py 140 159 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=3-00:0 python network_sweep_seg_length.py 160 179 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=3-00:0 python network_sweep_seg_length.py 180 199 &
wait
deactivate