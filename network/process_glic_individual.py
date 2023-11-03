from grlp import *
# from extras import *
from grlp_extras import *
import scipy
import os
import pickle
import copy

# def evolve_river_periodic(lp, period, A_Qs, A_Q, n):
# 
#     # ---- Set up time domain
#     # time, dt = np.linspace(0., period*4., 4000, retstep=True)
#     dt = period / 1000
#     time = np.arange(0., period*n, dt)
#     scale = np.sin(2. * np.pi * time / period)
# 
#     # ---- Set up arrays for output
#     z = np.zeros(( len(time), len(lp.z) ))
#     Qs = np.zeros(( len(time), len(lp.Q_s) ))    
# 
#     # ---- Initial sediment and water supplies
#     Qs0 = copy.deepcopy(lp.Q_s_0)
#     Qw0 = lp.Q.copy()
# 
#     # ---- Evolve
#     for i,s in enumerate(scale):
#         lp.set_Qs_input_upstream(Qs0 * (1. + A_Qs*s))
#         lp.evolve_threshold_width_river(nt=1, dt=dt)
#         z[i,:] = lp.z.copy()
#         lp.compute_Q_s()
#         Qs[i,:] = lp.Q_s.copy()
# 
#     return z, Qs, time, (1. + (A_Qs-A_Q)*scale)
# 
# 
# def evolve_network_periodic(net, period, A_Qs, A_Q, n):
# 
#     # ---- Set up time domain
#     # time, dt = np.linspace(0., period*4., 4000, retstep=True)
#     dt = period / 1000
#     time = np.arange(0., period*n, dt)
#     scale = np.sin(2. * np.pi * time / period)
# 
#     # ---- Set up arrays for output
#     z = [np.zeros(( len(time), len(seg.z) ))
#             for seg in net.list_of_LongProfile_objects]
#     Qs = [np.zeros(( len(time), len(seg.Q_s) ))
#             for seg in net.list_of_LongProfile_objects]
# 
#     # ---- Initial sediment and water supplies
#     Qs0 = net.list_of_LongProfile_objects[net.sources[0]].Q_s_0
#     Qw0 = [np.zeros(len(seg.Q)) for seg in net.list_of_LongProfile_objects]
#     for seg in net.list_of_LongProfile_objects:
#         Qw0[seg.ID] = seg.Q.copy()
# 
#     # ---- Evolve
#     for i,s in enumerate(scale):
#         for seg in net.list_of_LongProfile_objects:
#             seg.set_Q(Qw0[seg.ID] * (1. + A_Q*s))
#             if seg.ID in net.sources:
#                 seg.set_Qs_input_upstream(Qs0 * (1. + A_Qs*s))
#         net.evolve_threshold_width_river_network(nt=1, dt=dt)
#         for seg in net.list_of_LongProfile_objects:
#             z[seg.ID][i,:] = seg.z.copy()
#             seg.compute_Q_s()
#             Qs[seg.ID][i,:] = seg.Q_s.copy()
# 
#     return z, Qs, time, (1. + (A_Qs-A_Q)*scale)
# 
# def compute_network_z_gain(net, z, A_Qs, A_Q, S0):
#     gain = [np.zeros(len(seg.z)) for seg in net.list_of_LongProfile_objects]
#     for seg in net.list_of_LongProfile_objects:
#         amp = (
#             # z[seg.ID][2000:,:].max(axis=0) - 
#             # z[seg.ID][2000:,:].min(axis=0)
#             z[seg.ID].max(axis=0) - 
#             z[seg.ID].min(axis=0)
#             ) / 2.
#         gain[seg.ID] = (
#             amp / (
#                 S0 * 
#                 (net.list_of_LongProfile_objects[0].x_ext.max() - seg.x) *
#                 abs(A_Qs-A_Q) ) 
#             )
#     return gain
# 
# def compute_network_Qs_gain(net, Qs, A_Qs, A_Q, Qs0):
#     gain = [np.zeros(len(seg.Q_s)) for seg in net.list_of_LongProfile_objects]
#     for seg in net.list_of_LongProfile_objects:
#         amp = (
#             # Qs[seg.ID][2000:,:].max(axis=0) - 
#             # Qs[seg.ID][2000:,:].min(axis=0)
#             Qs[seg.ID].max(axis=0) - 
#             Qs[seg.ID].min(axis=0)
#             ) / 2.
#         gain[seg.ID] = amp / ( Qs0[seg.ID] * abs(A_Qs-A_Q) )
#     return gain
# 
# def find_network_lag(net, prop, time, scale, period):
#     lag = [np.zeros(len(seg.x)) for seg in net.list_of_LongProfile_objects]
#     for seg in net.list_of_LongProfile_objects:
#         lag[seg.ID] = find_lag_times(prop[seg.ID], time, scale) / period
#     return lag

