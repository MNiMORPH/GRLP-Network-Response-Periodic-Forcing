import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy

import grlp
import grlp_extras as grlpx

output_gmt = True

# ---- Linear part
x0 = 50.e3
L = 100.e3
Q_mean = 26.
Qs_mean = Q_mean * 1.e-4
B_mean = 254.
net = grlpx.set_up_long_profile(
    L=L,
    Q_mean=Q_mean,
    Qs_mean=Qs_mean,
    B_mean=B_mean,
    p_Q=0,
    p_Qs=0,
    p_B=0,
    x0=x0,
    dx=5.e2,
    evolve=True
    )
lp = net.list_of_LongProfile_objects[0]
lp.compute_equilibration_time()

indirs = {
    "m40_no_int": "../output/network/m40_fix_seg_length_no_internal/",
    "m40_w_int": "../output/network/m40_fix_seg_length_w_internal/",
    "m40_rnd_no_int": "../output/network/m40_rnd_seg_length_no_internal/",
    "m40_rnd_w_int": "../output/network/m40_rnd_seg_length_w_internal/",
    "m40_no_int_var_width": "../output/network/m40_fix_seg_length_no_internal_var_width/",
    "m40_w_int_var_width": "../output/network/m40_fix_seg_length_w_internal_var_width/",
    "m40_rnd_no_int_var_width": "../output/network/m40_rnd_seg_length_no_internal_var_width/",
    "m40_rnd_w_int_var_width": "../output/network/m40_rnd_seg_length_w_internal_var_width/"
    }
nets = {}
hacks = {}
gains = {}
for sweep in indirs.keys():
    sweep_nets, sweep_hacks, sweep_gains, sweep_lags = grlpx.read_sweep(indirs[sweep])
    nets[sweep] = sweep_nets
    hacks[sweep] = sweep_hacks
    gains[sweep] = sweep_gains

# ---- LINEAR GAIN
lin_periods = np.logspace(-2.5, 2.5, 81) * lp.equilibration_time
lin_gain_Qs = [lp.compute_Qs_gain(p, A_Qs=0.2)[-1] for p in lin_periods]
lin_gain_Qs_Qw = [lp.compute_Qs_gain(p, A_Q=0.2)[-1] for p in lin_periods]

# ---- Continuous Gain
continuous_gains = {}
continuous_ps = [1.4, 2.2]
continuous_periods = np.logspace(-2.5, 2.5, 29) * lp.equilibration_time
for i,p in enumerate(continuous_ps):
    net = grlpx.set_up_long_profile(
        L=L,
        Q_mean=Q_mean,
        Qs_mean=Qs_mean,
        B_mean=B_mean,
        p_Q=p,
        p_Qs=p,
        p_B=0,
        x0=x0,
        dx=5.e2,
        evolve=True
        )
    gs = []
    for period in continuous_periods:
        print(p,period)
        periodic = grlpx.evolve_network_periodic(deepcopy(net), period, 0.2, 0.)
        gs.append(periodic['G_Qs'][0][-1])
    continuous_gains[p] = gs


# ---- Teq_max_L
Teq_max_Ls = {}
for i,sweep in enumerate(indirs.keys()):
    Teqs = []
    for j in range(len(gains[sweep])):
        L = nets[sweep][j].list_of_LongProfile_objects[0].x_ext[0][-1]
        Teqs.append((L**2.)/nets[sweep][j].mean_diffusivity)
    Teq_max_Ls[sweep] = Teqs

