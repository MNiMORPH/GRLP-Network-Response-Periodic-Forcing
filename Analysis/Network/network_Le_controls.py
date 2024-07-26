import numpy as np
import matplotlib.pyplot as plt
# import scipy.stats as sts
from copy import deepcopy


import grlp
import grlp_extras as grlpx

output_gmt = False


def tokunaga(net):

    # Count numbers of streams of order i that join streams of order j
    N = np.zeros(( net.orders[-1]-1, net.orders[-1] ))
    for i in net.orders[:-1]:
        for stream in net.streams_by_order[i]:
            for ID in stream:
                downID = net.list_of_LongProfile_objects[ID].downstream_segment_IDs[0]
                if downID not in stream:
                    adjacentID = [id for id in net.list_of_LongProfile_objects[downID].upstream_segment_IDs if id != ID][0]
                    adjacent_order = net.segment_orders[adjacentID]+1
                    N[i-1,adjacent_order-1] += 1

    # Get averages by dividing by number of streams j
    T = np.zeros(( net.orders[-1]-1, net.orders[-1]-1 ))
    for i in net.orders[1:]:
        T[:i-1,i-2] = N[:i-1,i-1] / net.order_counts[i]

    # Tokunaga's e_k - Average number of streams i flowing into streams of i+k
    e_k = np.zeros(max(net.orders)-1)
    for k in range(1,max(net.orders)):
        e_k[k-1] = T.diagonal(k-1).mean()

    # Ratios of e_k / e_k-1
    K = e_k[1:]/e_k[:-1]
    
    k = [k for k in range(1,max(net.orders))]
    
    return np.array(k), e_k, K
    
    


