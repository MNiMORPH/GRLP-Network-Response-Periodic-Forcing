"""
This script performs the analysis presented in Figure S13 of McNab et al. (2025,
EGUsphere); produces a rough version of the Figure; and, optionally, generates
output files for plotting the final Figure in GMT.

The purpose of the script/figure is to explore how gain and lag vary along
stream for the single segment case with along stream sediment and water supply.
We compare the results with analytical solutions derived by McNab et al. (2023,
GRL) for the upstream supply case.

Here, in contrast with Figures S2, valley width is set to increase
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


# ---- Output?
output_gmt = False


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
ps = np.array([0.8, 1.2, 1.6, 2., 2.4])


# ---- Scaled periods to test
periods = np.array([0.1, 1., 10.])


# ---- Analysis

# Set up lists for output
G_zs = [[] for p in ps]
lag_zs = [[] for p in ps]

# Loop over Hack exponents
for i,p in enumerate(ps):
    print("Hack exponent, p = %.1f." % p)
    
    # Set up network object
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
    
    # Loop over periods
    for period in periods:
        period *= net.list_of_LongProfile_objects[0].equilibration_time        
        print(u"  \u2022 Period = %e kyr" % (period/3.154e10))

        # Evolve
        periodic = grlpx.evolve_network_periodic(
            net=copy.deepcopy(net),
            period=period,
            A_Qs=0., 
            A_Q=0.2
            )
        G_zs[i].append(periodic['G_z'][0])
        lag_zs[i].append(periodic['lag_z'][0])
        
    print()
    
# ---- Plot
print("Plotting.")
fig, axs = plt.subplots(2,3,sharex=True,sharey="row")

for i,period in enumerate(periods):
    period *= net.list_of_LongProfile_objects[0].equilibration_time
    axs[0,i].plot(
        net.list_of_LongProfile_objects[0].x/1000., 
        net.list_of_LongProfile_objects[0].compute_z_gain(period),
        "--")
    axs[1,i].plot(
        net.list_of_LongProfile_objects[0].x/1000., 
        net.list_of_LongProfile_objects[0].compute_z_lag(period)/period,
        "--")

for i,p in enumerate(ps):
    for j,period in enumerate(periods):
        axs[0,j].plot(net.list_of_LongProfile_objects[0].x/1000., G_zs[i][j])
        axs[1,j].plot(net.list_of_LongProfile_objects[0].x/1000., lag_zs[i][j])

axs[0,0].set_ylabel(r"$G_z$")
axs[1,0].set_ylabel(r"$\varphi_z~/~P$")
titles = [
    r"$P$ = $T_{eq}~/~10$",
    r"$P$ = $T_{eq}$",
    r"$P$ = $T_{eq}~\times~10$"
    ]
for i,ax in enumerate(axs[0]):
    ax.set_title(titles[i])
for ax in axs[1]:
    ax.set_xlabel(r"$x$ [km]")

plt.show()


# ---- Write output

if output_gmt:

    dirs = ["fast/", "medium/", "slow/"]
    for i,period in enumerate(periods):
        period *= net.list_of_LongProfile_objects[0].equilibration_time

        out_dir = "../../Output/SingleSegment/" + \
            "Figure_S13_SingleSegment_Spatial_Water_Non-Uniform_Width/" \
            + dirs[i]

        with open(out_dir + "G_z_lin.dg", "wb") as f:
            arr = np.column_stack((
                net.list_of_LongProfile_objects[0].x/1000.,
                net.list_of_LongProfile_objects[0].compute_z_gain(period)
                ))
            np.savetxt(f, arr)
        with open(out_dir + "G_z.dg", "wb") as f:
            for j,p in enumerate(ps):
                hdr = b"> -Z%f\n" % p
                f.write(hdr)
                arr = np.column_stack((
                    net.list_of_LongProfile_objects[0].x/1000., 
                    G_zs[j][i]))
                np.savetxt(f, arr)

        with open(out_dir + "Lag_z_lin.dl", "wb") as f:
            arr = np.column_stack((
                net.list_of_LongProfile_objects[0].x/1000.,
                net.list_of_LongProfile_objects[0].compute_z_lag(period)/period
                ))
            np.savetxt(f, arr)
        with open(out_dir + "Lag_z.dl", "wb") as f:
            for j,p in enumerate(ps):
                hdr = b"> -Z%f\n" % p
                f.write(hdr)
                arr = np.column_stack((
                    net.list_of_LongProfile_objects[0].x/1000.,
                    lag_zs[j][i]
                    ))
                np.savetxt(f, arr)