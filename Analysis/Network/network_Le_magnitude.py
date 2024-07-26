import numpy as np
import matplotlib.pyplot as plt
# import scipy.stats as sts
from scipy.stats import binned_statistic
from copy import deepcopy

import grlp
import grlp_extras as grlpx

indirs = {
    "m40_no_int": "../output/network/m40_fix_seg_length_no_internal/",
    "m2-100_no_int": "../output/network/m2-100_fix_seg_length_no_internal/",
    "m100-150_no_int": "../output/network/m100-150_fix_seg_length_no_internal/",
    "m40_w_int": "../output/network/m40_fix_seg_length_w_internal/",
    "m2-100_w_int": "../output/network/m2-100_fix_seg_length_w_internal/",
    "m100-150_w_int": "../output/network/m100-150_fix_seg_length_w_internal/",
    "m40_rnd_no_int": "../output/network/m40_rnd_seg_length_no_internal/",
    "m2-100_rnd_no_int": "../output/network/m2-100_rnd_seg_length_no_internal/",
    "m100-150_rnd_no_int": "../output/network/m100-150_rnd_seg_length_no_internal/",
    "m40_rnd_w_int": "../output/network/m40_rnd_seg_length_w_internal/",
    "m2-100_rnd_w_int": "../output/network/m2-100_rnd_seg_length_w_internal/",
    "m100-150_rnd_w_int": "../output/network/m100-150_rnd_seg_length_w_internal/",
    "m40_no_int_var_width": "../output/network/m40_fix_seg_length_no_internal_var_width/",
    "m2-100_no_int_var_width": "../output/network/m2-100_fix_seg_length_no_internal_var_width/",
    "m100-150_no_int_var_width": "../output/network/m100-150_fix_seg_length_no_internal_var_width/",
    "m40_w_int_var_width": "../output/network/m40_fix_seg_length_w_internal_var_width/",
    "m2-100_w_int_var_width": "../output/network/m2-100_fix_seg_length_w_internal_var_width/",
    "m40_rnd_no_int_var_width": "../output/network/m40_rnd_seg_length_no_internal_var_width/",
    "m2-100_rnd_no_int_var_width": "../output/network/m2-100_rnd_seg_length_no_internal_var_width/",
    "m40_rnd_w_int_var_width": "../output/network/m40_rnd_seg_length_w_internal_var_width/",
    "m2-100_rnd_w_int_var_width": "../output/network/m2-100_rnd_seg_length_w_internal_var_width/",
    "m100-150_rnd_w_int_var_width": "../output/network/m100-150_rnd_seg_length_w_internal_var_width/",
    }
nets = {}
hacks = {}
gains = {}
for sweep in indirs.keys():
    sweep_nets, sweep_hacks, sweep_gains, sweep_lags = grlpx.read_sweep(indirs[sweep])
    nets[sweep] = sweep_nets
    hacks[sweep] = sweep_hacks
    gains[sweep] = sweep_gains

# ---- Effective length
eff_lengths = {}
mean_lengths = {}
magnitudes = {}
for i,sweep in enumerate(indirs.keys()):
    ls = []
    for j in range(len(gains[sweep])):
        diffs = []
        ls.append( np.sqrt(gains[sweep][j]['Teq_Qs']*nets[sweep][j].mean_diffusivity) )
    eff_lengths[sweep] = ls
    magnitudes[sweep] = [len(n.streams_by_order[1]) for n in nets[sweep]]
    mean_lengths[sweep] = [n.mean_downstream_distance for n in nets[sweep]]

# ---- Bin lengths
binned_eff_lengths = {}
for i,sweep in enumerate(indirs.keys()):
    binned = binned_statistic(magnitudes[sweep], np.array(eff_lengths[sweep])/np.array(mean_lengths[sweep]))
    binned_eff_lengths[sweep] = {}
    binned_eff_lengths[sweep]['Le'] = binned.statistic
    binned_eff_lengths[sweep]['mag'] = binned.bin_edges[:-1] + (binned.bin_edges[1:] - binned.bin_edges[:-1])/2.

# ---- Plot
sweep_grps = {
    'no_int': ['m40_no_int', 'm2-100_no_int', 'm100-150_no_int'],
    'rnd_no_int': ['m40_rnd_no_int', 'm2-100_rnd_no_int', 'm100-150_rnd_no_int'],
    'w_int': ['m40_w_int', 'm2-100_w_int', 'm100-150_w_int'],
    'rnd_w_int': ['m40_rnd_w_int', 'm2-100_rnd_w_int', 'm100-150_rnd_w_int'],
    'no_int_var_width': ['m40_no_int_var_width', 'm2-100_no_int_var_width', 'm100-150_no_int_var_width'],
    'w_int_var_width': ['m40_w_int_var_width', 'm2-100_w_int_var_width'],
    'rnd_no_int_var_width': ['m40_rnd_no_int_var_width', 'm2-100_rnd_no_int_var_width'],
    'rnd_w_int_var_width': ['m40_rnd_w_int_var_width', 'm2-100_rnd_w_int_var_width', 'm100-150_rnd_w_int_var_width'],
    }
    
grp_results = {}

fig, axs = plt.subplots(2,4,sharex=True,sharey=True)
for i,grp in enumerate(['no_int', 'rnd_no_int', 'w_int', 'rnd_w_int']):
    for k,suff in enumerate(['', '_var_width']):
        
        eff_length = np.array([])
        mags = np.array([])
        for j,sweep in enumerate(sweep_grps[grp+suff]):
            eff_length = np.hstack((
                eff_length,
                np.array(eff_lengths[sweep])/np.array(mean_lengths[sweep])
                ))
            mags = np.hstack(( mags, magnitudes[sweep] ))
        axs[k,i].plot(mags, eff_length, "o", alpha=0.1)
    
        binned = binned_statistic(mags, eff_length)
        binned_mags = binned.bin_edges[:-1] + (binned.bin_edges[1:] - binned.bin_edges[:-1])/2.
        axs[k,i].plot(binned_mags, binned.statistic, "+")
    
        grp_results[grp+suff] = {
            'mag': mags,
            'eff_length': eff_length,
            'binned_mag': binned_mags,
            'binned_eff_length': binned.statistic
            }

plt.show()    
    
# import sys
# sys.exit()

# ---- Save

basedir = "../output/network/magnitude/"

for i,grp in enumerate(grp_results.keys()):
        
        outfile = basedir + grp + "_full.dat"
        with open(outfile, "wb") as f:
            arr = np.column_stack((
                grp_results[grp]['mag'],
                grp_results[grp]['eff_length']
                ))
            np.savetxt(f, arr)

        outfile = basedir + grp + "_bin.dat"
        with open(outfile, "wb") as f:
            arr = np.column_stack((
                grp_results[grp]['binned_mag'],
                grp_results[grp]['binned_eff_length']
                ))
            np.savetxt(f, arr)

for i,sweep in enumerate(indirs.keys()):
    
    outfile = basedir + sweep + "_full.dat"
    with open(outfile, "wb") as f:
        arr = np.column_stack((
            magnitudes[sweep],
            np.array(eff_lengths[sweep])/np.array(mean_lengths[sweep])
            ))
        np.savetxt(f, arr)