#!/bin/bash
#SBATCH --nodes=10
#SBATCH --ntasks=10
#SBATCH --cpus-per-task=10
#SBATCH --time=4-00:0

module load Python
source /home/mcnab/network/bin/activate
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=4-00:0 python network_sweep_seg_length.py 0 39 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=4-00:0 python network_sweep_seg_length.py 40 79 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=4-00:0 python network_sweep_seg_length.py 80 119 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=4-00:0 python network_sweep_seg_length.py 120 159 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=4-00:0 python network_sweep_seg_length.py 160 199 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=4-00:0 python network_sweep_seg_length.py 200 239 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=4-00:0 python network_sweep_seg_length.py 240 279 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=4-00:0 python network_sweep_seg_length.py 280 319 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=4-00:0 python network_sweep_seg_length.py 320 359 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=4-00:0 python network_sweep_seg_length.py 360 399 &
wait
deactivate