# from grlp import *
# from grlp_extras import *
# from copy import deepcopy
# 
# def find_lag_times(val, time, scale, threshold=0., can_lead=False, period=False, full=False):
# 
# 
#     peak_lags = np.zeros( len(val[0,:]) )
#     trough_lags = np.zeros( len(val[0,:]) )
# 
#     tps = []
# 
#     scl_peaks, __ = find_peaks(scale)
#     scl_troughs, __ = find_peaks(-scale)
#     scl_tps = np.sort( np.hstack(( scl_peaks, scl_troughs )) )
# 
#     for i in range(len(val[0,:])):
# 
#         if ( val[:,i].max() - val[:,i].min() ) < threshold:
#             peak_lags[i] = np.nan
#             trough_lags[i] = np.nan
#             continue
# 
#         obs_peaks, __ = find_peaks(val[:,i])
#         obs_troughs, __ = find_peaks(-val[:,i])
#         obs_tps = np.sort( np.hstack(( obs_peaks, obs_troughs )) )
#         if not can_lead:
#             obs_tps = obs_tps[ np.where( obs_tps >= scl_tps[0] ) ]
# 
#         obs_tps_attached = np.zeros( len(obs_tps), dtype=int )
#         obs_lag_time = np.zeros( len(obs_tps), dtype=int )
# 
#         for j,tp in enumerate(obs_tps):
#             if j > len(scl_tps)-1:
#                 continue
#             obs_tps_attached[j] = scl_tps[j]
#             obs_lag_time[j] = time[tp] - time[scl_tps[j]]
# 
#         peak_lags_i = []
#         trough_lags_i = []
# 
#         for k,tp in enumerate(obs_tps_attached):
# 
#             # if obs_lag_time[k] != 0.:
#             if any(scl_peaks == tp):
#                 peak_lags_i.append( obs_lag_time[k].copy() )
#             else:
#                 trough_lags_i.append( obs_lag_time[k].copy() )
# 
#         if len(peak_lags_i) > 1:
#             peak_lags[i] = np.array(peak_lags_i[1:]).mean()
#         else:
#             peak_lags[i] = np.nan
# 
#         if len(trough_lags_i) > 1:
#             trough_lags[i] = np.array(trough_lags_i[1:]).mean()
#         else:
#             trough_lags[i] = np.nan
# 
#         tps.append( obs_tps )
# 
#     if period:
#         for i in range(1,len(val[0,:])):
#             while (peak_lags[i] - peak_lags[i-1]) > 0.5*period:
#                 peak_lags[i] -= period
#             while (trough_lags[i] - trough_lags[i-1]) > 0.5*period:
#                 trough_lags[i] -= period
#         for i in range(len(val[0,:])-2,0,-1):
#             while (peak_lags[i] - peak_lags[i+1]) > 0.5*period:
#                 peak_lags[i] -= period
#             while (trough_lags[i] - trough_lags[i+1]) > 0.5*period:
#                 trough_lags[i] -= period
# 
#     if full:
#         return {'plags': peak_lags, 'tlags': trough_lags, 'obs_tps': tps, 'scl_tps': scl_tps, 'scl_p': scl_peaks, 'scl_t': scl_troughs}
#     else:
#         return (peak_lags + trough_lags)/2.
# 
# def find_network_lag(net, prop, time, scale, period, can_lead=False):
# 
#     # Initial attempt
#     lag = [np.zeros(len(seg.x)) for seg in net.list_of_LongProfile_objects]
#     for seg in net.list_of_LongProfile_objects:
#         lag[seg.ID] = find_lag_times(prop[seg.ID], time, scale, period=period, can_lead=can_lead) / period
# 
#     # Check for cycle-skipped segment
#     completed_segs = []
#     for segID in net.list_of_channel_head_segment_IDs:
#         while net.list_of_LongProfile_objects[segID].downstream_segment_IDs:
#             down_segID = net.list_of_LongProfile_objects[segID].downstream_segment_IDs[0]
#             if down_segID not in completed_segs:
#                 if (lag[down_segID][0] - lag[segID][-1]) > 0.5:
#                     lag[down_segID] -= 1.
#                 completed_segs.append(down_segID)
#             segID = down_segID
# 
#     return lag
# 
# def find_lag_time_single(val, time, scale, threshold=0., can_lead=False, period=False, full=False):
# 
#     scl_peaks, __ = find_peaks(scale)
#     scl_troughs, __ = find_peaks(-scale)
#     scl_tps = np.sort( np.hstack(( scl_peaks, scl_troughs )) )
# 
#     obs_peaks, __ = find_peaks(val)
#     obs_troughs, __ = find_peaks(-val)
#     obs_tps = np.sort( np.hstack(( obs_peaks, obs_troughs )) )
#     # plt.plot(val/val.mean())
#     # plt.plot(1+scale/scale.mean()*(val.max()-val.mean())/val.mean(), ":")
#     # plt.scatter(obs_peaks,val[obs_peaks]/val.mean())
#     # plt.scatter(obs_troughs,val[obs_troughs]/val.mean())
#     # plt.show()
#     if not can_lead:
#         obs_tps = obs_tps[ np.where( obs_tps >= scl_tps[0] ) ]
# 
#     obs_tps_attached = np.zeros( len(obs_tps), dtype=int )
#     obs_lag_time = np.zeros( len(obs_tps), dtype=int )
# 
#     for j,tp in enumerate(obs_tps):
#         if j > len(scl_tps)-1:
#             continue
#         obs_tps_attached[j] = scl_tps[j]
#         obs_lag_time[j] = time[tp] - time[scl_tps[j]]
# 
#     peak_lags_i = []
#     trough_lags_i = []
# 
#     for k,tp in enumerate(obs_tps_attached):
# 
#         if obs_lag_time[k] != 0.:
#             if any(scl_peaks == tp):
#                 peak_lags_i.append( obs_lag_time[k].copy() )
#             else:
#                 trough_lags_i.append( obs_lag_time[k].copy() )
# 
#     if len(peak_lags_i) > 1:
#         peak_lags = np.array(peak_lags_i[1:]).mean()
#     else:
#         peak_lags = np.nan
# 
#     if len(trough_lags_i) > 1:
#         trough_lags = np.array(trough_lags_i[1:]).mean()
#     else:
#         trough_lags = np.nan
# 
    # return (peak_lags + trough_lags)/2.

