from grlp import *
from extras import *
from copy import deepcopy
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap



# ---- River properties
x0 = 10.e3
L = 100.e3
mean_Qw = 10.
mean_Qs = 0.001
B = 98.1202038813591
hack_p = 1./0.55 # Hack
lp = set_up_long_profile(L, mean_Qw, mean_Qs, hack_p, B, dx=1.e2, evolve=True)

# ---- Loop over periods
periods = np.logspace(-2., 2., 7) * lp.equilibration_time
G_zs = []
G_Qss = []
G_Qs_Qws = []
lag_zs = []
lag_Qss = []
lag_Qs_Qws = []
for period in periods:
    
    print(period)
    
    lp_Qs = deepcopy(lp)
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
    A = 0.2
    time = np.arange(0., 6.*period, period/1000.)
    scale = 1. + A*np.sin(2.*np.pi*time/period)
    z = np.zeros((len(time), len(lp.x)))
    Qs = np.zeros((len(time), len(lp.x)))
    z_Qw = np.zeros((len(time), len(lp.x)))
    Qs_Qw = np.zeros((len(time), len(lp.x)))
    for j,s in enumerate(scale):
        
        lp_Qs.set_Qs_input_upstream(mean_Qs0 * s)
        lp_Qs.set_source_sink_distributed(mean_ssd * s)
        lp_Qs.evolve_threshold_width_river(nt=1, dt=period/1000.)
        lp_Qs.compute_Q_s()
        z[j,:] = lp_Qs.z.copy()
        Qs[j,:] = lp_Qs.Q_s.copy()
        
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
lin_periods = np.logspace(-2., 2., 21) * lp.equilibration_time
lin_gain = np.zeros((len(lin_periods), len(lp.x)))
lin_lag = np.zeros((len(lin_periods), len(lp.x)))
lin_gain_Qs = np.zeros((len(lin_periods), len(lp.x)))
lin_lag_Qs = np.zeros((len(lin_periods), len(lp.x)))
lin_gain_Qs_Qw = np.zeros((len(lin_periods), len(lp.x)))
lin_lag_Qs_Qw = np.zeros((len(lin_periods), len(lp.x)))
for i,p in enumerate(lin_periods):
    lin_gain[i,:] = lp.compute_z_gain(p)
    lin_lag[i,:] = lp.compute_z_lag(p, nsum=1000) / p
    lin_gain_Qs[i,:] = lp.compute_Qs_gain(p, A_Qs=0.2)
    lin_lag_Qs[i,:] = lp.compute_Qs_lag(p, A_Qs=0.2, nsum=1000) / p
    lin_gain_Qs_Qw[i,:] = lp.compute_Qs_gain(p, A_Q=0.2)
    lin_lag_Qs_Qw[i,:] = lp.compute_Qs_lag(p, A_Q=0.2, nsum=1000) / p


fig, axs = plt.subplots(2,3,sharex=True)

axs[0,0].plot(lin_periods/lp.equilibration_time, lin_gain[:,-1])
for i,p in enumerate(periods):
    axs[0,0].errorbar(
        p/lp.equilibration_time, 
        G_zs[i][-1], 
        yerr=[[G_zs[i][-1]-G_zs[i].min()], [G_zs[i].max()-G_zs[i][-1]]],
        marker="o")

axs[1,0].plot(lin_periods/lp.equilibration_time, lin_lag[:,-1])
for i,p in enumerate(periods):
    axs[1,0].errorbar(
        p/lp.equilibration_time, 
        lag_zs[i][-1], 
        yerr=[[lag_zs[i][-1]-lag_zs[i].min()], [lag_zs[i].max()-lag_zs[i][-1]]],
        marker="o")

axs[0,1].plot(lin_periods/lp.equilibration_time, lin_gain_Qs[:,-1])
for i,p in enumerate(periods):
    axs[0,1].errorbar(
        p/lp.equilibration_time, 
        G_Qss[i][-1], 
        yerr=[[G_Qss[i][-1]-G_Qss[i].min()], [G_Qss[i].max()-G_Qss[i][-1]]],
        marker="o")

axs[1,1].plot(lin_periods/lp.equilibration_time, lin_lag_Qs[:,-1])
for i,p in enumerate(periods):
    axs[1,1].errorbar(
        p/lp.equilibration_time, 
        lag_Qss[i][-1], 
        yerr=[[lag_Qss[i][-1]-lag_Qss[i].min()], [lag_Qss[i].max()-lag_Qss[i][-1]]],
        marker="o")

axs[0,2].plot(lin_periods/lp.equilibration_time, lin_gain_Qs_Qw[:,-1])
for i,p in enumerate(periods):
    axs[0,2].errorbar(
        p/lp.equilibration_time, 
        G_Qs_Qws[i][-1], 
        yerr=[[G_Qs_Qws[i][-1]-G_Qs_Qws[i].min()], [G_Qs_Qws[i].max()-G_Qs_Qws[i][-1]]],
        marker="o")

axs[1,2].plot(lin_periods/lp.equilibration_time, lin_lag_Qs_Qw[:,-1])
for i,p in enumerate(periods):
    axs[1,2].errorbar(
        p/lp.equilibration_time, 
        lag_Qs_Qws[i][-1], 
        yerr=[[lag_Qs_Qws[i][-1]-lag_Qs_Qws[i].min()], [lag_Qs_Qws[i].max()-lag_Qs_Qws[i][-1]]],
        marker="o")

axs[0,0].set_xscale("log")
plt.show()