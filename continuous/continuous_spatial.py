from grlp import *
from grlp_extras import *
# from extras import *
from copy import deepcopy
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap
from scipy.signal import find_peaks

# initial set up
lp = LongProfile()
lp.basic_constants()
lp.bedload_lumped_constants()
lp.set_hydrologic_constants()

# ---- River properties
x0 = 10.e3
L = 100.e3
mean_Qw = 10.
mean_Qs = 0.001
B = 98.1202038813591
S0=(mean_Qs/(lp.k_Qs * mean_Qw))**(6./7.)

# ---- Loop over ps
ps = np.array([1.4, 1.8, 2.2, 2.6])
periods = np.array([10., 100., 1000.]) * 3.154e10
G_zs = []
lag_zs = []
for period in periods:

    G_zs_p = []
    lag_zs_p = []
    
    for p in ps:
        
        print(p)
        
        net = set_up_long_profile(L, mean_Qw, mean_Qs, p, B, dx=1.e2, evolve=True)

        # ---- Evolve
        A = 0.2
        z, Qs, time, scale = evolve_network_periodic(deepcopy(net), period, 0.2, 0.)
        z_Qw, Qs_Qw, time_Qw, scale_Qw = evolve_network_periodic(deepcopy(net), period, 0., 0.2)

        # ---- Analyse
        z_gain = compute_network_z_gain(net, z, 0.2, 0., [S0])
        z_lag = find_network_lag(net, z, time, scale, period)
        G_zs_p.append(z_gain[0])
        lag_zs_p.append(z_lag[0])
        
    G_zs.append(G_zs_p)
    lag_zs.append(lag_zs_p)
    
    
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