"""
This script performs the analysis presented in Figures S18, S19 and S20 of McNab
et al. (2025, EGUsphere); produces a rough version of the Figures; and,
optionally, generates output files for plotting the final Figures in GMT.

The purpose of the main script/figure is to explore controls on the empirically
obtained effective lengths of our sets of networks. We compute correlation
coefficients of effective length against a series of network metrics (see text
for detailed definitions). We show scatter plots of effective length against
network mean length, which has the best correlation.

In the additional figures, we show scatter plots of effective length against
all additional network properties.

Here, in contrast with Figures 9, S5, and S6, valley width is set to increase
downstream with the same power-law exponent as water and sediment discharge,
rather than being held constant. This has the effect of keeping the diffusivity
constant along stream.
"""

# ---- Define functions
def compute_origin_gradient(x, y):
    """
    Compute the best-fitting gradient of a straight line through the data x
    and y, constrained to go through the origin.
    """
    x = np.array(x)
    y = np.array(y)
    return x.dot(y) / x.dot(x)


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
indirs = {
    'N1_40': "../../Output/Network/MC_N1_40/",
    'N1_2-150': "../../Output/Network/MC_N1_2-150/"
    }


# ---- Read data
print("Reading results.")
nets = {}
hacks = {}
gains = {}
for N1 in indirs.keys():
    nets[N1], hacks[N1], gains[N1] = grlpx.read_MC(
        indirs[N1],
        cases=['UUN', 'NUN', 'UAN', 'NAN'],
        toread=['nets', 'hacks', 'gains']
        )

# ---- Regressions
# Loop through networks and record correlation coefficients and best-fitting
# straight-line gradients between effective length and other network
# properties.
print("Computing regressions.")
regressions = {'N1_40': {}, 'N1_2-150': {}}

