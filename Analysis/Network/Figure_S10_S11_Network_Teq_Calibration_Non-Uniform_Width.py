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
indirs = {
    "MC_N1_40": "../../Output/Network/MC_N1_40/",
    # "MC_N1_2-102": "../../Output/Network/MC_N1_2-102/"
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


# ---- Linear gain
lin_periods = np.logspace(-2.5, 2.5, 81) * lp.equilibration_time
lin_gain_Qs = [lp.compute_Qs_gain(p, A_Qs=0.2)[-1] for p in lin_periods]
lin_gain_Qs_Qw = [lp.compute_Qs_gain(p, A_Q=0.2)[-1] for p in lin_periods]


# ---- Continuous gain
cont_gains = {}
cont_ps = [1.4, 2.2]
cont_periods = np.logspace(-2.5, 2.5, 3) * lp.equilibration_time
for i,p in enumerate(cont_ps):
    net = grlpx.generate_single_segment_network(
        L=L,
        Q_mean=Q_mean,
        Qs_mean=Qs_mean,
        B_mean=B_mean,
        p_Q=p,
        p_B=p,
        x0=x0,
        dx=5.e2,
        evolve=True
        )
    gs = []
    for period in cont_periods:
        print(p,period)
        periodic = grlpx.evolve_network_periodic(
            copy.deepcopy(net),
            period,
            0.2,
            0.
            )
        gs.append(periodic['G_Qs'][0][-1])
    cont_gains[p] = gs


# ---- Plot
print("Plotting.")

def plot(lin_periods, lin_gain_Qs, cont_periods, cont_gains, gains, lp, title):
    
    # Set up plot.
    fig, axs = plt.subplots(3, 4, sharey="row")

    # Loop over network cases.
    for i,case in enumerate(['UUN', 'NUN', 'UAN', 'NAN']):
        
        # Plot gain as a function of forcing period, for single segment cases
        # with upstream only and along stream supply of sediment and water, and
        # for network cases.
        # Normalise by equilibration time, if calculated with length of longest
        # stream.
        axs[0,i].plot(lin_periods/lp.equilibration_time, lin_gain_Qs)
        axs[0,i].fill(
            np.hstack((cont_periods, cont_periods[::-1]))/lp.equilibration_time,
            np.hstack((cont_gains[1.4], cont_gains[2.2][::-1])),
            c="0.6"
            )
        axs[0,i].plot(
            [p/lp.equilibration_time for gs in gains for p in gs[case]['P']],
            [g[0][-1] for gs in gains for g in gs[case]['G_Qs']['Qs']],
            "o",
            alpha=0.05
            )
        axs[0,i].set_xlabel(r"Period, $P$ / $T_{eq}$ [-]")
        if i==0:
            axs[0,i].set_ylabel("Gain, $G_{Q_s,L}$ [-]")
        axs[0,i].set_xscale("log")
        
        # Plot gain as a function of forcing period.
        # This time normalise by empirically optimised equilibration time.
        Teqs = [gs[case]['Teq'] for gs in gains]
        axs[1,i].plot(lin_periods/lp.equilibration_time, lin_gain_Qs)
        axs[1,i].fill(
            np.hstack((cont_periods, cont_periods[::-1]))/lp.equilibration_time,
            np.hstack((cont_gains[1.4], cont_gains[2.2][::-1])),
            c="0.6"
            )
        axs[1,i].plot(
            [p/Teqs[i] for i,gs in enumerate(gains) for p in gs[case]['P']],
            [g[0][-1] for gs in gains for g in gs[case]['G_Qs']['Qs']],
            "o",
            alpha=0.05
            )
        axs[1,i].set_xlabel(r"Period, $P$ / $\widehat{T_{eq}}$ [-]")
        if i==0:
            axs[1,i].set_ylabel("Gain, $G_{Q_s,L}$ [-]")
        axs[1,i].set_xscale("log")
        
        # Plot counts of empirical equilibration time.
        axs[2,i].hist([Teq/3.154e10 for Teq in Teqs])
        axs[2,i].set_xlabel(r"$\widehat{T_{eq}}$ [kyr]")
        if i==0:
            axs[2,i].set_ylabel("Count")
        
    # Format and show.
    fig.suptitle(title)
    for row in axs:
        for ax in row:
            ax.set_box_aspect(1)
    plt.show()

titles = {
    'MC_N1_40': \
        r'Figure S10: Network $\widehat{T_{eq}}$ Calibration, ' + 
        '$N_1$ = 40, Variable Width',
    'MC_N1_2-102': \
        r'Figure S11: Network $\widehat{T_{eq}}$ Calibration, ' +
        '$N_1$ = 2-102, Variable Width'
    }
for N1 in indirs.keys():
    plot(
        lin_periods, lin_gain_Qs, 
        cont_periods, cont_gains, 
        gains[N1], lp, titles[N1]
        )


if output_gmt:

    # ---- Save

    basedir = "../../Output/Network/" + \
        "Figure_S10_S11_Network_Teq_Calibration_Non-Uniform_Width/"

    with open(basedir + "linear_gain.pg", "wb") as f:
        arr = np.column_stack(( lin_periods/lp.equilibration_time, lin_gain_Qs ))
        np.savetxt(f, arr)
        
    with open(basedir + "continuous_gain.pg", "wb") as f:
        arr = np.column_stack(( 
            np.hstack(( cont_periods, cont_periods[::-1] ))/lp.equilibration_time,
            np.hstack(( cont_gains[1.4], cont_gains[2.2][::-1] ))
            ))
        np.savetxt(f, arr)
    
    for N1 in indirs.keys():
        for j,case in enumerate(['UUN', 'NUN', 'UAN', 'NAN']):
            Teqs = [gs[case]['Teq'] for gs in gains[N1]]
            
            with open(basedir + N1 + "/" + case + "/gain_L.pg", "wb") as f:
                arr = np.column_stack(( 
                    [p/lp.equilibration_time for gs in gains[N1] for p in gs[case]['P']],
                    [g[0][-1] for gs in gains[N1] for g in gs[case]['G_Qs']['Qs']]
                    ))
                np.savetxt(f, arr)
                
            with open(basedir + N1 + "/" + case + "/gain_Le.pg", "wb") as f:
                arr = np.column_stack(( 
                    [p/Teqs[i] for i,gs in enumerate(gains[N1]) for p in gs[case]['P']],
                    [g[0][-1] for gs in gains[N1] for g in gs[case]['G_Qs']['Qs']]
                    ))
                np.savetxt(f, arr)
                
            with open(basedir + N1 + "/" + case + "/Teq.t", "wb") as f:
                arr = [gs[case]['Teq']/3.15e10 for gs in gains[N1]]
                np.savetxt(f, arr)