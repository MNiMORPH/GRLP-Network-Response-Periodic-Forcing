"""
This script performs the analysis presented in Figures S14 and S15 of McNab et
al. (2025, EGUsphere); produces a rough version of the Figure; and, optionally,
generates output files for plotting the final Figure in GMT.

The purpose of the script/figure is to explore how gain and lag vary as
functions of the forcing period for the single segment case with along stream
sediment and water supply. We compare the results with analytical solutions
derived by McNab et al. (2023, GRL) for the upstream supply case.

Here, in contrast with Figures 6 and S3, valley width is set to increase
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
periods = np.logspace(-2., 2., 29)


# ---- Along stream sediment and water supply

# Set up lists for output
periodics_Qs = [[] for p in ps]
periodics_Q = [[] for p in ps]

# Loop over hack exponents
for i,p in enumerate(ps):
    print("Hack exponent, p = %.1f." % p)
    
    # Set up the network object.
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

    # Loop over periods.
    for j,period in enumerate(periods):
        period *= net.list_of_LongProfile_objects[0].equilibration_time
        
        # Sediment supply.
        print(
            "\r" + 
            u"\u25AE"*int(np.round((j*2)/(len(periods)*2)*50)) + 
            u"\u25AF"*int(np.round(50 - (j*2)/(len(periods)*2)*50)) + 
            " " + 
            str(int((j*2)/(len(periods)*2)*100)).rjust(3) + "%. " + 
            "Period = %e kyr." % (period/3.154e10),
            end=""
            )
        periodic_Qs = grlpx.evolve_network_periodic(
            net=copy.deepcopy(net),
            period=period,
            A_Qs=0.2, 
            A_Q=0.
            )

        # Water supply.
        print(
            "\r" + 
            u"\u25AE"*int(np.round((j*2+1)/(len(periods)*2)*50)) + 
            u"\u25AF"*int(np.round(50 - (j*2+1)/(len(periods)*2)*50)) + 
            " " + 
            str(int((j*2+1)/(len(periods)*2)*100)).rjust(3) + "%. " + 
            "Period = %e kyr." % (period/3.154e10),
            end=""
            )
        periodic_Q = grlpx.evolve_network_periodic(
            net=copy.deepcopy(net),
            period=period,
            A_Qs=0., 
            A_Q=0.2
            )
        periodics_Qs[i].append(periodic_Qs)
        periodics_Q[i].append(periodic_Q)

    print(
        "\r" + 
        u"\u25AE"*50 + 
        " 100%%. Period = %e kyr." % (period/3.154e10)
        )
    print()


# ---- Upstream sediment and water supply
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
    lin_gain_Qs[i,:] = lp.compute_Qs_gain(p, A_Qs=0.2)
    lin_lag_Qs[i,:] = lp.compute_Qs_lag(p, A_Qs=0.2, nsum=1000) / p
    lin_gain_Qs_Qw[i,:] = lp.compute_Qs_gain(p, A_Q=0.2)
    lin_lag_Qs_Qw[i,:] = lp.compute_Qs_lag(p, A_Q=0.2) / p
    
# ---- Plot
print("Plotting.")

# Main figure  -- gain and lag for elevation, in response to variation in
# sediment supply, and for sediment output, in response to variation in
# sediment and water supply.

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
        periods, 
        [periodic['G_z'][0][-1] for periodic in periodics_Qs[i]]
        )
    axs[0,0].plot(
        periods, 
        [periodic['G_z'][0][0] for periodic in periodics_Qs[i]],
        "--"
        )
        
    axs[1,0].plot(
        periods, 
        [periodic['lag_z'][0][-1]
            for i,periodic in enumerate(periodics_Qs[i])]
        )
    axs[1,0].plot(
        periods, 
        [periodic['lag_z'][0][0]
            for i,periodic in enumerate(periodics_Qs[i])],
        "--"
        )
    axs[1,0].plot(
        periods, 
        [periodic['lag_z'][0].max()
            for i,periodic in enumerate(periodics_Qs[i])],
        ":"
        )

    axs[0,1].plot(
        periods, 
        [periodic['G_Qs'][0][-1] for periodic in periodics_Qs[i]]
        )

    axs[1,1].plot(
        periods, 
        [periodic['lag_Qs'] for i,periodic in enumerate(periodics_Qs[i])]
        )

    axs[0,2].plot(
        periods, 
        [periodic['G_Qs'][0][-1] for periodic in periodics_Q[i]]
        )

    axs[1,2].plot(
        periods, 
        [periodic['lag_Qs'] for i,periodic in enumerate(periodics_Q[i])]
        )

axs[1,0].set_ylim(0., 0.5)
axs[1,1].set_ylim(0, 0.5)
for ax in axs[0]:
    ax.set_ylim(0., 1.2)
axs[0,0].set_xscale("log")

axs[0,0].set_ylabel(r"$G$")
axs[1,0].set_ylabel(r"$\varphi / P$")

for ax in axs[1]:
    ax.set_xlabel(r"$P$ / $T_{eq}$")
fig.suptitle("Figure S14")
plt.show()

# Extra figure  -- gain and lag for elevation, in response to variation in
# sediment and water supply.

fig, axs = plt.subplots(2,1,sharex=True)

axs[0].fill(
    np.hstack(( lin_periods, lin_periods[::-1] )) / lp.equilibration_time,
    np.hstack(( lin_gain[:,-1], lin_gain[:,0][::-1] )),
    "0.9"
    )
    
axs[1].fill(
    np.hstack(( lin_periods, lin_periods[::-1] )) / lp.equilibration_time,
    np.hstack(( lin_lag[:,-1], lin_lag[:,0][::-1] )),
    "0.9"
    )

axs[0].plot(lin_periods/lp.equilibration_time, lin_gain[:,-1], "0.6")
axs[1].plot(lin_periods/lp.equilibration_time, lin_lag[:,-1], "0.6")

for i in range(len(ps)):

    axs[0].plot(
        periods, 
        [periodic['G_z'][0][-1] for periodic in periodics_Q[i]]
        )
    axs[0].plot(
        periods, 
        [periodic['G_z'][0][0] for periodic in periodics_Q[i]],
        "--"
        )
        
    axs[1].plot(
        periods, 
        [periodic['lag_z'][0][-1]
            for i,periodic in enumerate(periodics_Q[i])]
        )
    axs[1].plot(
        periods, 
        [periodic['lag_z'][0][0]
            for i,periodic in enumerate(periodics_Q[i])],
        "--"
        )
    axs[1].plot(
        periods, 
        [periodic['lag_z'][0].max()
            for i,periodic in enumerate(periodics_Q[i])],
        ":"
        )

axs[1].set_ylim(0, 0.5)
axs[0].set_xscale("log")

axs[0].set_ylabel(r"$G_z$")
axs[1].set_ylabel(r"$\varphi_z~/~P$")

for ax in axs:
    ax.set_xlabel(r"$P$ / $T_{eq}$")
fig.suptitle("Figure S15")
plt.show()


# ---- Output

if output_gmt:

    out_dir = "../../Output/SingleSegment/" + \
        "Figure_S14_S15_SingleSegment_Periods_Non-Uniform_Width/"

    with open(out_dir + "G_z_out_lin.pg", "wb") as f:
        arr = np.column_stack((
            lin_periods/lp.equilibration_time,
            lin_gain[:,-1]
            ))
        np.savetxt(f, arr)
        
    with open(out_dir + "G_z_rng_lin.pg", "wb") as f:
        arr = np.column_stack((
            np.hstack(( lin_periods, lin_periods[::-1] ))/lp.equilibration_time,
            np.hstack(( lin_gain[:,-1], lin_gain[:,0][::-1] ))
            ))
        np.savetxt(f, arr)
        
    with open(out_dir + "G_z_num.pg", "wb") as f:
        for i,p in enumerate(ps):
            hdr = b"> -Z%f\n" % p
            f.write(hdr)
            arr = np.column_stack((
                periods, 
                [periodic['G_z'][0][0] for periodic in periodics_Qs[i]],
                [periodic['G_z'][0][-1] for periodic in periodics_Qs[i]],
                ))
            np.savetxt(f, arr)

    with open(out_dir + "G_z_num_Qw.pg", "wb") as f:
        for i,p in enumerate(ps):
            hdr = b"> -Z%f\n" % p
            f.write(hdr)
            arr = np.column_stack((
                periods, 
                [periodic['G_z'][0][0] for periodic in periodics_Q[i]],
                [periodic['G_z'][0][-1] for periodic in periodics_Q[i]],
                ))
            np.savetxt(f, arr)
            
    with open(out_dir + "lag_z_out_lin.pl", "wb") as f:
        arr = np.column_stack((
            lin_periods/lp.equilibration_time,
            lin_lag[:,-1]
            ))
        np.savetxt(f, arr)
        
    with open(out_dir + "lag_z_rng_lin.pl", "wb") as f:
        arr = np.column_stack((
            np.hstack(( lin_periods, lin_periods[::-1] ))/lp.equilibration_time,
            np.hstack(( lin_lag[:,-1], lin_lag[:,0][::-1] ))
            ))
        np.savetxt(f, arr)
        
    with open(out_dir + "lag_z_num.pl", "wb") as f:
        for i,p in enumerate(ps):
            hdr = b"> -Z%f\n" % p
            f.write(hdr)
            arr = np.column_stack((
                periods, 
                [periodic['lag_z'][0][0]
                    for i,periodic in enumerate(periodics_Qs[i])],
                [periodic['lag_z'][0][-1]
                    for i,periodic in enumerate(periodics_Qs[i])],
                [periodic['lag_z'][0].max()
                    for i,periodic in enumerate(periodics_Qs[i])],
                ))
            np.savetxt(f, arr)

    with open(out_dir + "lag_z_num_Qw.pl", "wb") as f:
        for i,p in enumerate(ps):
            hdr = b"> -Z%f\n" % p
            f.write(hdr)
            arr = np.column_stack((
                periods, 
                [periodic['lag_z'][0][0]
                    for i,periodic in enumerate(periodics_Q[i])],
                [periodic['lag_z'][0][-1]
                    for i,periodic in enumerate(periodics_Q[i])],
                [periodic['lag_z'][0].max()
                    for i,periodic in enumerate(periodics_Q[i])],
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
                periods, 
                [periodic['G_Qs'][0][-1] for periodic in periodics_Qs[i]]
                ))
            np.savetxt(f, arr)

    with open(out_dir + "lag_Qs_out_lin.pl", "wb") as f:
        arr = np.column_stack((
            lin_periods/lp.equilibration_time,
            lin_lag_Qs[:,-1]
            ))
        np.savetxt(f, arr)
        
    with open(out_dir + "lag_Qs_num.pl", "wb") as f:
        for i,p in enumerate(ps):
            hdr = b"> -Z%f\n" % p
            f.write(hdr)
            arr = np.column_stack((
                periods, 
                [periodic['lag_Qs'] for i,periodic in enumerate(periodics_Qs[i])]
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
                periods, 
                [periodic['G_Qs'][0][-1] for periodic in periodics_Q[i]]
                ))
            np.savetxt(f, arr)

    with open(out_dir + "lag_Qs_Qw_out_lin.pl", "wb") as f:
        arr = np.column_stack((
            lin_periods/lp.equilibration_time,
            lin_lag_Qs_Qw[:,-1]
            ))
        np.savetxt(f, arr)
        
    with open(out_dir + "lag_Qs_Qw_num.pl", "wb") as f:
        for i,p in enumerate(ps):
            hdr = b"> -Z%f\n" % p
            f.write(hdr)
            arr = np.column_stack((
                periods, 
                [periodic['lag_Qs'] for i,periodic in enumerate(periodics_Q[i])]
                ))
            np.savetxt(f, arr)