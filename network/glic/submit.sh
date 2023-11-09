#!/bin/bash
#SBATCH --nodes=10
#SBATCH --ntasks=10
#SBATCH --cpus-per-task=10
#SBATCH --time=2-00:0

module load Python
source /home/mcnab/network/bin/activate
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=2-00:0 python network_sweep.py 0 49 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=2-00:0 python network_sweep.py 50 99 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=2-00:0 python network_sweep.py 100 149 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=2-00:0 python network_sweep.py 150 199 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=2-00:0 python network_sweep.py 200 249 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=2-00:0 python network_sweep.py 250 299 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=2-00:0 python network_sweep.py 300 349 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=2-00:0 python network_sweep.py 350 399 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=2-00:0 python network_sweep.py 400 449 &
srun --nodes=1 --ntasks=1 --cpus-per-task=10 --time=2-00:0 python network_sweep.py 450 499 &
wait
deactivate