import numpy as np
import matplotlib.pyplot as plt
import copy

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
ps = np.array([1.4, 1.6, 1.8, 2., 2.2])


# ---- Loop over ps
periods = np.array([10., 100., 1000.]) * 3.154e10
G_zs = [[] for p in ps]
lag_zs = [[] for p in ps]

for i,p in enumerate(ps):
    
    print(p)

    # net = grlpx.set_up_long_profile(
    #     L=L,
    #     Q_mean=Q_mean,
    #     Qs_mean=Qs_mean,
    #     B_mean=B_mean,
    #     p_Q=p,
    #     p_Qs=p,
    #     p_B=0,
    #     x0=x0,
    #     dx=5.e2,
    #     evolve=True
    #     )
    net = grlpx.set_up_long_profile(
        L=L,
        Q_mean=Q_mean,
        Qs_mean=Qs_mean,
        B_mean=B_mean,
        p_Q=p,
        p_Qs=p,
        p_B=p,
        x0=x0,
        dx=5.e2,
        evolve=True
        )
        
    for period in periods:

        # ---- Evolve
        periodic = grlpx.evolve_network_periodic(
            net=copy.deepcopy(net),
            period=period,
            A_Qs=0.2, 
            A_Q=0.
            )
        G_zs[i].append(periodic['G_z'][0])
        lag_zs[i].append(periodic['lag_z'][0])
    
# ---- Plot
fig, axs = plt.subplots(2,3,sharex=True,sharey="row")

for i,period in enumerate(periods):
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

axs[0,0].set_ylabel(r"$G$")
axs[1,0].set_ylabel(r"$\varphi$")
titles = [r"$P$ = $T_{eq}$/10", r"$P$ = $T_{eq}$", r"$P$ = $T_{eq}\times$ 10"]
for i,ax in enumerate(axs[0]):
    ax.set_title(titles[i])
for ax in axs[1]:
    ax.set_xlabel(r"$x$ [km]")

plt.show()


# ---- Write output

if output_gmt:

    dirs = ["fast/", "medium/", "slow/"]
    for i,period in enumerate(periods):

        # out_dir = "../output/continuous/spatial/" + dirs[i]
        out_dir = "../output/continuous/spatial_var_B/" + dirs[i]

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