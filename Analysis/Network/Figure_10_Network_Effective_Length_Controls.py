"""
This script performs the analysis presented in Figure 10 of McNab et al. (2024,
EGUsphere); produces a rough version of the Figure; and, optionally, generates
output files for plotting the final Figure in GMT.

The purpose of the script/figure is to .
"""


# ---- Define functions
def compute_origin_gradient(x, y):
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


# ---- Regressions
regressions = {'N1_40': {}, 'N1_2-102': {}}

for N1 in indirs.keys():
    regressions[N1] = {'UUU': {}, 'NUU': {}, 'UAU': {}, 'NAU': {}}

    for case in ['UUU', 'NUU', 'UAU', 'NAU']:
        
        regressions[N1][case]['eff_lengths'] = np.sqrt([
                g[case]['Teq']*nets[N1][i][case].mean_diffusivity
                for i,g in enumerate(gains[N1])
                ])
            
        regressions[N1][case]['coeffs'] = {}
        regressions[N1][case]['grads'] = {}
        
        regressions[N1][case]['coeffs']['p'] = np.corrcoef(
            [h[case]['p'] for h in hacks[N1]],
            regressions[N1][case]['eff_lengths']
            )[0,1]
        regressions[N1][case]['grads']['p'] = compute_origin_gradient(
            [h[case]['p'] for h in hacks[N1]],
            regressions[N1][case]['eff_lengths']
            )

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
        
        Ks = np.array([n[case].tokunaga['K_mean'] for n in nets[N1]])
        non_nans = np.where(~np.isnan(Ks))
        regressions[N1][case]['coeffs']['K'] = np.corrcoef(
            Ks[non_nans],
            regressions[N1][case]['eff_lengths'][non_nans]
            )[0,1]
        regressions[N1][case]['grads']['K'] = compute_origin_gradient(
            Ks[non_nans],
            regressions[N1][case]['eff_lengths'][non_nans]
            )
            
        regressions[N1][case]['coeffs']['<L>'] = np.corrcoef(
            [n[case].mean_downstream_distance for n in nets[N1]],
            regressions[N1][case]['eff_lengths']
            )[0,1]
        regressions[N1][case]['grads']['<L>'] = compute_origin_gradient(
            [n[case].mean_downstream_distance for n in nets[N1]],
            regressions[N1][case]['eff_lengths']
            )
        
        regressions[N1][case]['coeffs']['<L>_50'] = np.corrcoef(
            [n[case].median_downstream_distance for n in nets[N1]],
            regressions[N1][case]['eff_lengths']
            )[0,1]
        regressions[N1][case]['grads']['<L>_50'] = compute_origin_gradient(
            [n[case].median_downstream_distance for n in nets[N1]],
            regressions[N1][case]['eff_lengths']
            )

# ---- Labels
labels = {
    'p': r'$p_{x,Q}$',
    'R_B': r'$R_B$',
    'R_L': r'$R_L$',
    'R_Q': r'$R_Q$',
    'K': r'$K$',
    '<L>': r'$\langle L \rangle$',
    '<L>_50': r'$\langle L \rangle_{50}$'
    }