# ---- Load expected lengths
arr = np.loadtxt("./expected_length/expected_lengths.dat")
magnitudes = arr[:,0]
expected_lengths = arr[:,1]

# ---- Linear part
L = 100.e3
mean_Q = 10.
mean_Qs = 0.001
B = 98.1202038813591
S0 = (mean_Qs / (0.040987384904837776 * mean_Q))**(6./7.)
lp = LongProfile()
lp.basic_constants()
lp.bedload_lumped_constants()
lp.set_hydrologic_constants()
dx = 1.e3
x = [np.arange(0., L+dx, dx)]
S0 = [(mean_Qs/(lp.k_Qs*mean_Q))**(6./7.)]
upstream_segment_IDs = [[]]
downstream_segment_IDs = [[]]
z = [(x[0].max()-x[0])*S0]
Q = [np.full(len(x),mean_Q)]
B = [np.full(len(x),B)]
net = Network()
net.initialize(
    config_file = None,
    x_bl =L+dx,
    z_bl = 0.,
    S0 = S0,
    upstream_segment_IDs = upstream_segment_IDs,
    downstream_segment_IDs = downstream_segment_IDs,
    x = x,
    z = z,
    Q = Q,
    B = B,
    overwrite = False
    )
net.set_niter(3)
net.get_z_lengths()
diff = (7./6.) * lp.k_Qs * mean_Q * (S0[0]**(1./6.)) / (B[0] * (1. - lp.lambda_p))
lp = net.list_of_LongProfile_objects[0]
lp.compute_equilibration_time()



# ---- Unpack network results
# indir = "./glic/output_170423/"
# indir = "./glic/output_200423/"
# indir = "./glic/output_210423/"
indir = "./glic/output_170523/"
netdirs = next(os.walk(indir))[1]
hacks = []
nets = []
gains = []
lags = []
for netdir in netdirs:
    with open(indir + netdir + "/hack.obj", "rb") as f:
        hack = pickle.load(f)
        hacks.append(hack)
    with open(indir + netdir + "/props.obj", "rb") as f:
        prop = pickle.load(f)
        net, net_topo = generate_random_network(
            24, 
            prop['L'], 
            prop['B'], 
            prop['Q_mean'], 
            prop['Qs_mean'], 
            evolve=False, 
            topology=prop['topology']
        )
        nets.append(net)
    with open(indir + netdir + "/gain.obj", "rb") as f:
        gain = pickle.load(f)
        gains.append(gain)
    with open(indir + netdir + "/lag.obj", "rb") as f:
        lag = pickle.load(f)
        lags.append(lag)

# ---- Select network
netID = 11

# ---- Repeat periodic

# Evolve to steady state
print("Wind up...")
nets[netID].evolve_threshold_width_river_network(nt=1000, dt=3.15e10)
for seg in nets[netID].list_of_LongProfile_objects: seg.compute_Q_s()

