from grlp import *
from extras import *
from copy import deepcopy
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap
from scipy.signal import find_peaks



# ---- River properties
x0 = 10.e3
L = 100.e3
mean_Qw = 10.
mean_Qs = 0.001
B = 98.1202038813591

# ---- Loop over ps
ps = np.array([0.5, 1., 1.5, 2., 2.5, 3., 3.5, 4.])
# ps = [2.]
# ps = np.arange(0., 10., 0.1)
G_zs = []
G_Qss = []
G_Qs_Qws = []
lag_zs = []
lag_Qss = []
lag_Qs_Qws = []
coeff = []
for p in ps:
    
    print(p)
    
    lp = set_up_long_profile(L, mean_Qw, mean_Qs, p, B, dx=1.e2, evolve=True)
    coeff.append(compute_coeff_internal_external(lp, A_Qs=0.2, A_Qs_i=0.2))
    lp_Qw = deepcopy(lp)
    Qw_x = deepcopy(lp.Q)
    mean_Qs0 = deepcopy(lp.Q_s_0)
    mean_ssd = deepcopy(lp.ssd)
    mean_ssd_Qs = deepcopy(lp.Q_s)

    # # ---- Plot
    # fig, axs = plt.subplots(3,1,sharex=True)
    # axs[0].plot([0., 100.], [mean_Qw, mean_Qw], ":")
    # axs[0].plot([0., 100.], [lp.Q.mean(), lp.Q.mean()], "--")
    # axs[0].plot(lp.x/1000., lp.Q)
    # axs[0].set_ylabel(r"$Q_w$ [m$^3$ s$^{-1}$]")
    # axs[1].plot([0., 100.], [mean_Qs, mean_Qs], ":")
    # axs[1].plot([0., 100.], [lp.Q_s.mean(), lp.Q_s.mean()], "--")
    # axs[1].plot(lp.x/1000., lp.Q_s)
    # axs[1].set_ylabel(r"$Q_s$ [m$^3$ s$^{-1}$]")
    # axs[2].plot(lp.x/1000., (L-lp.x) * (mean_Qs/(lp.k_Qs*mean_Qw))**(6./7.), "--")
    # axs[2].plot(lp.x/1000., lp.z)
    # axs[2].set_xlabel(r"$x$ [km]")
    # axs[2].set_ylabel(r"$z$ [m]")
    # plt.show()

    # ---- Evolve
    period = 100. * 3.15e10
    A = 0.2
    time = np.arange(0., 6.*period, period/1000.)
    scale = 1. + A*np.sin(2.*np.pi*time/period)
    z = np.zeros((len(time), len(lp.x)))
    Qs = np.zeros((len(time), len(lp.x)))
    z_Qw = np.zeros((len(time), len(lp.x)))
    Qs_Qw = np.zeros((len(time), len(lp.x)))
    for j,s in enumerate(scale):
        
        lp.set_Qs_input_upstream(mean_Qs0 * s)
        lp.set_source_sink_distributed(mean_ssd * s)
        lp.evolve_threshold_width_river(nt=1, dt=period/1000.)
        lp.compute_Q_s()
        z[j,:] = lp.z.copy()
        Qs[j,:] = lp.Q_s.copy()
        
        lp_Qw.set_Q(Qw_x * s)
        lp_Qw.evolve_threshold_width_river(nt=1, dt=period/1000.)
        lp_Qw.compute_Q_s()
        z_Qw[j,:] = lp_Qw.z.copy()
        Qs_Qw[j,:] = lp_Qw.Q_s.copy()
        
    # ---- Analyse
    G_zs.append((z[4000:,:].max(axis=0) - z[4000:,:].min(axis=0)) / \
        (2. * A * (L - lp.x) * (mean_Qs/(lp.k_Qs*mean_Qw))**(6./7.)))
    G_Qss.append((Qs[4000:,:].max(axis=0) - Qs[4000:,:].min(axis=0)) / \
        (2. * A * mean_ssd_Qs))
    G_Qs_Qws.append((Qs_Qw[4000:,:].max(axis=0) - Qs_Qw[4000:,:].min(axis=0)) / \
        (2. * A * mean_ssd_Qs))
    # lag_zs.append(find_lag_times(z, time, scale) / period)
    # lag_Qss.append(find_lag_times(Qs, time, scale, can_lead=True) / period)
    # lag_Qs_Qws.append(find_lag_times(Qs_Qw, time, scale, can_lead=True) / period)
    lag_zs.append(find_lag_times_x_corr(z[2000:,:], scale[2000:], time[:4000], period) / period)
    lag_Qss.append(find_lag_times_x_corr(Qs[2000:,:], scale[2000:], time[:4000], period) / period)
    lag_Qs_Qws.append(find_lag_times_x_corr(Qs_Qw[2000:,:], scale[2000:], time[:4000], period) / period)
    
    
