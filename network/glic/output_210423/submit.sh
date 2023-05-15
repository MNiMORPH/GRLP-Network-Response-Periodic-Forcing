#!/bin/bash
#SBATCH --nodes=4
#SBATCH --ntasks=4
#SBATCH --cpus-per-task=8
#SBATCH --time=1-12:0

module load Python
source grlp_venv/bin/activate
srun --nodes=1 --ntasks=1 --cpus-per-task=8 --time=1-12:0 python network_sweep.py 0 49 &
srun --nodes=1 --ntasks=1 --cpus-per-task=8 --time=1-12:0 python network_sweep.py 50 99 &
srun --nodes=1 --ntasks=1 --cpus-per-task=8 --time=1-12:0 python network_sweep.py 100 149 &
srun --nodes=1 --ntasks=1 --cpus-per-task=8 --time=1-12:0 python network_sweep.py 150 199 &
wait
deactivate