# Run
# periods = np.logspace(-0.5,5.,3) * lp.equilibration_time
periods = np.array([0.2, 1., 5.]) * lp.equilibration_time
nums = [25, 5, 2]
lin_zs = []
lin_Qss = []
zs = []
Qss = []
times = []
scales = []
z_gains = []
z_lags = []
Qs_gains = []
Qs_lags = []
for num, period in zip(nums,periods):
    
    print("Period: %.2f" % period)
    
    # Run, compute metrics
    lpi = copy.deepcopy(lp)
    neti = copy.deepcopy(nets[netID])
    lin_z, lin_Qs, time, scale = evolve_river_periodic(lpi, period, 0.2, 0., num)
    z, Qs, time, scale = evolve_network_periodic(neti, period, 0.2, 0., num)

    z_gain = compute_network_z_gain(neti, z, 0.2, 0., S0)
    Qs_gain = compute_network_Qs_gain(neti, Qs, 0.2, 0., [q[0,:] for q in Qs])
    z_lag = find_network_lag(neti, z, time, scale, period)
    Qs_lag = find_network_lag(neti, Qs, time, scale, period)

    # Record details
    lin_zs.append(lin_z)
    lin_Qss.append(lin_Qs)
    zs.append(z)
    Qss.append(Qs)
    times.append(time)
    scales.append(scale)
    
    # Record gain
    z_gains.append(z_gain)
    Qs_gains.append(Qs_gain)

    # Record lag
    z_lags.append(z_lag)
    Qs_lags.append(Qs_lag)

import sys
sys.exit()

# ---- Save

outdir = "../output/network_example/"
orders = np.arange(1,len(nets[netID].order_counts)+1,1)

with open(outdir + "gain_fast.dg", "wb") as f:
    for seg in nets[netID].list_of_LongProfile_objects:
        hdr = b"> -Z%d\n" % (nets[netID].segment_orders[seg.ID]+1)
        f.write(hdr)
        arr = np.column_stack((
            seg.x/1.e3,
            z_gains[0][seg.ID],
            ))
        np.savetxt(f, arr)

with open(outdir + "lag_fast.dl", "wb") as f:
    for seg in nets[netID].list_of_LongProfile_objects:
        hdr = b"> -Z%d\n" % (nets[netID].segment_orders[seg.ID]+1)
        f.write(hdr)
        arr = np.column_stack((
            seg.x/1.e3,
            z_lags[0][seg.ID],
            ))
        np.savetxt(f, arr)

with open(outdir + "gain_medium.dg", "wb") as f:
    for seg in nets[netID].list_of_LongProfile_objects:
        hdr = b"> -Z%d\n" % (nets[netID].segment_orders[seg.ID]+1)
        f.write(hdr)
        arr = np.column_stack((
            seg.x/1.e3,
            z_gains[1][seg.ID],
            ))
        np.savetxt(f, arr)

with open(outdir + "lag_medium.dl", "wb") as f:
    for seg in nets[netID].list_of_LongProfile_objects:
        hdr = b"> -Z%d\n" % (nets[netID].segment_orders[seg.ID]+1)
        f.write(hdr)
        arr = np.column_stack((
            seg.x/1.e3,
            z_lags[1][seg.ID],
            ))
        np.savetxt(f, arr)

with open(outdir + "gain_slow.dg", "wb") as f:
    for seg in nets[netID].list_of_LongProfile_objects:
        hdr = b"> -Z%d\n" % (nets[netID].segment_orders[seg.ID]+1)
        f.write(hdr)
        arr = np.column_stack((
            seg.x/1.e3,
            z_gains[2][seg.ID],
            ))
        np.savetxt(f, arr)

with open(outdir + "lag_slow.dl", "wb") as f:
    for seg in nets[netID].list_of_LongProfile_objects:
        hdr = b"> -Z%d\n" % (nets[netID].segment_orders[seg.ID]+1)
        f.write(hdr)
        arr = np.column_stack((
            seg.x/1.e3,
            z_lags[2][seg.ID],
            ))
        np.savetxt(f, arr)

with open(outdir + "lin_gain.dg", "wb") as f:
    arr = np.column_stack((
        lp.x/1.e3,
        lp.compute_z_gain(periods[0]),
        lp.compute_z_gain(periods[1]),
        lp.compute_z_gain(periods[2])
        ))
    np.savetxt(f, arr)