# # ---- Linear part
# L = 100.e3
# mean_Q = 10.
# mean_Qs = 0.001
# B = 98.1202038813591
# S0 = (mean_Qs / (0.040987384904837776 * mean_Q))**(6./7.)
# lp = LongProfile()
# lp.basic_constants()
# lp.bedload_lumped_constants()
# lp.set_hydrologic_constants()
# dx = 1.e3
# x = [np.arange(0., L, dx)]
# S0 = [(mean_Qs/(lp.k_Qs*mean_Q))**(6./7.)]
# upstream_segment_IDs = [[]]
# downstream_segment_IDs = [[]]
# z = [(x[0].max()-x[0])*S0]
# Q = [np.full(len(x),mean_Q)]
# B = [np.full(len(x),B)]
# net = Network()
# net.initialize(
#     config_file = None,
#     x_bl =L,
#     z_bl = 0.,
#     S0 = S0,
#     upstream_segment_IDs = upstream_segment_IDs,
#     downstream_segment_IDs = downstream_segment_IDs,
#     x = x,
#     z = z,
#     Q = Q,
#     B = B,
#     overwrite = False
#     )
# net.set_niter(3)
# net.get_z_lengths()
# diff = (7./6.) * lp.k_Qs * mean_Q * (S0[0]**(1./6.)) / (B[0] * (1. - lp.lambda_p))
# lp = net.list_of_LongProfile_objects[0]
# lp.compute_equilibration_time()


import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy

import grlp
import grlp_extras as grlpx

