"""
This script performs the analysis presented in Figures 8 and S4 of McNab et al.
(2025, EGUsphere); produces rough versions of the Figures; and, optionally,
generates output files for plotting the final Figure in GMT.

The purpose of the script/figure is to illustrate results of network
equilibration time calibration. We show gain for sediment discharge at the
network outlet for different sets of networks, and compare it to the results
for single segment cases with or without along stream sediment and water supply.
Results are shown first using the maximum (trunk) stream length to compute
the equilibration time, and second using the empirically calibration
equilibration time.

The main figure shows results for networks with 40 inlet segments, the extra
figure shows results for networks with between 2 and 150 segments.
"""

def gain_misfit(Teq_scale, net_gain, periods, single_seg_net):
    
    # Get the equilibration time of the single segment network
    lp = single_seg_net.list_of_LongProfile_objects[0]
    
    # Compute the gain for the single segment case.
    # We compute gain at a set of periods such that the scaled periods
    # (period/equilibraton time) match the scaled network periods for this
    # estimate of network equilibration time.
    lin_gain = [
        lp.compute_Qs_gain(p, A_Qs=0.2)[-1]
        for p in periods * Teq_scale
        ]
    
    # Compute the RMS misfit between the network and single segment gains.
    misfit = np.sqrt(
        (1./len(net_gain)) * sum((np.array(net_gain) - lin_gain)**2.)
        )
    return misfit


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
n = 184


# ---- Read data
print("Reading results.")
nets, gains = grlpx.read_MC(
    indir,
    cases=['UUU'],
    toread = ['nets', 'gains']
    )


# ---- Linear part
x0 = 50.e3
L = nets[n]['UUU'].list_of_LongProfile_objects[0].x.max()
Q_mean = 26.
Qs_mean = Q_mean * 1.e-4
B_mean = 254.
single_seg_net = grlpx.generate_single_segment_network(
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
lp = single_seg_net.list_of_LongProfile_objects[0]
lp.compute_equilibration_time()


# ---- Linear gain
lin_periods = np.logspace(-2.5, 2.5, 81) * lp.equilibration_time
lin_gain_Qs = [lp.compute_Qs_gain(p, A_Qs=0.2)[-1] for p in lin_periods]
lin_gain_Qs_Qw = [lp.compute_Qs_gain(p, A_Q=0.2)[-1] for p in lin_periods]


# ---- Equilibration times

Teq_max = nets[n]['UUU'].list_of_LongProfile_objects[0].x.max()**2. / lp.diffusivity.mean()
Teq_mean = gains[n]['UUU']['Teq']

Teq_rng = np.linspace(0.01, 2.99, 250) * lp.equilibration_time

rng_misfit = []
for i in range(len(Teq_rng)):
    rng_misfit.append(gain_misfit(lp.equilibration_time/Teq_rng[i], [g[0][-1] for g in gains[n]['UUU']['G_Qs']['Qs']], gains[n]['UUU']['P'], single_seg_net))
max_misfit = gain_misfit(lp.equilibration_time/Teq_max, [g[0][-1] for g in gains[n]['UUU']['G_Qs']['Qs']], gains[n]['UUU']['P'], single_seg_net)
mean_misfit = gain_misfit(lp.equilibration_time/Teq_mean, [g[0][-1] for g in gains[n]['UUU']['G_Qs']['Qs']], gains[n]['UUU']['P'], single_seg_net)


# ---- Plot
print("Plotting.")

# Set up plot.
fig, axs = plt.subplots(1, 2)

axs[0].plot(lin_periods/lp.equilibration_time, lin_gain_Qs)
axs[0].plot(
    gains[n]['UUU']['P']/Teq_max,
    [g[0][-1] for g in gains[n]['UUU']['G_Qs']['Qs']],
    "o",
    )
axs[0].plot(
    gains[n]['UUU']['P']/Teq_mean,
    [g[0][-1] for g in gains[n]['UUU']['G_Qs']['Qs']],
    "o",
    )
axs[0].set_xlabel(r"Period, / $T_{eq}$ [-]")
axs[0].set_ylabel("Gain, $G_{Q_s,L}$ [-]")
axs[0].set_xscale("log")

axs[1].plot(Teq_rng/3.154e10, rng_misfit)
axs[1].scatter(Teq_max/3.154e10, max_misfit)
axs[1].scatter(Teq_mean/3.154e10, mean_misfit)

plt.show()


if output_gmt:

    # ---- Save
    basedir = "../../Output/Network/Figure_8_Network_Teq_Calibration_Explainer/"

    with open(basedir + "linear_gain.pg", "wb") as f:
        arr = np.column_stack((lin_periods/lp.equilibration_time, lin_gain_Qs))
        np.savetxt(f, arr)
            
    with open(basedir + "/gain_L.pg", "wb") as f:
        arr = np.column_stack(( 
            gains[n]['UUU']['P']/Teq_max,
            [g[0][-1] for g in gains[n]['UUU']['G_Qs']['Qs']],
            ))
        np.savetxt(f, arr)

    with open(basedir + "/gain_Le.pg", "wb") as f:
        arr = np.column_stack(( 
            gains[n]['UUU']['P']/Teq_mean,
            [g[0][-1] for g in gains[n]['UUU']['G_Qs']['Qs']],
            ))
        np.savetxt(f, arr)
        
    with open(basedir + "/gain_connect.pg", "wb") as f:
        for i in range(len(gains[n]['UUU']['P'])):
            hdr = b">\n"
            f.write(hdr)
            arr = np.column_stack((
                [gains[n]['UUU']['P'][i]/Teq_max, gains[n]['UUU']['P'][i]/Teq_mean],
                [gains[n]['UUU']['G_Qs']['Qs'][i][0][-1]]*2
                ))
            np.savetxt(f, arr)

    with open(basedir + "/misfit_Le.dat", "wb") as f:
        arr = np.column_stack(( 
            Teq_mean/3.154e10,
            mean_misfit,
            ))
        np.savetxt(f, arr)

    with open(basedir + "/misfit_L.dat", "wb") as f:
        arr = np.column_stack(( 
            Teq_max/3.154e10,
            max_misfit,
            ))
        np.savetxt(f, arr)
        
    with open(basedir + "/misfit_rng.dat", "wb") as f:
        arr = np.column_stack(( 
            Teq_rng/3.154e10,
            rng_misfit,
            ))
        np.savetxt(f, arr)