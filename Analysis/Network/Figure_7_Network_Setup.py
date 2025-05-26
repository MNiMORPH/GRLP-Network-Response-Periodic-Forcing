"""
This script performs the analysis presented in Figures 7 of McNab et al. (2025,
EGUsphere); produces a rough version of the Figure; and, optionally, generates
output files for plotting the final Figure in GMT.

The purpose of the script/figure is to illustrate the different network cases
we analyse. We use uniform vs. non-uniform segment lengths, and upstream only
vs. along-stream supply of sediment and water, combining to give four different
setups. We show the different combinations for a single network topology.
"""


# ---- Import functions

# External packages
import numpy as np
import matplotlib.pyplot as plt
import grlp

# Local packages
import grlp_extras as grlpx


# ---- Variables
output_gmt = False
indir = "../../Output/Network/MC_N1_40/"
n = 177


# ---- Read data
print("Reading results.")
nets, hacks = grlpx.read_MC(
    indir,
    cases=['UUU', 'NUU', 'UAU', 'NAU'],
    toread=['nets', 'hacks']
    )


# ---- Evolve the profiles to reach steady state
print("Evolving the networks to steady state.")
for case in nets[n].keys():
    nets[n][case].evolve_threshold_width_river_network(nt=100, dt=3.15e12)


# ---- Plot
print("Plotting.")

# Set up
fig, axs = plt.subplots(5, 4, sharey="row", figsize=(8,24))

# Loop over networks
for i,case in enumerate(['UUU', 'NUU', 'UAU', 'NAU']):
    
    # Unpack the network
    net = nets[n][case]
    
    # Get the network planform, plot
    planform = grlp.plot_network(net, show=False)
    for seg in planform:
        axs[0,i].plot(planform[seg]['x'], planform[seg]['y'])
    axs[0,i].set_yticks([])
    axs[0,i].set_xlabel(r"$x$ [km]")
    
    # Plot discharge as a function of distance along stream
    # Look downstream to connect segments across junctions
    for seg in net.list_of_LongProfile_objects:
        if seg.downstream_segment_IDs:
            downID = seg.downstream_segment_IDs[0]
            x = np.hstack(( seg.x_ext[0][1:]/1.e3, seg.x_ext[0][-1]/1.e3 ))
            Q = np.hstack((
                seg.Q,
                seg.Q[-1],
                net.list_of_LongProfile_objects[downID].Q[0]
                ))
        else:
            x = seg.x/1.e3
            Q = seg.Q
        axs[1,i].plot(x, Q)
    if i==0:
        axs[1,i].set_ylabel(r"$Q$ [m$^3$ s$^{-1}$]")
    axs[1,i].set_xlabel(r"$x$ [km]")
        
    # Plot discharge as a function of distance from furthest upstream inlet
    hack = hacks[n][case]
    d = np.linspace(0,max(hack['d']), 100)
    Q = hack['k'] * (d**hack['p'])
    axs[2,i].plot(d/1.e3, Q, "--")
    axs[2,i].scatter(np.array(hack['d'])/1.e3, hack['Q'])
    if i==0:
        axs[2,i].set_ylabel(r"$Q$ [m$^3$ s$^{-1}$]")
    axs[2,i].set_xlabel(r"$d$ [km]")

    # Plot the long profile
    for seg in net.list_of_LongProfile_objects:
        axs[3,i].plot(seg.x/1.e3, seg.z)
    if i==0:
        axs[3,i].set_ylabel(r"$z$ [m]")
    axs[3,i].set_xlabel(r"$x$ [km]")

    # Plot Horton's metrics
    orders = np.linspace(1, max(net.orders), 10)
    axs[4,i].plot(
        orders,
        net.bifurcation_ratio**(orders.max()-orders),
        "--"
        )
    axs[4,i].scatter(
        net.orders,
        [net.order_counts[i] for i in net.orders]
        )
    axs[4,i].plot(
        orders,
        net.length_scale*net.length_ratio**(orders-1)/1.e3,
        "--"
        )
    axs[4,i].scatter(
        net.orders,
        [net.order_lengths[i]/1.e3 for i in net.orders]
        )
    axs[4,i].plot(
        orders,
        net.discharge_scale*net.discharge_ratio**(orders-1),
        "--"
        )
    axs[4,i].scatter(
        net.orders,
        [net.order_discharges[i] for i in net.orders]
        )
    axs[4,i].set_yscale("log")
    axs[4,i].set_xlabel(r"Order, $\omega$")
    if i==0:
        axs[4,i].set_ylabel(r"$N_\omega$, $L_\omega$, $Q_{w,\omega}$")

