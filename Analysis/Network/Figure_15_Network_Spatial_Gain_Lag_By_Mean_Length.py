"""
This script performs the analysis presented in Figure 15 of McNab et al. (2025,
EGUsphere); produces a rough version of the Figure; and, optionally, generates
output files for plotting the final Figure in GMT.

The purpose of the script/figure is to show how spatial patterns of gain and
lag vary with network structure. We show four examples, evenly spaced between
most compact and most elongate.
"""


# ---- Define functions
def compute_origin_gradient(x, y):
    x = np.array(x)
    y = np.array(y)
    return x.dot(y) / x.dot(x)


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
Pi = 3


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
nets, hacks, gains, lags = grlpx.read_MC(
    indir,
    cases=['UUU', 'NUU', 'UAU', 'NAU']
    )


# ---- Sort by effective length
mean_lengths = [net['UUU'].mean_head_length for net in nets]
mean_lengths_sort = np.array(mean_lengths).argsort()
sorted_nets = np.array(nets)[mean_lengths_sort]
sorted_gains = np.array(gains)[mean_lengths_sort]
sorted_hacks = np.array(hacks)[mean_lengths_sort]


# ---- Measure gain and lag with period equal to network equilibration time
print("Evolving networks:")

# Set up for output
net_periodic = []

# Loop over networks
for i in [0, 66, 132, 199]:
    print("    - %ith percentile" % (i/200*100))
    
    # Predict network Teq
    Teq = sorted_gains[i]['UUU']['Teq']
    L_eff = np.sqrt(Teq*sorted_nets[i]['UUU'].mean_diffusivity)

    # Evolve to ensure steady state
    sorted_nets[i]['UUU'].evolve_threshold_width_river_network(nt=100, dt=3.154e10)
    
    # Evolve with sinusoisal variation in sediment supply and period equal to
    # equilibration time.
    periodic = grlpx.evolve_network_periodic(
        net=copy.deepcopy(sorted_nets[i]['UUU']),
        period=Teq,
        A_Qs=0.2,
        A_Q=0.
        )
        
    # Save
    net_periodic.append({
        'G_z': periodic['G_z'],
        'lag_z': periodic['lag_z'],
        'Teq': Teq
        })


# ---- Single segment versions
print("Evolving single segment.")

single_segs_U = []
single_segs_A = []
single_segs_A_periodic = []

# Loop over networks
for i in [0, 66, 132, 199]:
    print(i)
    
    # Predict network Teq
    Teq = sorted_gains[i]['UUU']['Teq']
    L_eff = np.sqrt(Teq*sorted_nets[i]['UUU'].mean_diffusivity)

    # Upstream supply example
    single_segs_U.append(grlpx.generate_single_segment_network(
        L=L_eff,
        Q_mean=Q_mean,
        Qs_mean=Qs_mean,
        B_mean=B_mean,
        p_Q=0,
        p_B=0,
        x0=x0,
        dx=5.e2,
        evolve=True
        ))

    # Along stream supply example - also evolve it to measure gain and lag
    single_segs_A.append(grlpx.generate_single_segment_network(
        L=sorted_nets[i]['UUU'].list_of_LongProfile_objects[0].x_ext[0][-1],
        Q_mean=Q_mean,
        Qs_mean=Qs_mean,
        B_mean=B_mean,
        p_Q=sorted_hacks[i]['UUU']['p'],
        p_B=0,
        x0=x0,
        dx=5.e2,
        evolve=True
        ))
    single_segs_A_periodic.append(grlpx.evolve_network_periodic(
        net=copy.deepcopy(single_segs_A[-1]),
        period=Teq,
        A_Qs=0.2,
        A_Q=0.
        ))

    
# ---- Plot

fig, axs = plt.subplots(2, 4, sharex=True, sharey="row")

