"""
This script performs the analysis presented in Figure 17; produces a rough
version of the Figure; and, optionally, generates output files for plotting the
final Figure in GMT.

The purpose of the figure is to explore further controls on response lag at the
network outlet under relatively short period (i.e. P/Teq < 1) variation in
sediment supply.
"""


# ---- Import functions

# External packages
import numpy as np
import matplotlib.pyplot as plt
import copy
import grlp

# Local packages
import grlp_extras as grlpx


# ---- Variables
output_gmt = False
indir = "../../Output/Network/MC_N1_40/"
nets, gains, lags = grlpx.read_MC(
    indir,
    cases=['UUU', 'NUU'],
    toread=['nets', 'gains', 'lags']
    )


# ---- Analysis

# Set up figure
fig, axs = plt.subplots(1, 2, sharex=True, sharey=True)

for p in [0,1,2,3]:

    for i,case in enumerate(['UUU', 'NUU']):

        # Get empirical equilibration times
        Teqs = [gs[case]['Teq'] for gs in gains]

        # Get minimum distances upstream to first segment inlet
        min_head_length = []
        for net in nets:
            x_max = net[case].list_of_LongProfile_objects[0].x.max()
            xs = [x_max - net[case].list_of_LongProfile_objects[i].x[0]
                for i in net[case].list_of_channel_head_segment_IDs]
            min_head_length.append(min(xs)/1.e3)
        
        # Plot
        axs[i].scatter(
            [ls[case]['P'][p]/Teqs[i] for i,ls in enumerate(lags)],
            [ls[case]['lag_Qs']['Qs'][p] for ls in lags],
            c=min_head_length,
            alpha=0.5
            )
        axs[i].set_xscale("log")
    
plt.show()

# ---- Save

if output_gmt:

    basedir = "../../Output/Network/Figure_17_Network_Short_Period_Lag/"

    for i,case in enumerate(['UUU', 'NUU']):
        
        Teqs = [gs[case]['Teq'] for gs in gains]
        min_head_length = []

        for net in nets:
            x_max = net[case].list_of_LongProfile_objects[0].x.max()
            xs = [x_max - net[case].list_of_LongProfile_objects[i].x[0]
                    for i in net[case].list_of_channel_head_segment_IDs]
            min_head_length.append(min(xs)/1.e3)

        with open(basedir + "/" + case + "_Qs_lag.pl", "wb") as f:
            arr = np.column_stack((
                [p/Teqs[i]
                    for i,ls in enumerate(lags)
                    for p in ls[case]['P']],
                [l
                    for ls in lags
                    for l in ls[case]['lag_Qs']['Qs']],
                [min_head_length[i]
                    for i,ls in enumerate(lags)
                    for p in ls[case]['P']]
                ))
            np.savetxt(f, arr)