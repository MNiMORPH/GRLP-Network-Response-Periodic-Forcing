from grlp import *
from grlp_extras import *
from copy import deepcopy

def find_lag_times(val, time, scale, threshold=0., can_lead=False, period=False, full=False):


    peak_lags = np.zeros( len(val[0,:]) )
    trough_lags = np.zeros( len(val[0,:]) )

    tps = []

    scl_peaks, __ = find_peaks(scale)
    scl_troughs, __ = find_peaks(-scale)
    scl_tps = np.sort( np.hstack(( scl_peaks, scl_troughs )) )

    for i in range(len(val[0,:])):

        if ( val[:,i].max() - val[:,i].min() ) < threshold:
            peak_lags[i] = np.nan
            trough_lags[i] = np.nan
            continue

        obs_peaks, __ = find_peaks(val[:,i])
        obs_troughs, __ = find_peaks(-val[:,i])
        obs_tps = np.sort( np.hstack(( obs_peaks, obs_troughs )) )
        if not can_lead:
            obs_tps = obs_tps[ np.where( obs_tps >= scl_tps[0] ) ]

        obs_tps_attached = np.zeros( len(obs_tps), dtype=int )
        obs_lag_time = np.zeros( len(obs_tps), dtype=int )

        for j,tp in enumerate(obs_tps):
            if j > len(scl_tps)-1:
                continue
            obs_tps_attached[j] = scl_tps[j]
            obs_lag_time[j] = time[tp] - time[scl_tps[j]]

        peak_lags_i = []
        trough_lags_i = []

        for k,tp in enumerate(obs_tps_attached):

            # if obs_lag_time[k] != 0.:
            if any(scl_peaks == tp):
                peak_lags_i.append( obs_lag_time[k].copy() )
            else:
                trough_lags_i.append( obs_lag_time[k].copy() )

        if len(peak_lags_i) > 1:
            peak_lags[i] = np.array(peak_lags_i[1:]).mean()
        else:
            peak_lags[i] = np.nan

        if len(trough_lags_i) > 1:
            trough_lags[i] = np.array(trough_lags_i[1:]).mean()
        else:
            trough_lags[i] = np.nan

        tps.append( obs_tps )

    if period:
        for i in range(1,len(val[0,:])):
            while (peak_lags[i] - peak_lags[i-1]) > 0.5*period:
                peak_lags[i] -= period
            while (trough_lags[i] - trough_lags[i-1]) > 0.5*period:
                trough_lags[i] -= period
        for i in range(len(val[0,:])-2,0,-1):
            while (peak_lags[i] - peak_lags[i+1]) > 0.5*period:
                peak_lags[i] -= period
            while (trough_lags[i] - trough_lags[i+1]) > 0.5*period:
                trough_lags[i] -= period

    if full:
        return {'plags': peak_lags, 'tlags': trough_lags, 'obs_tps': tps, 'scl_tps': scl_tps, 'scl_p': scl_peaks, 'scl_t': scl_troughs}
    else:
        return (peak_lags + trough_lags)/2.
        
def find_network_lag(net, prop, time, scale, period, can_lead=False):
    
    # Initial attempt
    lag = [np.zeros(len(seg.x)) for seg in net.list_of_LongProfile_objects]
    for seg in net.list_of_LongProfile_objects:
        lag[seg.ID] = find_lag_times(prop[seg.ID], time, scale, period=period, can_lead=can_lead) / period
    
    # Check for cycle-skipped segment
    completed_segs = []
    for segID in net.list_of_channel_head_segment_IDs:
        while net.list_of_LongProfile_objects[segID].downstream_segment_IDs:
            down_segID = net.list_of_LongProfile_objects[segID].downstream_segment_IDs[0]
            if down_segID not in completed_segs:
                if (lag[down_segID][0] - lag[segID][-1]) > 0.5:
                    lag[down_segID] -= 1.
                completed_segs.append(down_segID)
            segID = down_segID
    
    return lag

