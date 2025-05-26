"""
This script performs the analysis presented in Figure S26 of McNab et al. (2025,
EGUsphere); produces a rough version of the Figure; and, optionally, generates
output files for plotting the final Figure in GMT.

The purpose of the script/figure is to show how gain and lag vary spatially
throughout a network. We show results for four network cases, in which segment
lengths are either uniform or non-uniform, and sediment and water are supplied
only at valley inlets or also along stream; and for three forcing periods, 
0.1*, 1* and 10* the empirically determined equilibration time.

Here, in contrast with Figures 13, valley width is set to increase
downstream with the same power-law exponent as water and sediment discharge,
rather than being held constant. This has the effect of keeping the diffusivity
constant along stream.
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
neti = 177


# ---- Valley properties
# Define properties to use when constructing the single segment valleys.
# Correspond to precipitation rate of c. 1 m/yr for a catchment with Hack
# exponent of 1.8 and runoff coefficent of 0.4; and an equilibration time of
# 100 kyr.
# See ../Compute_River_Properties.py for details.
x0 = 50.e3
L = 100.e3
Q_mean = 26.
Qs_mean = Q_mean * 1.e-4
B_mean = 254.
p = 1.8


# ---- Read data
print("Reading results.")
nets, hacks, gains = grlpx.read_MC(
    indir,
    cases=['UUN', 'NUN', 'UAN', 'NAN'],
    toread=['nets', 'hacks', 'gains']
    )


# ---- Measure gain and lag with period equal to network equilibration time
print("Evolving networks:")

# Set up for output
net_gains = {}
net_lags = {}

# Loop over cases
for case in ['UUN', 'NUN', 'UAN', 'NAN']:
    print("    - %s" % case)
    
    # Prepare for output
    net_gains[case] = []
    net_lags[case] = []
    
    # Predict network Teq
    Teq = gains[neti][case]['Teq']
    L_eff = np.sqrt(Teq*nets[neti][case].mean_diffusivity)

    # Evolve to ensure steady state
    nets[neti][case].evolve_threshold_width_river_network(nt=100, dt=3.154e10)

    # Evolve with sinusoisal variation in sediment supply and period scaled
    # by equilibration time. Save gains and lags
    for P_scl in [0.1, 1., 10.]:
        print("        - %f" % P_scl)
        periodic = grlpx.evolve_network_periodic(
            net=copy.deepcopy(nets[neti][case]),
            period=Teq*P_scl,
            A_Qs=0.2,
            A_Q=0.
            )
        net_gains[case].append(periodic['G_z'])
        net_lags[case].append(periodic['lag_z'])


# ---- Single segment versions
print("Evolving single segment.")

single_segs = {'UUN': {}, 'NUN': {}, 'UAN': {}, 'NAN': {}}

for case in ['UUN', 'NUN', 'UAN', 'NAN']:
    print("    - %s" % case)
    
    # Predict network Teq
    Teq = gains[neti][case]['Teq']
    L_eff = np.sqrt(Teq*nets[neti][case].mean_diffusivity)

    # Upstream supply example
    single_segs[case]['U'] = grlpx.generate_single_segment_network(
        L=L_eff,
        Q_mean=Q_mean,
        Qs_mean=Qs_mean,
        B_mean=B_mean,
        p_Q=0,
        p_B=0,
        x0=x0,
        dx=5.e2,
        evolve=True
        )
        
    # Along stream supply example - also evolve it to measure gain and lag
    single_segs[case]['A'] = grlpx.generate_single_segment_network(
        L=nets[neti][case].list_of_LongProfile_objects[0].x_ext[0][-1],
        Q_mean=Q_mean,
        Qs_mean=Qs_mean,
        B_mean=B_mean,
        p_Q=hacks[neti][case]['p'],
        p_B=0,
        x0=x0,
        dx=5.e2,
        evolve=True
        )
    single_segs[case]['A_gains'] = []
    single_segs[case]['A_lags'] = []
    for P_scl in [0.1, 1., 10.]:
        print("        - %f" % P_scl)
        periodic = grlpx.evolve_network_periodic(
            net=copy.deepcopy(single_segs[case]['A']),
            period=Teq*P_scl,
            A_Qs=0.2,
            A_Q=0.
            )
        single_segs[case]['A_gains'].append(periodic['G_z'])
        single_segs[case]['A_lags'].append(periodic['lag_z'])

    
# ---- Plot

fig, axs = plt.subplots(6, 4, sharex=True, sharey="row")

for i,case in enumerate(['UUN', 'NUN', 'UAN', 'NAN']):
    
    # Predict network Teq
    Teq = gains[neti][case]['Teq']
    L_eff = np.sqrt(Teq*nets[neti][case].mean_diffusivity)
    
    for j,P_scl in enumerate([0.1, 1., 10.]):

        # Plot gain and lag for single segment, upstream supply case
        axs[2*j,i].plot(
            (L - L_eff + 
                single_segs[case]['U'].list_of_LongProfile_objects[0].x)/1.e3,
            single_segs[case]['U'].list_of_LongProfile_objects[0].compute_z_gain(
                Teq*P_scl
                ),
            "k--"
            )
        axs[2*j+1,i].plot(
            (L - L_eff + 
                single_segs[case]['U'].list_of_LongProfile_objects[0].x)/1.e3,
            single_segs[case]['U'].list_of_LongProfile_objects[0].compute_z_lag(
                Teq*P_scl
                )/(Teq*P_scl),
            "k--"
            )
        
        # Plot gain and lag for single segment, along stream suppy case
        axs[2*j,i].plot(
            single_segs[case]['A'].list_of_LongProfile_objects[0].x/1.e3,
            single_segs[case]['A_gains'][j][0],
            "-.",
            c="0.5"
            )
        axs[2*j+1,i].plot(
            single_segs[case]['A'].list_of_LongProfile_objects[0].x/1.e3,
            single_segs[case]['A_lags'][j][0],
            "-.",
            c="0.5"
            )
        
        # Plot gain and lag for network
        for k,seg in enumerate(nets[neti][case].list_of_LongProfile_objects):
            axs[2*j,i].plot(seg.x/1.e3, net_gains[case][j][k])
            axs[2*j+1,i].plot(seg.x/1.e3, net_lags[case][j][k])

# Tidy up and label axes    
for i,row in enumerate(axs):
    for ax in row:
        ax.set_box_aspect(1)
        if i==5:
            ax.set_xlabel(r"Downstream distance, $x$ [km]")
axs[0,0].set_ylabel(r"Gain, $G_z$ [-]")
axs[1,0].set_ylabel(r"Lag, ${\varphi}_z$ [-]")
axs[2,0].set_ylabel(r"Gain, $G_z$ [-]")
axs[3,0].set_ylabel(r"Lag, ${\varphi}_z$ [-]")
axs[4,0].set_ylabel(r"Gain, $G_z$ [-]")
axs[5,0].set_ylabel(r"Lag, ${\varphi}_z$ [-]")

plt.show()

# ---- Save

basedir = "../../Output/Network/Figure_S26_Network_Spatial_Gain_Lag_Non-Uniform_Width/"

for case in ['UUN', 'NUN', 'UAN', 'NAN']:
    
    # Predict network Teq
    net = nets[neti][case]
    Teq = gains[neti][case]['Teq']
    L_eff = np.sqrt(Teq*nets[neti][case].mean_diffusivity)
    single_seg_U =  single_segs[case]['U'].list_of_LongProfile_objects[0]
    single_seg_A =  single_segs[case]['A'].list_of_LongProfile_objects[0]
    
    labels = ["fast", "medium", "slow"]
    
    for i,P_scl in enumerate([0.1, 1., 10.]):
        
        with open(basedir + case + "/" + labels[i] + "/gain.dg", "wb") as f:

            for j,seg in enumerate(net.list_of_LongProfile_objects):
                hdr = b"> -Z%i\n" % (net.segment_orders[j])
                f.write(hdr)
                arr = np.column_stack((
                    seg.x/1.e3,
                    net_gains[case][i][j]
                    ))
                np.savetxt(f, arr)
                
        with open(basedir + case + "/" + labels[i] + "/lag.dl", "wb") as f:
            for j,seg in enumerate(net.list_of_LongProfile_objects):
                hdr = b"> -Z%i\n" % (net.segment_orders[j])
                f.write(hdr)
                arr = np.column_stack((
                    seg.x/1.e3,
                    net_lags[case][i][j]
                    ))
                np.savetxt(f, arr)
        
        with open(basedir + case + "/" + labels[i] + "/single_seg_U_gain.dg", "wb") as f:
            arr = np.column_stack((
                (L - L_eff + single_seg_U.x)/1.e3,
                single_seg_U.compute_z_gain(Teq*P_scl)
                ))
            np.savetxt(f, arr)
            
        with open(basedir + case + "/" + labels[i] + "/single_seg_U_lag.dl", "wb") as f:
            arr = np.column_stack((
                (L - L_eff + single_seg_U.x)/1.e3,
                single_seg_U.compute_z_lag(Teq*P_scl)/(Teq*P_scl)
                ))
            np.savetxt(f, arr)

        with open(basedir + case + "/" + labels[i] + "/single_seg_A_gain.dg", "wb") as f:
            arr = np.column_stack((
                single_seg_A.x/1.e3,
                single_segs[case]['A_gains'][i][0]
                ))
            np.savetxt(f, arr)
            
        with open(basedir + case + "/" + labels[i] + "/single_seg_A_lag.dl", "wb") as f:
            arr = np.column_stack((
                single_seg_A.x/1.e3,
                single_segs[case]['A_lags'][i][0]
                ))
            np.savetxt(f, arr)