output_gmt = False

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
lags = {}
for sweep in indirs.keys():
    sweep_nets, sweep_hacks, sweep_gains, sweep_lags = grlpx.read_sweep(indirs[sweep])
    nets[sweep] = sweep_nets
    hacks[sweep] = sweep_hacks
    gains[sweep] = sweep_gains
    lags[sweep] = sweep_lags

# ---- LINEAR
lin_periods = np.logspace(-2.5, 2.5, 81) * lp.equilibration_time
lin_gain_z = [lp.compute_z_gain(p)[-1] for p in lin_periods]
lin_gain_z_up = [lp.compute_z_gain(p)[0] for p in lin_periods]
lin_lag_z = [lp.compute_z_lag(p, nsum=10000)[-1]/p for p in lin_periods]
lin_lag_z_up = [lp.compute_z_lag(p, nsum=10000)[0]/p for p in lin_periods]
lin_gain_Qs = [lp.compute_Qs_gain(p, A_Qs=0.2)[-1] for p in lin_periods]
lin_lag_Qs = [lp.compute_Qs_lag(p, A_Qs=0.2)[-1]/p for p in lin_periods]
lin_gain_Qs_Qw = [lp.compute_Qs_gain(p, A_Q=0.2)[-1] for p in lin_periods]
lin_lag_Qs_Qw = [lp.compute_Qs_lag(p, A_Q=0.2)[-1]/p for p in lin_periods]


# ---- CONTINUOUS
continuous_ps = [1.4, 2.2]
continuous_periodics = {1.4: [], 2.2: []}
continuous_periodics_Q = {1.4: [], 2.2: []}
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
        continuous_periodics[p].append(periodic)
        periodic = grlpx.evolve_network_periodic(deepcopy(net), period, 0., 0.2)
        continuous_periodics_Q[p].append(periodic)


# max_gains = []
# min_gains = []
# max_lags = []
# min_lags = []
# for i,p in enumerate(continuous_periods):
#     gain_stack = np.column_stack((
#         continuous_periodics[1.4][i]['G_z'][0],
#         continuous_periodics[2.2][i]['G_z'][0]
#         ))
#     max_gains.append(gain_stack.max())
#     min_gains.append(gain_stack.min())
#     lag_stack = np.column_stack((
#         continuous_periodics[1.4][i]['lag_z'][0],
#         continuous_periodics[2.2][i]['lag_z'][0]
#         ))
#     max_lags.append(lag_stack.max())
#     min_lags.append(lag_stack.min())
# 
# 
# plt.fill(
#     np.hstack((continuous_periods, continuous_periods[::-1]))/lp.equilibration_time,
#     np.hstack((max_gains, min_gains[::-1])),
#     alpha=0.2
#     )
# plt.fill(
#     np.hstack((lin_periods, lin_periods[::-1]))/lp.equilibration_time,
#     np.hstack((lin_gain_z, lin_gain_z_up[::-1])),
#     alpha=0.2
#     )
# 
# plt.plot(continuous_periods/lp.equilibration_time, "k--")
# plt.plot(lin_periods/lp.equilibration_time, lin_gain_z, "k-")
# plt.xscale("log")
# plt.show()
# 
# plt.fill(
#     np.hstack((continuous_periods, continuous_periods[::-1]))/lp.equilibration_time,
#     np.hstack((max_lags, min_lags[::-1])),
#     alpha=0.2
#     )
# plt.fill(
#     np.hstack((lin_periods, lin_periods[::-1]))/lp.equilibration_time,
#     np.hstack((lin_lag_z, lin_lag_z_up[::-1])),
#     alpha=0.2,
#     color="grey"
#     )
# 
# plt.plot(lin_periods/lp.equilibration_time, lin_lag_z, "k-")
# plt.xscale("log")
# plt.ylim(0,1)
# plt.show()


# ---- Plot
fig, axs = plt.subplots(max(2,len(indirs.keys())),6,sharex=True)
axs[0,0].set_xscale("log")