for col in axs:
    for ax in col:
        ax.set_box_aspect(1)

plt.show()

# ---- Write output

if output_gmt:

    basedir = "../../Output/Network/Figure_7_Network_Setup/"

    for i,case in enumerate(['UUU', 'NUU', 'UAU', 'NAU']):
        
        net = nets[n][case]
        
        # Planform
        planform = grlp.plot_network(net, show=False)
        with open(basedir + case + "/planform.d", "wb") as f:
            for j,seg in enumerate(net.list_of_LongProfile_objects):
                hdr = b"> -Z%i\n" % (net.segment_orders[j])
                f.write(hdr)
                arr = np.column_stack(( planform[j]['x'], planform[j]['y'] ))
                np.savetxt(f, arr)

        # Discharge
        with open(basedir + case + "/discharge.dq", "wb") as f:
            for j,seg in enumerate(net.list_of_LongProfile_objects):
                if seg.downstream_segment_IDs:
                    downID = seg.downstream_segment_IDs[0]
                    x = np.hstack((
                        seg.x_ext[0][1:]/1.e3,
                        seg.x_ext[0][-1]/1.e3
                        ))
                    Q = np.hstack((
                        seg.Q, 
                        seg.Q[-1], 
                        net.list_of_LongProfile_objects[downID].Q[0]
                        ))
                else:
                    x = seg.x/1.e3
                    Q = seg.Q
                hdr = b"> -Z%i\n" % (net.segment_orders[j])
                f.write(hdr)
                arr = np.column_stack(( x, Q ))
                np.savetxt(f, arr)
                
        # Hack
        hack = hacks[n][case]
        with open(basedir + case + "/hack_fit.dq", "wb") as f:
            d = np.linspace(0,max(hack['d']), 100)
            Q = hack['k'] * (d**hack['p'])
            arr = np.column_stack(( d/1.e3, Q ))
            np.savetxt(f, arr)
        with open(basedir + case + "/hack.dq", "wb") as f:
            arr = np.column_stack(( 
                np.array(hack['d'])/1.e3,
                hack['Q'],
                net.segment_orders
                ))
            np.savetxt(f, arr)

        # Profile
        with open(basedir + case + "/profile.de", "wb") as f:
            for j,seg in enumerate(net.list_of_LongProfile_objects):
                hdr = b"> -Z%i\n" % (net.segment_orders[j])
                f.write(hdr)
                arr = np.column_stack(( seg.x/1.e3, seg.z ))
                np.savetxt(f, arr)
                
        # Ratios
        with open(basedir + case + "/counts.oc", "wb") as f:
            arr = np.column_stack((
                net.orders,
                [net.order_counts[i] for i in net.orders]
                ))
            np.savetxt(f, arr)
        with open(basedir + case + "/count_fit.oc", "wb") as f:
            arr = np.column_stack((
                net.orders,
                net.bifurcation_ratio**(max(net.orders)-net.orders)
                ))
            np.savetxt(f, arr)
        with open(basedir + case + "/lengths.oc", "wb") as f:
            arr = np.column_stack((
                net.orders,
                [net.order_lengths[i]/1.e3 for i in net.orders]
                ))
            np.savetxt(f, arr)
        with open(basedir + case + "/length_fit.oc", "wb") as f:
            arr = np.column_stack((
                net.orders,
                net.length_scale*net.length_ratio**(np.array(net.orders)-1)/1.e3
                ))
            np.savetxt(f, arr)
        with open(basedir + case + "/discharges.oc", "wb") as f:
            arr = np.column_stack((
                net.orders,
                [net.order_discharges[i] for i in net.orders]
                ))
            np.savetxt(f, arr)
        with open(basedir + case + "/discharge_fit.oc", "wb") as f:
            arr = np.column_stack((
                net.orders,
                net.discharge_scale * \
                net.discharge_ratio**(np.array(net.orders)-1)
                ))
            np.savetxt(f, arr)   

        with open(basedir + case + "/info.i", "wb") as f:
            arr = np.column_stack((
                net.bifurcation_ratio,
                net.length_ratio,
                net.discharge_ratio,
                hacks[0][case]['p']
                ))
            np.savetxt(f, arr)