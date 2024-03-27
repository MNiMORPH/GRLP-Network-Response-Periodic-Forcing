from grlp import *
from grlp_extras import *


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
    
    

# indirs = {
#     "m40": "./glic/output_081123/",
#     "m2-100": "./glic/output_101123/",
#     "m40_w_int": "../output/network/m40_fix_seg_length_w_internal/",
#     "m2-100_w_int": "../output/network/m2-100_fix_seg_length_w_internal/",
#     "m40_var_no_int": "../output/network/m40_rnd_seg_length_no_internal/",
#     "m40_var": "../output/network/m40_rnd_seg_length/",
#     "m2-100_var": "../output/network/m2-100_rnd_seg_length/"
#     }
indirs = {"m40": "./glic/test/"}
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
        # ls.append(K[:-1].mean())
        ls.append(e_k[0])
    tokunagas[sweep] = ls

# ---- Plot
fig, axs = plt.subplots(max(2,len(indirs.keys())),6,sharey=True,sharex="col")
for i,sweep in enumerate(indirs.keys()):
    mags = [len(n.streams_by_order[1]) for n in nets[sweep]]
    axs[i,0].scatter(
        [n.bifurcation_ratio for n in nets[sweep]],
        eff_lengths[sweep],
        c=mags
        )
    axs[i,1].scatter(
        [n.length_ratio for n in nets[sweep]],
        eff_lengths[sweep],
        c=mags
        )
    axs[i,2].scatter(
        [n.discharge_ratio for n in nets[sweep]],
        eff_lengths[sweep],
        c=mags
        )
    axs[i,3].scatter(
        [1./h['p'] for h in hacks[sweep]],
        eff_lengths[sweep],
        c=mags
        )
    axs[i,4].scatter(
        [e_k for e_k in tokunagas[sweep]],
        eff_lengths[sweep],
        c=mags
        )
    axs[i,5].scatter(
        [n.mean_downstream_distance for n in nets[sweep]],
        eff_lengths[sweep],
        c=mags
        )
plt.show()

import sys
sys.exit()

# ---- save

basedir = "../output/network/controls/"
outfiles = {
    "m20": "m20_fix_seg_length.dat",
    "m40": "m40_fix_seg_length.dat",
    "m2-100": "m2-100_fix_seg_length.dat",
    "m40_var": "m40_rnd_seg_length.dat",
    "m2-100_var": "m2-100_rnd_seg_length.dat"
    }
    
for i,sweep in enumerate(indirs.keys()):
    with open(basedir + outfiles[sweep], "wb") as f:
        arr = np.column_stack((
            [n.bifurcation_ratio for n in nets[sweep]],
            [n.length_ratio for n in nets[sweep]],
            [n.discharge_ratio for n in nets[sweep]],
            [1./h['p'] for h in hacks[sweep]],
            [n.mean_downstream_distance/1.e3 for n in nets[sweep]],
            np.array(eff_lengths[sweep])/1.e3,
            [len(n.streams_by_order[1]) for n in nets[sweep]]
            ))
        np.savetxt(f, arr)