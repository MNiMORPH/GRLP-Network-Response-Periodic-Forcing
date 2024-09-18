"""
This script performs the analysis presented in Figure 11 of McNab et al. (2024,
EGUsphere); produces a rough version of the Figure; and, optionally, generates
output files for plotting the final Figure in GMT.

The purpose of the script/figure is to .
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
    'N1_2-102': "../../Output/Network/MC_N1_2-102/"
    }


# ---- Read data
print("Reading results.")
nets = {}
hacks = {}
gains = {}
lags = {}
for N1 in indirs.keys():
    nets[N1], hacks[N1], gains[N1], lags[N1] = grlpx.read_MC(indirs[N1])


# ---- Plot

fig, axs = plt.subplots(1, 4, sharex=True, sharey=True)

eff_lengths = {}
mean_lengths = {}
N1s = {}
bins = {}

for N1 in indirs.keys():
    
    eff_lengths[N1] = {}
    mean_lengths[N1] = {}
    N1s[N1] = {}
    bins[N1] = {}
    
    for i,case in enumerate(['UUU', 'NUU', 'UAU', 'NAU']):
        
        eff_lengths[N1][case] = np.sqrt([
                g[case]['Teq']*nets[N1][i][case].mean_diffusivity
                for i,g in enumerate(gains[N1])
                ])
                
        mean_lengths[N1][case] = np.array(
            [n[case].mean_downstream_distance for n in nets[N1]]
            )
                
        N1s[N1][case] = [
            (len(n[case].list_of_LongProfile_objects)+1)/2 for n in nets[N1]
            ]
            
        axs[i].plot(
            N1s[N1][case],
            eff_lengths[N1][case]/mean_lengths[N1][case],
            "o",
            alpha=0.5
            )
            
        binned = binned_statistic(
            N1s[N1][case],
            eff_lengths[N1][case]/mean_lengths[N1][case]
            )
        binned_N1s = (
            binned.bin_edges[:-1] +
            (binned.bin_edges[1:] - binned.bin_edges[:-1])/2.
            )
        axs[i].plot(binned_N1s, binned.statistic, "k+")
        bins[N1][case] = {
            'eff_lengths': binned.statistic,
            'N1s': binned_N1s
            }
            
        axs[i].set_xlabel(r"Number of inlet segments, $N_1$")
        
axs[0].set_ylabel(
    r"Effective length / Mean length, $\widehat{L}$ / $\langle L \rangle$"
    )

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
                        eff_lengths[N1][case]/mean_lengths[N1][case]
                        ))
                    np.savetxt(f, arr)

                outfile = basedir + N1 + "_" + case + "_bin.dat"
                with open(outfile, "wb") as f:
                    arr = np.column_stack((
                        bins[N1][case]['N1s'],
                        bins[N1][case]['eff_lengths']
                        ))
                    np.savetxt(f, arr)