def find_lag_time_single(val, time, scale, threshold=0., can_lead=False, period=False, full=False):
    
    scl_peaks, __ = find_peaks(scale)
    scl_troughs, __ = find_peaks(-scale)
    scl_tps = np.sort( np.hstack(( scl_peaks, scl_troughs )) )

    obs_peaks, __ = find_peaks(val)
    obs_troughs, __ = find_peaks(-val)
    obs_tps = np.sort( np.hstack(( obs_peaks, obs_troughs )) )
    # plt.plot(val/val.mean())
    # plt.plot(1+scale/scale.mean()*(val.max()-val.mean())/val.mean(), ":")
    # plt.scatter(obs_peaks,val[obs_peaks]/val.mean())
    # plt.scatter(obs_troughs,val[obs_troughs]/val.mean())
    # plt.show()
    if not can_lead:
        obs_tps = obs_tps[ np.where( obs_tps >= scl_tps[0] ) ]
    
    obs_tps_attached = np.zeros( len(obs_tps), dtype=int )
    obs_lag_time = np.zeros( len(obs_tps), dtype=int )

    for j,tp in enumerate(obs_tps):
        if j > len(scl_tps)-1:
            continue
        obs_tps_attached[j] = scl_tps[j]
        obs_lag_time[j] = time[tp] - time[scl_tps[j]]
        
    peak_lags_i = []
    trough_lags_i = []

    for k,tp in enumerate(obs_tps_attached):

        if obs_lag_time[k] != 0.:
            if any(scl_peaks == tp):
                peak_lags_i.append( obs_lag_time[k].copy() )
            else:
                trough_lags_i.append( obs_lag_time[k].copy() )

    if len(peak_lags_i) > 1:
        peak_lags = np.array(peak_lags_i[1:]).mean()
    else:
        peak_lags = np.nan

    if len(trough_lags_i) > 1:
        trough_lags = np.array(trough_lags_i[1:]).mean()
    else:
        trough_lags = np.nan
    
    return (peak_lags + trough_lags)/2.


# ---- Linear part
L = 100.e3
mean_Q = 10.
mean_Qs = 0.001
B = 98.1202038813591
S0 = (mean_Qs / (0.040987384904837776 * mean_Q))**(6./7.)
lp = LongProfile()
lp.basic_constants()
lp.bedload_lumped_constants()
lp.set_hydrologic_constants()
dx = 1.e3
x = [np.arange(0., L, dx)]
S0 = [(mean_Qs/(lp.k_Qs*mean_Q))**(6./7.)]
upstream_segment_IDs = [[]]
downstream_segment_IDs = [[]]
z = [(x[0].max()-x[0])*S0]
Q = [np.full(len(x),mean_Q)]
B = [np.full(len(x),B)]
net = Network()
net.initialize(
    config_file = None,
    x_bl =L,
    z_bl = 0.,
    S0 = S0,
    upstream_segment_IDs = upstream_segment_IDs,
    downstream_segment_IDs = downstream_segment_IDs,
    x = x,
    z = z,
    Q = Q,
    B = B,
    overwrite = False
    )
net.set_niter(3)
net.get_z_lengths()
diff = (7./6.) * lp.k_Qs * mean_Q * (S0[0]**(1./6.)) / (B[0] * (1. - lp.lambda_p))
lp = net.list_of_LongProfile_objects[0]
lp.compute_equilibration_time()

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
lags = {}
for sweep in indirs.keys():
    sweep_nets, sweep_hacks, sweep_gains, sweep_lags = read_sweep(indirs[sweep])
    nets[sweep] = sweep_nets
    hacks[sweep] = sweep_hacks
    gains[sweep] = sweep_gains
    lags[sweep] = sweep_lags