with open(outdir + "lin_lag.dl", "wb") as f:
    arr = np.column_stack((
        lp.x/1.e3,
        lp.compute_z_lag(periods[0]) / periods[0],
        lp.compute_z_lag(periods[1]) / periods[1],
        lp.compute_z_lag(periods[2]) / periods[2]
        ))
    np.savetxt(f, arr)

outdir = "../output/network_example/gif/"
orders = np.arange(1,len(nets[netID].order_counts)+1,1)
labels = ["fast/", "medium/", "slow/"]
ts = np.linspace(0., times[1][-1], 200)
segs = [22, 21, 18, 17, 1]
seg_xs = [0, 15, 5, 20, 11]
lin_xs = [0, 19, 39, 59, 79]

with open(outdir + "steady_profile.de", "wb") as f:
    arr = np.column_stack(( lp.x/1000., lp.z ))
    np.savetxt(f, arr)
    
with open(outdir + "z_refs.te", "wb") as f:
    for segID, seg_x in zip(segs, seg_xs):
        seg = nets[netID].list_of_LongProfile_objects[segID]
        hdr = b"> -Z%d\n" % (nets[netID].segment_orders[seg.ID]+1)
        f.write(hdr)
        arr = np.column_stack(([0., 500.], [seg.z[seg_x], seg.z[seg_x]]))
        np.savetxt(f, arr)
        
with open(outdir + "lin_z_refs.te", "wb") as f:
    for x in lin_xs:
        hdr = b"> -Z%.2f\n" % (lp.x[x]/1.e3)
        f.write(hdr)
        arr = np.column_stack(([0., 500.], [lp.z[x]]*2))
        np.savetxt(f, arr)

