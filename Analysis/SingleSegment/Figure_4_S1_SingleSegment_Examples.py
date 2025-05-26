"""
This script performs the analysis presented in Figures 4 and S1 of McNab et al.
(2025, EGUsphere); produces a rough version of the Figure; and, optionally,
generates output files for plotting the final Figure in GMT.

The purpose of the script/figure is to illustrate how a valley's long profile
and sediment output vary in response to sinusoidal variations in sediment or
water supply. We compare the upstream supply case, in which sediment and water
are only supplied at the inlet, and the along stream supply case, in which
sediment and water are also supplied along the valley. 
"""


# ---- Import functions

# External packages
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
import copy
import grlp

# Local packages
import grlp_extras as grlpx


# ---- Output?
output_gmt = False


# ---- Valley properties
# Define properties to use when constructing the single segment valleys.
# Correspond to precipitation rate of c. 1 m/yr for a catchment with Hack
# exponent of 1.6 and runoff coefficent of 0.4; and an equilibration time of
# 100 kyr.
# See ../Compute_River_Properties.py for details.
x0 = 50.e3
L = 100.e3
Q_mean = 26.
Qs_mean = Q_mean * 1.e-4
B_mean = 254.
p = 1.6


# ---- Set up the network object(s)
net = grlpx.generate_single_segment_network(
    L=L, 
    Q_mean=Q_mean,
    Qs_mean=Qs_mean, 
    B_mean=B_mean,
    p_Q=p,
    p_B=0., 
    dx=5.e2, 
    evolve=True
    )
ref_net = grlpx.generate_single_segment_network(
    L=L, 
    Q_mean=Q_mean,
    Qs_mean=Qs_mean, 
    B_mean=B_mean,
    p_Q=0.,
    p_B=0., 
    dx=5.e2, 
    evolve=True
    )


# ---- Evolve

# Periods to use
Teq = ref_net.list_of_LongProfile_objects[0].equilibration_time
periods = np.array([0.1, 1., 10.]) * Teq

# Prepare for analysis - variation in sediment supply
evolutions_Qs = []
ref_evolutions_Qs = []
spinups_Qs = []
ref_spinups_Qs = []

# Loop over periods
print("Varying sediment supply:")
for i,period in enumerate(periods):
    print(u"  \u2022 Period = %e kyr" % (period/3.154e10))

    # Make clean copies of network objects
    neti = copy.deepcopy(net)
    ref_neti = copy.deepcopy(ref_net)

    # Run spin-up phase - constant sediment supply prior to onset of periodic
    # forcing. Save output.
    print("    - Spin-up.")
    spinup_time, dt = np.linspace(-period/4., 0., 250, retstep=True)
    spinup_z, spinup_Qs = grlpx.evolve_network(
        net=neti,
        time=spinup_time,
        Qs_scale=np.ones_like(spinup_time),
        Q_scale=np.ones_like(spinup_time),
        S_scale=np.ones_like(spinup_time)
    )
    ref_spinup_z, ref_spinup_Qs = grlpx.evolve_network(
        net=ref_neti,
        time=spinup_time,
        Qs_scale=np.ones_like(spinup_time),
        Q_scale=np.ones_like(spinup_time),
        S_scale=np.ones_like(spinup_time)
    )
    spinups_Qs.append({
        'time': spinup_time,
        'z': spinup_z,
        'Qs': spinup_Qs
    })
    ref_spinups_Qs.append({
        'time': spinup_time,
        'z': ref_spinup_z,
        'Qs': ref_spinup_Qs
    })
    
    # Run periodic phase, save output.
    print("    - Periodic.")
    periodic = grlpx.evolve_network_periodic(
        net=neti,
        period=period,
        A_Qs=0.2,
        A_Q=0.
        )
    ref_periodic = grlpx.evolve_network_periodic(
        net=ref_neti,
        period=period,
        A_Qs=0.2,
        A_Q=0.
        )
    evolutions_Qs.append(periodic)
    ref_evolutions_Qs.append(ref_periodic)
    
print()

# Prepare for analysis - variation in water supply
evolutions_Qw = []
ref_evolutions_Qw = []
spinups_Qw = []
ref_spinups_Qw = []

