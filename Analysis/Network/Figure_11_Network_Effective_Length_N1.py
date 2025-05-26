"""
This script performs the analysis presented in Figure 11 of McNab et al. (2025,
EGUsphere); produces a rough version of the Figure; and, optionally, generates
output files for plotting the final Figure in GMT.

The purpose of the script/figure is to show how a network effective lengths,
and their relationships with network mean lengths, depend on the number of
segments in the network.
"""


# ---- Import functions

# External packages
import numpy as np
import matplotlib.pyplot as plt
import copy
import grlp
from scipy.stats import binned_statistic

# Local packages
import grlp_extras as grlpx


# ---- Variables
output_gmt = False
indirs = {
    'N1_40': "../../Output/Network/MC_N1_40/",
    'N1_2-150': "../../Output/Network/MC_N1_2-150/"
    }


# ---- Read data
print("Reading results.")
nets = {}
gains = {}
for N1 in indirs.keys():
    nets[N1], gains[N1] = grlpx.read_MC(
        indirs[N1],
        cases=['UUU', 'NUU', 'UAU', 'NAU'],
        toread=['nets', 'gains']
        )


# ---- Plot
print("Plotting.")

# Initialize plot
fig, axs = plt.subplots(3, 4, sharex=True, sharey="row")

# Create dictionaries for saving results
eff_lengths = {}
mean_lengths = {}
N1s = {}
bins = {}

# Loop over sweep directories
for N1 in indirs.keys():
    
    # Create sub-dictionaries for saving results
    eff_lengths[N1] = {}
    mean_lengths[N1] = {}
    N1s[N1] = {}
    bins[N1] = {}
    
    # Loop over network cases
    for i,case in enumerate(['UUU', 'NUU', 'UAU', 'NAU']):
        
        # Compute effective lengths from empirical equilibration times
        eff_lengths[N1][case] = np.sqrt([
                g[case]['Teq']*nets[N1][i][case].mean_diffusivity
                for i,g in enumerate(gains[N1])
                ])
        
        # Create list of mean lengths    
        mean_lengths[N1][case] = np.array(
            [n[case].mean_head_length for n in nets[N1]]
            )
        
        # Create list of numbers of network inlet segments
        N1s[N1][case] = [
            (len(n[case].list_of_LongProfile_objects)+1)/2 for n in nets[N1]
            ]
        
        # Plot effective length against number of inlet segments
        axs[0,i].plot(
            N1s[N1][case],
            eff_lengths[N1][case]/1.e3,
            "o",
            alpha=0.5
            )
        
        # Plot mean length against number of inlet segments
        axs[1,i].plot(
            N1s[N1][case],
            mean_lengths[N1][case]/1.e3,
            "o",
            alpha=0.5
            )

        # Plot effective length / mean length against number of inlet segments
        axs[2,i].plot(
            N1s[N1][case],
            eff_lengths[N1][case]/mean_lengths[N1][case],
            "o",
            alpha=0.5
            )
        
        # Bin effective lengths and mean lengths, plot the binned values
        binned_eff_lengths = binned_statistic(
            N1s[N1][case],
            eff_lengths[N1][case]
            )
        binned_mean_lengths = binned_statistic(
            N1s[N1][case],
            mean_lengths[N1][case]
            )            
        binned_N1s = (
            binned_eff_lengths.bin_edges[:-1] +
            (binned_eff_lengths.bin_edges[1:] - 
                binned_eff_lengths.bin_edges[:-1])/2.
            )
        axs[0,i].plot(binned_N1s, binned_eff_lengths.statistic/1.e3, "k+")
        axs[1,i].plot(binned_N1s, binned_mean_lengths.statistic/1.e3, "k+")
        axs[2,i].plot(
            binned_N1s,
            binned_eff_lengths.statistic/binned_mean_lengths.statistic,
            "k+"
            )
        bins[N1][case] = {
            'eff_lengths': binned_eff_lengths.statistic,
            'mean_lengths': binned_mean_lengths.statistic,
            'N1s': binned_N1s
            }
            
        # Label x axis
        axs[2,i].set_xlabel(r"Number of inlet segments, $N_1$ [-]")

# Label y axes
axs[0,0].set_ylabel(
    r"Effective length, $\widehat{L}$ [km]"
    )
axs[1,0].set_ylabel(
    r"Mean length, $\langle L \rangle$ [km]"
    )
axs[2,0].set_ylabel(
    r"$\widehat{L}$ / $\langle L \rangle$ [-]"
    )
    
for ax in axs:
    for a in ax:
        a.set_box_aspect(1)

plt.show()

# ---- Save

if output_gmt:
    
    basedir = "../../Output/Network/Figure_11_Network_Effective_Length_N1/"

    for N1 in indirs.keys():
        for i,case in enumerate(['UUU', 'NUU', 'UAU', 'NAU']):
                
                outfile = basedir + N1 + "_" + case + "_full.dat"
                with open(outfile, "wb") as f:
                    arr = np.column_stack((
                        N1s[N1][case],
                        eff_lengths[N1][case]/1.e3,
                        mean_lengths[N1][case]/1.e3
                        ))
                    np.savetxt(f, arr)

                outfile = basedir + N1 + "_" + case + "_bin.dat"
                with open(outfile, "wb") as f:
                    arr = np.column_stack((
                        bins[N1][case]['N1s'],
                        bins[N1][case]['eff_lengths']/1.e3,
                        bins[N1][case]['mean_lengths']/1.e3
                        ))
                    np.savetxt(f, arr)