"""
This script performs the analysis presented in Figure 9 of McNab et al. (2024,
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
indirs = {
    "MC_N1_40": "../../Output/Network/MC_N1_40/",
    "MC_N1_2-102": "../../Output/Network/MC_N1_2-102/"
    }


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
nets = {}
hacks = {}
gains = {}
lags = {}
for N1 in indirs.keys():
    nets[N1], hacks[N1], gains[N1], lags[N1] = grlpx.read_MC(indirs[N1])


# ---- LINEAR
lin_periods = np.logspace(-2.5, 2.5, 81) * lp.equilibration_time
lin_periodics = {}
lin_periodics_Q = {}
lin_periodics['z_gain'] = [lp.compute_z_gain(p)[-1] for p in lin_periods]
lin_periodics['z_gain_up'] = [lp.compute_z_gain(p)[0] for p in lin_periods]
lin_periodics['z_lag'] = [lp.compute_z_lag(p, nsum=10000)[-1]/p for p in lin_periods]
lin_periodics['z_lag_up'] = [lp.compute_z_lag(p, nsum=10000)[0]/p for p in lin_periods]
lin_periodics['Qs_gain'] = [lp.compute_Qs_gain(p, A_Qs=0.2)[-1] for p in lin_periods]
lin_periodics['Qs_lag'] = [lp.compute_Qs_lag(p, A_Qs=0.2)[-1]/p for p in lin_periods]
lin_periodics_Q['Qs_gain'] = [lp.compute_Qs_gain(p, A_Q=0.2)[-1] for p in lin_periods]
lin_periodics_Q['Qs_lag'] = [lp.compute_Qs_lag(p, A_Q=0.2)[-1]/p for p in lin_periods]


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

def plot_main(lin_periods, lin_periodics, lin_periodics_Q, cont_periods, cont_periodics, cont_periodics_Q, gains, lags):

    # Set up plot.
    fig, axs = plt.subplots(6, 4, sharey="row", sharex=True)

    # Loop over network cases.
    for i,case in enumerate(['UUU', 'NUU', 'UAU', 'NAU']):
        
        Teqs = [gs[case]['Teq'] for gs in gains]
        
        # Plot gain as a function of forcing period.
        # This time normalise by empirically optimised equilibration time.
        axs[0,i].fill(
            np.hstack(( lin_periods, lin_periods[::-1] ))/lp.equilibration_time,
            np.hstack(( lin_periodics['z_gain'], lin_periodics['z_gain_up'][::-1] )),
            c="0.6",
            alpha=0.5
            )
        axs[0,i].plot(lin_periods/lp.equilibration_time, lin_periodics['z_gain'], "k")
        axs[0,i].fill(
            np.hstack(( cont_periods, cont_periods[::-1] ))/lp.equilibration_time,
            np.hstack((
                np.column_stack((
                    [p['G_z'][0].min() for p in cont_periodics[1.4]],
                    [p['G_z'][0].min() for p in cont_periodics[2.2]]
                    )).min(axis=1),
                np.column_stack((
                    [p['G_z'][0].max() for p in cont_periodics[1.4]],
                    [p['G_z'][0].max() for p in cont_periodics[2.2]]
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
            np.hstack(( lin_periodics['z_lag'], lin_periodics['z_lag_up'][::-1] )),
            c="0.6",
            alpha=0.5
            )
        axs[1,i].plot(lin_periods/lp.equilibration_time, lin_periodics['z_lag'], "k")
        axs[1,i].fill(
            np.hstack(( cont_periods, cont_periods[::-1] ))/lp.equilibration_time,
            np.hstack((
                np.column_stack((
                    [p['lag_z'][0].min() for p in cont_periodics[1.4]],
                    [p['lag_z'][0].min() for p in cont_periodics[2.2]]
                    )).min(axis=1),
                np.column_stack((
                    [p['lag_z'][0].max() for p in cont_periodics[1.4]],
                    [p['lag_z'][0].max() for p in cont_periodics[2.2]]
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
        axs[2,i].plot(lin_periods/lp.equilibration_time, lin_periodics['Qs_gain'], "k")
        axs[2,i].fill(
            np.hstack(( cont_periods, cont_periods[::-1] ))/lp.equilibration_time,
            np.hstack((
                np.column_stack((
                    [p['G_Qs'][0][-1] for p in cont_periodics[1.4]],
                    [p['G_Qs'][0][-1] for p in cont_periodics[2.2]]
                    )).min(axis=1),
                np.column_stack((
                    [p['G_Qs'][0][-1] for p in cont_periodics[1.4]],
                    [p['G_Qs'][0][-1] for p in cont_periodics[2.2]]
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
        axs[3,i].plot(lin_periods/lp.equilibration_time, lin_periodics['Qs_lag'], "k")
        axs[3,i].fill(
            np.hstack(( cont_periods, cont_periods[::-1] ))/lp.equilibration_time,
            np.hstack((
                np.column_stack((
                    [p['lag_Qs'] for p in cont_periodics[1.4]],
                    [p['lag_Qs'] for p in cont_periodics[2.2]]
                    )).min(axis=1),
                np.column_stack((
                    [p['lag_Qs'] for p in cont_periodics[1.4]],
                    [p['lag_Qs'] for p in cont_periodics[2.2]]
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
        axs[4,i].plot(lin_periods/lp.equilibration_time, lin_periodics_Q['Qs_gain'], "k")
        axs[4,i].fill(
            np.hstack(( cont_periods, cont_periods[::-1] ))/lp.equilibration_time,
            np.hstack((
                np.column_stack((
                    [p['G_Qs'][0][-1] for p in cont_periodics_Q[1.4]],
                    [p['G_Qs'][0][-1] for p in cont_periodics_Q[2.2]]
                    )).min(axis=1),
                np.column_stack((
                    [p['G_Qs'][0][-1] for p in cont_periodics_Q[1.4]],
                    [p['G_Qs'][0][-1] for p in cont_periodics_Q[2.2]]
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
        axs[5,i].plot(lin_periods/lp.equilibration_time, lin_periodics_Q['Qs_lag'], "k")
        axs[5,i].fill(
            np.hstack(( cont_periods, cont_periods[::-1] ))/lp.equilibration_time,
            np.hstack((
                np.column_stack((
                    [p['lag_Qs'] for p in cont_periodics_Q[1.4]],
                    [p['lag_Qs'] for p in cont_periodics_Q[2.2]]
                    )).min(axis=1),
                np.column_stack((
                    [p['lag_Qs'] for p in cont_periodics_Q[1.4]],
                    [p['lag_Qs'] for p in cont_periodics_Q[2.2]]
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
    
    
def plot_supp(lin_periods, lin_periodics, lin_periodics_Q, cont_periods, cont_periodics, cont_periodics_Q, gains, lags):
    
    # Set up plot.
    fig, axs = plt.subplots(2, 4, sharey="row", sharex=True)

    # Loop over network cases.
    for i,case in enumerate(['UUU', 'NUU', 'UAU', 'NAU']):
        
        Teqs = [gs[case]['Teq'] for gs in gains]
        
        # Plot gain as a function of forcing period.
        # This time normalise by empirically optimised equilibration time.
        axs[0,i].fill(
            np.hstack(( lin_periods, lin_periods[::-1] ))/lp.equilibration_time,
            np.hstack(( lin_periodics['z_gain'], lin_periodics['z_gain_up'][::-1] )),
            c="0.6",
            alpha=0.5
            )
        axs[0,i].plot(lin_periods/lp.equilibration_time, lin_periodics['z_gain'], "k")
        axs[0,i].fill(
            np.hstack(( cont_periods, cont_periods[::-1] ))/lp.equilibration_time,
            np.hstack((
                np.column_stack((
                    [p['G_z'][0].min() for p in cont_periodics_Q[1.4]],
                    [p['G_z'][0].min() for p in cont_periodics_Q[2.2]]
                    )).min(axis=1),
                np.column_stack((
                    [p['G_z'][0].max() for p in cont_periodics_Q[1.4]],
                    [p['G_z'][0].max() for p in cont_periodics_Q[2.2]]
                    )).max(axis=1)[::-1],    
                )),
            c=(1,0.5,0.5),
            alpha=0.5
            )
        axs[0,i].errorbar(
            [p/Teqs[i] for i,gs in enumerate(gains) for p in gs[case]['P']],
            [g[0][-1] for gs in gains for g in gs[case]['G_z']['Qw']],
            yerr=[ [g[0][-1]-np.hstack(g).min() for gs in gains for g in gs[case]['G_z']['Qw']],
              [np.hstack(g).max()-g[0][-1] for gs in gains for g in gs[case]['G_z']['Qw']] ],
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
            np.hstack(( lin_periodics['z_lag'], lin_periodics['z_lag_up'][::-1] )),
            c="0.6",
            alpha=0.5
            )
        axs[1,i].plot(lin_periods/lp.equilibration_time, lin_periodics['z_lag'], "k")
        axs[1,i].fill(
            np.hstack(( cont_periods, cont_periods[::-1] ))/lp.equilibration_time,
            np.hstack((
                np.column_stack((
                    [p['lag_z'][0].min() for p in cont_periodics_Q[1.4]],
                    [p['lag_z'][0].min() for p in cont_periodics_Q[2.2]]
                    )).min(axis=1),
                np.column_stack((
                    [p['lag_z'][0].max() for p in cont_periodics_Q[1.4]],
                    [p['lag_z'][0].max() for p in cont_periodics_Q[2.2]]
                    )).max(axis=1)[::-1],    
                )),
            c=(1,0.5,0.5),
            alpha=0.5
            )
        axs[1,i].errorbar(
            [p/Teqs[i] for i,gs in enumerate(lags) for p in gs[case]['P']],
            [l[0][-1] for ls in lags for l in ls[case]['lag_z']['Qw']],
            yerr=[ [l[0][-1]-np.hstack(l).min() for ls in lags for l in ls[case]['lag_z']['Qw']],
              [np.hstack(l).max()-l[0][-1] for ls in lags for l in ls[case]['lag_z']['Qw']] ],
            fmt="o",
            alpha=0.05,
            color="steelblue"
            )
        if i==0:
            axs[1,i].set_ylabel("Lag, $L_{Q_s,L}$ [-]")
        axs[1,i].set_ylim(-0.1,1.1)
        axs[1,i].set_xscale("log")
        axs[1,i].set_xlabel(r"Period, $P$ / $\widehat{T_{eq}}$ [-]")

    # Format and show.
    for row in axs:
        for ax in row:
            ax.set_box_aspect(1)
    plt.show()


for N1 in indirs.keys():
    
    plot_main(
        lin_periods, lin_periodics, lin_periodics_Q,
        continuous_periods, continuous_periodics, continuous_periodics_Q,
        gains[N1], lags[N1]
        )
        
    plot_supp(
        lin_periods, lin_periodics, lin_periodics_Q,
        continuous_periods, continuous_periodics, continuous_periodics_Q,
        gains[N1], lags[N1]
        )

# ---- Save

if output_gmt:

    basedir = "../../Output/Network/Figure_9_S5_S6_S7_Network_Full_Gain_Lag/"

    with open(basedir + "z_linear_gain.pg", "wb") as f:
        arr = np.column_stack(( lin_periods/lp.equilibration_time, lin_periodics['z_gain'] ))
        np.savetxt(f, arr)
        
    with open(basedir + "z_linear_gain_rng.pg", "wb") as f:
        arr = np.column_stack(( 
            np.hstack(( lin_periods, lin_periods[::-1] ))/lp.equilibration_time,
            np.hstack(( lin_periodics['z_gain'], lin_periodics['z_gain_up'][::-1] ))
            ))
        np.savetxt(f, arr)
        
    with open(basedir + "z_continuous_gain.pg", "wb") as f:
        arr = np.column_stack(( 
            np.hstack((
                continuous_periods,
                continuous_periods[::-1]
                ))/lp.equilibration_time,
            np.hstack((
                np.column_stack((
                    [p['G_z'][0].min() for p in continuous_periodics[1.4]],
                    [p['G_z'][0].min() for p in continuous_periodics[2.2]]
                    )).min(axis=1),
                np.column_stack((
                    [p['G_z'][0].max() for p in continuous_periodics[1.4]],
                    [p['G_z'][0].max() for p in continuous_periodics[2.2]]
                    )).max(axis=1)[::-1],    
                ))
            ))
        np.savetxt(f, arr)
        
    with open(basedir + "z_Q_continuous_gain.pg", "wb") as f:
        arr = np.column_stack(( 
            np.hstack((
                continuous_periods,
                continuous_periods[::-1]
                ))/lp.equilibration_time,
            np.hstack((
                np.column_stack((
                    [p['G_z'][0].min() for p in continuous_periodics_Q[1.4]],
                    [p['G_z'][0].min() for p in continuous_periodics_Q[2.2]]
                    )).min(axis=1),
                np.column_stack((
                    [p['G_z'][0].max() for p in continuous_periodics_Q[1.4]],
                    [p['G_z'][0].max() for p in continuous_periodics_Q[2.2]]
                    )).max(axis=1)[::-1],    
                ))
            ))
        np.savetxt(f, arr)
        
    with open(basedir + "z_linear_lag.pl", "wb") as f:
        arr = np.column_stack(( lin_periods/lp.equilibration_time, lin_periodics['z_lag'] ))
        np.savetxt(f, arr)

    with open(basedir + "z_linear_lag_rng.pl", "wb") as f:
        arr = np.column_stack(( 
            np.hstack(( lin_periods, lin_periods[::-1] ))/lp.equilibration_time,
            np.hstack(( lin_periodics['z_lag'], lin_periodics['z_lag_up'][::-1] ))
            ))
        np.savetxt(f, arr)        

    with open(basedir + "z_continuous_lag.pl", "wb") as f:
        arr = np.column_stack(( 
            np.hstack((
                continuous_periods,
                continuous_periods[::-1]
                ))/lp.equilibration_time,
            np.hstack((
                np.column_stack((
                    [p['lag_z'][0].min() for p in continuous_periodics[1.4]],
                    [p['lag_z'][0].min() for p in continuous_periodics[2.2]]
                    )).min(axis=1),
                np.column_stack((
                    [p['lag_z'][0].max() for p in continuous_periodics[1.4]],
                    [p['lag_z'][0].max() for p in continuous_periodics[2.2]]
                    )).max(axis=1)[::-1],    
                ))
            ))
        np.savetxt(f, arr)
        
    with open(basedir + "z_Q_continuous_lag.pl", "wb") as f:
        arr = np.column_stack(( 
            np.hstack((
                continuous_periods,
                continuous_periods[::-1]
                ))/lp.equilibration_time,
            np.hstack((
                np.column_stack((
                    [p['lag_z'][0].min() for p in continuous_periodics_Q[1.4]],
                    [p['lag_z'][0].min() for p in continuous_periodics_Q[2.2]]
                    )).min(axis=1),
                np.column_stack((
                    [p['lag_z'][0].max() for p in continuous_periodics_Q[1.4]],
                    [p['lag_z'][0].max() for p in continuous_periodics_Q[2.2]]
                    )).max(axis=1)[::-1],    
                ))
            ))
        np.savetxt(f, arr)

    with open(basedir + "Qs_linear_gain.pg", "wb") as f:
        arr = np.column_stack((
            lin_periods/lp.equilibration_time,
            lin_periodics['Qs_gain'] ))
        np.savetxt(f, arr)

    with open(basedir + "Qs_continuous_gain.pg", "wb") as f:
        arr = np.column_stack(( 
            np.hstack((
                continuous_periods,
                continuous_periods[::-1]
                ))/lp.equilibration_time,
            np.hstack((
                np.column_stack((
                    [p['G_Qs'][0][-1].min() for p in continuous_periodics[1.4]],
                    [p['G_Qs'][0][-1].min() for p in continuous_periodics[2.2]]
                    )).min(axis=1),
                np.column_stack((
                    [p['G_Qs'][0][-1].max() for p in continuous_periodics[1.4]],
                    [p['G_Qs'][0][-1].max() for p in continuous_periodics[2.2]]
                    )).max(axis=1)[::-1],    
                ))
            ))
        np.savetxt(f, arr)
        
    with open(basedir + "Qs_linear_lag.pl", "wb") as f:
        arr = np.column_stack(( lin_periods/lp.equilibration_time, lin_periodics['Qs_lag'] ))
        np.savetxt(f, arr)

    with open(basedir + "Qs_continuous_lag.pl", "wb") as f:
        arr = np.column_stack(( 
            np.hstack((
                continuous_periods,
                continuous_periods[::-1]
                ))/lp.equilibration_time,
            np.hstack((
                np.column_stack((
                    [p['lag_Qs'] for p in continuous_periodics[1.4]],
                    [p['lag_Qs'] for p in continuous_periodics[2.2]]
                    )).min(axis=1),
                np.column_stack((
                    [p['lag_Qs'] for p in continuous_periodics[1.4]],
                    [p['lag_Qs'] for p in continuous_periodics[2.2]]
                    )).max(axis=1)[::-1],    
                ))
            ))
        np.savetxt(f, arr)

    with open(basedir + "Qs_Qw_linear_gain.pg", "wb") as f:
        arr = np.column_stack((
            lin_periods/lp.equilibration_time,
            lin_periodics_Q['Qs_gain']
            ))
        np.savetxt(f, arr)
        
    with open(basedir + "Qs_Qw_continuous_gain.pg", "wb") as f:
        arr = np.column_stack(( 
            np.hstack((
                continuous_periods,
                continuous_periods[::-1]
                ))/lp.equilibration_time,
            np.hstack((
                np.column_stack((
                    [p['G_Qs'][0][-1] for p in continuous_periodics_Q[1.4]],
                    [p['G_Qs'][0][-1] for p in continuous_periodics_Q[2.2]]
                    )).min(axis=1),
                np.column_stack((
                    [p['G_Qs'][0][-1] for p in continuous_periodics_Q[1.4]],
                    [p['G_Qs'][0][-1] for p in continuous_periodics_Q[2.2]]
                    )).max(axis=1)[::-1],    
                ))
            ))
        np.savetxt(f, arr)

    with open(basedir + "Qs_Qw_linear_lag.pl", "wb") as f:
        arr = np.column_stack((
            lin_periods/lp.equilibration_time,
            lin_periodics_Q['Qs_lag']
            ))
        np.savetxt(f, arr)

    with open(basedir + "Qs_Qw_continuous_lag.pl", "wb") as f:
        arr = np.column_stack(( 
            np.hstack((
                continuous_periods,
                continuous_periods[::-1]
                ))/lp.equilibration_time,
            np.hstack((
                np.column_stack((
                    [p['lag_Qs'] for p in continuous_periodics_Q[1.4]],
                    [p['lag_Qs'] for p in continuous_periodics_Q[2.2]]
                    )).min(axis=1),
                np.column_stack((
                    [p['lag_Qs'] for p in continuous_periodics_Q[1.4]],
                    [p['lag_Qs'] for p in continuous_periodics_Q[2.2]]
                    )).max(axis=1)[::-1],    
                ))
            ))
        np.savetxt(f, arr)        


    for N1 in indirs.keys():
        
        for case in ['UUU', 'NUU', 'UAU', 'NAU']:
            
            Teqs = [gs[case]['Teq'] for gs in gains[N1]]
            
            with open(basedir + N1 + "/" + case + "/z_gain.pg", "wb") as f:
                arr = np.column_stack((
                    [p/Teqs[i] for i,gs in enumerate(gains[N1]) for p in gs[case]['P']],
                    [g[0][-1] for gs in gains[N1] for g in gs[case]['G_z']['Qs']],
                    [g[0][-1]-np.hstack(g).min() for gs in gains[N1] for g in gs[case]['G_z']['Qs']],
                    [np.hstack(g).max()-g[0][-1] for gs in gains[N1] for g in gs[case]['G_z']['Qs']]
                    ))
                np.savetxt(f, arr)
            
            with open(basedir + N1 + "/" + case + "/z_lag.pl", "wb") as f:
                arr = np.column_stack((
                    [p/Teqs[i] for i,gs in enumerate(lags[N1]) for p in gs[case]['P']],
                    [l[0][-1] for ls in lags[N1] for l in ls[case]['lag_z']['Qs']],
                    [l[0][-1]-np.hstack(l).min() for ls in lags[N1] for l in ls[case]['lag_z']['Qs']],
                    [np.hstack(l).max()-l[0][-1] for ls in lags[N1] for l in ls[case]['lag_z']['Qs']]
                    ))
                np.savetxt(f, arr)
                
            with open(basedir + N1 + "/" + case + "/z_Q_gain.pg", "wb") as f:
                arr = np.column_stack((
                    [p/Teqs[i] for i,gs in enumerate(gains[N1]) for p in gs[case]['P']],
                    [g[0][-1] for gs in gains[N1] for g in gs[case]['G_z']['Qw']],
                    [g[0][-1]-np.hstack(g).min() for gs in gains[N1] for g in gs[case]['G_z']['Qw']],
                    [np.hstack(g).max()-g[0][-1] for gs in gains[N1] for g in gs[case]['G_z']['Qw']]
                    ))
                np.savetxt(f, arr)
            
            with open(basedir + N1 + "/" + case + "/z_Q_lag.pl", "wb") as f:
                arr = np.column_stack((
                    [p/Teqs[i] for i,gs in enumerate(lags[N1]) for p in gs[case]['P']],
                    [l[0][-1] for ls in lags[N1] for l in ls[case]['lag_z']['Qw']],
                    [l[0][-1]-np.hstack(l).min() for ls in lags[N1] for l in ls[case]['lag_z']['Qw']],
                    [np.hstack(l).max()-l[0][-1] for ls in lags[N1] for l in ls[case]['lag_z']['Qw']]
                    ))
                np.savetxt(f, arr)

                
            with open(basedir + N1 + "/" + case + "/Qs_gain.pg", "wb") as f:
                arr = np.column_stack((
                    [p/Teqs[i] for i,gs in enumerate(gains[N1]) for p in gs[case]['P']],
                    [g[0][-1] for gs in gains[N1] for g in gs[case]['G_Qs']['Qs']]
                    ))
                np.savetxt(f, arr)
                
            with open(basedir + N1 + "/" + case + "/Qs_lag.pl", "wb") as f:
                arr = np.column_stack((
                    [p/Teqs[i] for i,ls in enumerate(lags[N1]) for p in ls[case]['P']],
                    [l for ls in lags[N1] for l in ls[case]['lag_Qs']['Qs']]
                    ))
                np.savetxt(f, arr)
                
            with open(basedir + N1 + "/" + case + "/Qs_Qw_gain.pg", "wb") as f:
                arr = np.column_stack((
                    [p/Teqs[i] for i,gs in enumerate(gains[N1]) for p in gs[case]['P']],
                    [g[0][-1] for gs in gains[N1] for g in gs[case]['G_Qs']['Qw']]
                    ))
                np.savetxt(f, arr)
                
            with open(basedir + N1 + "/" + case + "/Qs_Qw_lag.pl", "wb") as f:
                arr = np.column_stack((
                    [p/Teqs[i] for i,ls in enumerate(lags[N1]) for p in ls[case]['P']],
                    [l for ls in lags[N1] for l in ls[case]['lag_Qs']['Qw']]
                    ))
                np.savetxt(f, arr)