for i,neti in enumerate([0, 66, 132, 199]):
    
    # Predict network Teq
    Teq = sorted_gains[neti]['UUU']['Teq']
    L_eff = np.sqrt(Teq*sorted_nets[neti]['UUU'].mean_diffusivity)
    L = sorted_nets[neti]['UUU'].list_of_LongProfile_objects[0].x.max()
    
    # Plot gain and lag for single segment, upstream supply case
    axs[0,i].plot(
        (L-L_eff+single_segs_U[i].list_of_LongProfile_objects[0].x)/1.e3,
        single_segs_U[i].list_of_LongProfile_objects[0].compute_z_gain(
            Teq
            ),
        "k--"
        )
    axs[1,i].plot(
        (L-L_eff+single_segs_U[i].list_of_LongProfile_objects[0].x)/1.e3,
        single_segs_U[i].list_of_LongProfile_objects[0].compute_z_lag(
            Teq
            )/Teq,
        "k--"
        )
    
    # Plot gain and lag for single segment, along stream suppy case
    axs[0,i].plot(
        single_segs_A[i].list_of_LongProfile_objects[0].x/1.e3,
        single_segs_A_periodic[i]['G_z'][0],
        "-.",
        c="0.5"
        )
    axs[1,i].plot(
        single_segs_A[i].list_of_LongProfile_objects[0].x/1.e3,
        single_segs_A_periodic[i]['lag_z'][0],
        "-.",
        c="0.5"
        )
    
    # Plot gain and lag for network
    for j,seg in enumerate(sorted_nets[neti]['UUU'].list_of_LongProfile_objects):
        axs[0,i].plot(seg.x/1.e3, net_periodic[i]['G_z'][j])
        axs[1,i].plot(seg.x/1.e3, net_periodic[i]['lag_z'][j])

# Tidy up and label axes    
for i,row in enumerate(axs):
    for ax in row:
        ax.set_box_aspect(1)
        if i==1:
            ax.set_xlabel(r"Downstream distance, $x$ [km]")
axs[0,0].set_ylabel(r"Gain, $G_z$ [-]")
axs[1,0].set_ylabel(r"Lag, ${\varphi}_z$ [-]")

plt.show()

# ---- Save

if output_gmt:

    basedir = "../../Output/Network/Figure_15_Network_Spatial_Gain_Lag_By_Mean_Length/"

    for i,neti in enumerate([0, 66, 132, 199]):
        
        # Predict network Teq
        net = sorted_nets[neti]['UUU']
        Teq = sorted_gains[neti]['UUU']['Teq']
        L_eff = np.sqrt(Teq*sorted_nets[neti]['UUU'].mean_diffusivity)
        L = sorted_nets[neti]['UUU'].list_of_LongProfile_objects[0].x.max()
        single_seg_U = single_segs_U[i].list_of_LongProfile_objects[0]
        single_seg_A = single_segs_A[i].list_of_LongProfile_objects[0]
        
        planform = grlp.plot_network(net, show=False)
        with open(basedir + str(neti) + "/planform.d", "wb") as f:
            for j,seg in enumerate(net.list_of_LongProfile_objects):
                hdr = b"> -Z%i\n" % (net.segment_orders[j])
                f.write(hdr)
                arr = np.column_stack(( planform[j]['x'], planform[j]['y'] ))
                np.savetxt(f, arr)

        with open(basedir + str(neti) + "/gain.dg", "wb") as f:

            for j,seg in enumerate(net.list_of_LongProfile_objects):
                hdr = b"> -Z%i\n" % (net.segment_orders[j])
                f.write(hdr)
                arr = np.column_stack((
                    seg.x/1.e3,
                    net_periodic[i]['G_z'][j]
                    ))
                np.savetxt(f, arr)
                
        with open(basedir + str(neti) + "/lag.dl", "wb") as f:
            for j,seg in enumerate(net.list_of_LongProfile_objects):
                hdr = b"> -Z%i\n" % (net.segment_orders[j])
                f.write(hdr)
                arr = np.column_stack((
                    seg.x/1.e3,
                    net_periodic[i]['lag_z'][j]
                    ))
                np.savetxt(f, arr)
        
        with open(basedir + str(neti) + "/single_seg_U_gain.dg", "wb") as f:
            arr = np.column_stack((
                (L - L_eff + single_seg_U.x)/1.e3,
                single_seg_U.compute_z_gain(Teq)
                ))
            np.savetxt(f, arr)
            
        with open(basedir + str(neti) + "/single_seg_U_lag.dl", "wb") as f:
            arr = np.column_stack((
                (L - L_eff + single_seg_U.x)/1.e3,
                single_seg_U.compute_z_lag(Teq)/Teq
                ))
            np.savetxt(f, arr)

        with open(basedir + str(neti) + "/single_seg_A_gain.dg", "wb") as f:
            arr = np.column_stack((
                single_seg_A.x/1.e3,
                single_segs_A_periodic[i]['G_z'][0]
                ))
            np.savetxt(f, arr)
            
        with open(basedir + str(neti) + "/single_seg_A_lag.dl", "wb") as f:
            arr = np.column_stack((
                single_seg_A.x/1.e3,
                single_segs_A_periodic[i]['lag_z'][0]
                ))
            np.savetxt(f, arr)