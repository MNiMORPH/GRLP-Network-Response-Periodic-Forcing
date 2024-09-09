"""
This script performs the analysis presented in Figure 8 of McNab et al. (2024,
EGUsphere); produces a rough version of the Figure; and, optionally, generates
output files for plotting the final Figure in GMT.

The purpose of the script/figure is to .
"""


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
indir = "../../Output/Network/MC_N1_40/"


# ---- Linear part
x0 = 50.e3
L = 100.e3
Q_mean = 26.
Qs_mean = Q_mean * 1.e-4
B_mean = 254.
net = grlpx.generate_single_segment_network(
    L=L,
    Q_mean=Q_mean,
    Qs_mean=Qs_mean,
    B_mean=B_mean,
    p_Q=0,
    p_B=0,
    x0=x0,
    dx=5.e2,
    evolve=True
    )
lp = net.list_of_LongProfile_objects[0]
lp.compute_equilibration_time()


# ---- Read data
print("Reading results.")
nets, hacks, gains, lags = grlpx.read_MC(indir)


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
continuous_periods = np.logspace(-2.5, 2.5, 3) * lp.equilibration_time
for i,p in enumerate(continuous_ps):
    net = grlpx.generate_single_segment_network(
        L=L,
        Q_mean=Q_mean,
        Qs_mean=Qs_mean,
        B_mean=B_mean,
        p_Q=p,
        p_B=0,
        x0=x0,
        dx=5.e2,
        evolve=True
        )
    gs = []
    for period in continuous_periods:
        print(p,period)
        periodic = grlpx.evolve_network_periodic(
            copy.deepcopy(net), period, 0.2, 0.
            )
        continuous_periodics[p].append(periodic)
        periodic = grlpx.evolve_network_periodic(
            copy.deepcopy(net), period, 0., 0.2
            )
        continuous_periodics_Q[p].append(periodic)


# ---- Plot
print("Plotting.")

# Set up plot.
fig, axs = plt.subplots(6, 4, sharey="row", sharex=True)