for i,sweep in enumerate(indirs.keys()):
    
    sweep_periods = np.hstack([g['P']/g['Teq_Qs'] for g in gains[sweep]])
    sweep_mags = np.hstack([np.full(len(gains[sweep][j]['P']), len(n.streams_by_order[1])) for j,n in enumerate(nets[sweep])])
    
    gain1 = [max(np.hstack((p1['G_z'][0], p2['G_z'][0]))) for p1,p2 in zip(continuous_periodics[1.4], continuous_periodics[2.2])]
    gain2 = [min(np.hstack((p1['G_z'][0], p2['G_z'][0]))) for p1,p2 in zip(continuous_periodics[1.4], continuous_periodics[2.2])]
    axs[i,0].fill(
        np.hstack(( continuous_periods, continuous_periods[::-1] ))/lp.equilibration_time,
        np.hstack(( gain1, gain2[::-1] )),
        alpha=0.2
        )
    axs[i,0].fill(
        np.hstack(( lin_periods, lin_periods[::-1] ))/lp.equilibration_time,
        np.hstack(( lin_gain_z, lin_gain_z_up[::-1] )),
        c="grey",
        alpha=0.2
        )
    axs[i,0].plot(lin_periods/lp.equilibration_time, lin_gain_z, c="black")
    sweep_gains = [g['G_z']['Qs'][j][0][-1] for g in gains[sweep] for j in range(len(g['P']))]
    axs[i,0].scatter(
        sweep_periods,
        sweep_gains,
        alpha=0.1,
        c=sweep_mags
        )    
    
    lag1 = [max(np.hstack((p1['lag_z'][0], p2['lag_z'][0]))) for p1,p2 in zip(continuous_periodics[1.4], continuous_periodics[2.2])]
    lag2 = [min(np.hstack((p1['lag_z'][0], p2['lag_z'][0]))) for p1,p2 in zip(continuous_periodics[1.4], continuous_periodics[2.2])]
    axs[i,1].fill(
        np.hstack(( continuous_periods, continuous_periods[::-1] ))/lp.equilibration_time,
        np.hstack(( lag1, lag2[::-1] )),
        alpha=0.2
        )
    axs[i,1].fill(
        np.hstack(( lin_periods, lin_periods[::-1] ))/lp.equilibration_time,
        np.hstack(( lin_lag_z, lin_lag_z_up[::-1] )),
        c="grey",
        alpha=0.2
        )
    axs[i,1].plot(lin_periods/lp.equilibration_time, lin_lag_z, c="black")
    axs[i,1].set_ylim(-0.05,0.95)
    sweep_lags = [l['lag_z']['Qs'][j][0][-1] for l in lags[sweep] for j in range(len(l['P']))]
    axs[i,1].scatter(
        sweep_periods,
        sweep_lags,
        alpha=0.1,
        c=sweep_mags
        ) 
    
    gain1 = [p['G_Qs'][0][-1] for p in continuous_periodics[1.4]]
    gain2 = [p['G_Qs'][0][-1] for p in continuous_periodics[2.2]]
    axs[i,2].fill(
        np.hstack(( continuous_periods, continuous_periods[::-1] ))/lp.equilibration_time,
        np.hstack(( gain1, gain2[::-1] )),
        c="lightgrey"
        )
    axs[i,2].plot(continuous_periods/lp.equilibration_time, gain1, "--", c="grey")
    axs[i,2].plot(continuous_periods/lp.equilibration_time, gain2, "--", c="grey")
    axs[i,2].plot(lin_periods/lp.equilibration_time, lin_gain_Qs, c="black")
    sweep_gains = [g['G_Qs']['Qs'][j][0][-1] for g in gains[sweep] for j in range(len(g['P']))]
    axs[i,2].scatter(
        sweep_periods,
        sweep_gains,
        alpha=0.1,
        c=sweep_mags
        )    

    lag1 = np.array([p['lag_Qs'] for p in continuous_periodics[1.4]])/continuous_periods
    lag2 = np.array([p['lag_Qs'] for p in continuous_periodics[2.2]])/continuous_periods
    # nonnans_a = np.where(~np.isnan(continuous_Qs_lags[0.5]['Qs']))
    # nonnans_b = np.where(~np.isnan(continuous_Qs_lags[1]['Qs']))
    # axs[i,3].fill(
    #     np.hstack(( continuous_periods[nonnans_a], continuous_periods[nonnans_b][::-1] ))/lp.equilibration_time,
    #     np.hstack(( np.array(continuous_Qs_lags[0.5]['Qs'])[nonnans_a], np.array(continuous_Qs_lags[1]['Qs'])[nonnans_b][::-1] )),
    #     c="lightgrey"
    #     )
    # axs[i,3].plot(continuous_periods/lp.equilibration_time, continuous_Qs_lags[0.5]['Qs'], "--", c="grey")
    # axs[i,3].plot(continuous_periods/lp.equilibration_time, continuous_Qs_lags[1]['Qs'], "--", c="grey")
    axs[i,3].fill(
        np.hstack(( continuous_periods, continuous_periods[::-1] ))/lp.equilibration_time,
        np.hstack(( lag1, lag2[::-1] )),
        c="lightgrey"
        )
    axs[i,3].plot(continuous_periods/lp.equilibration_time, lag1, "--", c="grey")
    axs[i,3].plot(continuous_periods/lp.equilibration_time, lag2, "--", c="grey")
    axs[i,3].plot(lin_periods/lp.equilibration_time, lin_lag_Qs, c="black")
    axs[i,3].set_ylim(-0.05,0.95)
    if i>3:
        sweep_lags = [l['lag_Qs']['Qs'][j]/l['P'][j] for l in lags[sweep] for j in range(len(l['P']))]
    else:
        sweep_lags = [l['lag_Qs']['Qs'][j] for l in lags[sweep] for j in range(len(l['P']))]
    axs[i,3].scatter(
        sweep_periods,
        sweep_lags,
        alpha=0.1,
        c=sweep_mags
        ) 

    gain1 = [p['G_Qs'][0][-1] for p in continuous_periodics_Q[1.4]]
    gain2 = [p['G_Qs'][0][-1] for p in continuous_periodics_Q[2.2]]
    axs[i,4].fill(
        np.hstack(( continuous_periods, continuous_periods[::-1] ))/lp.equilibration_time,
        np.hstack(( gain1, gain2[::-1] )),
        c="lightgrey"
        )
    axs[i,4].plot(continuous_periods/lp.equilibration_time, gain1, "--", c="grey")
    axs[i,4].plot(continuous_periods/lp.equilibration_time, gain2, "--", c="grey")
    axs[i,4].plot(lin_periods/lp.equilibration_time, lin_gain_Qs_Qw, c="black")
    sweep_gains = [g['G_Qs']['Qw'][j][0][-1] for g in gains[sweep] for j in range(len(g['P']))]
    axs[i,4].scatter(
        sweep_periods,
        sweep_gains,
        alpha=0.1,
        c=sweep_mags
        )    

    lag1 = np.array([p['lag_Qs'] for p in continuous_periodics_Q[1.4]])/continuous_periods
    lag2 = np.array([p['lag_Qs'] for p in continuous_periodics_Q[2.2]])/continuous_periods
    # nonnans_a = np.where(~np.isnan(continuous_Qs_lags[0.5]['Qw']))
    # nonnans_b = np.where(~np.isnan(continuous_Qs_lags[1]['Qw']))
    # axs[i,5].fill(
    #     np.hstack(( continuous_periods[nonnans_a], continuous_periods[nonnans_b][::-1] ))/lp.equilibration_time,
    #     np.hstack(( np.array(continuous_Qs_lags[0.5]['Qw'])[nonnans_a], np.array(continuous_Qs_lags[1]['Qw'])[nonnans_b][::-1] )),
    #     c="lightgrey"
    #     )
    # axs[i,5].plot(continuous_periods/lp.equilibration_time, continuous_Qs_lags[0.5]['Qw'], "--", c="grey")
    # axs[i,5].plot(continuous_periods/lp.equilibration_time, continuous_Qs_lags[1]['Qw'], "--", c="grey")
    axs[i,5].fill(
        np.hstack(( continuous_periods, continuous_periods[::-1] ))/lp.equilibration_time,
        np.hstack(( lag1, lag2[::-1] )),
        c="lightgrey"
        )
    axs[i,5].plot(continuous_periods/lp.equilibration_time, lag1, "--", c="grey")
    axs[i,5].plot(continuous_periods/lp.equilibration_time, lag2, "--", c="grey")
    axs[i,5].plot(lin_periods/lp.equilibration_time, lin_lag_Qs_Qw, c="black")
    if i>3:
        sweep_lags = [l['lag_Qs']['Qw'][j]/l['P'][j] for l in lags[sweep] for j in range(len(l['P']))]
    else:
        sweep_lags = [l['lag_Qs']['Qw'][j] for l in lags[sweep] for j in range(len(l['P']))]
    axs[i,5].scatter(
        sweep_periods,
        sweep_lags,
        alpha=0.1,
        c=sweep_mags
        )