# ---- Plot
fig, axs = plt.subplots(3, 4, sharey="row", sharex="row")
for i,case in enumerate(['UUU', 'NUU', 'UAU', 'NAU']):
    
    axs[0,i].bar(
        np.arange(len(regressions['N1_40'][case]['coeffs'])) - 0.15,
        list(regressions['N1_40'][case]['coeffs'].values()),
        0.3
        )
    axs[0,i].bar(
        np.arange(len(regressions['N1_2-102'][case]['coeffs'])) + 0.15,
        list(regressions['N1_2-102'][case]['coeffs'].values()),
        0.3
        )

    rng = np.array([
        min([n[case].mean_downstream_distance for n in nets['N1_40']]),
        max([n[case].mean_downstream_distance for n in nets['N1_40']])
        ])
    axs[1,i].plot(rng/1.e3, rng*regressions['N1_40'][case]['grads']['<L>']/1.e3, "k--")
    axs[1,i].plot(
        [n[case].mean_downstream_distance/1.e3 for n in nets['N1_40']],
        np.array(regressions['N1_40'][case]['eff_lengths'])/1.e3,
        "o",
        alpha=0.2
        )
        
    rng = np.array([
        min([n[case].mean_downstream_distance for n in nets['N1_2-102']]),
        max([n[case].mean_downstream_distance for n in nets['N1_2-102']])
        ])
    axs[2,i].plot(rng/1.e3, rng*regressions['N1_2-102'][case]['grads']['<L>']/1.e3, "k--")
    axs[2,i].plot(
        [n[case].mean_downstream_distance/1.e3 for n in nets['N1_2-102']],
        np.array(regressions['N1_2-102'][case]['eff_lengths'])/1.e3,
        "o",
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


# ---- Plot S5

fig, axs = plt.subplots(6, 4, sharey="row", sharex="row")
for i,case in enumerate(['UUU', 'NUU', 'UAU', 'NAU']):
    
    axs[0,i].plot(
        [h[case]['p'] for h in hacks],
        np.array(regressions[case]['eff_lengths'])/1.e3,
        "o",
        alpha=0.2
        )
    axs[0,i].set_xlabel(r'$p_{x,Q}$')

    axs[1,i].plot(
        [n[case].bifurcation_ratio for n in nets],
        np.array(regressions[case]['eff_lengths'])/1.e3,
        "o",
        alpha=0.2
        )
    axs[1,i].set_xlabel(r'$R_B$')

    axs[2,i].plot(
        [n[case].length_ratio for n in nets],
        np.array(regressions[case]['eff_lengths'])/1.e3,
        "o",
        alpha=0.2
        )
    axs[2,i].set_xlabel(r'$R_L$')
    
    axs[3,i].plot(
        [n[case].discharge_ratio for n in nets],
        np.array(regressions[case]['eff_lengths'])/1.e3,
        "o",
        alpha=0.2
        )
    axs[3,i].set_xlabel(r'$R_Q$')
    
    axs[4,i].plot(
        [n[case].tokunaga['K_mean'] for n in nets],
        np.array(regressions[case]['eff_lengths'])/1.e3,
        "o",
        alpha=0.2
        )
    axs[4,i].set_xlabel(r'$K$')

    axs[5,i].plot(
        [n[case].median_downstream_distance/1.e3 for n in nets],
        np.array(regressions[case]['eff_lengths'])/1.e3,
        "o",
        alpha=0.2
        )
    axs[5,i].set_xlabel(r'$\langle L \rangle_{50}$')

    
for row in axs:
    for i,ax in enumerate(row):
        ax.set_box_aspect(1)
        if i==0:
            ax.set_ylabel(r'$\widehat{L}$ [km]')

plt.show()

# ---- save

if output_gmt:

    basedir = "../../Output/Network/Figure_10_Network_Effective_Length_Controls/"
        
    for N1 in indirs.keys():
        for case in ['UUU', 'NUU', 'UAU', 'NAU']:
        
            with open(basedir + N1 + "_" + case + ".dat", "wb") as f:
                arr = np.column_stack((
                    [n[case].bifurcation_ratio for n in nets[N1]],
                    [n[case].length_ratio for n in nets[N1]],
                    [n[case].discharge_ratio for n in nets[N1]],
                    [h[case]['p'] for h in hacks[N1]],
                    [n[case].mean_downstream_distance/1.e3 for n in nets[N1]],
                    [n[case].median_downstream_distance/1.e3 for n in nets[N1]],
                    np.array(regressions[N1][case]['eff_lengths'])/1.e3,
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
                min([n[case].mean_downstream_distance for n in nets[N1]]),
                max([n[case].mean_downstream_distance for n in nets[N1]])
                ])
            with open(basedir + N1 + "_" + case + "_fit.dat", "wb") as f:
                arr = np.column_stack((
                    rng/1.e3,
                    rng*regressions[N1][case]['grads']['<L>']/1.e3
                    ))
                np.savetxt(f, arr)