# Loop over periods
print("Varying water supply:")
for i,period in enumerate(periods):
    print(u"  \u2022 Period = %e kyr" % (period/3.154e10))

    # Make clean copies of network objects
    neti = copy.deepcopy(net)
    ref_neti = copy.deepcopy(ref_net)

    # Run spin-up phase - constant water supply prior to onset of periodic
    # forcing. Save output.
    print("    - Spin-up.")
    spinup_time, dt = np.linspace(-period/4., 0., 250, retstep=True)
    spinup_z, spinup_Qs = grlpx.evolve_network(
        net=neti,
        time=spinup_time,
        Qs_scale=np.ones_like(spinup_time),
        Q_scale=np.ones_like(spinup_time),
        S_scale=np.ones_like(spinup_time)
    )
    ref_spinup_z, ref_spinup_Qs = grlpx.evolve_network(
        net=ref_neti,
        time=spinup_time,
        Qs_scale=np.ones_like(spinup_time),
        Q_scale=np.ones_like(spinup_time),
        S_scale=np.ones_like(spinup_time)
    )
    spinups_Qw.append({
        'time': spinup_time,
        'z': spinup_z,
        'Qs': spinup_Qs
    })
    ref_spinups_Qw.append({
        'time': spinup_time,
        'z': ref_spinup_z,
        'Qs': ref_spinup_Qs
    })
    
    # Run periodic phase, save output.
    print("    - Periodic.")
    periodic = grlpx.evolve_network_periodic(
        net=neti,
        period=period,
        A_Qs=0.,
        A_Q=0.2
        )
    ref_periodic = grlpx.evolve_network_periodic(
        net=ref_neti,
        period=period,
        A_Qs=0.,
        A_Q=0.2
        )
    evolutions_Qw.append(periodic)
    ref_evolutions_Qw.append(ref_periodic)

print()


# ---- Plots
print("Plotting.")

# Main figure -- sediment output for variation in sediment supply and water
# supply; variation in long profile for variation in sediment supply.

fig, axs = plt.subplots(4,3,sharey='row')

for i,period in enumerate(periods):

    ev = evolutions_Qs[i]
    ref_ev = ref_evolutions_Qs[i]
    
    ev_Qw = evolutions_Qw[i]
    ref_ev_Qw = ref_evolutions_Qw[i]

    axs[0,i].plot(ev['time']/3.154e10, ev['Qs_scale'], color="0.7")
    axs[0,i].plot(
        ev['time']/3.154e10,
        ref_ev['Qs'][0][:,-1] / ref_ev['Qs'][0][:,-1].mean(),
        "--",
        color="0.3"
        )
    axs[0,i].plot(
        ev['time']/3.154e10,
        ev['Qs'][0][:,-1] / ev['Qs'][0][:,-1].mean()
        )

    axs[1,i].plot(ev['time']/3.154e10, ev_Qw['Q_scale'], color="0.7")
    axs[1,i].plot(
        ev['time']/3.154e10,
        ref_ev_Qw['Qs'][0][:,-1] / ref_ev_Qw['Qs'][0][:,-1].mean(),
        "--",
        color="0.3"
        )
    axs[1,i].plot(
        ev['time']/3.154e10,
        ev_Qw['Qs'][0][:,-1] / ev_Qw['Qs'][0][:,-1].mean()
        )


    xs = [0, 40, 80, 120, 160]
    axs[2,i].plot(ev['time']/3.154e10, ref_ev['z'][0][:,xs], "--", color="0.3")
    axs[2,i].plot(ev['time']/3.154e10, ev['z'][0][:,xs])

    ts = [3000,3050,3100,3150,3200,3250]
    for t in ts:
        axs[3,i].plot(
            net.list_of_LongProfile_objects[0].x/1.e3,
            ev['z'][0][t,:]
            )
        axs[3,i].plot(
            net.list_of_LongProfile_objects[0].x/1.e3,
            ev['z'][0][t,:]-ev['z'][0][0,:],
            "--"
            )

