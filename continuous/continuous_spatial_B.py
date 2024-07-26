from copy import deepcopy
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap
from scipy.signal import find_peaks
import numpy as np
import matplotlib.pyplot as plt

import grlp
import grlp_extras as grlpx


# initial set up
lp = grlp.LongProfile()
lp.basic_constants()
lp.bedload_lumped_constants()
lp.set_hydrologic_constants()

# ---- Reference properties
x0 = 50.e3
L = 100.e3
p__x_A = 1./0.54 # global mean from He et al. (2024)
k__x_A = 2.1*1.e3/(1.e6**0.55) # global mean from He et al. (2024), converted to m & m^2
P = 1.e3 / 1.e3 / 3.154e7 # precipitation rate in m/s
C_R = 0.4 # runoff coefficient
Qw_mean = P * C_R * k__x_A * ((L+x0)**(p__x_A+1.) - x0**(p__x_A+1.)) / (L * (p__x_A+1.))
Qs_mean = Qw_mean * 1.e-4
Teq = 3.154e12
diffusivity = L**2. / Teq
S0 = (Qs_mean/(lp.k_Qs*Qw_mean))**(6./7.)
B_mean = (7./6.) * (lp.k_Qs * Qw_mean * S0**(1./6.)) / (diffusivity * (1. - lp.lambda_p))
D = 0.1

# # ---- River properties
# x0 = 10.e3
# L = 100.e3
# mean_Qw = 10.
# mean_Qs = 0.001
# B = 98.1202038813591
# S0=(mean_Qs/(lp.k_Qs * mean_Qw))**(6./7.)

# ---- Loop over ps
ps = np.array([1.4, 1.6, 1.8, 2., 2.2])
periods = np.array([10., 100., 1000.]) * 3.154e10
G_zs = []
lag_zs = []
for period in periods:

    G_zs_p = []
    lag_zs_p = []
    
    for p in ps:
        
        print(p)
        
        net = grlpx.set_up_long_profile(L, Qw_mean, Qs_mean, B_mean, p, p, p, x0=x0, dx=5.e2, evolve=True)

        # ---- Evolve
        A = 0.2
        Qs_periodic = grlpx.evolve_network_periodic(deepcopy(net), period, 0.2, 0.)
        # Qw_periodic = evolve_network_periodic(deepcopy(net), period, 0., 0.2)

        # ---- Analyse
        # z_gain = compute_network_gain(Qs_periodic['z'], 0.2)
        # z_lag = find_network_lag(net, Qs_periodic['z'], Qs_periodic['time'], Qs_periodic['Qs_scale'], period)
        G_zs_p.append(Qs_periodic['G_z'][0])
        lag_zs_p.append(Qs_periodic['lag_z'][0])
        
    G_zs.append(G_zs_p)
    lag_zs.append(lag_zs_p)

# plt.show()


# ---- Plot
fig, axs = plt.subplots(2,3,sharex=True,sharey="row")

for i,period in enumerate(periods):

    axs[0,i].plot(
        net.list_of_LongProfile_objects[0].x/1000., 
        net.list_of_LongProfile_objects[0].compute_z_gain(period),
        "--")
    for G_z in G_zs[i]:
        axs[0,i].plot(net.list_of_LongProfile_objects[0].x/1000., G_z)


    axs[1,i].plot(
        net.list_of_LongProfile_objects[0].x/1000., 
        net.list_of_LongProfile_objects[0].compute_z_lag(period)/period,
        "--")
    for lag_z in lag_zs[i]:
        axs[1,i].plot(net.list_of_LongProfile_objects[0].x/1000., lag_z)
    
axs[0,0].set_ylabel(r"$G$")
axs[1,0].set_xlabel(r"$x$ [km]")
axs[1,0].set_ylabel(r"$\varphi$")

plt.show()


# ---- Plot
# lags = find_lag_times(Qs, time, scale, can_lead=True, full=True) 
# i = 30
# plt.plot(Qs[:,i]/mean_ssd_Qs[i])
# plt.plot(lags['obs_tps'][i], Qs[lags['obs_tps'][i],i]/mean_ssd_Qs[i], "o")
# plt.plot(scale, "--")
# plt.show()


# lags = find_lag_times_x_corr(Qs[2000:,:], scale[2000:], (time[2000:]-time[2000]), period)/period
# plt.plot(lags)
# plt.plot(lag_Qss[0], "--")
# plt.show()
# 
# start = 0
# for i in range(0,30):
#     plt.plot(Qs[start:,i]/mean_ssd_Qs[i])
# plt.plot(scale, "--")
# plt.show()


import sys
sys.exit()

# ---- Write output

dirs = ["fast/", "medium/", "slow/"]
for i,period in enumerate(periods):

    out_dir = "../output/continuous/spatial/" + dirs[i]

    with open(out_dir + "G_z_lin.dg", "wb") as f:
        arr = np.column_stack((
            net.list_of_LongProfile_objects[0].x/1000.,
            net.list_of_LongProfile_objects[0].compute_z_gain(period) ))
        np.savetxt(f, arr)
    with open(out_dir + "G_z.dg", "wb") as f:
        for j,p in enumerate(ps):
            hdr = b"> -Z%f\n" % p
            f.write(hdr)
            arr = np.column_stack((
                net.list_of_LongProfile_objects[0].x/1000., 
                G_zs[i][j]))
            np.savetxt(f, arr)

    with open(out_dir + "Lag_z_lin.dl", "wb") as f:
        arr = np.column_stack((
            net.list_of_LongProfile_objects[0].x/1000.,
            net.list_of_LongProfile_objects[0].compute_z_lag(period)/period ))
        np.savetxt(f, arr)
    with open(out_dir + "Lag_z.dl", "wb") as f:
        for j,p in enumerate(ps):
            hdr = b"> -Z%f\n" % p
            f.write(hdr)
            arr = np.column_stack((
                net.list_of_LongProfile_objects[0].x/1000.,
                lag_zs[i][j]))
            np.savetxt(f, arr)