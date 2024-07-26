import numpy as np
import matplotlib.pyplot as plt

import grlp
import grlp_extras as grlpx


# ---- Output?
output_gmt = True

# ---- River properties
x0 = 50.e3
L = 100.e3
Q_mean = 26.
Qs_mean = Q_mean * 1.e-4
B_mean = 254.
D = 0.1
ps = np.array([1.4, 1.6, 1.8, 2., 2.2])

# ---- River properties
lps = {}
for p in ps:
    net = grlpx.set_up_long_profile(
        L=L,
        Q_mean=Q_mean,
        Qs_mean=Qs_mean,
        B_mean=B_mean,
        p_Qw=p,
        p_Qs=p,
        p_B=0,
        x0=x0,
        dx=5.e2,
        evolve=True)
    net.list_of_LongProfile_objects[0].D = D
    net.list_of_LongProfile_objects[0].compute_flow_depth()
    net.list_of_LongProfile_objects[0].compute_channel_width()
    lps[p] = net

lp_ref = grlpx.set_up_long_profile(
    L=L,
    Q_mean=Q_mean,
    Qs_mean=Qs_mean,
    B_mean=B_mean,
    p_Qw=0,
    p_Qs=0,
    p_B=0,
    x0=x0,
    dx=5.e2,
    evolve=True)
lp_ref.list_of_LongProfile_objects[0].D = D
lp_ref.list_of_LongProfile_objects[0].compute_flow_depth()
lp_ref.list_of_LongProfile_objects[0].compute_channel_width()

# ---- Plots

# Simple plot

fig, axs = plt.subplots(2, 1, sharex=True)

axs[0].plot(
    lp_ref.list_of_LongProfile_objects[0].x/1000.,
    lp_ref.list_of_LongProfile_objects[0].Q,
    "--"
    )
for p in lps.keys():
    axs[0].plot(
        lps[p].list_of_LongProfile_objects[0].x/1000.,
        lps[p].list_of_LongProfile_objects[0].Q
        )
axs[0].set_ylabel(r'$Q$ [m$^3$ s$^{-1}$]')
axs[0].set_box_aspect(1)

ax_twin = axs[0].twinx()
for p in lps.keys():
    ax_twin.plot(
        lps[p].list_of_LongProfile_objects[0].x/1000.,
        lps[p].list_of_LongProfile_objects[0].Q_s*1.e3,
        "k:")
ax_twin.set_ylabel(r'$Q_s$ [x10$^3$ m$^3$ s$^{-1}$]')
ax_twin.set_box_aspect(1)

for p in lps.keys():
    axs[1].plot(
        lps[p].list_of_LongProfile_objects[0].x/1000.,
        lps[p].list_of_LongProfile_objects[0].z
        )
axs[1].plot(
    lp_ref.list_of_LongProfile_objects[0].x/1000.,
    lp_ref.list_of_LongProfile_objects[0].z, 
    "k--"
    )
axs[1].set_ylabel(r'$z$ [m]')
axs[1].set_xlabel(r'$x$ [km]')
axs[1].set_box_aspect(1)

fig.tight_layout()
plt.show()

# -- Full plot

fig, axs = plt.subplots(3, 2, sharex=True)

# Discharge
axs[0,0].plot(
    lp_ref.list_of_LongProfile_objects[0].x/1000.,
    lp_ref.list_of_LongProfile_objects[0].Q,
    "--"
    )
for p in lps.keys():
    axs[0,0].plot(
        lps[p].list_of_LongProfile_objects[0].x/1000.,
        lps[p].list_of_LongProfile_objects[0].Q
        )
axs[0,0].set_ylabel(r'$Q$ [m$^3$ s$^{-1}$]')

# Sediment discharge
axs[0,1].plot(
    lp_ref.list_of_LongProfile_objects[0].x/1000.,
    lp_ref.list_of_LongProfile_objects[0].Q_s*1.e3,
    "--"
    )
for p in lps.keys():
    axs[0,1].plot(
        lps[p].list_of_LongProfile_objects[0].x/1000.,
        lps[p].list_of_LongProfile_objects[0].Q_s*1.e3
        )
axs[0,1].set_ylabel(r'$Q_s$ [x10$^3$ m$^3$ s$^{-1}$]')

# Valley width
axs[1,0].plot(
    lp_ref.list_of_LongProfile_objects[0].x/1000.,
    lp_ref.list_of_LongProfile_objects[0].B,
    "--"
    )
for p in lps.keys():
    axs[1,0].plot(
        lps[p].list_of_LongProfile_objects[0].x/1000.,
        lps[p].list_of_LongProfile_objects[0].B
        )
axs[1,0].set_ylabel(r'$B$ [m]')

# Elevation
axs[1,1].plot(
    lp_ref.list_of_LongProfile_objects[0].x/1000.,
    lp_ref.list_of_LongProfile_objects[0].z,
    "--"
    )
for p in lps.keys():
    axs[1,1].plot(
        lps[p].list_of_LongProfile_objects[0].x/1000.,
        lps[p].list_of_LongProfile_objects[0].z
        )
axs[1,1].set_ylabel(r'$z$ [m]')

# Channel width
axs[2,0].plot(
    lp_ref.list_of_LongProfile_objects[0].x/1000.,
    lp_ref.list_of_LongProfile_objects[0].b,
    "--"
    )
for p in lps.keys():
    axs[2,0].plot(
        lps[p].list_of_LongProfile_objects[0].x/1000.,
        lps[p].list_of_LongProfile_objects[0].b
        )
axs[2,0].set_ylabel(r'$b$ [m]')
axs[2,0].set_xlabel(r'$x$ [km]')

# Channel depth
axs[2,1].plot(
    lp_ref.list_of_LongProfile_objects[0].x/1000.,
    lp_ref.list_of_LongProfile_objects[0].h,
    "--"
    )
for p in lps.keys():
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

    out_dir = "../output/continuous/setup/"

    with open(out_dir + "numerical_profile.de", "wb") as f:
        for p in list(lps.keys())[::-1]:
            hdr = b"> -Z%f\n" % p
            f.write(hdr)
            arr = np.column_stack((
                lps[p].list_of_LongProfile_objects[0].x/1000.,
                lps[p].list_of_LongProfile_objects[0].z))
            np.savetxt(f, arr)

    with open(out_dir + "analytical_profile.de", "wb") as f:
        arr = np.column_stack((
            lp_ref.list_of_LongProfile_objects[0].x/1000., 
            lp_ref.list_of_LongProfile_objects[0].z ))
        np.savetxt(f, arr)

    with open(out_dir + "water.dq", "wb") as f:
        for p in lps.keys():
            hdr = b"> -Z%f\n" % p
            f.write(hdr)
            arr = np.column_stack((
                lps[p].list_of_LongProfile_objects[0].x/1000.,
                lps[p].list_of_LongProfile_objects[0].Q ))
            np.savetxt(f, arr)

    with open(out_dir + "sediment.dq", "wb") as f:
        for p in lps.keys():
            hdr = b"> -Z%f\n" % p
            f.write(hdr)
            arr = np.column_stack((
                lps[p].list_of_LongProfile_objects[0].x/1000.,
                lps[p].list_of_LongProfile_objects[0].Q_s*1000. ))
            np.savetxt(f, arr)

    with open(out_dir + "constant.dq", "wb") as f:
        arr = np.column_stack(( [0., L/1.e3], [Q_mean, Q_mean] ))
        np.savetxt(f, arr)