axs[0,0].set_ylabel(r"${Q_{s,0}}'$, ${Q_{s,L}}'$")
for ax in axs[0]:
    ax.set_xlabel(r"$t$ [kyr]")
    
axs[1,0].set_ylabel(r"${Q_{w,0}}'$, ${Q_{s,L}}'$")
for ax in axs[1]:
    ax.set_xlabel(r"$t$ [kyr]")

axs[2,0].set_ylabel(r"$z$ [m]")
for ax in axs[2]:
    ax.set_xlabel(r"$t$ [kyr]")

axs[3,0].set_ylabel(r"$z$ [m]")
for ax in axs[3]:
    ax.set_xlabel(r"$x$ [km]")

fig.suptitle("Figure 4")
plt.show()

# Extra figure -- sediment output and long profile variation for variation in
# water supply.

fig, axs = plt.subplots(3,3,sharey='row')

for i,period in enumerate(periods):

    ev = evolutions_Qs[i]
    ref_ev = ref_evolutions_Qs[i]
    
    ev_Qw = evolutions_Qw[i]
    ref_ev_Qw = ref_evolutions_Qw[i]

    axs[0,i].plot(ev['time']/3.154e10, ev_Qw['Q_scale'], color="0.7")
    axs[0,i].plot(
        ev['time']/3.154e10,
        ref_ev_Qw['Qs'][0][:,-1] / ref_ev_Qw['Qs'][0][:,-1].mean(),
        "--",
        color="0.3"
        )
    axs[0,i].plot(
        ev['time']/3.154e10,
        ev_Qw['Qs'][0][:,-1] / ev_Qw['Qs'][0][:,-1].mean()
        )


    xs = [0, 40, 80, 120, 160]
    axs[1,i].plot(
        ev['time']/3.154e10, ref_ev_Qw['z'][0][:,xs], "--", color="0.3"
        )
    axs[1,i].plot(ev['time']/3.154e10, ev_Qw['z'][0][:,xs])

    ts = [3000,3050,3100,3150,3200,3250]
    for t in ts:
        axs[2,i].plot(
            net.list_of_LongProfile_objects[0].x/1.e3,
            ev_Qw['z'][0][t,:]
            )
        axs[2,i].plot(
            net.list_of_LongProfile_objects[0].x/1.e3,
            ev_Qw['z'][0][t,:]-ev_Qw['z'][0][0,:],
            "--"
            )

axs[0,0].set_ylabel(r"${Q_{w,0}}'$, ${Q_{s,L}}'$")
for ax in axs[0]:
    ax.set_xlabel(r"$t$ [kyr]")

axs[1,0].set_ylabel(r"$z$ [m]")
for ax in axs[1]:
    ax.set_xlabel(r"$t$ [kyr]")

axs[2,0].set_ylabel(r"$z$ [m]")
for ax in axs[2]:
    ax.set_xlabel(r"$x$ [km]")

fig.suptitle("Figure S1")
plt.show()


# ---- Write output