# ---- Plot
fig, axs = plt.subplots(2,3,sharex=True)
axs[0,0].plot(lp.x/1000., lp.compute_z_gain(period), "--")
for G_z in G_zs:
    axs[0,0].plot(lp.x/1000., G_z)
axs[0,0].set_ylabel(r"$G_z$")
axs[0,0].set_ylim(0., 1.2)
axs[1,0].plot(lp.x/1000., lp.compute_z_lag(period)/period, "--")
for lag_z in lag_zs:
    axs[1,0].plot(lp.x/1000., lag_z)
axs[1,0].set_xlabel(r"$x$ [km]")
axs[1,0].set_ylabel(r"$\varphi_z$")
axs[0,1].plot(lp.x/1000., lp.compute_Qs_gain(period, A_Qs=A), "--")
for G_Qs in G_Qss:
    axs[0,1].plot(lp.x/1000., G_Qs)
axs[1,1].plot(lp.x/1000., lp.compute_Qs_lag(period, A_Qs=A)/period, "--")
for lag_Qs in lag_Qss:
    axs[1,1].plot(lp.x/1000., lag_Qs)
axs[1,1].set_xlabel(r"$x$ [km]")
axs[0,2].plot(lp.x/1000., lp.compute_Qs_gain(period, A_Q=A), "--")
for G_Qs in G_Qs_Qws:
    axs[0,2].plot(lp.x/1000., G_Qs)
axs[1,2].plot(lp.x/1000., lp.compute_Qs_lag(period, A_Q=A)/period, "--")
for lag_Qs in lag_Qs_Qws:
    axs[1,2].plot(lp.x/1000., lag_Qs)
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

out_dir = "./output/continuous_spatial/"

with open(out_dir + "G_z_lin.dg", "wb") as f:
    arr = np.column_stack(( lp.x/1000., lp.compute_z_gain(period) ))
    np.savetxt(f, arr)
with open(out_dir + "G_z.dg", "wb") as f:
    for i,p in enumerate(ps):
        hdr = b"> -Z%f\n" % p
        f.write(hdr)
        arr = np.column_stack((lp.x/1000., G_zs[i]))
        np.savetxt(f, arr)
        
with open(out_dir + "G_Qs_lin.dg", "wb") as f:
    arr = np.column_stack(( lp.x/1000., lp.compute_Qs_gain(period, A_Qs=A) ))
    np.savetxt(f, arr)
with open(out_dir + "G_Qs.dg", "wb") as f:
    for i,p in enumerate(ps):
        hdr = b"> -Z%f\n" % p
        f.write(hdr)
        arr = np.column_stack((lp.x/1000., G_Qss[i]))
        np.savetxt(f, arr)
        
with open(out_dir + "G_Qs_Qw_lin.dg", "wb") as f:
    arr = np.column_stack(( lp.x/1000., lp.compute_Qs_gain(period, A_Q=A) ))
    np.savetxt(f, arr)
with open(out_dir + "G_Qs_Qw.dg", "wb") as f:
    for i,p in enumerate(ps):
        hdr = b"> -Z%f\n" % p
        f.write(hdr)
        arr = np.column_stack((lp.x/1000., G_Qs_Qws[i]))
        np.savetxt(f, arr)
        
with open(out_dir + "Lag_z_lin.dl", "wb") as f:
    arr = np.column_stack(( lp.x/1000., lp.compute_z_lag(period)/period ))
    np.savetxt(f, arr)
with open(out_dir + "Lag_z.dl", "wb") as f:
    for i,p in enumerate(ps):
        hdr = b"> -Z%f\n" % p
        f.write(hdr)
        arr = np.column_stack((lp.x/1000., lag_zs[i]))
        np.savetxt(f, arr)
        
with open(out_dir + "Lag_Qs_lin.dl", "wb") as f:
    arr = np.column_stack(( lp.x/1000., lp.compute_Qs_lag(period, A_Qs=A)/period ))
    np.savetxt(f, arr)
with open(out_dir + "Lag_Qs.dl", "wb") as f:
    for i,p in enumerate(ps):
        hdr = b"> -Z%f\n" % p
        f.write(hdr)
        arr = np.column_stack((lp.x/1000., lag_Qss[i]))
        np.savetxt(f, arr)
        
with open(out_dir + "Lag_Qs_Qw_lin.dl", "wb") as f:
    arr = np.column_stack(( lp.x/1000., lp.compute_Qs_lag(period, A_Q=A)/period ))
    np.savetxt(f, arr)
with open(out_dir + "Lag_Qs_Qw.dl", "wb") as f:
    for i,p in enumerate(ps):
        hdr = b"> -Z%f\n" % p
        f.write(hdr)
        arr = np.column_stack((lp.x/1000., lag_Qs_Qws[i]))
        np.savetxt(f, arr)