# ---- LINEAR GAIN
lin_periods = np.logspace(-2.5, 2.5, 81) * lp.equilibration_time
lin_gain_z = [lp.compute_z_gain(p)[-1] for p in lin_periods]
lin_lag_z = [lp.compute_z_lag(p)[-1]/p for p in lin_periods]
lin_gain_Qs = [lp.compute_Qs_gain(p, A_Qs=0.2)[-1] for p in lin_periods]
lin_lag_Qs = [lp.compute_Qs_lag(p, A_Qs=0.2)[-1]/p for p in lin_periods]
lin_gain_Qs_Qw = [lp.compute_Qs_gain(p, A_Q=0.2)[-1] for p in lin_periods]
lin_lag_Qs_Qw = [lp.compute_Qs_lag(p, A_Q=0.2)[-1]/p for p in lin_periods]

# # ---- Continuous Gain
# continuous_z_gains = {}
# continuous_z_lags = {}
# continuous_Qs_gains = {}
# continuous_Qs_lags = {}
# continuous_ps = [0.5, 1.]
# continuous_periods = np.logspace(-2.5, 2.5, 19) * lp.equilibration_time
# for i,p in enumerate(continuous_ps):
#     net = set_up_long_profile(L, mean_Q, mean_Qs, 1/p, B[0], dx=1.e3, evolve=True)
#     z_gs = {'Qs': [], 'Qw': []}
#     z_ls = {'Qs': [], 'Qw': []}
#     Qs_gs = {'Qs': [], 'Qw': []}
#     Qs_ls = {'Qs': [], 'Qw': []}
#     for period in continuous_periods:
#         for lab, A_Qs, A_Qw, can_lead in zip(['Qs','Qw'], [0.2,0.], [0.,0.2], [False,True]):
#             print(p,period,lab)
#             z, Qs, time, scale = evolve_network_periodic(deepcopy(net), period, A_Qs, A_Qw)
#             z_g = compute_network_z_gain(net, z, A_Qs, A_Qw, S0)
#             Qs_g = compute_network_Qs_gain(net, Qs, A_Qs, A_Qw, [q[0,:] for q in Qs])
#             z_l = find_network_lag(net, z, time, scale, period)
#             Qs_l = find_lag_time_single(Qs[0][:,-1], time, scale, period, can_lead=can_lead)/period
#             if Qs_l < -0.5:
#                 Qs_l = np.nan
#             z_gs[lab].append(z_g[0][-1])
#             z_ls[lab].append(z_l[0][-1])
#             Qs_gs[lab].append(Qs_g[0][-1])
#             Qs_ls[lab].append(Qs_l)
#     continuous_z_gains[p] = z_gs
#     continuous_z_lags[p] = z_ls
#     continuous_Qs_gains[p] = Qs_gs
#     continuous_Qs_lags[p] = Qs_ls

# ---- Plot
fig, axs = plt.subplots(len(indirs.keys()),6,sharex=True)
axs[0,0].set_xscale("log")