if output_gmt:
    
    basedir = "../../Output/SingleSegment/Figure_4_S1_SingleSegment_Examples/"

    labels = ["fast/", "medium/", "slow/"]

    for i,period in enumerate(periods):
        
        outdir = basedir + labels[i]

        with open(outdir + "force_tps_ref.te", "wb") as f:
            tps = [250 + 500*i for i in range(8)]*2
            for tp in tps:
                hdr = b">\n"
                f.write(hdr)
                arr = np.column_stack((
                    [evolutions_Qs[i]['time'][tp]/3.154e10]*2,
                    [0, 1.e3]
                    ))
                np.savetxt(f, arr)
                
        with open(outdir + "force_tps.tq", "wb") as f:
            tps = [250 + 500*i for i in range(8)]*2
            arr = np.column_stack((
                evolutions_Qs[i]['time'][np.array(tps)]/3.154e10,
                [1.2, 0.8]*8
                ))
            np.savetxt(f, arr)
            
        with open(outdir + "Qs_scale.tq", "wb") as f:
            arr = np.column_stack((
                np.hstack((
                    spinups_Qs[i]['time'][0],
                    evolutions_Qs[i]['time']
                    )) / 3.15e10,
                np.hstack((
                    1.,
                    evolutions_Qs[i]['Qs_scale']
                    ))
                ))
            np.savetxt(f, arr)
            
        with open(outdir + "Qs_out.tq", "wb") as f:
            arr = np.column_stack((
                np.hstack((
                    spinups_Qs[i]['time'],
                    evolutions_Qs[i]['time']
                    )) / 3.15e10,
                np.hstack((
                    spinups_Qs[i]['Qs'][0][:,-1],
                    evolutions_Qs[i]['Qs'][0][:,-1]
                    )) / spinups_Qs[i]['Qs'][0][0,-1]
                ))
            np.savetxt(f, arr)
            
        with open(outdir + "Qs_out_tps.tq", "wb") as f:
            pks = sig.find_peaks(evolutions_Qs[i]['Qs'][0][:,-1])[0]
            trs = sig.find_peaks(-evolutions_Qs[i]['Qs'][0][:,-1])[0]
            tps = np.hstack((pks, trs))
            tps = tps[tps > 250]
            arr = np.column_stack((
                evolutions_Qs[i]['time'][tps]/3.154e10,
                evolutions_Qs[i]['Qs'][0][tps,-1]/spinups_Qs[i]['Qs'][0][0,-1]
                ))
            np.savetxt(f, arr)
            
        with open(outdir + "ref_Qs_out.tq", "wb") as f:
            arr = np.column_stack((
                np.hstack((
                    spinups_Qs[i]['time'],
                    evolutions_Qs[i]['time']
                    )) / 3.15e10,
                np.hstack((
                    ref_spinups_Qs[i]['Qs'][0][:,-1],
                    ref_evolutions_Qs[i]['Qs'][0][:,-1]
                    )) / ref_spinups_Qs[i]['Qs'][0][0,-1]
                ))
            np.savetxt(f, arr)
            
        with open(outdir + "ref_Qs_out_tps.tq", "wb") as f:
            pks = sig.find_peaks(ref_evolutions_Qs[i]['Qs'][0][:,-1])[0]
            trs = sig.find_peaks(-ref_evolutions_Qs[i]['Qs'][0][:,-1])[0]
            tps = np.hstack((pks, trs))
            tps = tps[tps > 250]
            arr = np.column_stack((
                ref_evolutions_Qs[i]['time'][tps]/3.154e10,
                ref_evolutions_Qs[i]['Qs'][0][tps,-1]/ref_spinups_Qs[i]['Qs'][0][0,-1]
                ))
            np.savetxt(f, arr)


        xs = [0, 40, 80, 120, 160]
        with open(outdir + "profile.te", "wb") as f:
            for x in xs:
                hdr = b"> -Z%.f\n" % (
                    net.list_of_LongProfile_objects[0].x[x]/1.e3
                    )
                f.write(hdr)
                arr = np.column_stack((
                    np.hstack((
                        spinups_Qs[i]['time'],
                        evolutions_Qs[i]['time']
                        )) / 3.15e10,
                    np.hstack((
                        spinups_Qs[i]['z'][0][:,x],
                        evolutions_Qs[i]['z'][0][:,x]
                        ))
                    ))
                np.savetxt(f, arr)

        with open(outdir + "profile_tps.te", "wb") as f:
            for x in xs:
                pks = sig.find_peaks(evolutions_Qs[i]['z'][0][:,x])[0]
                trs = sig.find_peaks(-evolutions_Qs[i]['z'][0][:,x])[0]
                tps = np.hstack((pks, trs))
                tps = tps[tps > 250]
                arr = np.column_stack((
                    evolutions_Qs[i]['time'][tps]/3.154e10,
                    evolutions_Qs[i]['z'][0][tps,x],
                    np.full(len(tps), net.list_of_LongProfile_objects[0].x[x]/1.e3)
                    ))
                np.savetxt(f, arr)

        with open(outdir + "ref_profile.te", "wb") as f:
            for x in xs:
                hdr = b"> -Z%.f\n" % (
                    net.list_of_LongProfile_objects[0].x[x]/1.e3
                    )
                f.write(hdr)
                arr = np.column_stack((
                    np.hstack((
                        ref_spinups_Qs[i]['time'],
                        ref_evolutions_Qs[i]['time']
                        )) / 3.15e10,
                    np.hstack((
                        ref_spinups_Qs[i]['z'][0][:,x],
                        ref_evolutions_Qs[i]['z'][0][:,x]
                        ))
                    ))
                np.savetxt(f, arr)
                
        with open(outdir + "ref_profile_tps.te", "wb") as f:
            for x in xs:
                pks = sig.find_peaks(ref_evolutions_Qs[i]['z'][0][:,x])[0]
                trs = sig.find_peaks(-ref_evolutions_Qs[i]['z'][0][:,x])[0]
                tps = np.hstack((pks, trs))
                tps = tps[tps > 250]
                arr = np.column_stack((
                    ref_evolutions_Qs[i]['time'][tps]/3.154e10,
                    ref_evolutions_Qs[i]['z'][0][tps,x],
                    ))
                np.savetxt(f, arr)

        ts = np.linspace(2000, 2250, 5).astype(int)
        with open(outdir + "profile.de", "wb") as f:
            for t in ts:
                hdr = b"> -Z%.f\n" % t
                f.write(hdr)
                arr = np.column_stack((
                    net.list_of_LongProfile_objects[0].x/1.e3,
                    evolutions_Qs[i]['z'][0][t,:]
                    ))
                np.savetxt(f, arr)
                
        with open(outdir + "profile_pert.de", "wb") as f:
            for t in ts:
                hdr = b"> -Z%.f\n" % t
                f.write(hdr)
                arr = np.column_stack((
                    net.list_of_LongProfile_objects[0].x/1.e3,
                    evolutions_Qs[i]['z'][0][t,:]-evolutions_Qs[i]['z'][0][0,:]
                    ))
                np.savetxt(f, arr)
                
        with open(outdir + "scale_circles.ts", "wb") as f:
            arr = np.column_stack((
                evolutions_Qs[i]['time'][ts]/3.15e10,
                evolutions_Qs[i]['Qs_scale'][ts],
                ts
                ))
            np.savetxt(f, arr)

        with open(outdir + "Qw_scale.tq", "wb") as f:
            arr = np.column_stack((
                np.hstack((
                    spinups_Qw[i]['time'][0],
                    evolutions_Qw[i]['time']
                    )) / 3.15e10,
                np.hstack(( 1., evolutions_Qw[i]['Q_scale']))
                ))
            np.savetxt(f, arr)
            
        with open(outdir + "Qw_Qs_out.tq", "wb") as f:
            arr = np.column_stack((
                np.hstack((
                    spinups_Qw[i]['time'],
                    evolutions_Qw[i]['time']
                    )) / 3.15e10,
                np.hstack((
                    spinups_Qw[i]['Qs'][0][:,-1],
                    evolutions_Qw[i]['Qs'][0][:,-1]
                    )) / spinups_Qw[i]['Qs'][0][0,-1]
                ))
            np.savetxt(f, arr)
            
        with open(outdir + "Qw_Qs_out_tps.tq", "wb") as f:
            pks = sig.find_peaks(evolutions_Qw[i]['Qs'][0][:,-1])[0]
            trs = sig.find_peaks(-evolutions_Qw[i]['Qs'][0][:,-1])[0]
            tps = np.hstack((pks, trs))
            arr = np.column_stack((
                evolutions_Qw[i]['time'][tps]/3.154e10,
                evolutions_Qw[i]['Qs'][0][tps,-1]/spinups_Qw[i]['Qs'][0][0,-1]
                ))
            np.savetxt(f, arr)

        with open(outdir + "Qw_ref_Qs_out.tq", "wb") as f:
            arr = np.column_stack((
                np.hstack((
                    spinups_Qw[i]['time'],
                    evolutions_Qw[i]['time']
                    )) / 3.15e10,
                np.hstack((
                    ref_spinups_Qw[i]['Qs'][0][:,-1],
                    ref_evolutions_Qw[i]['Qs'][0][:,-1]
                    )) / ref_spinups_Qw[i]['Qs'][0][0,-1]
                ))
            np.savetxt(f, arr)
            
        with open(outdir + "Qw_ref_Qs_out_tps.tq", "wb") as f:
            pks = sig.find_peaks(ref_evolutions_Qw[i]['Qs'][0][:,-1])[0]
            trs = sig.find_peaks(-ref_evolutions_Qw[i]['Qs'][0][:,-1])[0]
            tps = np.hstack((pks, trs))
            arr = np.column_stack((
                ref_evolutions_Qw[i]['time'][tps]/3.154e10,
                ref_evolutions_Qw[i]['Qs'][0][tps,-1]/ref_spinups_Qw[i]['Qs'][0][0,-1]
                ))
            np.savetxt(f, arr)

        
        xs = [0, 40, 80, 120, 160]
        with open(outdir + "Qw_profile.te", "wb") as f:
            for x in xs:
                hdr = b"> -Z%.f\n" % (
                    net.list_of_LongProfile_objects[0].x[x]/1.e3
                    )
                f.write(hdr)
                arr = np.column_stack((
                    np.hstack((
                        spinups_Qw[i]['time'],
                        evolutions_Qw[i]['time']
                        )) / 3.15e10,
                    np.hstack((
                        spinups_Qw[i]['z'][0][:,x],
                        evolutions_Qw[i]['z'][0][:,x]
                        ))
                    ))
                np.savetxt(f, arr)
                
        with open(outdir + "Qw_profile_tps.te", "wb") as f:
            for x in xs:
                pks = sig.find_peaks(evolutions_Qw[i]['z'][0][:,x])[0]
                trs = sig.find_peaks(-evolutions_Qw[i]['z'][0][:,x])[0]
                tps = np.hstack((pks, trs))
                tps = tps[tps > 250]
                arr = np.column_stack((
                    evolutions_Qw[i]['time'][tps]/3.154e10,
                    evolutions_Qw[i]['z'][0][tps,x],
                    np.full(len(tps), net.list_of_LongProfile_objects[0].x[x]/1.e3)
                    ))
                np.savetxt(f, arr)

        with open(outdir + "Qw_ref_profile.te", "wb") as f:
            for x in xs:
                hdr = b"> -Z%.f\n" % (
                    net.list_of_LongProfile_objects[0].x[x]/1.e3
                    )
                f.write(hdr)
                arr = np.column_stack((
                    np.hstack((
                        ref_spinups_Qw[i]['time'],
                        ref_evolutions_Qw[i]['time']
                        )) / 3.15e10,
                    np.hstack((
                        ref_spinups_Qw[i]['z'][0][:,x],
                        ref_evolutions_Qw[i]['z'][0][:,x]
                        ))
                    ))
                np.savetxt(f, arr)
                
        with open(outdir + "Qw_ref_profile_tps.te", "wb") as f:
            for x in xs:
                pks = sig.find_peaks(ref_evolutions_Qw[i]['z'][0][:,x])[0]
                trs = sig.find_peaks(-ref_evolutions_Qw[i]['z'][0][:,x])[0]
                tps = np.hstack((pks, trs))
                tps = tps[tps > 250]
                arr = np.column_stack((
                    ref_evolutions_Qw[i]['time'][tps]/3.154e10,
                    ref_evolutions_Qw[i]['z'][0][tps,x],
                    ))
                np.savetxt(f, arr)

        ts = np.linspace(2000, 2250, 5).astype(int)
        with open(outdir + "Qw_profile.de", "wb") as f:
            for t in ts:
                hdr = b"> -Z%.f\n" % t
                f.write(hdr)
                arr = np.column_stack((
                    net.list_of_LongProfile_objects[0].x/1.e3,
                    evolutions_Qw[i]['z'][0][t,:]
                    ))
                np.savetxt(f, arr)
                
        with open(outdir + "Qw_profile_pert.de", "wb") as f:
            for t in ts:
                hdr = b"> -Z%.f\n" % t
                f.write(hdr)
                arr = np.column_stack((
                    net.list_of_LongProfile_objects[0].x/1.e3,
                    evolutions_Qw[i]['z'][0][t,:]-evolutions_Qw[i]['z'][0][0,:]
                    ))
                np.savetxt(f, arr)