for i,p in enumerate(periods):
    
    scl_peaks = find_peaks(scales[i])[0]
    scl_troughs = find_peaks(-scales[i])[0]
    scl_tps = np.sort( np.hstack(( scl_peaks, scl_troughs )) )
    
    outfile = outdir + labels[i] + "scale.ts"
    with open(outfile, "wb") as f:
        arr = np.column_stack(( times[i]/3.15e10, scales[i] ))
        np.savetxt(f, arr)
        
        
    for j,t in enumerate(ts):
        
        outfile = outdir + labels[i] + "scale%s_tps.ts" % (str(j).zfill(3))
        with open(outfile, "wb") as f:
            tinterp = np.interp(t, times[i], np.arange(0,len(times[i]),1))
            tps = scl_tps[np.where(scl_tps < tinterp)]
            arr = np.column_stack(( times[i][tps]/3.15e10, scales[i][tps] ))
            np.savetxt(f, arr)
            
        outfile = outdir + labels[i] + "scale%s_tps_refs.ts" % (str(j).zfill(3))
        with open(outfile, "wb") as f:
            tinterp = np.interp(t, times[i], np.arange(0,len(times[i]),1))
            tps = scl_tps[np.where(scl_tps < tinterp)]
            for tp in tps:
                f.write(b">\n")
                arr = np.column_stack((
                    [times[i][tp]/3.15e10]*2,
                    [0,scales[i][tp]]
                    ))
                np.savetxt(f, arr)
                
        outfile = outdir + labels[i] + "scale%s_tps_refs.te" % (str(j).zfill(3))
        with open(outfile, "wb") as f:
            tinterp = np.interp(t, times[i], np.arange(0,len(times[i]),1))
            tps = scl_tps[np.where(scl_tps < tinterp)]
            for tp in tps:
                f.write(b">\n")
                arr = np.column_stack((
                    [times[i][tp]/3.15e10]*2,
                    [0,1000]
                    ))
                np.savetxt(f, arr)

        outfile = outdir + labels[i] + "scale%s.ts" % (str(j).zfill(3))
        with open(outfile, "wb") as f:
            arr = np.column_stack(( 
                ts[:j+1]/3.15e10,
                np.interp(ts[:j+1], times[i], scales[i])
                ))
            np.savetxt(f, arr)
            
        outfile = outdir + labels[i] + "scale%s.ts" % (str(j).zfill(3))
        with open(outfile, "wb") as f:
            arr = np.column_stack(( 
                ts[:j+1]/3.15e10,
                np.interp(ts[:j+1], times[i], scales[i])
                ))
            np.savetxt(f, arr)
            
        outfile = outdir + labels[i] + "lin_Qs%s.ts" % (str(j).zfill(3))
        with open(outfile, "wb") as f:
            arr = np.column_stack(( 
                ts[:j+1]/3.15e10,
                np.interp(ts[:j+1], times[i], lin_Qss[i][:,-1]/lp.Q_s_0)
                ))
            np.savetxt(f, arr)

        outfile = outdir + labels[i] + "lin_z%s.te" % (str(j).zfill(3))
        with open(outfile, "wb") as f:
            for x in lin_xs:
                hdr = b"> -Z%d\n" % (lp.x[x]/1.e3)
                f.write(hdr)
                arr = np.column_stack(( 
                    ts[:j+1]/3.15e10,
                    np.interp(ts[:j+1], times[i], lin_zs[i][:,x])
                    ))
                np.savetxt(f, arr)
                
        outfile = outdir + labels[i] + "lin_z%s.de" % (str(j).zfill(3))
        with open(outfile, "wb") as f:
            for k,x in enumerate(lp.x):
                arr = np.column_stack(( 
                    x/1.e3,
                    np.interp(t, times[i], lin_zs[i][:,k])
                    ))
                np.savetxt(f, arr)

        outfile = outdir + labels[i] + "lin_z%s_circles.de" % (str(j).zfill(3))
        with open(outfile, "wb") as f:
            for x in lin_xs:
                arr = np.column_stack(( 
                    lp.x[x]/1.e3,
                    np.interp(t, times[i], lin_zs[i][:,x]),
                    lp.x[x]/1.e3
                    ))
                np.savetxt(f, arr)

        outfile = outdir + labels[i] + "Qs%s.ts" % (str(j).zfill(3))
        with open(outfile, "wb") as f:
            arr = np.column_stack(( 
                ts[:j+1]/3.15e10,
                np.interp(ts[:j+1], times[i], Qss[i][0][:,-1]/nets[netID].list_of_LongProfile_objects[0].Q_s[-1])
                ))
            np.savetxt(f, arr)

        outfile = outdir + labels[i] + "z%s.de" % (str(j).zfill(3))
        with open(outfile, "wb") as f:
            for seg in nets[netID].list_of_LongProfile_objects:
                hdr = b"> -Z%d\n" % (nets[netID].segment_orders[seg.ID]+1)
                f.write(hdr)
                for k,x in enumerate(seg.x):
                    arr = np.column_stack(( 
                        x/1.e3,
                        np.interp(t, times[i], zs[i][seg.ID][:,k])
                        ))
                    np.savetxt(f, arr)
                    
        outfile = outdir + labels[i] + "z%s_circles.de" % (str(j).zfill(3))
        with open(outfile, "wb") as f:
            for segID,seg_x in zip(segs, seg_xs):
                seg = nets[netID].list_of_LongProfile_objects[segID]
                arr = np.column_stack(( 
                    seg.x[seg_x]/1.e3,
                    np.interp(t, times[i], zs[i][seg.ID][:,seg_x]),
                    nets[netID].segment_orders[seg.ID]+1
                    ))
                np.savetxt(f, arr)
                
        outfile = outdir + labels[i] + "z%s.te" % (str(j).zfill(3))
        with open(outfile, "wb") as f:
            for segID,seg_x in zip(segs, seg_xs):
                seg = nets[netID].list_of_LongProfile_objects[segID]
                hdr = b"> -Z%d\n" % (nets[netID].segment_orders[seg.ID]+1)
                f.write(hdr)
                arr = np.column_stack(( 
                    ts[:j+1]/3.15e10,
                    np.interp(ts[:j+1], times[i], zs[i][seg.ID][:,seg_x])
                    ))
                np.savetxt(f, arr)