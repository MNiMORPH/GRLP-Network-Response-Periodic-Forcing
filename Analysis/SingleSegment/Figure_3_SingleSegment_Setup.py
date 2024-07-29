"""
This script performs the analysis presented in Figure 3 of McNab et al. (2024,
EGUsphere); produces a rough version of the Figure; and, optionally, generates
output files for plotting the final Figure in GMT.

The purpose of the script/figure is to illustrate the 'single segment' setup
used in the paper. Sediment discharge, water discharge and elevation are shown
as functions of distance along stream.
"""

# ---- Import functions

# External packages
import numpy as np
import matplotlib.pyplot as plt
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
D = 0.01
ps = np.array([0., 1.4, 1.6, 1.8, 2., 2.2])


# ---- Generate long profile objects
# Loop over hack exponents and generate the long profile objects.
lps = {}
for p in ps:
    net = grlpx.generate_single_segment_network(
        L=L,
        Q_mean=Q_mean,
        Qs_mean=Qs_mean,
        B_mean=B_mean,
        p_Q=p,
        p_Qs=p,
        p_B=0,
        x0=x0,
        dx=5.e2,
        evolve=True)
    net.list_of_LongProfile_objects[0].D = D
    net.list_of_LongProfile_objects[0].compute_flow_depth()
    net.list_of_LongProfile_objects[0].compute_channel_width()
    lps[p] = net


# ---- Plots

# Simple plot

fig, axs = plt.subplots(2, 1, sharex=True)

axs[0].plot(
    lps[0].list_of_LongProfile_objects[0].x/1000.,
    lps[0].list_of_LongProfile_objects[0].Q,
    "--"
    )
for p in [p for p in lps.keys() if p != 0]:
    axs[0].plot(
        lps[p].list_of_LongProfile_objects[0].x/1000.,
        lps[p].list_of_LongProfile_objects[0].Q
        )
axs[0].set_ylabel(r'$Q$ [m$^3$ s$^{-1}$]')
axs[0].set_box_aspect(1)

ax_twin = axs[0].twinx()
for p in [p for p in lps.keys() if p != 0]:
    ax_twin.plot(
        lps[p].list_of_LongProfile_objects[0].x/1000.,
        lps[p].list_of_LongProfile_objects[0].Q_s*1.e3,
        "k:")
ax_twin.set_ylabel(r'$Q_s$ [x10$^3$ m$^3$ s$^{-1}$]')
ax_twin.set_box_aspect(1)

for p in [p for p in lps.keys() if p != 0]:
    axs[1].plot(
        lps[p].list_of_LongProfile_objects[0].x/1000.,
        lps[p].list_of_LongProfile_objects[0].z
        )
axs[1].plot(
    lps[0].list_of_LongProfile_objects[0].x/1000.,
    lps[0].list_of_LongProfile_objects[0].z, 
    "k--"
    )
axs[1].set_ylabel(r'$z$ [m]')
axs[1].set_xlabel(r'$x$ [km]')
axs[1].set_box_aspect(1)

fig.tight_layout()
plt.show()

# Full plot

fig, axs = plt.subplots(3, 2, sharex=True)

# Discharge
axs[0,0].plot(
    lps[0].list_of_LongProfile_objects[0].x/1000.,
    lps[0].list_of_LongProfile_objects[0].Q,
    "--"
    )
for p in [p for p in lps.keys() if p != 0]:
    axs[0,0].plot(
        lps[p].list_of_LongProfile_objects[0].x/1000.,
        lps[p].list_of_LongProfile_objects[0].Q
        )
axs[0,0].set_ylabel(r'$Q$ [m$^3$ s$^{-1}$]')

# Sediment discharge
axs[0,1].plot(
    lps[0].list_of_LongProfile_objects[0].x/1000.,
    lps[0].list_of_LongProfile_objects[0].Q_s*1.e3,
    "--"
    )
for p in [p for p in lps.keys() if p != 0]:
    axs[0,1].plot(
        lps[p].list_of_LongProfile_objects[0].x/1000.,
        lps[p].list_of_LongProfile_objects[0].Q_s*1.e3
        )