# ---- Stacks
stacks = {}
for i,sweep in enumerate(indirs.keys()):
    for j in range(len(gains[sweep])):
        periods1 = gains[sweep][j]['P']/Teq_max_Ls[sweep][j]
        periods2 = gains[sweep][j]['P']/gains[sweep][j]['Teq_Qs']
        if i>=0:
            gain = [gains[sweep][j]['G_Qs']['Qs'][k][0][-1] for k in range(len(gains[sweep][j]['P']))]
        else:
            gain = [gains[sweep][j]['G_Qs'][k][0][-1] for k in range(len(gains[sweep][j]['P']))]
        mag = np.full(len(periods1), len(nets[sweep][j].streams_by_order[1]))
        combine = np.column_stack(( periods1, periods2, gain, mag ))
        if j==0:
            arr = combine
        else:
            arr = np.vstack(( arr, combine ))
        stacks[sweep] = arr

fig, axs = plt.subplots(max(2,len(indirs.keys())),3,sharex='col')

for axs_i in axs:
    for ax_ij in axs_i[:2]:
        # ax_ij.fill(
        #     np.hstack(( continuous_periods, continuous_periods[::-1] ))/lp.equilibration_time,
        #     np.hstack(( continuous_gains[1.4], continuous_gains[2.2][::-1] )),
        #     c="lightgrey"
        #     )
        ax_ij.plot(lin_periods/lp.equilibration_time, lin_gain_Qs, c="black")        

for k,sweep in enumerate(indirs.keys()):

    for i in range(len(gains[sweep])):
    
        axs[k,0].scatter(
            stacks[sweep][:,0],
            stacks[sweep][:,2],
            c="red",
            alpha=0.01
            )
        axs[k,1].scatter(
            stacks[sweep][:,1],
            stacks[sweep][:,2],
            c="red",
            alpha=0.01
            )
            
    Teqs = [g['Teq_Qs']/3.154e10 for g in gains[sweep]]
    axs[k,2].hist(Teqs)
    
    print(min(Teqs), max(Teqs))

axs[0,0].set_xscale("log")
axs[0,1].set_xscale("log")

plt.show()

if output_gmt:

    # ---- Save

    basedir = "../output/network/calibration/"

    with open(basedir + "linear_gain.pg", "wb") as f:
        arr = np.column_stack(( lin_periods/lp.equilibration_time, lin_gain_Qs ))
        np.savetxt(f, arr)
        
    with open(basedir + "continuous_gain.pg", "wb") as f:
        arr = np.column_stack(( 
            np.hstack(( continuous_periods, continuous_periods[::-1] ))/lp.equilibration_time,
            np.hstack(( continuous_gains[1.4], continuous_gains[2.2][::-1] ))
            ))
        np.savetxt(f, arr)
        
    outdirs = {
        "m40_no_int": "m40_fix_seg_length_no_internal/",
        "m40_w_int": "m40_fix_seg_length_w_internal/",
        "m40_rnd_no_int": "m40_rnd_seg_length_no_internal/",
        "m40_rnd_w_int": "m40_rnd_seg_length_w_internal/",
        "m40_no_int_var_width": "m40_fix_seg_length_no_internal_var_width/",
        "m40_w_int_var_width": "m40_fix_seg_length_w_internal_var_width/",
        "m40_rnd_no_int_var_width": "m40_rnd_seg_length_no_internal_var_width/",
        "m40_rnd_w_int_var_width": "m40_rnd_seg_length_w_internal_var_width/",
        }

    for i,sweep in enumerate(indirs.keys()):
        
        with open(basedir + outdirs[sweep] + "gain_L.pg", "wb") as f:
            arr = np.column_stack(( stacks[sweep][:,0], stacks[sweep][:,2], stacks[sweep][:,3] ))
            np.savetxt(f, arr)
            
        with open(basedir + outdirs[sweep] + "gain_Le.pg", "wb") as f:
            arr = np.column_stack(( stacks[sweep][:,1], stacks[sweep][:,2], stacks[sweep][:,3] ))
            np.savetxt(f, arr)
            
        with open(basedir + outdirs[sweep] + "Teq.t", "wb") as f:
            arr = [g['Teq_Qs']/3.154e10 for g in gains[sweep]]
            np.savetxt(f, arr)