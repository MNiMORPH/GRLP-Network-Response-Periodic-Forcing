from grlp import *
from grlp_extras import *
from scipy.stats import binned_statistic

indirs = {
    "m40": "./glic/output_081123/",
    "m2-100": "./glic/output_101123/",
    "m40_w_int": "../output/network/m40_fix_seg_length_w_internal/",
    "m2-100_w_int": "../output/network/m2-100_fix_seg_length_w_internal/",
    "m40_var_no_int": "../output/network/m40_rnd_seg_length_no_internal/",
    "m40_var": "../output/network/m40_rnd_seg_length/",
    "m2-100_var": "../output/network/m2-100_rnd_seg_length/"
    }
nets = {}
hacks = {}
gains = {}
for sweep in indirs.keys():
    sweep_nets, sweep_hacks, sweep_gains, sweep_lags = read_sweep(indirs[sweep])
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
        for seg in nets[sweep][j].list_of_LongProfile_objects:
            seg.compute_diffusivity()
            diffs.append(seg.diffusivity)
        if i in [0, 1, 5, 6]:
            ls.append( np.sqrt(3*gains[sweep][j]['Teq_Qs']*np.mean(np.hstack(diffs))) )
        else:
            ls.append( np.sqrt(gains[sweep][j]['Teq_Qs']*np.mean(np.hstack(diffs))) )
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
fig, axs = plt.subplots(1,4,sharex=True,sharey=True)
for i,sweep in enumerate(indirs.keys()):
    if i==0 or i==1:
        j=0
    elif i==2 or i==3:
        j=1
    elif i==4:
        j=2
    else:
        j=3

    axs[j].scatter(
        magnitudes[sweep],
        np.array(eff_lengths[sweep])/np.array(mean_lengths[sweep]),
        alpha=0.1
        )
    axs[j].scatter(
        binned_eff_lengths[sweep]['mag'],
        binned_eff_lengths[sweep]['Le'],
        marker="+"
        )
        
plt.show()

# # ---- Save
# 
# basedir = "../output/network/magnitude/"
# 
# fixed_length_sweeps = ["m20", "m40", "m2-100"]
# variable_length_sweeps = ["m40_var", "m2-100_var"]
# 
# with open(basedir + "fixed_segment_lengths.dat", "wb") as f:
#     for sweep in fixed_length_sweeps:
#         arr = np.column_stack((
#             magnitudes[sweep],
#             np.array(eff_lengths[sweep])/np.array(mean_lengths[sweep]),
#             magnitudes[sweep] ))
#         np.savetxt(f, arr)
# 
# with open(basedir + "variable_segment_lengths.dat", "wb") as f:
#     for sweep in variable_length_sweeps:
#         arr = np.column_stack((
#             magnitudes[sweep],
#             np.array(eff_lengths[sweep])/np.array(mean_lengths[sweep]),
#             magnitudes[sweep] ))
#         np.savetxt(f, arr)