axs[0,1].set_ylabel(r'$Q_s$ [x10$^3$ m$^3$ s$^{-1}$]')

# Valley width
axs[1,0].plot(
    lps[0].list_of_LongProfile_objects[0].x/1000.,
    lps[0].list_of_LongProfile_objects[0].B,
    "--"
    )
for p in [p for p in lps.keys() if p != 0]:
    axs[1,0].plot(
        lps[p].list_of_LongProfile_objects[0].x/1000.,
        lps[p].list_of_LongProfile_objects[0].B
        )
axs[1,0].set_ylabel(r'$B$ [m]')

# Elevation
axs[1,1].plot(
    lps[0].list_of_LongProfile_objects[0].x/1000.,
    lps[0].list_of_LongProfile_objects[0].z,
    "--"
    )
for p in [p for p in lps.keys() if p != 0]:
    axs[1,1].plot(
        lps[p].list_of_LongProfile_objects[0].x/1000.,
        lps[p].list_of_LongProfile_objects[0].z
        )
axs[1,1].set_ylabel(r'$z$ [m]')

# Channel width
axs[2,0].plot(
    lps[0].list_of_LongProfile_objects[0].x/1000.,
    lps[0].list_of_LongProfile_objects[0].b,
    "--"
    )
for p in [p for p in lps.keys() if p != 0]:
    axs[2,0].plot(
        lps[p].list_of_LongProfile_objects[0].x/1000.,
        lps[p].list_of_LongProfile_objects[0].b
        )
axs[2,0].set_ylabel(r'$b$ [m]')
axs[2,0].set_xlabel(r'$x$ [km]')

# Channel depth
axs[2,1].plot(
    lps[0].list_of_LongProfile_objects[0].x/1000.,
    lps[0].list_of_LongProfile_objects[0].h,
    "--"
    )
for p in [p for p in lps.keys() if p != 0]:
    label = 'p = %.1f' % p
    axs[2,1].plot(
        lps[p].list_of_LongProfile_objects[0].x/1000.,
        lps[p].list_of_LongProfile_objects[0].h,
        label=label
        )
axs[2,1].set_ylabel(r'$h$ [m]')
axs[2,1].set_xlabel(r'$x$ [km]')
axs[2,1].legend()

fig.tight_layout()
plt.show()

# ---- Save

if output_gmt:

    out_dir = "../../Output/SingleSegment/Figure_3_SingleSegment_Setup/"

    with open(out_dir + "numerical_profile.de", "wb") as f:
        for p in [p for p in lps.keys() if p != 0][::-1]:
            hdr = b"> -Z%f\n" % p
            f.write(hdr)
            arr = np.column_stack((
                lps[p].list_of_LongProfile_objects[0].x/1000.,
                lps[p].list_of_LongProfile_objects[0].z))
            np.savetxt(f, arr)

    with open(out_dir + "analytical_profile.de", "wb") as f:
        arr = np.column_stack((
            lps[0].list_of_LongProfile_objects[0].x/1000., 
            lps[0].list_of_LongProfile_objects[0].z ))
        np.savetxt(f, arr)

    with open(out_dir + "water.dq", "wb") as f:
        for p in [p for p in lps.keys() if p != 0]:
            hdr = b"> -Z%f\n" % p
            f.write(hdr)
            arr = np.column_stack((
                lps[p].list_of_LongProfile_objects[0].x/1000.,
                lps[p].list_of_LongProfile_objects[0].Q ))
            np.savetxt(f, arr)

    with open(out_dir + "sediment.dq", "wb") as f:
        for p in [p for p in lps.keys() if p != 0]:
            hdr = b"> -Z%f\n" % p
            f.write(hdr)
            arr = np.column_stack((
                lps[p].list_of_LongProfile_objects[0].x/1000.,
                lps[p].list_of_LongProfile_objects[0].Q_s*1000. ))
            np.savetxt(f, arr)

    with open(out_dir + "constant.dq", "wb") as f:
        arr = np.column_stack(( [0., L/1.e3], [Q_mean, Q_mean] ))
        np.savetxt(f, arr)