for N1 in indirs.keys():
    regressions[N1] = {'UUN': {}, 'NUN': {}, 'UAN': {}, 'NAN': {}}

    for case in ['UUN', 'NUN', 'UAN', 'NAN']:
        
        regressions[N1][case]['eff_lengths'] = np.sqrt([
                g[case]['Teq']*nets[N1][i][case].mean_diffusivity
                for i,g in enumerate(gains[N1])
                ])
            
        regressions[N1][case]['coeffs'] = {}
        regressions[N1][case]['grads'] = {}
        
        regressions[N1][case]['coeffs']['R_B'] = np.corrcoef(
            [n[case].bifurcation_ratio for n in nets[N1]],
            regressions[N1][case]['eff_lengths']
            )[0,1]
        regressions[N1][case]['grads']['R_B'] = compute_origin_gradient(
            [n[case].bifurcation_ratio for n in nets[N1]],
            regressions[N1][case]['eff_lengths']
            )

        regressions[N1][case]['coeffs']['R_L'] = np.corrcoef(
            [n[case].length_ratio for n in nets[N1]],
            regressions[N1][case]['eff_lengths']
            )[0,1]
        regressions[N1][case]['grads']['R_L'] = compute_origin_gradient(
            [n[case].length_ratio for n in nets[N1]],
            regressions[N1][case]['eff_lengths']
            )
            
        regressions[N1][case]['coeffs']['R_Q'] = np.corrcoef(
            [n[case].discharge_ratio for n in nets[N1]],
            regressions[N1][case]['eff_lengths']
            )[0,1]
        regressions[N1][case]['grads']['R_Q'] = compute_origin_gradient(
            [n[case].discharge_ratio for n in nets[N1]],
            regressions[N1][case]['eff_lengths']
            )
        
        # Need to be careful with Tokunaga's K because it can contain NaNs,
        # which mess up the regression.
        Ks = np.array([n[case].tokunaga['K_mean'] for n in nets[N1]])
        non_nans = np.where(np.isfinite(Ks))
        regressions[N1][case]['coeffs']['K'] = np.corrcoef(
            Ks[non_nans],
            regressions[N1][case]['eff_lengths'][non_nans]
            )[0,1]
        regressions[N1][case]['grads']['K'] = compute_origin_gradient(
            Ks[non_nans],
            regressions[N1][case]['eff_lengths'][non_nans]
            )

        regressions[N1][case]['coeffs']['l'] = np.corrcoef(
            [net[case].max_topological_length for net in nets[N1]],
            regressions[N1][case]['eff_lengths']
            )[0,1]
        regressions[N1][case]['grads']['l'] = compute_origin_gradient(
            [net[case].max_topological_length for net in nets[N1]],
            regressions[N1][case]['eff_lengths']
            )        

        regressions[N1][case]['coeffs']['<l>'] = np.corrcoef(
            [net[case].mean_topological_length for net in nets[N1]],
            regressions[N1][case]['eff_lengths']
            )[0,1]
        regressions[N1][case]['grads']['<l>'] = compute_origin_gradient(
            [net[case].mean_topological_length for net in nets[N1]],
            regressions[N1][case]['eff_lengths']
            )
            
        regressions[N1][case]['coeffs']['<l_I>'] = np.corrcoef(
            [net[case].mean_head_topological_length for net in nets[N1]],
            regressions[N1][case]['eff_lengths']
            )[0,1]
        regressions[N1][case]['grads']['<l_I>'] = compute_origin_gradient(
            [net[case].mean_head_topological_length for net in nets[N1]],
            regressions[N1][case]['eff_lengths']
            )     

        regressions[N1][case]['coeffs']['L'] = np.corrcoef(
            [n[case].list_of_LongProfile_objects[0].x.max() for n in nets[N1]],
            regressions[N1][case]['eff_lengths']
            )[0,1]
        regressions[N1][case]['grads']['L'] = compute_origin_gradient(
            [n[case].list_of_LongProfile_objects[0].x.max() for n in nets[N1]],
            regressions[N1][case]['eff_lengths']
            )

        regressions[N1][case]['coeffs']['<L>'] = np.corrcoef(
            [n[case].mean_length for n in nets[N1]],
            regressions[N1][case]['eff_lengths']
            )[0,1]
        regressions[N1][case]['grads']['<L>'] = compute_origin_gradient(
            [n[case].mean_length for n in nets[N1]],
            regressions[N1][case]['eff_lengths']
            )

        regressions[N1][case]['coeffs']['<L_I>'] = np.corrcoef(
            [n[case].mean_head_length for n in nets[N1]],
            regressions[N1][case]['eff_lengths']
            )[0,1]
        regressions[N1][case]['grads']['<L_I>'] = compute_origin_gradient(
            [n[case].mean_head_length for n in nets[N1]],
            regressions[N1][case]['eff_lengths']
            )

        regressions[N1][case]['coeffs']['w'] = np.corrcoef(
            [net[case].max_topological_width for net in nets[N1]],
            regressions[N1][case]['eff_lengths']
            )[0,1]
        regressions[N1][case]['grads']['w'] = compute_origin_gradient(
            [net[case].max_topological_width for net in nets[N1]],
            regressions[N1][case]['eff_lengths']
            )

        regressions[N1][case]['coeffs']['<w>'] = np.corrcoef(
            [net[case].mean_topological_width for net in nets[N1]],
            regressions[N1][case]['eff_lengths']
            )[0,1]
        regressions[N1][case]['grads']['<w>'] = compute_origin_gradient(
            [net[case].mean_topological_width for net in nets[N1]],
            regressions[N1][case]['eff_lengths']
            )        

        regressions[N1][case]['coeffs']['p'] = np.corrcoef(
            [h[case]['p'] for h in hacks[N1]],
            regressions[N1][case]['eff_lengths']
            )[0,1]
        regressions[N1][case]['grads']['p'] = compute_origin_gradient(
            [h[case]['p'] for h in hacks[N1]],
            regressions[N1][case]['eff_lengths']
            )

# ---- Labels
# Properly formatted variables for plotting.
labels = {
    'R_B': r'$R_B$',
    'R_L': r'$R_L$',
    'R_Q': r'$R_Q$',
    'K': r'$K$',
    'l': r'$l$',
    '<l>': r'$\langle l \rangle$',
    '<l_I>': r'$\langle l_I \rangle$',
    'L': r'$L$',
    '<L>': r'$\langle L \rangle$',
    '<L_I>': r'$\langle L_I \rangle$',
    'w': r'$w$',
    '<w>': r'$\langle w \rangle$',
    'p': r'$p$'
    }


# ---- Plot
print("Plotting.")
fig, axs = plt.subplots(3, 4, sharey="row", sharex="row")
for i,case in enumerate(['UUN', 'NUN', 'UAN', 'NAN']):
    
    axs[0,i].bar(
        np.arange(len(regressions['N1_40'][case]['coeffs'])) - 0.15,
        list(regressions['N1_40'][case]['coeffs'].values()),
        0.3
        )
    axs[0,i].bar(
        np.arange(len(regressions['N1_2-150'][case]['coeffs'])) + 0.15,
        list(regressions['N1_2-150'][case]['coeffs'].values()),
        0.3
        )

    rng = np.array([
        min([n[case].mean_head_length for n in nets['N1_40']]),
        max([n[case].mean_head_length for n in nets['N1_40']])
        ])
    axs[1,i].plot(
        rng/1.e3,
        rng*regressions['N1_40'][case]['grads']['<L_I>']/1.e3,
        "k--"
        )
    axs[1,i].plot(
        [n[case].mean_head_length/1.e3 for n in nets['N1_40']],
        np.array(regressions['N1_40'][case]['eff_lengths'])/1.e3,
        "o",
        alpha=0.2
        )
        
    rng = np.array([
        min([n[case].mean_head_length for n in nets['N1_2-150']]),
        max([n[case].mean_head_length for n in nets['N1_2-150']])
        ])
    axs[2,i].plot(
        rng/1.e3,
        rng*regressions['N1_2-150'][case]['grads']['<L_I>']/1.e3,
        "k--"
        )
    axs[2,i].scatter(
        [n[case].mean_head_length/1.e3 for n in nets['N1_2-150']],
        np.array(regressions['N1_2-150'][case]['eff_lengths'])/1.e3,
        c = [len(n[case].list_of_channel_head_segment_IDs)
            for n in nets['N1_2-150']],
        alpha=0.2
        )

