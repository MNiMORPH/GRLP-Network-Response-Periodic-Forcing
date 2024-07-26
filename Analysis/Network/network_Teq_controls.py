import numpy as np
import matplotlib.pyplot as plt

import grlp
import grlp_extras as grlpx


def compute_mean_sqr_downstream_distance(net):
    """
    Return mean distance from source to mouth.
    Added: FM, 03/2021.
    """
    x_max = [net.list_of_LongProfile_objects[i].x[-1] for i in net.IDs if not net.list_of_LongProfile_objects[i].downstream_segment_IDs][0]
    x_arr = np.array([])
    for i in net.list_of_channel_head_segment_IDs:
        x_arr = np.hstack(( x_arr, net.list_of_LongProfile_objects[i].x[0] ))
    # self.mean_downstream_distance = np.sqrt(((x_max - x_arr)**2).mean())
    return np.sqrt(((x_max - x_arr)**2.).mean())



indirs = {
    "m40_no_int": "../output/network/m40_fix_seg_length_no_internal/",
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
    


fit = np.polyfit(
    [n.mean_downstream_distance for n in nets['m40_no_int']],
    eff_lengths['m40_no_int'],
    1
    )

Le = np.linspace(
    45.e3,
    90.e3,
    100
    )


plt.plot(
    [n.mean_downstream_distance/1.e3 for n in nets['m40_no_int']],
    [g['Teq_Qs']/3.15e10 for g in gains['m40_no_int']],
    "o",
    alpha=0.5
    )
plt.plot(Le/1.e3, ((fit[0]*Le)**2.)/nets['m40_no_int'][0].mean_diffusivity/3.15e10, "--")
# plt.xscale("log")
# plt.yscale("log")
# plt.show()

fit2 = np.polyfit(
    [compute_mean_sqr_downstream_distance(n) for n in nets['m40_no_int']],
    eff_lengths['m40_no_int'],
    1
    )
plt.plot(
    [compute_mean_sqr_downstream_distance(n)/1.e3 for n in nets['m40_no_int']],
    [g['Teq_Qs']/3.15e10 for g in gains['m40_no_int']],
    "o",
    alpha=0.5
    )
plt.plot(Le/1.e3, ((fit2[0]*Le + fit2[1])**2.)/nets['m40_no_int'][0].mean_diffusivity/3.15e10, "--")
plt.xscale("log")
plt.yscale("log")
plt.show()


fit3 = np.polyfit(
    np.log10([n.mean_downstream_distance/1.e3 for n in nets['m40_no_int']]),
    np.log10([g['Teq_Qs']/3.15e10 for g in gains['m40_no_int']]),
    1
)

fit4 = np.polyfit(
    np.log10([compute_mean_sqr_downstream_distance(n) for n in nets['m40_no_int']]),
    np.log10([g['Teq_Qs']/3.15e10 for g in gains['m40_no_int']]),
    1
)

import sys
sys.exit()


basedir = "../output/network/Teq_controls/"

with open(basedir + "Teq_vs_Le.txt", "wb") as f:
    arr = np.column_stack((
        [n.mean_downstream_distance/1.e3 for n in nets['m40_no_int']],
        [g['Teq_Qs']/3.15e10 for g in gains['m40_no_int']]))
    np.savetxt(f, arr)
    
with open(basedir + "Teq_vs_Le_fit.txt", "wb") as f:
    arr = np.column_stack((
        Le/1.e3,
        ((fit[0]*Le)**2.)/nets['m40_no_int'][0].mean_diffusivity/3.15e10))
    np.savetxt(f, arr)

for i in range(6):
    net = nets["m40_no_int"][i]
    planform = grlp.plot_network(net, show=False)
    outfile = basedir + "planform_%i.d" % i
    with open(outfile, "wb") as f:
        for j,seg in enumerate(net.list_of_LongProfile_objects):
            hdr = b"> -Z%i\n" % (net.segment_orders[j]+1)
            f.write(hdr)
            arr = np.column_stack(( planform[j]['x'], planform[j]['y'] ))
            np.savetxt(f, arr)