for i,sweep in enumerate(indirs.keys()):
    
    sweep_periods = np.hstack([g['P']/g['Teq_Qs'] for g in gains[sweep]])
    sweep_mags = np.hstack([np.full(len(gains[sweep][j]['P']), len(n.streams_by_order[1])) for j,n in enumerate(nets[sweep])])
    
    # axs[i,0].fill(
    #     np.hstack(( continuous_periods, continuous_periods[::-1] ))/lp.equilibration_time,
    #     np.hstack(( continuous_z_gains[0.5]['Qs'], continuous_z_gains[1]['Qs'][::-1] )),
    #     c="lightgrey"
    #     )
    # axs[i,0].plot(continuous_periods/lp.equilibration_time, continuous_z_gains[0.5]['Qs'], "--", c="grey")
    # axs[i,0].plot(continuous_periods/lp.equilibration_time, continuous_z_gains[1]['Qs'], "--", c="grey")
    axs[i,0].plot(lin_periods/lp.equilibration_time, lin_gain_z, c="black")
    if i < 2:
        sweep_gains = [g['G_z'][j][0][-1] for g in gains[sweep] for j in range(len(g['P']))]
    else:
        sweep_gains = [g['G_z']['Qs'][j][0][-1] for g in gains[sweep] for j in range(len(g['P']))]
    axs[i,0].scatter(
        sweep_periods,
        sweep_gains,
        alpha=0.1,
        c=sweep_mags
        )    
    
    # axs[i,1].fill(
    #     np.hstack(( continuous_periods, continuous_periods[::-1] ))/lp.equilibration_time,
    #     np.hstack(( continuous_z_lags[0.5]['Qs'], continuous_z_lags[1]['Qs'][::-1] )),
    #     c="lightgrey"
    #     )
    # axs[i,1].plot(continuous_periods/lp.equilibration_time, continuous_z_lags[0.5]['Qs'], "--", c="grey")
    # axs[i,1].plot(continuous_periods/lp.equilibration_time, continuous_z_lags[1]['Qs'], "--", c="grey")
    axs[i,1].plot(lin_periods/lp.equilibration_time, lin_lag_z, c="black")
    axs[i,1].set_ylim(-0.05,0.95)
    if i < 2:
        sweep_lags = [l['lag_z'][j][0][-1] for l in lags[sweep] for j in range(len(l['P']))]
    else:
        sweep_lags = [l['lag_z']['Qs'][j][0][-1] for l in lags[sweep] for j in range(len(l['P']))]
    axs[i,1].scatter(
        sweep_periods,
        sweep_lags,
        alpha=0.1,
        c=sweep_mags
        ) 
    
    # axs[i,2].fill(
    #     np.hstack(( continuous_periods, continuous_periods[::-1] ))/lp.equilibration_time,
    #     np.hstack(( continuous_Qs_gains[0.5]['Qs'], continuous_Qs_gains[1]['Qs'][::-1] )),
    #     c="lightgrey"
    #     )
    # axs[i,2].plot(continuous_periods/lp.equilibration_time, continuous_Qs_gains[0.5]['Qs'], "--", c="grey")
    # axs[i,2].plot(continuous_periods/lp.equilibration_time, continuous_Qs_gains[1]['Qs'], "--", c="grey")
    axs[i,2].plot(lin_periods/lp.equilibration_time, lin_gain_Qs, c="black")
    if i < 2:
        sweep_gains = [g['G_Qs'][j][0][-1] for g in gains[sweep] for j in range(len(g['P']))]
    else:
        sweep_gains = [g['G_Qs']['Qs'][j][0][-1] for g in gains[sweep] for j in range(len(g['P']))]
    axs[i,2].scatter(
        sweep_periods,
        sweep_gains,
        alpha=0.1,
        c=sweep_mags
        )    

    # nonnans_a = np.where(~np.isnan(continuous_Qs_lags[0.5]['Qs']))
    # nonnans_b = np.where(~np.isnan(continuous_Qs_lags[1]['Qs']))
    # axs[i,3].fill(
    #     np.hstack(( continuous_periods[nonnans_a], continuous_periods[nonnans_b][::-1] ))/lp.equilibration_time,
    #     np.hstack(( np.array(continuous_Qs_lags[0.5]['Qs'])[nonnans_a], np.array(continuous_Qs_lags[1]['Qs'])[nonnans_b][::-1] )),
    #     c="lightgrey"
    #     )
    # axs[i,3].plot(continuous_periods/lp.equilibration_time, continuous_Qs_lags[0.5]['Qs'], "--", c="grey")
    # axs[i,3].plot(continuous_periods/lp.equilibration_time, continuous_Qs_lags[1]['Qs'], "--", c="grey")
    axs[i,3].plot(lin_periods/lp.equilibration_time, lin_lag_Qs, c="black")
    axs[i,3].set_ylim(-0.05,0.95)
    if i < 2:
        sweep_lags = [l['lag_Qs'][j][0][-1] for l in lags[sweep] for j in range(len(l['P']))]
    else:
        sweep_lags = [l['lag_Qs']['Qs'][j] for l in lags[sweep] for j in range(len(l['P']))]
    axs[i,3].scatter(
        sweep_periods,
        sweep_lags,
        alpha=0.1,
        c=sweep_mags
        ) 

    # axs[i,4].fill(
    #     np.hstack(( continuous_periods, continuous_periods[::-1] ))/lp.equilibration_time,
    #     np.hstack(( continuous_Qs_gains[0.5]['Qw'], continuous_Qs_gains[1]['Qw'][::-1] )),
    #     c="lightgrey"
    #     )
    # axs[i,4].plot(continuous_periods/lp.equilibration_time, continuous_Qs_gains[0.5]['Qw'], "--", c="grey")
    # axs[i,4].plot(continuous_periods/lp.equilibration_time, continuous_Qs_gains[1]['Qw'], "--", c="grey")
    axs[i,4].plot(lin_periods/lp.equilibration_time, lin_gain_Qs_Qw, c="black")
    if i > 1:
        sweep_gains = [g['G_Qs']['Qw'][j][0][-1] for g in gains[sweep] for j in range(len(g['P']))]
        axs[i,4].scatter(
            sweep_periods,
            sweep_gains,
            alpha=0.1,
            c=sweep_mags
            )    

    # nonnans_a = np.where(~np.isnan(continuous_Qs_lags[0.5]['Qw']))
    # nonnans_b = np.where(~np.isnan(continuous_Qs_lags[1]['Qw']))
    # axs[i,5].fill(
    #     np.hstack(( continuous_periods[nonnans_a], continuous_periods[nonnans_b][::-1] ))/lp.equilibration_time,
    #     np.hstack(( np.array(continuous_Qs_lags[0.5]['Qw'])[nonnans_a], np.array(continuous_Qs_lags[1]['Qw'])[nonnans_b][::-1] )),
    #     c="lightgrey"
    #     )
    # axs[i,5].plot(continuous_periods/lp.equilibration_time, continuous_Qs_lags[0.5]['Qw'], "--", c="grey")
    # axs[i,5].plot(continuous_periods/lp.equilibration_time, continuous_Qs_lags[1]['Qw'], "--", c="grey")
    axs[i,5].plot(lin_periods/lp.equilibration_time, lin_lag_Qs_Qw, c="black")
    if i > 1:
        sweep_lags = [l['lag_Qs']['Qw'][j] for l in lags[sweep] for j in range(len(l['P']))]
        axs[i,5].scatter(
            sweep_periods,
            sweep_lags,
            alpha=0.1,
            c=sweep_mags
            )