axs[0,0].set_ylabel(r'Correlation coefficient, $r$')
axs[0,0].set_xticks(
    np.arange(len(regressions['N1_40'][case]['coeffs'])),
    labels.values()
    )
    
axs[1,0].set_ylabel(r'Effective length, $\widehat{L}$ [km]')
axs[2,0].set_ylabel(r'Effective length, $\widehat{L}$ [km]')
for ax in axs[2,:]:
    ax.set_xlabel(r'Mean length, $\langle L \rangle$ [km]')
    
for row in axs:
    for ax in row:
        ax.set_box_aspect(1)

plt.show()

# ---- Plot S5 & S6

for N1 in indirs.keys():

    fig, axs = plt.subplots(4, 13, sharey=True, sharex="col")
    for i,case in enumerate(['UUN', 'NUN', 'UAN', 'NAN']):
        

        axs[i,0].scatter(
            [n[case].bifurcation_ratio for n in nets[N1]],
            np.array(regressions[N1][case]['eff_lengths'])/1.e3,
            c = [len(n[case].list_of_channel_head_segment_IDs)
                    for n in nets[N1]],
            alpha=0.2
            )
        if i==3:
            axs[i,0].set_xlabel(r'$R_B$')

        axs[i,1].scatter(
            [n[case].length_ratio for n in nets[N1]],
            np.array(regressions[N1][case]['eff_lengths'])/1.e3,
            c = [len(n[case].list_of_channel_head_segment_IDs)
                    for n in nets[N1]],
            alpha=0.2
            )
        if i==3:
            axs[i,1].set_xlabel(r'$R_L$')
        
        axs[i,2].scatter(
            [n[case].discharge_ratio for n in nets[N1]],
            np.array(regressions[N1][case]['eff_lengths'])/1.e3,
            c = [len(n[case].list_of_channel_head_segment_IDs)
                    for n in nets[N1]],
            alpha=0.2
            )
        if i==3:
            axs[i,2].set_xlabel(r'$R_Q$')
        
        axs[i,3].scatter(
            [n[case].tokunaga['K_mean'] for n in nets[N1]],
            np.array(regressions[N1][case]['eff_lengths'])/1.e3,
            c = [len(n[case].list_of_channel_head_segment_IDs)
                    for n in nets[N1]],
            alpha=0.2
            )
        if i==3:
            axs[i,3].set_xlabel(r'$K$')

        axs[i,4].scatter(
            [net[case].max_topological_length for net in nets[N1]],
            np.array(regressions[N1][case]['eff_lengths'])/1.e3,
            c = [len(n[case].list_of_channel_head_segment_IDs)
                    for n in nets[N1]],
            alpha=0.2
            )
        if i==3:
            axs[i,4].set_xlabel(r'$l$')

        axs[i,5].scatter(
            [net[case].mean_topological_length for net in nets[N1]],
            np.array(regressions[N1][case]['eff_lengths'])/1.e3,
            c = [len(n[case].list_of_channel_head_segment_IDs)
                    for n in nets[N1]],
            alpha=0.2
            )
        if i==3:
            axs[i,5].set_xlabel(r'$\langle l \rangle$')
            
        axs[i,6].scatter(
            [net[case].mean_head_topological_length for net in nets[N1]],
            np.array(regressions[N1][case]['eff_lengths'])/1.e3,
            c = [len(n[case].list_of_channel_head_segment_IDs)
                    for n in nets[N1]],
            alpha=0.2
            )
        if i==3:
            axs[i,6].set_xlabel(r'$\langle l_I \rangle$')

        axs[i,7].scatter(
            [n[case].list_of_LongProfile_objects[0].x.max()/1.e3
                for n in nets[N1]],
            np.array(regressions[N1][case]['eff_lengths'])/1.e3,
            c = [len(n[case].list_of_channel_head_segment_IDs)
                    for n in nets[N1]],
            alpha=0.2
            )
        if i==3:
            axs[i,7].set_xlabel(r'$L$')
            
        axs[i,8].scatter(
            [net[case].mean_length/1.e3 for net in nets[N1]],
            np.array(regressions[N1][case]['eff_lengths'])/1.e3,
            c = [len(n[case].list_of_channel_head_segment_IDs)
                    for n in nets[N1]],
            alpha=0.2
            )
        if i==3:
            axs[i,8].set_xlabel(r'$\langle L \rangle$')

        axs[i,9].scatter(
            [net[case].mean_head_length/1.e3 for net in nets[N1]],
            np.array(regressions[N1][case]['eff_lengths'])/1.e3,
            c = [len(n[case].list_of_channel_head_segment_IDs)
                    for n in nets[N1]],
            alpha=0.2
            )
        if i==3:
            axs[i,9].set_xlabel(r'$\langle L_I \rangle$')
            
        axs[i,10].scatter(
            [net[case].max_topological_width for net in nets[N1]],
            np.array(regressions[N1][case]['eff_lengths'])/1.e3,
            c = [len(n[case].list_of_channel_head_segment_IDs)
                    for n in nets[N1]],
            alpha=0.2
            )
        if i==3:
            axs[i,10].set_xlabel(r'$w$')

        axs[i,11].scatter(
            [net[case].mean_topological_width for net in nets[N1]],
            np.array(regressions[N1][case]['eff_lengths'])/1.e3,
            c = [len(n[case].list_of_channel_head_segment_IDs)
                    for n in nets[N1]],
            alpha=0.2
            )
        if i==3:
            axs[i,11].set_xlabel(r'$\langle w \rangle$')
            
        axs[i,12].scatter(
            [h[case]['p'] for h in hacks[N1]],
            np.array(regressions[N1][case]['eff_lengths'])/1.e3,
            c = [len(n[case].list_of_channel_head_segment_IDs)
                    for n in nets[N1]],
            alpha=0.2
            )
        if i==3:
            axs[i,12].set_xlabel(r'$p$')


    for row in axs:
        for i,ax in enumerate(row):
            ax.set_box_aspect(1)
            if i==0:
                ax.set_ylabel(r'$\widehat{L}$ [km]')

    plt.show()

