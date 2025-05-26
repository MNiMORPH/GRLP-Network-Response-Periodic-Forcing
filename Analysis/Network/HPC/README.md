The scripts contained in this directory are intended to be run on a high performance cluster with the `Slurm` workload manager. `Network_MC.py` is a `Python` script that creates a eight versions of a single network topology (with uniform/non-uniform segment lengths, upstream/along-stream water and sediment supply, uniform/non-uniform valley width) and performs the analaysis for each of them. The analysis involves varying sediment and water supply sinusoidally and then measuring the corresponding network gain and lag. `Submit_MC_N1_40.sh` and `Submit_MC_N1_2-150.sh` are `Slurm` shell scripts that submit `Network_MC.py` multiple times to the cluster. For example, to submit the former script, type at the command line:

```
$ sbatch Submit_MC_N1_40.sh
```

This script submits a set of 200 networks each with 40 valley inlet segments. The other script submits a set of 496 networks with 2-150 valley inlet segments. The scripts expect an accessible `Python` virtual environment to be set up with this project's dependencies installed (see instructions in the base directory).