plt.show()

import sys
sys.exit()

# ---- Save

basedir = "../output/network/full_sweep/"

with open(basedir + "z_linear_gain.pg", "wb") as f:
    arr = np.column_stack(( lin_periods/lp.equilibration_time, lin_gain_z ))
    np.savetxt(f, arr)
    
with open(basedir + "z_continuous_gain.pg", "wb") as f:
    arr = np.column_stack(( 
        np.hstack(( continuous_periods, continuous_periods[::-1] ))/lp.equilibration_time,
        np.hstack(( continuous_z_gains[0.5]['Qs'], continuous_z_gains[1]['Qs'][::-1] ))
        ))
    np.savetxt(f, arr)
    
with open(basedir + "z_linear_lag.pl", "wb") as f:
    arr = np.column_stack(( lin_periods/lp.equilibration_time, lin_lag_z ))
    np.savetxt(f, arr)
    
with open(basedir + "z_continuous_lag.pl", "wb") as f:
    arr = np.column_stack(( 
        np.hstack(( continuous_periods, continuous_periods[::-1] ))/lp.equilibration_time,
        np.hstack(( continuous_z_lags[0.5]['Qs'], continuous_z_lags[1]['Qs'][::-1] ))
        ))
    np.savetxt(f, arr)

with open(basedir + "Qs_linear_gain.pg", "wb") as f:
    arr = np.column_stack(( lin_periods/lp.equilibration_time, lin_gain_Qs ))
    np.savetxt(f, arr)

