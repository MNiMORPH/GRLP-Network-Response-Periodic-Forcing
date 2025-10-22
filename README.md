# Software and data supplement to "Influence of network geometry on long-term morphodynamics of alluvial rivers" by M<sup>c</sup>Nab et al. (2025, ESurf)

This repository contains scripts and data to reproduce the analyses and figures presented in:

- M<sup>c</sup>Nab, F., Schildgen, T.F., Turowski, J.M. and Wickert, A.D., 2025, Influence of network geometry on long-term morphodynamics of alluvial rivers, *Earth Surface Dynamics*, **13**, p. 1,059-1,092 [doi:10.5194/esurf-13-1059-2025](https://doi.org/10.5194/esurf-13-1059-2025).

The repository is structured as follows:

- `Analysis/`: Directory containing `Python` scripts for performing the core analysis of the paper.
  - `SingleSegment/`: Scripts associated with single segment analysis.
  - `Network/`: Scripts associated with network analysis.
    - `HPC/`: Scripts to submit and run large batches of network analyses to a high performance computing cluster (using `slurm`).
    - `Expected_Length/`: `C++` script to compute expected network lengths.
- `Figures/`: Directory the final figures presented in the paper.
- `Video_Supplement/`: Directory containing scripts for generating the supplementary GIF.
- `LICENCE`: CC-BY-4.0 Licence.
- `Output/`: Directory containing files produced during the analyis for final plotting in `GMT`.
- `Plotting/`: Directory containing `GMT` scripts to plot the final figures presented in the paper.
  - `Introduction/`: Scripts for plotting introductory figures.
    - `Cartoon_Drawings`: `.svg` files containing cartoons for Figure 3.
    - `Photos`: Photographs shown in Figure 2.
    - `Planform_Data`: Data for network planforms in Figure 1 (originally from the HydroRIVERS database; Lehner and Grill, 2013).
  - `SingleSegment`: Scripts for plotting figures showing results for single-segment valleys.
  - `Network`: Scripts for plotting figures showing results for valley networks.
- `src/`: Directory containing source code for the analyses.
- `pyproject.toml`: `Python` project setup file, for installing dependencies and source code.
- `README.md`: The text you are reading.

## Running the code

### Python

To run the Python scripts in `Analysis/` you will need a working `Python3` environment with dependencies as listed in `pyproject.toml`. Constructing random networks and soliving the equations of long profile evolution and sediment transport is achieved using the `GRLP` package (Wickert and Schildgen, 2019; Wickert et al., 2025).

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

## Data

The majority of the analysis is self-contained and does not rely on any external data. An exception is our introductory Figure 1, which shows some example network planforms from the western USA. The data for these planforms, stored at `Plotting/Introduction/Planform_Data/`, was originally derived from the [HydroRIVERS](https://www.hydrosheds.org/products/hydrorivers]) database (Lehner and Grill, 2013). Photographs in `Plotting/Introduction/Photos/` were provided by T. Schildgen and S. Tofelde.

## Citation

If you use this code, please cite the original paper as well as this repository:

- M<sup>c</sup>Nab, F., Schildgen, T.F., Turowski, J.M. and Wickert, A.D., 2025, Influence of network geometry on long-term morphodynamics of alluvial rivers, *Earth Surface Dynamics*, **13**, p. 1,059-1,092 [doi:10.5194/esurf-13-1059-2025](https://doi.org/10.5194/esurf-13-1059-2025).
- M<sup>c</sup>Nab, F., 2025, Software and data supplement to "Influence of network geometry on long-term morphodynamics of alluvial rivers" by M<sup>c</sup>Nab et al. (2025, ESurf), Version 2.1, *Zenodo*, [doi:10.5281/zenodo.15524964](https://doi.org/10.5281/zenodo.15524964).

In addition, please cite the version of `GRLP` you use. For results presented in M<sup>c</sup>Nab et al. (2025, ESurf), we used:

- Wickert, A.D., M<sup>c</sup>Nab, F. and Barefoot, E., 2025, GRLP, Version 2.0.0, *Zenodo*, [doi:10.5281/zenodo.17091246](https://doi.org/10.5281/zenodo.17091246).

## Licence

This repository is distributed under the terms of the Creative Commons Attribution 4.0 International (see `LICENCE` for details).

## References

- Lehner. B. and Grill, G., 2013, Global river hydrography and network routing: baseline data and new approaches to study the world’s large river systems, *Hydrological Processes*, **27**(15), p. 2,171-2,186, [doi:10.1002/hyp.9740](https://doi.org/10.1002/hyp.9740).
- Wessel, P., Luis, J. F., Uieda, L., Scharroo, R., Wobbe, F., Smith, W. H. F. and Tian, D., 2019, The Generic Mapping Tools version 6, *Geochemistry, Geophysics, Geosystems*, **20**, p. 5,556-5,564, [doi:10.1029/2019GC008515](https://doi.org/10.1029/2019GC008515).
- Wickert, A.D. and Schildgen, T.F., 2019, Long-profile evolution of transport-limited gravel-bed rivers, *Earth Surface Dynamics*, **7**, p. 17-43, [doi:10.5194/esurf-7-17-2019](https://doi.org/10.5194/esurf-7-17-2019).