# ---- save

if output_gmt:

    basedir = "../../Output/Network/Figure_S18_S19_S20_Network_Effective_Length_Controls_Non-Uniform_Width/"
        
    for N1 in indirs.keys():
        for case in ['UUN', 'NUN', 'UAN', 'NAN']:
        
            with open(basedir + N1 + "_" + case + ".dat", "wb") as f:
                arr = np.column_stack((
                    np.array(regressions[N1][case]['eff_lengths'])/1.e3,
                    [n[case].bifurcation_ratio for n in nets[N1]],
                    [n[case].length_ratio for n in nets[N1]],
                    [n[case].discharge_ratio for n in nets[N1]],
                    [n[case].tokunaga['K_mean'] for n in nets[N1]],
                    [n[case].max_topological_length for n in nets[N1]],
                    [n[case].mean_topological_length for n in nets[N1]],
                    [n[case].mean_head_topological_length for n in nets[N1]],
                    [n[case].list_of_LongProfile_objects[0].x.max()/1.e3
                        for n in nets[N1]],
                    [n[case].mean_length/1.e3 for n in nets[N1]],
                    [n[case].mean_head_length/1.e3 for n in nets[N1]],
                    [n[case].max_topological_width for n in nets[N1]],
                    [n[case].mean_topological_width for n in nets[N1]],
                    [h[case]['p'] for h in hacks[N1]],
                    [len(n[case].streams_by_order[1]) for n in nets[N1]]
                    ))
                np.savetxt(f, arr)
                
            with open(basedir + N1 + "_" + case + "_corr.dat", "wb") as f:
                arr = np.column_stack((
                    np.arange(len(regressions[N1][case]['coeffs'])),
                    list(regressions[N1][case]['coeffs'].values())
                    ))
                np.savetxt(f, arr)
            
            rng = np.array([
                min([n[case].mean_head_length for n in nets[N1]]),
                max([n[case].mean_head_length for n in nets[N1]])
                ])
            with open(basedir + N1 + "_" + case + "_fit.dat", "wb") as f:
                arr = np.column_stack((
                    rng/1.e3,
                    rng*regressions[N1][case]['grads']['<L_I>']/1.e3
                    ))
                np.savetxt(f, arr)
                
            with open(basedir + N1 + "_" + case + "_grad.dat", "wb") as f:
                np.savetxt(f, [regressions[N1][case]['grads']['<L_I>']])