plt.show()

if output_gmt:

    # ---- Save

    basedir = "../output/network/full_sweep/"

    with open(basedir + "z_linear_gain.pg", "wb") as f:
        arr = np.column_stack(( lin_periods/lp.equilibration_time, lin_gain_z ))
        np.savetxt(f, arr)
        
    with open(basedir + "z_linear_gain_rng.pg", "wb") as f:
        arr = np.column_stack(( 
            np.hstack(( lin_periods, lin_periods[::-1] ))/lp.equilibration_time,
            np.hstack(( lin_gain_z, lin_gain_z_up[::-1] ))
            ))
        np.savetxt(f, arr)
        
    with open(basedir + "z_continuous_gain.pg", "wb") as f:
        gain1 = [max(np.hstack((p1['G_z'][0], p2['G_z'][0]))) for p1,p2 in zip(continuous_periodics[1.4], continuous_periodics[2.2])]
        gain2 = [min(np.hstack((p1['G_z'][0], p2['G_z'][0]))) for p1,p2 in zip(continuous_periodics[1.4], continuous_periodics[2.2])]
        arr = np.column_stack(( 
            np.hstack(( continuous_periods, continuous_periods[::-1] ))/lp.equilibration_time,
            np.hstack(( gain1, gain2[::-1] ))
            ))
        np.savetxt(f, arr)
        
    with open(basedir + "z_linear_lag.pl", "wb") as f:
        arr = np.column_stack(( lin_periods/lp.equilibration_time, lin_lag_z ))
        np.savetxt(f, arr)

    with open(basedir + "z_linear_lag_rng.pl", "wb") as f:
        arr = np.column_stack(( 
            np.hstack(( lin_periods, lin_periods[::-1] ))/lp.equilibration_time,
            np.hstack(( lin_lag_z, lin_lag_z_up[::-1] ))
            ))
        np.savetxt(f, arr)        

    with open(basedir + "z_continuous_lag.pl", "wb") as f:
        lag1 = [max(np.hstack((p1['lag_z'][0], p2['lag_z'][0]))) for p1,p2 in zip(continuous_periodics[1.4], continuous_periodics[2.2])]
        lag2 = [min(np.hstack((p1['lag_z'][0], p2['lag_z'][0]))) for p1,p2 in zip(continuous_periodics[1.4], continuous_periodics[2.2])]
        arr = np.column_stack(( 
            np.hstack(( continuous_periods, continuous_periods[::-1] ))/lp.equilibration_time,
            np.hstack(( lag1, lag2[::-1] ))
            ))
        np.savetxt(f, arr)

    with open(basedir + "Qs_linear_gain.pg", "wb") as f:
        arr = np.column_stack(( lin_periods/lp.equilibration_time, lin_gain_Qs ))
        np.savetxt(f, arr)

    with open(basedir + "Qs_continuous_gain.pg", "wb") as f:
        gain1 = [p['G_Qs'][0][-1] for p in continuous_periodics[1.4]]
        gain2 = [p['G_Qs'][0][-1] for p in continuous_periodics[2.2]]
        arr = np.column_stack(( 
            np.hstack(( continuous_periods, continuous_periods[::-1] ))/lp.equilibration_time,
            np.hstack(( gain1, gain2[::-1] ))
            ))
        np.savetxt(f, arr)
        
    with open(basedir + "Qs_linear_lag.pl", "wb") as f:
        arr = np.column_stack(( lin_periods/lp.equilibration_time, lin_lag_Qs ))
        np.savetxt(f, arr)

    # nonnans_a = np.where(~np.isnan(continuous_Qs_lags[0.5]['Qs']))
    # nonnans_b = np.where(~np.isnan(continuous_Qs_lags[1]['Qs']))
    # with open(basedir + "Qs_continuous_lag.pl", "wb") as f:
    #     arr = np.column_stack(( 
    #         np.hstack(( continuous_periods[nonnans_a], continuous_periods[nonnans_b][::-1] ))/lp.equilibration_time,
    #         np.hstack(( np.array(continuous_Qs_lags[0.5]['Qs'])[nonnans_a], np.array(continuous_Qs_lags[1]['Qs'])[nonnans_b][::-1] ))
    #         ))
    #     np.savetxt(f, arr)
    with open(basedir + "Qs_continuous_lag.pl", "wb") as f:
        lag1 = np.array([p['lag_Qs'] for p in continuous_periodics[1.4]])/continuous_periods
        lag2 = np.array([p['lag_Qs'] for p in continuous_periodics[2.2]])/continuous_periods
        arr = np.column_stack(( 
            np.hstack(( continuous_periods, continuous_periods[::-1] ))/lp.equilibration_time,
            np.hstack(( lag1, lag2[::-1] ))
            ))
        np.savetxt(f, arr)


    with open(basedir + "Qs_Qw_linear_gain.pg", "wb") as f:
        arr = np.column_stack(( lin_periods/lp.equilibration_time, lin_gain_Qs_Qw ))
        np.savetxt(f, arr)
        
    with open(basedir + "Qs_Qw_continuous_gain.pg", "wb") as f:
        gain1 = [p['G_Qs'][0][-1] for p in continuous_periodics_Q[1.4]]
        gain2 = [p['G_Qs'][0][-1] for p in continuous_periodics_Q[2.2]]
        arr = np.column_stack(( 
            np.hstack(( continuous_periods, continuous_periods[::-1] ))/lp.equilibration_time,
            np.hstack(( gain1, gain2[::-1] ))
            ))
        np.savetxt(f, arr)

    with open(basedir + "Qs_Qw_linear_lag.pl", "wb") as f:
        arr = np.column_stack(( lin_periods/lp.equilibration_time, lin_lag_Qs_Qw ))
        np.savetxt(f, arr)

    # nonnans_a = np.where(~np.isnan(continuous_Qs_lags[0.5]['Qs']))
    # nonnans_b = np.where(~np.isnan(continuous_Qs_lags[1]['Qs']))
    # with open(basedir + "Qs_Qw_continuous_lag.pl", "wb") as f:
    #     arr = np.column_stack(( 
    #         np.hstack(( continuous_periods[nonnans_a], continuous_periods[nonnans_b][::-1] ))/lp.equilibration_time,
    #         np.hstack(( np.array(continuous_Qs_lags[0.5]['Qw'])[nonnans_a], np.array(continuous_Qs_lags[1]['Qw'])[nonnans_b][::-1] ))
    #         ))
    #     np.savetxt(f, arr)
    with open(basedir + "Qs_Qw_continuous_lag.pl", "wb") as f:
        lag1 = np.array([p['lag_Qs'] for p in continuous_periodics_Q[1.4]])/continuous_periods
        lag2 = np.array([p['lag_Qs'] for p in continuous_periodics_Q[2.2]])/continuous_periods
        arr = np.column_stack(( 
            np.hstack(( continuous_periods, continuous_periods[::-1] ))/lp.equilibration_time,
            np.hstack(( lag1, lag2[::-1] ))
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
        "m40_rnd_w_int_var_width": "m40_rnd_seg_length_w_internal_var_width/"
        }

    for i,sweep in enumerate(indirs.keys()):
        
        sweep_periods = np.hstack([g['P']/g['Teq_Qs'] for g in gains[sweep]])
        sweep_mags = np.hstack([np.full(len(gains[sweep][j]['P']), len(n.streams_by_order[1])) for j,n in enumerate(nets[sweep])])

        sweep_gains = [g['G_z']['Qs'][j][0][-1] for g in gains[sweep] for j in range(len(g['P']))]
        sweep_gains_plus = [np.nanmax(np.hstack(g['G_z']['Qs'][j]))-g['G_z']['Qs'][j][0][-1] for g in gains[sweep] for j in range(len(g['P']))]
        sweep_gains_minus = [g['G_z']['Qs'][j][0][-1]-np.nanmin(np.hstack(g['G_z']['Qs'][j])) for g in gains[sweep] for j in range(len(g['P']))]
        with open(basedir + outdirs[sweep] + "z_gain.pg", "wb") as f:
            arr = np.column_stack(( sweep_periods, sweep_gains, sweep_mags, sweep_gains_minus, sweep_gains_plus ))
            np.savetxt(f, arr)
            
        sweep_lags = [l['lag_z']['Qs'][j][0][-1] for l in lags[sweep] for j in range(len(l['P']))]
        sweep_lags_plus = [np.nanmin(np.hstack(l['lag_z']['Qs'][j]))-l['lag_z']['Qs'][j][0][-1] for l in lags[sweep] for j in range(len(l['P']))]
        sweep_lags_minus = [l['lag_z']['Qs'][j][0][-1]-np.nanmin(np.hstack(l['lag_z']['Qs'][j])) for l in lags[sweep] for j in range(len(l['P']))]
        with open(basedir + outdirs[sweep] + "z_lag.pl", "wb") as f:
            arr = np.column_stack(( sweep_periods, sweep_lags, sweep_mags, sweep_lags_minus, sweep_lags_plus ))
            np.savetxt(f, arr)
            
        sweep_gains = [g['G_Qs']['Qs'][j][0][-1] for g in gains[sweep] for j in range(len(g['P']))]
        with open(basedir + outdirs[sweep] + "Qs_gain.pg", "wb") as f:
            arr = np.column_stack(( sweep_periods, sweep_gains, sweep_mags ))
            np.savetxt(f, arr)
            
        if i>3:
            sweep_lags = [l['lag_Qs']['Qs'][j]/l['P'][j] for l in lags[sweep] for j in range(len(l['P']))]
        else:
            sweep_lags = [l['lag_Qs']['Qs'][j] for l in lags[sweep] for j in range(len(l['P']))]
        with open(basedir + outdirs[sweep] + "Qs_lag.pl", "wb") as f:
            arr = np.column_stack(( sweep_periods, sweep_lags, sweep_mags ))
            np.savetxt(f, arr)
            
        sweep_gains = [g['G_Qs']['Qw'][j][0][-1] for g in gains[sweep] for j in range(len(g['P']))]
        with open(basedir + outdirs[sweep] + "Qs_Qw_gain.pg", "wb") as f:
            arr = np.column_stack(( sweep_periods, sweep_gains, sweep_mags ))
            np.savetxt(f, arr)

        if i>3:
            sweep_lags = [l['lag_Qs']['Qw'][j]/l['P'][j] for l in lags[sweep] for j in range(len(l['P']))]
        else:
            sweep_lags = [l['lag_Qs']['Qw'][j] for l in lags[sweep] for j in range(len(l['P']))]
        with open(basedir + outdirs[sweep] + "Qs_Qw_lag.pl", "wb") as f:
            arr = np.column_stack(( sweep_periods, sweep_lags, sweep_mags ))
            np.savetxt(f, arr)