indirs = {
    "m40_no_int": "../output/network/m40_fix_seg_length_no_internal/",
    "m40_w_int": "../output/network/m40_fix_seg_length_w_internal/",
    "m40_rnd_no_int": "../output/network/m40_rnd_seg_length_no_internal/",
    "m40_rnd_w_int": "../output/network/m40_rnd_seg_length_w_internal/",
    "m2-100_no_int": "../output/network/m2-100_fix_seg_length_no_internal/",
    "m2-100_w_int": "../output/network/m2-100_fix_seg_length_w_internal/",
    "m2-100_rnd_no_int": "../output/network/m2-100_rnd_seg_length_no_internal/",
    "m2-100_rnd_w_int": "../output/network/m2-100_rnd_seg_length_w_internal/",
    "m100-150_no_int": "../output/network/m100-150_fix_seg_length_no_internal/",
    "m100-150_w_int": "../output/network/m100-150_fix_seg_length_w_internal/",
    "m100-150_rnd_no_int": "../output/network/m100-150_rnd_seg_length_no_internal/",
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
    "m100-150_rnd_w_int_var_width": "../output/network/m100-150_rnd_seg_length_w_internal_var_width/"
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
for i,sweep in enumerate(indirs.keys()):
    ls = []
    for j in range(len(gains[sweep])):
        diffs = []
        ls.append( np.sqrt(gains[sweep][j]['Teq_Qs']*nets[sweep][i].mean_diffusivity) )
    eff_lengths[sweep] = ls
    
# ---- Tokunaga
tokunagas = {}
for i,sweep in enumerate(indirs.keys()):
    ls = []
    for j in range(len(nets[sweep])):
        k, e_k, K = tokunaga(nets[sweep][j])
        ls.append(K[:-1].mean())
        # ls.append(e_k[0])
    tokunagas[sweep] = ls


# ---- Plot

sweep_grps = {
    "m40_no_int": ["m40_no_int"],
    "m40_w_int": ["m40_w_int"],
    "m40_rnd_no_int": ["m40_rnd_no_int"],
    "m40_rnd_w_int": ["m40_rnd_w_int"],
    "m2-150_no_int": ["m2-100_no_int", "m100-150_no_int"],
    "m2-150_w_int": ["m2-100_w_int", "m100-150_w_int"],
    "m2-150_rnd_no_int": ["m2-100_rnd_no_int", "m100-150_rnd_no_int"],
    "m2-150_rnd_w_int": ["m2-100_rnd_w_int", "m100-150_rnd_w_int"],
    "m40_no_int_var_width": ["m40_no_int_var_width"],
    "m40_w_int_var_width": ["m40_w_int_var_width"],
    "m40_rnd_no_int_var_width": ["m40_rnd_no_int_var_width"],
    "m40_rnd_w_int_var_width": ["m40_rnd_w_int_var_width"],
    "m2-150_no_int_var_width": ["m2-100_no_int_var_width", "m100-150_no_int_var_width"],
    "m2-150_w_int_var_width": ["m2-100_w_int_var_width"],
    "m2-150_rnd_no_int_var_width": ["m2-100_rnd_no_int_var_width"],
    "m2-150_rnd_w_int_var_width": ["m2-100_rnd_w_int_var_width", "m100-150_rnd_w_int_var_width"],
    }

# fig, axs = plt.subplots(max(2,len(sweep_grps.keys())),7,sharey=True,sharex="col")
# for i,grp in enumerate(sweep_grps.keys()):
#     for sweep in sweep_grps[grp]:
#         mags = [len(n.streams_by_order[1]) for n in nets[sweep]]
#         axs[i,0].scatter(
#             [n.bifurcation_ratio for n in nets[sweep]],
#             eff_lengths[sweep],
#             c=mags
#             )
#         axs[i,1].scatter(
#             [n.length_ratio for n in nets[sweep]],
#             eff_lengths[sweep],
#             c=mags
#             )
#         axs[i,2].scatter(
#             [n.discharge_ratio for n in nets[sweep]],
#             eff_lengths[sweep],
#             c=mags
#             )
#         axs[i,3].scatter(
#             [1./h['p'] for h in hacks[sweep]],
#             eff_lengths[sweep],
#             c=mags
#             )
#         axs[i,4].scatter(
#             [e_k for e_k in tokunagas[sweep]],
#             eff_lengths[sweep],
#             c=mags
#             )
# 
#         eff_length = np.array(eff_lengths[sweep])
#         L_mean = np.array([n.mean_downstream_distance for n in nets[sweep]])
#         grad = L_mean.dot(eff_length) / L_mean.dot(L_mean)
#         axs[i,5].scatter(
#             [n.mean_downstream_distance for n in nets[sweep]],
#             eff_lengths[sweep],
#             c=mags
#             )
#         axs[i,5].plot(
#             [L_mean.min(), L_mean.max()],
#             [L_mean.min()*grad, L_mean.max()*grad],
#             "--"
#             )
# 
#         L_median = np.array([n.mean_downstream_distance for n in nets[sweep]])
#         grad = L_median.dot(eff_length) / L_median.dot(L_mean)
#         axs[i,6].scatter(
#             [n.median_downstream_distance for n in nets[sweep]],
#             eff_lengths[sweep],
#             c=mags
#             )
#         axs[i,6].plot(
#             [L_median.min(), L_median.max()],
#             [L_median.min()*grad, L_median.max()*grad],
#             "--"
#             )
# 
# plt.show()
    
# ---- Plot2

grp_corrs = {}
grp_L_mean_grad = {}

for i,grp in enumerate(sweep_grps.keys()):
    
    corrs = []
    
    corrs.append(
        np.corrcoef(
            [h['p'] for sweep in sweep_grps[grp] for h in hacks[sweep]],
            [eff_length for sweep in sweep_grps[grp] for eff_length in eff_lengths[sweep]]
            )[0,1]
        )
    corrs.append(
        np.corrcoef(
            [n.bifurcation_ratio for sweep in sweep_grps[grp] for n in nets[sweep]],
            [eff_length for sweep in sweep_grps[grp] for eff_length in eff_lengths[sweep]]
            )[0,1]
        )
    corrs.append(
        np.corrcoef(
            [n.length_ratio for sweep in sweep_grps[grp] for n in nets[sweep]],
            [eff_length for sweep in sweep_grps[grp] for eff_length in eff_lengths[sweep]]
            )[0,1]
        )
    corrs.append(
        np.corrcoef(
            [n.discharge_ratio for sweep in sweep_grps[grp] for n in nets[sweep]],
            [eff_length for sweep in sweep_grps[grp] for eff_length in eff_lengths[sweep]]
            )[0,1]
        )
    
    Ks = np.array([K for sweep in sweep_grps[grp] for K in tokunagas[sweep]])
    nonnan = np.where(np.isfinite(Ks))[0]
    corrs.append(
        np.corrcoef(
            Ks[nonnan],
            np.array([eff_length for sweep in sweep_grps[grp] for eff_length in eff_lengths[sweep]])[nonnan]
            )[0,1]
        )
        
    eff_length = np.array([eff_length for sweep in sweep_grps[grp] for eff_length in eff_lengths[sweep]])
    L_mean = np.array([n.mean_downstream_distance for sweep in sweep_grps[grp] for n in nets[sweep]])
    where = np.where(np.array([len(n.streams_by_order[1]) for sweep in sweep_grps[grp] for n in nets[sweep]]) >= 40)
    grad = L_mean[where].dot(eff_length[where]) / L_mean[where].dot(L_mean[where])
    corrs.append(
        np.corrcoef(
            [n.mean_downstream_distance for sweep in sweep_grps[grp] for n in nets[sweep]],
            [eff_length for sweep in sweep_grps[grp] for eff_length in eff_lengths[sweep]]
            )[0,1]
        )
    grp_L_mean_grad[grp] = {
        'grad': grad,
        'L_mean': [L_mean[where].min()/1.e3, L_mean[where].max()/1.e3],
        'eff_length': [L_mean[where].min()*grad/1.e3, L_mean[where].max()*grad/1.e3]
    }

    eff_length = np.array([eff_length for sweep in sweep_grps[grp] for eff_length in eff_lengths[sweep]])
    L_median = np.array([n.median_downstream_distance for sweep in sweep_grps[grp] for n in nets[sweep]])
    where = np.where(np.array([len(n.streams_by_order[1]) for sweep in sweep_grps[grp] for n in nets[sweep]]) >= 40)
    grad = L_median[where].dot(eff_length[where]) / L_median[where].dot(L_median[where])
    corrs.append(
        np.corrcoef(
            [n.median_downstream_distance for sweep in sweep_grps[grp] for n in nets[sweep]],
            [eff_length for sweep in sweep_grps[grp] for eff_length in eff_lengths[sweep]]
            )[0,1]
        )
        
    grp_corrs[grp] = corrs
    plt.plot(corrs, "o")
    
plt.show()

# ---- save

if output_gmt:

    basedir = "../output/network/controls/"
    outfiles = {
        "m40_no_int": "m40_fix_seg_length_no_internal.dat",
        "m40_w_int": "m40_fix_seg_length_w_internal.dat",
        "m40_rnd_no_int": "m40_rnd_seg_length_no_internal.dat",
        "m40_rnd_w_int": "m40_rnd_seg_length_w_internal.dat",
        "m2-150_no_int": "m2-150_fix_seg_length_no_internal.dat",
        "m2-150_w_int": "m2-150_fix_seg_length_w_internal.dat",
        "m2-150_rnd_no_int": "m2-150_rnd_seg_length_no_internal.dat",
        "m2-150_rnd_w_int": "m2-150_rnd_seg_length_w_internal.dat",
        "m40_no_int_var_width": "m40_fix_seg_length_no_internal_var_width.dat",
        "m40_w_int_var_width": "m40_fix_seg_length_w_internal_var_width.dat",
        "m40_rnd_no_int_var_width": "m40_rnd_seg_length_no_internal_var_width.dat",
        "m40_rnd_w_int_var_width": "m40_rnd_seg_length_w_internal_var_width.dat",
        "m2-150_no_int_var_width": "m2-150_fix_seg_length_no_internal_var_width.dat",
        "m2-150_w_int_var_width": "m2-150_fix_seg_length_w_internal_var_width.dat",
        "m2-150_rnd_no_int_var_width": "m2-150_rnd_seg_length_no_internal_var_width.dat",
        "m2-150_rnd_w_int_var_width": "m2-150_rnd_seg_length_w_internal_var_width.dat"
        }
    corr_outfiles = {
        "m40_no_int": "corr_m40_fix_seg_length_no_internal.dat",
        "m40_w_int": "corr_m40_fix_seg_length_w_internal.dat",
        "m40_rnd_no_int": "corr_m40_rnd_seg_length_no_internal.dat",
        "m40_rnd_w_int": "corr_m40_rnd_seg_length_w_internal.dat",
        "m2-150_no_int": "corr_m2-150_fix_seg_length_no_internal.dat",
        "m2-150_w_int": "corr_m2-150_fix_seg_length_w_internal.dat",
        "m2-150_rnd_no_int": "corr_m2-150_rnd_seg_length_no_internal.dat",
        "m2-150_rnd_w_int": "corr_m2-150_rnd_seg_length_w_internal.dat",
        "m40_no_int_var_width": "corr_m40_fix_seg_length_no_internal_var_width.dat",
        "m40_w_int_var_width": "corr_m40_fix_seg_length_w_internal_var_width.dat",
        "m40_rnd_no_int_var_width": "corr_m40_rnd_seg_length_no_internal_var_width.dat",
        "m40_rnd_w_int_var_width": "corr_m40_rnd_seg_length_w_internal_var_width.dat",
        "m2-150_no_int_var_width": "corr_m2-150_fix_seg_length_no_internal_var_width.dat",
        "m2-150_w_int_var_width": "corr_m2-150_fix_seg_length_w_internal_var_width.dat",
        "m2-150_rnd_no_int_var_width": "corr_m2-150_rnd_seg_length_no_internal_var_width.dat",
        "m2-150_rnd_w_int_var_width": "corr_m2-150_rnd_seg_length_w_internal_var_width.dat"
        }
        
    fit_outfiles = {
        "m40_no_int": "fit_m40_fix_seg_length_no_internal.dat",
        "m40_w_int": "fit_m40_fix_seg_length_w_internal.dat",
        "m40_rnd_no_int": "fit_m40_rnd_seg_length_no_internal.dat",
        "m40_rnd_w_int": "fit_m40_rnd_seg_length_w_internal.dat",
        "m2-150_no_int": "fit_m2-150_fix_seg_length_no_internal.dat",
        "m2-150_w_int": "fit_m2-150_fix_seg_length_w_internal.dat",
        "m2-150_rnd_no_int": "fit_m2-150_rnd_seg_length_no_internal.dat",
        "m2-150_rnd_w_int": "fit_m2-150_rnd_seg_length_w_internal.dat",
        "m40_no_int_var_width": "fit_m40_fix_seg_length_no_internal_var_width.dat",
        "m40_w_int_var_width": "fit_m40_fix_seg_length_w_internal_var_width.dat",
        "m40_rnd_no_int_var_width": "fit_m40_rnd_seg_length_no_internal_var_width.dat",
        "m40_rnd_w_int_var_width": "fit_m40_rnd_seg_length_w_internal_var_width.dat",
        "m2-150_no_int_var_width": "fit_m2-150_fix_seg_length_no_internal_var_width.dat",
        "m2-150_w_int_var_width": "fit_m2-150_fix_seg_length_w_internal_var_width.dat",
        "m2-150_rnd_no_int_var_width": "fit_m2-150_rnd_seg_length_no_internal_var_width.dat",
        "m2-150_rnd_w_int_var_width": "fit_m2-150_rnd_seg_length_w_internal_var_width.dat"
        }
        
    for i,grp in enumerate(sweep_grps.keys()):
        
        with open(basedir + outfiles[grp], "wb") as f:
            arr = np.column_stack((
                [n.bifurcation_ratio for sweep in sweep_grps[grp] for n in nets[sweep]],
                [n.length_ratio for sweep in sweep_grps[grp] for n in nets[sweep]],
                [n.discharge_ratio for sweep in sweep_grps[grp] for n in nets[sweep]],
                [1./h['p'] for sweep in sweep_grps[grp] for h in hacks[sweep]],
                [n.mean_downstream_distance/1.e3 for sweep in sweep_grps[grp] for n in nets[sweep]],
                [n.median_downstream_distance/1.e3 for sweep in sweep_grps[grp] for n in nets[sweep]],
                np.array([eff_length for sweep in sweep_grps[grp] for eff_length in eff_lengths[sweep]])/1.e3,
                [len(n.streams_by_order[1]) for sweep in sweep_grps[grp] for n in nets[sweep]]
                ))
            np.savetxt(f, arr)
            
        with open(basedir + corr_outfiles[grp], "wb") as f:
            arr = np.column_stack((
                np.arange(len(grp_corrs[grp])),
                grp_corrs[grp]
                ))
            np.savetxt(f, arr)
        
        with open(basedir + fit_outfiles[grp], "wb") as f:
            arr = np.column_stack((
                grp_L_mean_grad[grp]['L_mean'],
                grp_L_mean_grad[grp]['eff_length']
                ))
            np.savetxt(f, arr)    
        