with open(basedir + "Qs_continuous_gain.pg", "wb") as f:
    arr = np.column_stack(( 
        np.hstack(( continuous_periods, continuous_periods[::-1] ))/lp.equilibration_time,
        np.hstack(( continuous_Qs_gains[0.5]['Qs'], continuous_Qs_gains[1]['Qs'][::-1] ))
        ))
    np.savetxt(f, arr)
    
with open(basedir + "Qs_linear_lag.pl", "wb") as f:
    arr = np.column_stack(( lin_periods/lp.equilibration_time, lin_lag_Qs ))
    np.savetxt(f, arr)

nonnans_a = np.where(~np.isnan(continuous_Qs_lags[0.5]['Qs']))
nonnans_b = np.where(~np.isnan(continuous_Qs_lags[1]['Qs']))
with open(basedir + "Qs_continuous_lag.pl", "wb") as f:
    arr = np.column_stack(( 
        np.hstack(( continuous_periods[nonnans_a], continuous_periods[nonnans_b][::-1] ))/lp.equilibration_time,
        np.hstack(( np.array(continuous_Qs_lags[0.5]['Qs'])[nonnans_a], np.array(continuous_Qs_lags[1]['Qs'])[nonnans_b][::-1] ))
        ))
    np.savetxt(f, arr)

with open(basedir + "Qs_Qw_linear_gain.pg", "wb") as f:
    arr = np.column_stack(( lin_periods/lp.equilibration_time, lin_gain_Qs_Qw ))
    np.savetxt(f, arr)
    
with open(basedir + "Qs_Qw_continuous_gain.pg", "wb") as f:
    arr = np.column_stack(( 
        np.hstack(( continuous_periods, continuous_periods[::-1] ))/lp.equilibration_time,
        np.hstack(( continuous_Qs_gains[0.5]['Qw'], continuous_Qs_gains[1]['Qw'][::-1] ))
        ))
    np.savetxt(f, arr)

with open(basedir + "Qs_Qw_linear_lag.pl", "wb") as f:
    arr = np.column_stack(( lin_periods/lp.equilibration_time, lin_lag_Qs_Qw ))
    np.savetxt(f, arr)

nonnans_a = np.where(~np.isnan(continuous_Qs_lags[0.5]['Qs']))
nonnans_b = np.where(~np.isnan(continuous_Qs_lags[1]['Qs']))
with open(basedir + "Qs_Qw_continuous_lag.pl", "wb") as f:
    arr = np.column_stack(( 
        np.hstack(( continuous_periods[nonnans_a], continuous_periods[nonnans_b][::-1] ))/lp.equilibration_time,
        np.hstack(( np.array(continuous_Qs_lags[0.5]['Qw'])[nonnans_a], np.array(continuous_Qs_lags[1]['Qw'])[nonnans_b][::-1] ))
        ))
    np.savetxt(f, arr)

outdirs = {
    "m20": "m20_fix_seg_length/",
    "m40": "m40_fix_seg_length/",
    "m2-100": "m2-100_fix_seg_length/",
    "m40_var": "m40_rnd_seg_length/"
    }

