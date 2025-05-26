# Software and data supplement to "Influence of network geometry on long-term morphodynamics of alluvial rivers" by M<sup>c</sup>Nab et al. (2025, EGUsphere)

This repository contains scripts and data to reproduce the analyses and figures presented in:

- M<sup>c</sup>Nab, F., Schildgen, T.F., Turowski, J.M. and Wickert, A.D., 2025, Influence of network geometry on long-term morphodynamics of alluvial rivers, *EGUSphere [Preprint]*, [doi:10.5194/egusphere-2025-2468](https://doi.org/10.5194/egusphere-2025-2468).

The repository is structured as follows:

- `Analysis/`: Directory containing `Python` scripts for performing the core analysis of the paper.
  - `SingleSegment/`: Scripts associated with single segment analysis.
  - `Network/`: Scripts associated with network analysis.
    - `HPC/`: Scripts to submit and run large batches of network analyses to a high performance computing cluster (using `slurm`).
    - `Expected_Length/`: `C++` script to compute expected network lengths.
- `Cartoon`: `svg` files associated with the cartoon in Figure 2 of the paper.
- `Figures/`: Directory the final figures presented in the paper.
- `LICENCE`:
- `Output`: Directory containing files produced during the analyis for final plotting in `GMT`.
- `Photos`: Photographs shown in Figure 1 of the paper.
- `Plotting/`: Directory containing `GMT` scripts to plot the final figures presented in the paper.
- `src`: Directory containing source code for the analyses.
- `pyproject.toml`: `Python` project setup file, for installing dependencies and source code.
- `README.md`: The text you are reading.

## Running the code

### Python

To run the Python scripts in `Analysis/` you will need a working `Python3` environment with dependencies as listed in `pyproject.toml`. Constructing random networks and soliving the equations of long profile evolution and sediment transport is achieved using the `GRLP` package (Wickert and Schildgen, 2019; Wickert et al., 2024).

The following instructions apply for `UNIX` systems. You may need to make small adjustments depending on your specific system. The steps may be significantly different on Windows, depending on how you use Python. But it should be possible to install and run the code in the way you normally install and run Python code.

To install all the dependencies, and the source code in stored in `src/`, run the following command(s) in a terminal. First, optionally create and activate a virtual environment in your desired location, here for example called "network":

```
$ # Create and activate a virtual environment:
$ python3 -m venv path/to/virtual/environment/network
$ source path/to/virtual/environment/network/bin/activate
```

Next download this repository, navigate into it, and run:

```
(network) $ pip install .
```

### GMT

The scripts in `Plotting/` use `Bash` shell, which will be available by default on most `UNIX` systems. They primarily use commands from the `Generic Mapping Tools v6.5` (Wessel et al., 2019). See the documentation for instructions on how to install GMT. They also use `ImageMagick`'s convert command to convert `pdf` output files to `jpg`. Once you have GMT installed, you should be able to run the scripts in the `Plotting/` directory.

## Citation

If you use this code, please cite the original paper as well as this repository:

- M<sup>c</sup>Nab, F., Schildgen, T.F., Turowski, J.M. and Wickert, A.D., 2025, Influence of network geometry on long-term morphodynamics of alluvial rivers, *EGUSphere [Preprint]*, [doi:10.5194/egusphere-2025-2468](https://doi.org/10.5194/egusphere-2025-2468).
- M<sup>c</sup>Nab, F., 2025, Software and data supplement to "Influence of network geometry on long-term morphodynamics of alluvial rivers" by M<sup>c</sup>Nab et al. (2025, EGUsphere), Version 1, *Zenodo*.

## Licence

This repository is distributed under the terms of the Creative Commons Attribution 4.0 International (see `LICENCE` for details).

## References

- Wessel, P., Luis, J. F., Uieda, L., Scharroo, R., Wobbe, F., Smith, W. H. F. and Tian, D., 2019, The Generic Mapping Tools version 6, *Geochemistry, Geophysics, Geosystems*, **20**, p. 5556-5564, [doi:10.1029/2019GC008515](https://doi.org/10.1029/2019GC008515).
- Wickert, A.D. and Schildgen, T.F., 2019, Long-profile evolution of transport-limited gravel-bed rivers, *Earth Surface Dynamics*, **7**, p. 17-43, [doi:10.5194/esurf-7-17-2019](https://doi.org/10.5194/esurf-7-17-2019).
- Wickert, A.D., M<sup>c</sup>Nab, F. and Barefoot, E., 2024, GRLP, Version 2.0.0-beta, *Zenodo*, [doi:10.5281/zenodo.14237263](https://doi.org/10.5281/zenodo.14237263).