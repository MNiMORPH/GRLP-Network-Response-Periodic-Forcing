from grlp import *
from grlp_extras import *
from copy import deepcopy
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap

def find_lag_time_single(val, time, scale, threshold=0., can_lead=False, period=False, full=False):
    
    scl_peaks, __ = find_peaks(scale)
    scl_troughs, __ = find_peaks(-scale)
    scl_tps = np.sort( np.hstack(( scl_peaks, scl_troughs )) )

    obs_peaks, __ = find_peaks(val)
    obs_troughs, __ = find_peaks(-val)
    obs_tps = np.sort( np.hstack(( obs_peaks, obs_troughs )) )
    if not can_lead:
        obs_tps = obs_tps[ np.where( obs_tps >= scl_tps[0] ) ]
    
    obs_tps_attached = np.zeros( len(obs_tps), dtype=int )
    obs_lag_time = np.zeros( len(obs_tps), dtype=int )

    for j,tp in enumerate(obs_tps):
        if j > len(scl_tps)-1:
            continue
        obs_tps_attached[j] = scl_tps[j]
        obs_lag_time[j] = time[tp] - time[scl_tps[j]]
        
    peak_lags_i = []
    trough_lags_i = []

    for k,tp in enumerate(obs_tps_attached):

        if obs_lag_time[k] != 0.:
            if any(scl_peaks == tp):
                peak_lags_i.append( obs_lag_time[k].copy() )
            else:
                trough_lags_i.append( obs_lag_time[k].copy() )

    if len(peak_lags_i) > 1:
        peak_lags = np.array(peak_lags_i[1:]).mean()
    else:
        peak_lags = np.nan

    if len(trough_lags_i) > 1:
        trough_lags = np.array(trough_lags_i[1:]).mean()
    else:
        trough_lags = np.nan
    
    return (peak_lags + trough_lags)/2.


# initial set up
lp = LongProfile()
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

# ---- Loop over periods
periods = np.logspace(-2., 2., 9) * 3.154e12
# ps = np.array([0.4, 0.5, 0.6, 0.7])
ps = np.array([1.4, 1.8, 2.2, 2.6])
G_zs = []
G_Qss = []
G_Qs_Qws = []
lag_zs = []
lag_Qss = []
lag_Qs_Qws = []
G_z_errs = []
G_Qs_errs = []
# G_Qs_Qw_errs = []
lag_z_errs = []
# lag_Qs_errs = []
# lag_Qs_Qw_errs = []
for p in ps:
    
    # net = set_up_long_profile(L, mean_Qw, mean_Qs, 1/p, B, dx=1.e3, evolve=True)
    net = set_up_long_profile(L, Qw_mean, Qs_mean, B_mean, p, p, p, x0=x0, dx=1.e3, evolve=True)
    G_z_p = []
    lag_z_p = []
    G_Qs_p = []
    lag_Qs_p = []
    G_Qs_Qw_p = []
    lag_Qs_Qw_p = []
    G_z_err_p = []
    lag_z_err_p = []
    # G_Qs_err_p = []
    # lag_Qs_err_p = []
    # G_Qs_Qw_err_p = []
    # lag_Qs_Qw_err_p = []

    for period in periods:
        
        print(period)
        
        A = 0.2
        Qs_periodic = evolve_network_periodic(deepcopy(net), period, 0.2, 0.)
        Qw_periodic = evolve_network_periodic(deepcopy(net), period, 0., 0.2)

        z_gain = compute_network_gain(Qs_periodic['z'], 0.2)
        Qs_gain = compute_network_gain(Qs_periodic['Qs'], 0.2)
        z_lag = find_network_lag(net, Qs_periodic['z'], Qs_periodic['time'], Qs_periodic['Qs_scale'], period)
        # Qs_lag = find_network_lag(net, Qs, time, scale, period)
        Qs_lag = find_lag_time_single(Qs_periodic['z'][0][:,-1], Qs_periodic['time'], Qs_periodic['Qs_scale'], period)/period
        G_z_p.append(z_gain[0][-1])
        G_Qs_p.append(Qs_gain[0][-1])
        lag_z_p.append(z_lag[0][-1])
        # lag_Qs_p.append(Qs_lag[0][-1])
        lag_Qs_p.append(Qs_lag)
        G_z_err_p.append([z_gain[0][-1]-z_gain[0].min(), z_gain[0].max()-z_gain[0][-1]])
        # G_Qs_err_p.append([Qs_gain[0][-1]-Qs_gain[0].min(), Qs_gain[0].max()-Qs_gain[0][-1]])
        lag_z_err_p.append([z_lag[0][-1]-z_lag[0].min(), z_lag[0].max()-z_lag[0][-1]])
        # lag_Qs_err_p.append([Qs_lag[0][-1]-Qs_lag[0].min(), Qs_lag[0].max()-Qs_lag[0][-1]])

        Qs_gain = compute_network_gain(Qw_periodic['Qs'], 0.2)
        # Qs_lag = find_network_lag(net, Qs_Qw, time_Qw, scale_Qw, period, can_lead=True)
        Qs_lag = find_lag_time_single(Qw_periodic['Qs'][0][:,-1], Qw_periodic['time'], Qw_periodic['Qw_scale'], period, can_lead=True)/period
        G_Qs_Qw_p.append(Qs_gain[0][-1])
        # lag_Qs_Qw_p.append(Qs_lag[0][-1])
        lag_Qs_Qw_p.append(Qs_lag)
        # G_Qs_Qw_err_p.append([Qs_gain[0][-1]-Qs_gain[0].min(), Qs_gain[0].max()-Qs_gain[0][-1]])
        # lag_Qs_Qw_err_p.append([Qs_lag[0][-1]-Qs_lag[0].min(), Qs_lag[0].max()-Qs_lag[0][-1]])
    
    G_zs.append(G_z_p)
    G_Qss.append(G_Qs_p)
    G_Qs_Qws.append(G_Qs_Qw_p)
    lag_zs.append(lag_z_p)
    lag_Qss.append(lag_Qs_p)
    lag_Qs_Qws.append(lag_Qs_Qw_p)

    G_z_errs.append(G_z_err_p)
    # G_Qs_errs.append(G_Qs_err_p)
    # G_Qs_Qw_errs.append(G_Qs_Qw_err_p)
    lag_z_errs.append(lag_z_err_p)
    # lag_Qs_errs.append(lag_Qs_err_p)
    # lag_Qs_Qw_errs.append(lag_Qs_Qw_err_p)
    
