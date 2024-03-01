#!/bin/bash
#SBATCH --nodes=10
#SBATCH --ntasks=10
#SBATCH --cpus-per-task=10
#SBATCH --time=3-00:0

module load Python
source /home/mcnab/network/bin/activate
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=3-00:0 python network_sweep_seg_length.py 200 219 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=3-00:0 python network_sweep_seg_length.py 220 239 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=3-00:0 python network_sweep_seg_length.py 240 259 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=3-00:0 python network_sweep_seg_length.py 260 279 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=3-00:0 python network_sweep_seg_length.py 280 299 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=3-00:0 python network_sweep_seg_length.py 300 319 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=3-00:0 python network_sweep_seg_length.py 320 339 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=3-00:0 python network_sweep_seg_length.py 340 359 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=3-00:0 python network_sweep_seg_length.py 360 379 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=3-00:0 python network_sweep_seg_length.py 380 399 &
wait
deactivate