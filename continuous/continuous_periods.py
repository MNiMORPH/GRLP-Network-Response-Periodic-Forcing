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


# ---- Loop over periods
periods = np.logspace(-2., 2., 29) * 3.154e12
periodics_Qs = [[] for p in ps]
periodics_Qw = [[] for p in ps]
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
        
        periodic_Qs = grlpx.evolve_network_periodic(
            net=copy.deepcopy(net),
            period=period,
            A_Qs=0.2, 
            A_Q=0.
            )
        periodic_Qw = grlpx.evolve_network_periodic(
            net=copy.deepcopy(net),
            period=period,
            A_Qs=0., 
            A_Q=0.2
            )
        periodics_Qs[i].append(periodic_Qs)
        periodics_Qw[i].append(periodic_Qw)

    
# ---- Linear
lp = net.list_of_LongProfile_objects[0]
lin_periods = np.logspace(-2., 2., 81) * lp.equilibration_time
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

axs[0,0].fill(
    np.hstack(( lin_periods, lin_periods[::-1] )) / lp.equilibration_time,
    np.hstack(( lin_gain[:,-1], lin_gain[:,0][::-1] )),
    "0.9"
    )
    
axs[1,0].fill(
    np.hstack(( lin_periods, lin_periods[::-1] )) / lp.equilibration_time,
    np.hstack(( lin_lag[:,-1], lin_lag[:,0][::-1] )),
    "0.9"
    )

axs[0,0].plot(lin_periods/lp.equilibration_time, lin_gain[:,-1], "0.6")
axs[1,0].plot(lin_periods/lp.equilibration_time, lin_lag[:,-1], "0.6")
axs[0,1].plot(lin_periods/lp.equilibration_time, lin_gain_Qs[:,-1], "0.6")
axs[1,1].plot(lin_periods/lp.equilibration_time, lin_lag_Qs[:,-1], "0.6")
axs[0,2].plot(lin_periods/lp.equilibration_time, lin_gain_Qs_Qw[:,-1], "0.6")
axs[1,2].plot(lin_periods/lp.equilibration_time, lin_lag_Qs_Qw[:,-1], "0.6")

for i in range(len(ps)):

    axs[0,0].plot(
        periods/lp.equilibration_time, 
        [periodic['G_z'][0][-1] for periodic in periodics_Qs[i]]
        )
    axs[0,0].plot(
        periods/lp.equilibration_time, 
        [periodic['G_z'][0][0] for periodic in periodics_Qs[i]],
        "--"
        )
        
    axs[1,0].plot(
        periods/lp.equilibration_time, 
        [periodic['lag_z'][0][-1] for i,periodic in enumerate(periodics_Qs[i])]
        )
    axs[1,0].plot(
        periods/lp.equilibration_time, 
        [periodic['lag_z'][0][0] for i,periodic in enumerate(periodics_Qs[i])],
        "--"
        )
    axs[1,0].plot(
        periods/lp.equilibration_time, 
        [periodic['lag_z'][0].max() for i,periodic in enumerate(periodics_Qs[i])],
        ":"
        )

    axs[0,1].plot(
        periods/lp.equilibration_time, 
        [periodic['G_Qs'][0][-1] for periodic in periodics_Qs[i]]
        )

    axs[1,1].plot(
        periods/lp.equilibration_time, 
        [periodic['lag_Qs']/periods[i] for i,periodic in enumerate(periodics_Qs[i])]
        )

    axs[0,2].plot(
        periods/lp.equilibration_time, 
        [periodic['G_Qs'][0][-1] for periodic in periodics_Qw[i]]
        )

    axs[1,2].plot(
        periods/lp.equilibration_time, 
        [periodic['lag_Qs']/periods[i] for i,periodic in enumerate(periodics_Qw[i])]
        )

axs[1,0].set_ylim(0., 0.4)
axs[1,1].set_ylim(0, 0.4)
for ax in axs[0]:
    ax.set_ylim(0., 1.2)
axs[0,0].set_xscale("log")

axs[0,0].set_ylabel(r"$G$")
axs[1,0].set_ylabel(r"$\varphi / P$")

for ax in axs[1]:
    ax.set_xlabel(r"$P$ / $T_{eq}$")
plt.show()


# ---- Output

if output_gmt:

    # out_dir = "../output/continuous/periods/"
    out_dir = "../output/continuous/periods_var_width/"

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
                [periodic['G_z'][0][0] for periodic in periodics_Qs[i]],
                [periodic['G_z'][0][-1] for periodic in periodics_Qs[i]],
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
            hdr = b"> -Z%f\n" % p
            f.write(hdr)
            arr = np.column_stack((
                periods/lp.equilibration_time, 
                [periodic['lag_z'][0][0] for i,periodic in enumerate(periodics_Qs[i])],
                [periodic['lag_z'][0][-1] for i,periodic in enumerate(periodics_Qs[i])],
                [periodic['lag_z'][0].max() for i,periodic in enumerate(periodics_Qs[i])],
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
            hdr = b"> -Z%f\n" % p
            f.write(hdr)
            arr = np.column_stack((
                periods/lp.equilibration_time, 
                [periodic['G_Qs'][0][-1] for periodic in periodics_Qs[i]]
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
            hdr = b"> -Z%f\n" % p
            f.write(hdr)
            arr = np.column_stack((
                periods/lp.equilibration_time, 
                [periodic['lag_Qs']/periods[i] for i,periodic in enumerate(periodics_Qs[i])]
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
            hdr = b"> -Z%f\n" % p
            f.write(hdr)
            arr = np.column_stack((
                periods/lp.equilibration_time, 
                [periodic['G_Qs'][0][-1] for periodic in periodics_Qw[i]]
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
            hdr = b"> -Z%f\n" % p
            f.write(hdr)
            arr = np.column_stack((
                periods/lp.equilibration_time, 
                [periodic['lag_Qs']/periods[i] for i,periodic in enumerate(periodics_Qw[i])]
                ))
            np.savetxt(f, arr)