# ---- Linear
lp = net.list_of_LongProfile_objects[0]
lin_periods = np.logspace(-2.5, 2.5, 81) * lp.equilibration_time
lin_gain = np.zeros((len(lin_periods), len(lp.x)))
lin_lag = np.zeros((len(lin_periods), len(lp.x)))
lin_gain_Qs = np.zeros((len(lin_periods), len(lp.x)))
lin_lag_Qs = np.zeros((len(lin_periods), len(lp.x)))
lin_gain_Qs_Qw = np.zeros((len(lin_periods), len(lp.x)))
lin_lag_Qs_Qw = np.zeros((len(lin_periods), len(lp.x)))
for i,p in enumerate(lin_periods):
    lin_gain[i,:] = lp.compute_z_gain(p)
    lin_lag[i,:] = lp.compute_z_lag(p, nsum=1000) / p
    
    while lin_lag[i,0] > 0.5:
        lin_lag[i,:] -= 0.5
    
    lin_gain_Qs[i,:] = lp.compute_Qs_gain(p, A_Qs=0.2)
    lin_lag_Qs[i,:] = lp.compute_Qs_lag(p, A_Qs=0.2, nsum=1000) / p
    lin_gain_Qs_Qw[i,:] = lp.compute_Qs_gain(p, A_Q=0.2)
    lin_lag_Qs_Qw[i,:] = lp.compute_Qs_lag(p, A_Q=0.2) / p
    
# ---- Plot
fig, axs = plt.subplots(2,3,sharex=True)

axs[0,0].plot(lin_periods/lp.equilibration_time, lin_gain[:,-1])
axs[1,0].plot(lin_periods/lp.equilibration_time, lin_lag[:,-1])
axs[1,0].plot(lin_periods/lp.equilibration_time, lin_lag[:,-0], "--")
axs[0,1].plot(lin_periods/lp.equilibration_time, lin_gain_Qs[:,-1])
axs[1,1].plot(lin_periods/lp.equilibration_time, lin_lag_Qs[:,-1])
axs[0,2].plot(lin_periods/lp.equilibration_time, lin_gain_Qs_Qw[:,-1])
axs[1,2].plot(lin_periods/lp.equilibration_time, lin_lag_Qs_Qw[:,-1])

for i in range(len(ps)):

    axs[0,0].errorbar(
        periods/lp.equilibration_time, 
        G_zs[i], 
        yerr=np.vstack(G_z_errs[i]).transpose(),
        fmt="o")

    axs[1,0].errorbar(
        periods/lp.equilibration_time, 
        lag_zs[i], 
        yerr=np.vstack(lag_z_errs[i]).transpose(),
        fmt="o")
        
    axs[0,1].scatter(
        periods/lp.equilibration_time, 
        G_Qss[i])

    axs[1,1].scatter(
        periods/lp.equilibration_time, 
        lag_Qss[i])

    axs[0,2].scatter(
        periods/lp.equilibration_time, 
        G_Qs_Qws[i])

    axs[1,2].scatter(
        periods/lp.equilibration_time, 
        lag_Qs_Qws[i])

axs[1,0].set_ylim(0,0.4)
axs[1,1].set_ylim(0,0.4)
axs[0,0].set_xscale("log")
plt.show()