for i,sweep in enumerate(indirs.keys()):
    
    sweep_periods = np.hstack([g['P']/g['Teq_Qs'] for g in gains[sweep]])
    sweep_mags = np.hstack([np.full(len(gains[sweep][j]['P']), len(n.streams_by_order[1])) for j,n in enumerate(nets[sweep])])

    if i < 3:
        sweep_gains = [g['G_z'][j][0][-1] for g in gains[sweep] for j in range(len(g['P']))]
        sweep_gains_plus = [np.nanmax(np.hstack(g['G_z'][j]))-g['G_z'][j][0][-1] for g in gains[sweep] for j in range(len(g['P']))]
        sweep_gains_minus = [g['G_z'][j][0][-1]-np.nanmin(np.hstack(g['G_z'][j])) for g in gains[sweep] for j in range(len(g['P']))]
    else:
        sweep_gains = [g['G_z']['Qs'][j][0][-1] for g in gains[sweep] for j in range(len(g['P']))]
        sweep_gains_plus = [np.nanmax(np.hstack(g['G_z']['Qs'][j]))-g['G_z']['Qs'][j][0][-1] for g in gains[sweep] for j in range(len(g['P']))]
        sweep_gains_minus = [g['G_z']['Qs'][j][0][-1]-np.nanmin(np.hstack(g['G_z']['Qs'][j])) for g in gains[sweep] for j in range(len(g['P']))]
    with open(basedir + outdirs[sweep] + "z_gain.pg", "wb") as f:
        arr = np.column_stack(( sweep_periods, sweep_gains, sweep_mags, sweep_gains_minus, sweep_gains_plus ))
        np.savetxt(f, arr)
        
    if i < 3:
        sweep_lags = [l['lag_z'][j][0][-1] for l in lags[sweep] for j in range(len(l['P']))]
        sweep_lags_plus = [np.nanmin(np.hstack(l['lag_z'][j]))-l['lag_z'][j][0][-1] for l in lags[sweep] for j in range(len(l['P']))]
        sweep_lags_minus = [l['lag_z'][j][0][-1]-np.nanmin(np.hstack(l['lag_z'][j])) for l in lags[sweep] for j in range(len(l['P']))]
    else:
        sweep_lags = [l['lag_z']['Qs'][j][0][-1] for l in lags[sweep] for j in range(len(l['P']))]
        sweep_lags_plus = [np.nanmin(np.hstack(l['lag_z']['Qs'][j]))-l['lag_z']['Qs'][j][0][-1] for l in lags[sweep] for j in range(len(l['P']))]
        sweep_lags_minus = [l['lag_z']['Qs'][j][0][-1]-np.nanmin(np.hstack(l['lag_z']['Qs'][j])) for l in lags[sweep] for j in range(len(l['P']))]
    with open(basedir + outdirs[sweep] + "z_lag.pl", "wb") as f:
        arr = np.column_stack(( sweep_periods, sweep_lags, sweep_mags, sweep_lags_minus, sweep_lags_plus ))
        np.savetxt(f, arr)
        
    if i < 3:
        sweep_gains = [g['G_Qs'][j][0][-1] for g in gains[sweep] for j in range(len(g['P']))]
    else:
        sweep_gains = [g['G_Qs']['Qs'][j][0][-1] for g in gains[sweep] for j in range(len(g['P']))]
    with open(basedir + outdirs[sweep] + "Qs_gain.pg", "wb") as f:
        arr = np.column_stack(( sweep_periods, sweep_gains, sweep_mags ))
        np.savetxt(f, arr)
        
    if i < 3:
        sweep_lags = [l['lag_Qs'][j][0][-1] for l in lags[sweep] for j in range(len(l['P']))]
    else:
        sweep_lags = [l['lag_Qs']['Qs'][j] for l in lags[sweep] for j in range(len(l['P']))]
    with open(basedir + outdirs[sweep] + "Qs_lag.pl", "wb") as f:
        arr = np.column_stack(( sweep_periods, sweep_lags, sweep_mags ))
        np.savetxt(f, arr)
        
    if i < 3:
        sweep_gains = [g['G_Qs'][j][0][-1] for g in gains[sweep] for j in range(len(g['P']))]
    else:
        sweep_gains = [g['G_Qs']['Qw'][j][0][-1] for g in gains[sweep] for j in range(len(g['P']))]
    with open(basedir + outdirs[sweep] + "Qs_Qw_gain.pg", "wb") as f:
        arr = np.column_stack(( sweep_periods, sweep_gains, sweep_mags ))
        np.savetxt(f, arr)

    if i < 3:
        sweep_lags = [l['lag_Qs'][j][0][-1] for l in lags[sweep] for j in range(len(l['P']))]
    else:
        sweep_lags = [l['lag_Qs']['Qw'][j] for l in lags[sweep] for j in range(len(l['P']))]
    with open(basedir + outdirs[sweep] + "Qs_Qw_lag.pl", "wb") as f:
        arr = np.column_stack(( sweep_periods, sweep_lags, sweep_mags ))
        np.savetxt(f, arr)