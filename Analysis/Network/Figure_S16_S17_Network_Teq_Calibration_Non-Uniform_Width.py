"""
This script performs the analysis presented in Figures S16 and S17 of McNab et
al. (2025, EGUsphere); produces a rough version of the Figures; and, optionally,
generates output files for plotting the final Figure in GMT.

The purpose of the script/figure is to illustrate results of network
equilibration time calibration for networks with non-uniform valley width
(Figures 8 and S4 are equivalent, respectively, but with uniform valley width).
We show gain for sediment discharge at the network outlet for different sets of
networks, and compare it to the results for single segment cases with or without
along stream sediment and water supply. Results are shown first using the
maximum (trunk) stream length to compute  the equilibration time, and second
using the empirically calibration equilibration time.

The first figure shows results for networks with 40 inlet segments, the second
figure shows results for networks with between 2 and 150 segments.
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
    "MC_N1_2-150": "../../Output/Network/MC_N1_2-150/"
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
gains = {}
for N1 in indirs.keys():
    nets[N1], gains[N1] = grlpx.read_MC(
        indirs[N1],
        cases=['UUN', 'NUN', 'UAN', 'NAN'],
        toread = ['nets', 'gains']
        )
print()

# ---- Linear gain
lin_periods = np.logspace(-2.5, 2.5, 81) * lp.equilibration_time
lin_gain_Qs = [lp.compute_Qs_gain(p, A_Qs=0.2)[-1] for p in lin_periods]
lin_gain_Qs_Qw = [lp.compute_Qs_gain(p, A_Q=0.2)[-1] for p in lin_periods]


# ---- Continuous gain
print("Running single segment, continuous supply case.")
cont_gains = {}
cont_ps = [0.8, 2.4]
cont_periods = np.logspace(-2.5, 2.5, 29) * lp.equilibration_time
for i,p in enumerate(cont_ps):
    print("Hack exponent, p = %.1f." % p)
    net = grlpx.generate_single_segment_network(
        L=L,
        Q_mean=Q_mean,
        Qs_mean=Qs_mean,
        B_mean=B_mean,
        p_Q=p,
        p_B=p,
        x0=x0,
        dx=2.5e2,
        evolve=True
        )
    gs = []
    for j,period in enumerate(cont_periods):
        print(
            "\r" + 
            u"\u25AE"*int(np.round((j*2)/(len(cont_periods)*2)*50)) + 
            u"\u25AF"*int(np.round(50 - (j*2)/(len(cont_periods)*2)*50)) + 
            " " + 
            str(int((j*2)/(len(cont_periods)*2)*100)).rjust(3) + "%. " + 
            "Period = %e kyr." % (period/3.154e10),
            end=""
            )
        periodic = grlpx.evolve_network_periodic(
            copy.deepcopy(net),
            period,
            0.2,
            0.
            )
        gs.append(periodic['G_Qs'][0][-1])
    cont_gains[p] = gs
    print(
        "\r" + 
        u"\u25AE"*50 + 
        " 100%%. Period = %e kyr." % (period/3.154e10)
        )
print()


# ---- Plot
print("Plotting.")

def plot(lin_periods, lin_gain_Qs, cont_periods, cont_gains, gains, lp, nets, title):
    
    # Set up plot.
    fig, axs = plt.subplots(3, 4, sharey="row", sharex="row")

    # Loop over network cases.
    for i,case in enumerate(['UUN', 'NUN', 'UAN', 'NAN']):
        
        # Plot gain as a function of forcing period, for single segment cases
        # with upstream only and along stream supply of sediment and water,
        # and for network cases.
        Teqs = [
            n[case].list_of_LongProfile_objects[0].x.max()**2. /
                lp.diffusivity.mean()
            for n in nets
            ]
        axs[0,i].plot(lin_periods/lp.equilibration_time, lin_gain_Qs)
        axs[0,i].fill(
            np.hstack((cont_periods, cont_periods[::-1]))/lp.equilibration_time,
            np.hstack((cont_gains[0.8], cont_gains[2.4][::-1])),
            c="0.6"
            )
        axs[0,i].plot(
            [p/Teqs[i] for i,gs in enumerate(gains) for p in gs[case]['P']],
            [g[0][-1] for gs in gains for g in gs[case]['G_Qs']['Qs']],
            "o",
            alpha=0.05
            )
        axs[0,i].set_xlabel(r"Period, / $T_{eq,max}$ [-]")
        if i==0:
            axs[0,i].set_ylabel("Gain, $G_{Q_s,L}$ [-]")
        axs[0,i].set_xscale("log")
        
        # Plot gain as a function of forcing period.
        # This time normalise by empirically optimised equilibration time.
        Teqs = [gs[case]['Teq'] for gs in gains]
        axs[1,i].plot(lin_periods/lp.equilibration_time, lin_gain_Qs)
        axs[1,i].fill(
            np.hstack((cont_periods, cont_periods[::-1]))/lp.equilibration_time,
            np.hstack((cont_gains[0.8], cont_gains[2.4][::-1])),
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
    'MC_N1_40': r'Figure S16: $N_1$ = 40',
    'MC_N1_2-150': r'Figure S17: $N_1$ = 2-150'
    }
for N1 in indirs.keys():
    plot(
        lin_periods,
        lin_gain_Qs,
        cont_periods,
        cont_gains,
        gains[N1],
        lp,
        nets[N1],
        titles[N1]
        )


if output_gmt:

    # ---- Save

    basedir = "../../Output/Network/" + \
        "Figure_S16_S17_Network_Teq_Calibration_Non-Uniform_Width/"

    with open(basedir + "linear_gain.pg", "wb") as f:
        arr = np.column_stack((lin_periods/lp.equilibration_time, lin_gain_Qs))
        np.savetxt(f, arr)
        
    with open(basedir + "continuous_gain.pg", "wb") as f:
        arr = np.column_stack(( 
            np.hstack((cont_periods, cont_periods[::-1]))/lp.equilibration_time,
            np.hstack((cont_gains[0.8], cont_gains[2.4][::-1]))
            ))
        np.savetxt(f, arr)
    
    for N1 in indirs.keys():
        for j,case in enumerate(['UUN', 'NUN', 'UAN', 'NAN']):
            
            Teqs = [
                n[case].list_of_LongProfile_objects[0].x.max()**2. /
                    lp.diffusivity.mean()
                for n in nets[N1]
                ]
                
            with open(basedir + N1 + "/" + case + "/gain_L.pg", "wb") as f:
                arr = np.column_stack(( 
                    [p/Teqs[i] 
                        for i,gs in enumerate(gains[N1])
                            for p in gs[case]['P']],
                    [g[0][-1]
                        for gs in gains[N1]
                            for g in gs[case]['G_Qs']['Qs']]
                    ))
                np.savetxt(f, arr)
                
            with open(basedir + N1 + "/" + case + "/Teq_max.t", "wb") as f:
                arr = [Teq/3.154e10 for Teq in Teqs]
                np.savetxt(f, arr)
            
            Teqs = [gs[case]['Teq'] for gs in gains[N1]]

            with open(basedir + N1 + "/" + case + "/gain_Le.pg", "wb") as f:
                arr = np.column_stack(( 
                    [p/Teqs[i]
                        for i,gs in enumerate(gains[N1])
                            for p in gs[case]['P']],
                    [g[0][-1]
                        for gs in gains[N1]
                            for g in gs[case]['G_Qs']['Qs']]
                    ))
                np.savetxt(f, arr)
                
            with open(basedir + N1 + "/" + case + "/Teq.t", "wb") as f:
                arr = [gs[case]['Teq']/3.154e10 for gs in gains[N1]]
                np.savetxt(f, arr)