# Loop over network cases.
for i,case in enumerate(nets[0].keys()):
    
    Teqs = [gs[case]['Teq'] for gs in gains]
    
    # Plot gain as a function of forcing period.
    # This time normalise by empirically optimised equilibration time.
    axs[0,i].fill(
        np.hstack(( lin_periods, lin_periods[::-1] ))/lp.equilibration_time,
        np.hstack(( lin_gain_z, lin_gain_z_up[::-1] )),
        c="0.6",
        alpha=0.5
        )
    axs[0,i].plot(lin_periods/lp.equilibration_time, lin_gain_z, "k")
    axs[0,i].fill(
        np.hstack(( continuous_periods, continuous_periods[::-1] ))/lp.equilibration_time,
        np.hstack((
            np.column_stack((
                [p['G_z'][0].min() for p in continuous_periodics[1.4]],
                [p['G_z'][0].min() for p in continuous_periodics[2.2]]
                )).min(axis=1),
            np.column_stack((
                [p['G_z'][0].max() for p in continuous_periodics[1.4]],
                [p['G_z'][0].max() for p in continuous_periodics[2.2]]
                )).max(axis=1)[::-1],    
            )),
        c=(1,0.5,0.5),
        alpha=0.5
        )
    axs[0,i].errorbar(
        [p/Teqs[i] for i,gs in enumerate(gains) for p in gs[case]['P']],
        [g[0][-1] for gs in gains for g in gs[case]['G_z']['Qs']],
        yerr=[ [g[0][-1]-np.hstack(g).min() for gs in gains for g in gs[case]['G_z']['Qs']],
          [np.hstack(g).max()-g[0][-1] for gs in gains for g in gs[case]['G_z']['Qs']] ],
        fmt="o",
        alpha=0.05,
        color="steelblue"
        )
    if i==0:
        axs[0,i].set_ylabel("Gain, $G_{Q_s,L}$ [-]")
    axs[0,i].set_xscale("log")
    
    # Plot lag as a function of forcing period.
    # This time normalise by empirically optimised equilibration time.
    axs[1,i].fill(
        np.hstack(( lin_periods, lin_periods[::-1] ))/lp.equilibration_time,
        np.hstack(( lin_lag_z, lin_lag_z_up[::-1] )),
        c="0.6",
        alpha=0.5
        )
    axs[1,i].plot(lin_periods/lp.equilibration_time, lin_lag_z, "k")
    axs[1,i].fill(
        np.hstack(( continuous_periods, continuous_periods[::-1] ))/lp.equilibration_time,
        np.hstack((
            np.column_stack((
                [p['lag_z'][0].min() for p in continuous_periodics[1.4]],
                [p['lag_z'][0].min() for p in continuous_periodics[2.2]]
                )).min(axis=1),
            np.column_stack((
                [p['lag_z'][0].max() for p in continuous_periodics[1.4]],
                [p['lag_z'][0].max() for p in continuous_periodics[2.2]]
                )).max(axis=1)[::-1],    
            )),
        c=(1,0.5,0.5),
        alpha=0.5
        )
    axs[1,i].errorbar(
        [p/Teqs[i] for i,gs in enumerate(lags) for p in gs[case]['P']],
        [l[0][-1] for ls in lags for l in ls[case]['lag_z']['Qs']],
        yerr=[ [l[0][-1]-np.hstack(l).min() for ls in lags for l in ls[case]['lag_z']['Qs']],
          [np.hstack(l).max()-l[0][-1] for ls in lags for l in ls[case]['lag_z']['Qs']] ],
        fmt="o",
        alpha=0.05,
        color="steelblue"
        )
    if i==0:
        axs[1,i].set_ylabel("Lag, $L_{Q_s,L}$ [-]")
    axs[1,i].set_ylim(-0.1,1.1)
    axs[1,i].set_xscale("log")


    # Plot gain as a function of forcing period.
    # This time normalise by empirically optimised equilibration time.
    Teqs = [gs[case]['Teq'] for gs in gains]
    axs[2,i].plot(lin_periods/lp.equilibration_time, lin_gain_Qs, "k")
    axs[2,i].fill(
        np.hstack(( continuous_periods, continuous_periods[::-1] ))/lp.equilibration_time,
        np.hstack((
            np.column_stack((
                [p['G_Qs'][0][-1] for p in continuous_periodics[1.4]],
                [p['G_Qs'][0][-1] for p in continuous_periodics[2.2]]
                )).min(axis=1),
            np.column_stack((
                [p['G_Qs'][0][-1] for p in continuous_periodics[1.4]],
                [p['G_Qs'][0][-1] for p in continuous_periodics[2.2]]
                )).max(axis=1)[::-1],    
            )),
        c=(1,0.5,0.5),
        alpha=0.5
        )
    axs[2,i].plot(
        [p/Teqs[i] for i,gs in enumerate(gains) for p in gs[case]['P']],
        [g[0][-1] for gs in gains for g in gs[case]['G_Qs']['Qs']],
        "o",
        alpha=0.05,
        color="steelblue"
        )
    if i==0:
        axs[2,i].set_ylabel("Gain, $G_{Q_s,L}$ [-]")
    axs[2,i].set_xscale("log")


    # Plot lag as a function of forcing period.
    # This time normalise by empirically optimised equilibration time.
    axs[3,i].plot(lin_periods/lp.equilibration_time, lin_lag_Qs, "k")
    axs[3,i].fill(
        np.hstack(( continuous_periods, continuous_periods[::-1] ))/lp.equilibration_time,
        np.hstack((
            np.column_stack((
                [p['lag_Qs'] for p in continuous_periodics[1.4]],
                [p['lag_Qs'] for p in continuous_periodics[2.2]]
                )).min(axis=1),
            np.column_stack((
                [p['lag_Qs'] for p in continuous_periodics[1.4]],
                [p['lag_Qs'] for p in continuous_periodics[2.2]]
                )).max(axis=1)[::-1],    
            )),
        c=(1,0.5,0.5),
        alpha=0.5
        )
    axs[3,i].plot(
        [p/Teqs[i] for i,ls in enumerate(lags) for p in ls[case]['P']],
        [l for ls in lags for l in ls[case]['lag_Qs']['Qs']],
        "o",
        alpha=0.05,
        color="steelblue"
        )
    if i==0:
        axs[3,i].set_ylabel("Lag, $L_{Q_s,L}$ [-]")
    axs[3,i].set_ylim(-0.1,1.1)
    axs[3,i].set_xscale("log")

    
    # Plot gain as a function of forcing period.
    # This time normalise by empirically optimised equilibration time.
    Teqs = [gs[case]['Teq'] for gs in gains]
    axs[4,i].plot(lin_periods/lp.equilibration_time, lin_gain_Qs_Qw, "k")
    axs[4,i].fill(
        np.hstack(( continuous_periods, continuous_periods[::-1] ))/lp.equilibration_time,
        np.hstack((
            np.column_stack((
                [p['G_Qs'][0][-1] for p in continuous_periodics_Q[1.4]],
                [p['G_Qs'][0][-1] for p in continuous_periodics_Q[2.2]]
                )).min(axis=1),
            np.column_stack((
                [p['G_Qs'][0][-1] for p in continuous_periodics_Q[1.4]],
                [p['G_Qs'][0][-1] for p in continuous_periodics_Q[2.2]]
                )).max(axis=1)[::-1],    
            )),
        c=(1,0.5,0.5),
        alpha=0.5
        )
    axs[4,i].plot(
        [p/Teqs[i] for i,gs in enumerate(gains) for p in gs[case]['P']],
        [g[0][-1] for gs in gains for g in gs[case]['G_Qs']['Qw']],
        "o",
        alpha=0.05,
        color="steelblue"
        )
    if i==0:
        axs[4,i].set_ylabel("Gain, $G_{Q_s,L}$ [-]")
    axs[4,i].set_xscale("log")


    # Plot lag as a function of forcing period.
    # This time normalise by empirically optimised equilibration time.
    axs[5,i].plot(lin_periods/lp.equilibration_time, lin_lag_Qs_Qw, "k")
    axs[5,i].fill(
        np.hstack(( continuous_periods, continuous_periods[::-1] ))/lp.equilibration_time,
        np.hstack((
            np.column_stack((
                [p['lag_Qs'] for p in continuous_periodics_Q[1.4]],
                [p['lag_Qs'] for p in continuous_periodics_Q[2.2]]
                )).min(axis=1),
            np.column_stack((
                [p['lag_Qs'] for p in continuous_periodics_Q[1.4]],
                [p['lag_Qs'] for p in continuous_periodics_Q[2.2]]
                )).max(axis=1)[::-1],    
            )),
        c=(1,0.5,0.5),
        alpha=0.5
        )
    axs[5,i].plot(
        [p/Teqs[i] for i,ls in enumerate(lags) for p in ls[case]['P']],
        [l for ls in lags for l in ls[case]['lag_Qs']['Qw']],
        "o",
        alpha=0.05,
        color="steelblue"
        )
    if i==0:
        axs[5,i].set_ylabel("Lag, $L_{Q_s,L}$ [-]")
    axs[5,i].set_xscale("log")
    axs[5,i].set_xlabel(r"Period, $P$ / $\widehat{T_{eq}}$ [-]")

    
# Format and show.
for row in axs:
    for ax in row:
        ax.set_box_aspect(1)
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