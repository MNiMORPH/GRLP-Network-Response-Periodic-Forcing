#!/bin/bash
#SBATCH --nodes=10
#SBATCH --ntasks=10
#SBATCH --cpus-per-task=10
#SBATCH --time=3-00:0

module load Python
source /home/mcnab/network/bin/activate
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=3-00:0 python network_sweep_seg_length.py 0 49 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=3-00:0 python network_sweep_seg_length.py 50 99 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=3-00:0 python network_sweep_seg_length.py 100 149 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=3-00:0 python network_sweep_seg_length.py 150 199 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=3-00:0 python network_sweep_seg_length.py 200 249 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=3-00:0 python network_sweep_seg_length.py 250 299 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=3-00:0 python network_sweep_seg_length.py 300 349 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=3-00:0 python network_sweep_seg_length.py 350 399 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=3-00:0 python network_sweep_seg_length.py 400 449 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=3-00:0 python network_sweep_seg_length.py 450 499 &
wait
deactivate