"""
Loop through all networks plotting gain and lag.
"""

# External packages
import numpy as np
import matplotlib.pyplot as plt
import grlp

# Local packages
import grlp_extras as grlpx


# ---- Select set of results to plot.
nets, hacks, gains, lags = grlpx.read_MC("../../Output/Network/MC_N1_40/")

# ----- Select desired period index between 0 and 6.
# Ranges from c. 0.01 x Teq to c. 100 x Teq.
# Not exact because this analysis is used to calibrate Teq - so Teq here is
# out initial guess. 
P = 0

# Some problems with: 20 129

# ---- Plot.
# Loops over different network cases, plotting gain and lag.
# Plots networks with uniform valley width in colour, those with variable
# valley width in light grey.

for i,net in enumerate(nets):

    fig, axs = plt.subplots(2, 4, sharex=True, sharey="row", figsize=(14,7))

    for j,seg in enumerate(net['UUN'].list_of_LongProfile_objects):
        axs[0,0].plot(seg.x/1.e3, gains[i]['UUN']['G_z']['Qs'][P][j], "0.8")
        axs[1,0].plot(seg.x/1.e3, lags[i]['UUN']['lag_z']['Qs'][P][j], "0.8")    
    for j,seg in enumerate(net['UUU'].list_of_LongProfile_objects):
        axs[0,0].plot(seg.x/1.e3, gains[i]['UUU']['G_z']['Qs'][P][j])
        axs[1,0].plot(seg.x/1.e3, lags[i]['UUU']['lag_z']['Qs'][P][j])
    axs[0,0].set_title("Uniform segment lengths\nUpstream supply")
    axs[0,0].set_ylabel(r"$G_z$ [-]")
    axs[1,0].set_ylabel(r"$\varphi_z$ / $P$ [-]")
    axs[1,0].set_xlabel(r"$x$ [km]")

    for j,seg in enumerate(net['NUN'].list_of_LongProfile_objects):
        axs[0,1].plot(seg.x/1.e3, gains[i]['NUN']['G_z']['Qs'][P][j], "0.8")
        axs[1,1].plot(seg.x/1.e3, lags[i]['NUN']['lag_z']['Qs'][P][j], "0.8")
    for j,seg in enumerate(net['NUU'].list_of_LongProfile_objects):
        axs[0,1].plot(seg.x/1.e3, gains[i]['NUU']['G_z']['Qs'][P][j])
        axs[1,1].plot(seg.x/1.e3, lags[i]['NUU']['lag_z']['Qs'][P][j])
    axs[0,1].set_title("Non-uniform segment lengths\nUpstream supply")
    axs[1,1].set_xlabel(r"$x$ [km]")
        
    for j,seg in enumerate(net['UAN'].list_of_LongProfile_objects):
        axs[0,2].plot(seg.x/1.e3, gains[i]['UAN']['G_z']['Qs'][P][j], "0.8")
        axs[1,2].plot(seg.x/1.e3, lags[i]['UAN']['lag_z']['Qs'][P][j], "0.8")
    for j,seg in enumerate(net['UAU'].list_of_LongProfile_objects):
        axs[0,2].plot(seg.x/1.e3, gains[i]['UAU']['G_z']['Qs'][P][j])
        axs[1,2].plot(seg.x/1.e3, lags[i]['UAU']['lag_z']['Qs'][P][j])
    axs[0,2].set_title("Uniform segment lengths\nAlong stream supply")
    axs[1,2].set_xlabel(r"$x$ [km]")

    for j,seg in enumerate(net['NAN'].list_of_LongProfile_objects):
        if j==0:
            lab="Non-uniform widths"
        else:
            lab=""
        axs[0,3].plot(seg.x/1.e3, gains[i]['NAN']['G_z']['Qs'][P][j], "0.8")
        axs[1,3].plot(seg.x/1.e3, lags[i]['NAN']['lag_z']['Qs'][P][j], "0.8", label=lab)
    for j,seg in enumerate(net['NAU'].list_of_LongProfile_objects):
        if j==0:
            lab="Uniform widths"
        else:
            lab=""
        axs[0,3].plot(seg.x/1.e3, gains[i]['NAU']['G_z']['Qs'][P][j])
        axs[1,3].plot(seg.x/1.e3, lags[i]['NAU']['lag_z']['Qs'][P][j], label=lab)
    axs[0,3].set_title("Non-uniform segment lengths\nAlong stream supply")
    axs[1,3].set_xlabel(r"$x$ [km]")
    axs[1,3].legend()

    for row in axs:
        for ax in row:
            ax.set_box_aspect(1)

    fig.suptitle("Network %i" % i)
    plt.show()