import sys
sys.exit()

# ---- Output

out_dir = "../output/continuous/periods/"

with open(out_dir + "G_z_out_lin.pg", "wb") as f:
    arr = np.column_stack((
        lin_periods/lp.equilibration_time,
        lin_gain[:,-1]
        ))
    np.savetxt(f, arr)
    
with open(out_dir + "G_z_rng_lin.pg", "wb") as f:
    arr = np.column_stack((
        np.hstack(( lin_periods, lin_periods[::-1] )) / lp.equilibration_time,
        np.hstack(( lin_gain[:,-1], lin_gain[:,0][::-1] ))
        ))
    np.savetxt(f, arr)
    
with open(out_dir + "G_z_num.pg", "wb") as f:
    for i,p in enumerate(ps):
        hdr = b"> -Z%f\n" % p
        f.write(hdr)
        arr = np.column_stack((
            periods/lp.equilibration_time, 
            G_zs[i],
            np.full(len(periods), p),
            np.vstack(G_z_errs[i]).transpose()[0],
            np.vstack(G_z_errs[i]).transpose()[1]
            ))
        np.savetxt(f, arr)
        
with open(out_dir + "G_z_in_num.pg", "wb") as f:
    for i,p in enumerate(ps):
        hdr = b"> -Z%f\n" % p
        f.write(hdr)
        arr = np.column_stack((
            periods/lp.equilibration_time, 
            G_zs[i] - np.vstack(G_z_errs[i]).transpose()[0],
            np.full(len(periods), p),
            np.vstack(G_z_errs[i]).transpose()[0],
            np.vstack(G_z_errs[i]).transpose()[1]
            ))
        np.savetxt(f, arr)
        
with open(out_dir + "lag_z_out_lin.pg", "wb") as f:
    arr = np.column_stack((
        lin_periods/lp.equilibration_time,
        lin_lag[:,-1]
        ))
    np.savetxt(f, arr)
    
with open(out_dir + "lag_z_rng_lin.pg", "wb") as f:
    arr = np.column_stack((
        np.hstack(( lin_periods, lin_periods[::-1] )) / lp.equilibration_time,
        np.hstack(( lin_lag[:,-1], lin_lag[:,0][::-1] ))
        ))
    np.savetxt(f, arr)
    
with open(out_dir + "lag_z_num.pg", "wb") as f:
    for i,p in enumerate(ps):
        arr = np.column_stack((
            periods/lp.equilibration_time, 
            lag_zs[i],
            np.full(len(periods), p),
            np.vstack(lag_z_errs[i]).transpose()[0],
            np.vstack(lag_z_errs[i]).transpose()[1]
            ))
        np.savetxt(f, arr)
        
with open(out_dir + "G_Qs_out_lin.pg", "wb") as f:
    arr = np.column_stack((
        lin_periods/lp.equilibration_time,
        lin_gain_Qs[:,-1]
        ))
    np.savetxt(f, arr)
    
with open(out_dir + "G_Qs_num.pg", "wb") as f:
    for i,p in enumerate(ps):
        arr = np.column_stack((
            periods/lp.equilibration_time, 
            G_Qss[i],
            np.full(len(periods), p)
            ))
        np.savetxt(f, arr)

with open(out_dir + "lag_Qs_out_lin.pg", "wb") as f:
    arr = np.column_stack((
        lin_periods/lp.equilibration_time,
        lin_lag_Qs[:,-1]
        ))
    np.savetxt(f, arr)
    
with open(out_dir + "lag_Qs_num.pg", "wb") as f:
    for i,p in enumerate(ps):
        arr = np.column_stack((
            periods/lp.equilibration_time, 
            lag_Qss[i],
            np.full(len(periods), p)
            ))
        np.savetxt(f, arr)
        
with open(out_dir + "G_Qs_Qw_out_lin.pg", "wb") as f:
    arr = np.column_stack((
        lin_periods/lp.equilibration_time,
        lin_gain_Qs_Qw[:,-1]
        ))
    np.savetxt(f, arr)
    
with open(out_dir + "G_Qs_Qw_num.pg", "wb") as f:
    for i,p in enumerate(ps):
        arr = np.column_stack((
            periods/lp.equilibration_time, 
            G_Qs_Qws[i],
            np.full(len(periods), p)
            ))
        np.savetxt(f, arr)

with open(out_dir + "lag_Qs_Qw_out_lin.pg", "wb") as f:
    arr = np.column_stack((
        lin_periods/lp.equilibration_time,
        lin_lag_Qs_Qw[:,-1]
        ))
    np.savetxt(f, arr)
    
with open(out_dir + "lag_Qs_Qw_num.pg", "wb") as f:
    for i,p in enumerate(ps):
        arr = np.column_stack((
            periods/lp.equilibration_time, 
            lag_Qs_Qws[i],
            np.full(len(periods), p)
            ))
        np.savetxt(f, arr)