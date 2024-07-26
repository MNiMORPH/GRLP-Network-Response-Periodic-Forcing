import matplotlib.pyplot as plt
import numpy as np

import grlp
import grlp_extras as grlpx

sweep_nets, sweep_hacks, sweep_gains, sweep_lags = grlpx.read_sweep(
    "../output/network/m40_fix_seg_length_no_internal_var_width/"
    )



# ---- Effective length
eff_lengths = []
for i in range(len(sweep_gains)):
    diffs = []
    eff_lengths.append( np.sqrt(sweep_gains[i]['Teq_Qs']*sweep_nets[i].mean_diffusivity) )

    
# ---- Linear part
net = grlpx.set_up_long_profile(
    L=100.e3,
    Q_mean=10.,
    Qs_mean=10. * 1.e-4,
    B_mean=98.1202038813591,
    p_Q=0,
    p_Qs=0,
    p_B=0,
    x0=10.e3,
    dx=5.e2,
    evolve=True
    )
lin_periods = np.logspace(-2., 3., 81) * net.list_of_LongProfile_objects[0].equilibration_time
lin_gain_z = [
    net.list_of_LongProfile_objects[0].compute_z_gain(p)[-1]
    for p in lin_periods
    ]
lin_lag_z = [
    net.list_of_LongProfile_objects[0].compute_z_lag(p, nsum=1000)[-1]/p
    for p in lin_periods
    ]
lin_gain_Qs = [
    net.list_of_LongProfile_objects[0].compute_Qs_gain(p, A_Qs=0.2)[-1]
    for p in lin_periods
    ]
lin_lag_Qs = [
    net.list_of_LongProfile_objects[0].compute_Qs_lag(p, A_Qs=0.2, nsum=1000)[-1]/p
    for p in lin_periods
    ]
lin_gain_Qs_Qw = [
    net.list_of_LongProfile_objects[0].compute_Qs_gain(p, A_Q=0.2)[-1]
    for p in lin_periods
    ]
lin_lag_Qs_Qw = [
    net.list_of_LongProfile_objects[0].compute_Qs_lag(p, A_Q=0.2, nsum=1000)[-1]/p
    for p in lin_periods
    ]


# ---- Calibration
fig, axs = plt.subplots(1,2,sharex=True,sharey=True)
for ax in axs:
    ax.plot(lin_periods/net.list_of_LongProfile_objects[0].equilibration_time, lin_gain_Qs)
for i in range(len(sweep_gains)):
    periods1 = sweep_gains[i]['P']/3.154e12
    periods2 = sweep_gains[i]['P']/sweep_gains[i]['Teq_Qs']
    gains = [sweep_gains[i]['G_Qs']['Qs'][k][0][-1] for k in range(len(sweep_gains[i]['P']))]
    axs[0].scatter(
        periods1,
        gains,
        c="red",
        alpha=0.01
        )
    axs[1].scatter(
        periods2,
        gains,
        c="red",
        alpha=0.01
        )
axs[0].set_xscale("log")
plt.show()


# ---- Full sweep
fig, axs = plt.subplots(1,6,sharex=True,sharey=True)

axs[0].plot(lin_periods/net.list_of_LongProfile_objects[0].equilibration_time, lin_gain_z)
axs[1].plot(lin_periods/net.list_of_LongProfile_objects[0].equilibration_time, lin_lag_z)
axs[2].plot(lin_periods/net.list_of_LongProfile_objects[0].equilibration_time, lin_gain_Qs)
axs[3].plot(lin_periods/net.list_of_LongProfile_objects[0].equilibration_time, lin_lag_Qs)
axs[4].plot(lin_periods/net.list_of_LongProfile_objects[0].equilibration_time, lin_gain_Qs_Qw)
axs[5].plot(lin_periods/net.list_of_LongProfile_objects[0].equilibration_time, lin_lag_Qs_Qw)

for i in range(len(sweep_gains)):
    periods = sweep_gains[i]['P']/sweep_gains[i]['Teq_Qs']
    
    axs[0].scatter(
        periods,
        [sweep_gains[i]['G_z']['Qs'][k][0][-1] for k in range(len(sweep_gains[i]['P']))],
        c="red",
        alpha=0.1
        )

    axs[1].scatter(
        periods,
        [sweep_lags[i]['lag_z']['Qs'][k][0][-1] for k in range(len(sweep_gains[i]['P']))],
        c="red",
        alpha=0.1
        )
        
    axs[2].scatter(
        periods,
        [sweep_gains[i]['G_Qs']['Qs'][k][0][-1] for k in range(len(sweep_gains[i]['P']))],
        c="red",
        alpha=0.1
        )
        
    axs[3].scatter(
        periods,
        [sweep_lags[i]['lag_Qs']['Qs'][k]/sweep_gains[i]['P'][k] for k in range(len(sweep_gains[i]['P']))],
        c="red",
        alpha=0.1
        )

        
    axs[4].scatter(
        periods,
        [sweep_gains[i]['G_Qs']['Qw'][k][0][-1] for k in range(len(sweep_gains[i]['P']))],
        c="red",
        alpha=0.1
        )
        
    axs[5].scatter(
        periods,
        [sweep_lags[i]['lag_Qs']['Qw'][k]/sweep_gains[i]['P'][k] for k in range(len(sweep_gains[i]['P']))],
        c="red",
        alpha=0.1
        )
        
axs[0].set_xscale("log")
plt.show()


# ---- Controls
fig, axs = plt.subplots(1,6,sharey=True,sharex="col")
mags = [len(n.streams_by_order[1]) for n in sweep_nets]
axs[0].scatter(
    [n.bifurcation_ratio for n in sweep_nets],
    eff_lengths,
    c=mags
    )
axs[1].scatter(
    [n.length_ratio for n in sweep_nets],
    eff_lengths,
    c=mags
    )
axs[2].scatter(
    [n.discharge_ratio for n in sweep_nets],
    eff_lengths,
    c=mags
    )
axs[3].scatter(
    [1./h['p'] for h in sweep_hacks],
    eff_lengths,
    c=mags
    )
# axs[i,4].scatter(
#     [e_k for e_k in tokunagas[sweep]],
#     eff_lengths[sweep],
#     c=mags
#     )
axs[5].scatter(
    [n.mean_downstream_distance for n in sweep_nets],
    eff_lengths,
    c=mags
    )
plt.show()

