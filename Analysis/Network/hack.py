from grlp import *
from extras import *
from copy import deepcopy
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap
import random
from scipy import stats

# ----- Expected length
expected_lengths = np.loadtxt("./expected_length/expected_lengths.dat")

# ---- River properties
x0 = 10.e3
L = 100.e3
mean_Qw = 10.
mean_Qs = 0.001
B = 98.1202038813591
# lp = set_up_long_profile(L, mean_Qw, mean_Qs, 0., B, dx=5.e2, evolve=True)


# ---- Set up network
# mag = 200

# mags = [10,100,200,300,400,500,600,700,800]
mags = [100, 200]
mag_hacks_src = []
mag_hacks_seg = []
mag_Rbs = []
mag_Rls = []
mag_RQs = []
mag_meanLs = []
mag_topoLs = []
mag_topoWs = []
for mag in mags:
    hacks_src = []
    hacks_seg = []
    Rbs = []
    Rls = []
    RQs = []
    meanLs = []
    topoLs = []
    topoWs = []
    for i in range(200):
        print(i,mag)
        net, net_topo = generate_random_network(mag, L, B, mean_Qw, mean_Qs)
        hack_nondim = find_network_hack_parameters_non_dim(net)
        hacks_src.append(1./hack_nondim['p_src'])
        hacks_seg.append(1./hack_nondim['p_seg'])
        
        upstream_topo_distance = []
        for seg in net.list_of_LongProfile_objects:
            upstream_topo_distance.append(len(net.find_downstream_IDs(seg.ID)))
        width = stats.mode(upstream_topo_distance).count[0]
        
        Rbs.append(net.bifurcation_ratio)
        Rls.append(net.length_ratio)
        RQs.append(net.discharge_ratio)
        meanLs.append(net.mean_downstream_distance/1.e3)
        topoLs.append(net.max_topological_length/(expected_lengths[mag-1,1]))
        topoWs.append(width)
    mag_hacks_src.append(hacks_src)
    mag_hacks_seg.append(hacks_seg)
    mag_Rbs.append(Rbs)
    mag_Rls.append(Rls)
    mag_RQs.append(RQs)
    mag_meanLs.append(meanLs)
    mag_topoLs.append(topoLs)
    mag_topoWs.append(topoWs)

fig, axs = plt.subplots(1,2,sharex=True,sharey=True)

axs[0].violinplot(mag_hacks_src, mags, widths=40, showmeans=True)
# axs[0].plot([min(mags),max(mags)],[0.55,0.55],":")
axs[0].set_xlabel("Number of sources")
axs[0].set_ylabel("Exponent")
axs[0].set_title("Upstream sources")
axs[0].grid(linestyle=":")

axs[1].violinplot(mag_hacks_seg, mags, widths=40, showmeans=True)
# axs[1].plot([min(mags),max(mags)],[0.55,0.55],":")
axs[1].set_xlabel("Number of sources")
axs[1].set_title("Upstream segments (total)")
axs[1].grid(linestyle=":")

plt.show()

# Qarr = np.linspace(min(hack['d']), max(hack['d']), 10)
larr = np.linspace(min(hack_nondim['lengths']), max(hack_nondim['lengths']), 10)
# plt.scatter(hack['d'], hack['Q'])
# plt.scatter(hack_nondim['lengths'], hack_nondim['sources'])
# plt.plot(Qarr, hack['k']*(Qarr**hack['p']), "--")
# plt.plot(larr, hack_nondim['k']*(larr**hack_nondim['p']), "--")
# # plt.xscale("log")
# # plt.yscale("log")
# plt.show()

plt.scatter(hack_nondim['lengths'], hack_nondim['sources'], label="Upstream sources")
plt.plot(larr, hack_nondim['k_src']*(larr**hack_nondim['p_src']), "--")
plt.scatter(hack_nondim['lengths'], hack_nondim['segments'], label="Upstream segments (total)")
plt.plot(larr, hack_nondim['k_seg']*(larr**hack_nondim['p_seg']), "--")
plt.legend()
plt.xlabel("Distance downstream")
plt.ylabel("Number of segments")
plt.show()


# plt.plot([min(hacks),max(hacks)],[min(hacks),max(hacks)],":")
# plt.scatter(hacks, hacks_nondim)
# plt.show()
# 
# plt.hist(1./np.array(hacks))
# plt.hist(1./np.array(hacks_nondim))
# plt.show()

# plt.scatter(mags, 1./np.array(hacks_src['p']))
# plt.scatter(mags, 1./np.array(hacks_seg['p']))
# plt.plot([min(mags),max(mags)],[0.55,0.55],"--")
# plt.show()

fig, axs = plt.subplots(2,3,sharey=True)
axs[0,0].scatter(mag_Rbs, mag_hacks_seg, c=[np.full(200,100), np.full(200,200)])
axs[0,1].scatter(mag_Rls, mag_hacks_seg, c=[np.full(200,100), np.full(200,200)])
axs[0,2].scatter(mag_RQs, mag_hacks_seg, c=[np.full(200,100), np.full(200,200)])
axs[1,0].scatter(mag_topoLs, mag_hacks_seg, c=[np.full(200,100), np.full(200,200)])
axs[1,1].scatter(mag_topoWs, mag_hacks_seg, c=[np.full(200,100), np.full(200,200)])
axs[1,2].scatter(mag_meanLs, mag_hacks_seg, c=[np.full(200,100), np.full(200,200)])
plt.show()

plt.scatter(np.array(mag_meanLs[0])/np.array(mag_topoWs[0]), mag_hacks_seg[0])
plt.show()


import sys
sys.exit()


# ---- Network
mag = 10
net_topo = Shreve_Random_Network(magnitude=mag, min_link_length=1, max_link_length=1)
sources = [i for i,up_ids in enumerate(net_topo.upstream_segment_IDs) if len(up_ids)==0]
topo_lengths = [len(downstream_IDs(net_topo.downstream_segment_IDs, i)) for i in range(len(net_topo.nxs))]
link_length = L / max(topo_lengths)
link_n = max(5, int(link_length/5.e2))
net_topo.nxs = [link_n for i in range(len(net_topo.nxs))]
dx = link_length / link_n
up_sources = []
for i in range(len(net_topo.upstream_segment_IDs)):
    count = 0
    up_IDs = upstream_IDs(net_topo.upstream_segment_IDs, i)
    for ID in up_IDs:
        if len(upstream_IDs(net_topo.upstream_segment_IDs, ID)) == 1:
            count += 1
    up_sources.append(count)
Qw_max = (mean_Qw / np.mean(up_sources)) * mag
Qs_max = (mean_Qs / np.mean(up_sources)) * mag
net = set_up_network_object(
    nx_list=net_topo.nxs,
    dx=dx,
    upstream_segment_list=net_topo.upstream_segment_IDs,
    downstream_segment_list=net_topo.downstream_segment_IDs,
    Q_max=Qw_max,
    Qs_max=Qs_max,
    evolve=True)
net.compute_network_properties()
for seg in net.list_of_LongProfile_objects: seg.compute_Q_s()
for seg in net.list_of_LongProfile_objects: seg.set_B(B)

# ---- Plot
# planform = plot_network(net)

# ---- Evolve
period = 3.15e13
Qs0 = net.list_of_LongProfile_objects[net.sources[0]].Q_s_0
Qw0 = [np.zeros(len(seg.Q)) for seg in net.list_of_LongProfile_objects]
dt = period/1000.
time = np.arange(-0.3*period, 4*period+dt, dt)
scale = np.ones(len(time))
scale[time >= 0] = 1. + 0.2*np.sin(2.*np.pi*time[time >= 0]/period)
for seg in net.list_of_LongProfile_objects:
    Qw0[seg.ID] = seg.Q.copy()
z = [np.zeros((len(time), len(seg.z)))
    for seg in net.list_of_LongProfile_objects]
Qs = [np.zeros((len(time), len(seg.Q_s)))
    for seg in net.list_of_LongProfile_objects]
for i,s in enumerate(scale):
    for seg in net.list_of_LongProfile_objects:
        if seg.ID in net.sources:
            seg.set_Qs_input_upstream(Qs0 * s)
    net.evolve_threshold_width_river_network(nt=1, dt=dt)
    for seg in net.list_of_LongProfile_objects:
        z[seg.ID][i,:] = seg.z.copy()
        seg.compute_Q_s()
        Qs[seg.ID][i,:] = seg.Q_s.copy()

# ---- Compute gain
gain = [np.zeros(len(seg.z)) for seg in net.list_of_LongProfile_objects]
for seg in net.list_of_LongProfile_objects:
    amp = (z[seg.ID][2000:,:].max(axis=0) - z[seg.ID][2000:,:].min(axis=0)) / 2.
    z0 = z[seg.ID][0,:]
    gain[seg.ID] = amp / (z0 * 0.2)

# ---- Compute lag
lag = {}
lag_simple = [np.zeros(len(seg.z)) for seg in net.list_of_LongProfile_objects]
Qs_lag = {}
for seg in net.list_of_LongProfile_objects:
    lag[seg.ID] = find_lag_times(z[seg.ID], time, scale, full=True)
    lag_simple[seg.ID] = find_lag_times(z[seg.ID], time, scale) / period
    Qs_lag[seg.ID] = find_lag_times(Qs[seg.ID], time, scale, full=True)

# ---- Plot
fig, axs = plt.subplots(1,2)
axs[0].plot(lp.x/1000., lp.compute_z_gain(period), "--")
axs[1].plot(lp.x/1000., lp.compute_z_lag(period)/period, "--")
for seg in net.list_of_LongProfile_objects:
    axs[0].plot(seg.x/1000., gain[seg.ID])
    axs[1].plot(seg.x/1000., (lag[seg.ID]['plags']+lag[seg.ID]['tlags'])/(2*period))
plt.show()

# ---- Select segs
segs = {}
xs = {}
for seg in net.list_of_LongProfile_objects:
    if (seg.x < 1.).any():
        segs[0] = seg
        xs[0] = np.where( seg.x < 1. )[0][0]
    if (seg.x > 19000.).any() and (seg.x < 21000.).any():
        segs[1] = seg
        xs[1] = np.where( (seg.x > 19000.) & (seg.x < 21000.) )[0][0]
    if (seg.x > 39000.).any() and (seg.x < 41000.).any():
        segs[2] = seg
        xs[2] = np.where( (seg.x > 39000.) & (seg.x < 41000.) )[0][0]
    if (seg.x > 59000.).any() and (seg.x < 61000.).any():
        segs[3] = seg
        xs[3] = np.where( (seg.x > 59000.) & (seg.x < 61000.) )[0][0]
    if (seg.x > 79000.).any() and (seg.x < 81000.).any():
        segs[4] = seg
        xs[4] = np.where( (seg.x > 79000.) & (seg.x < 81000.) )[0][0]
        
        
# # ---- Save
out_dir = "../periodic_output_networks/gif/medium/"
slices = np.linspace(0, 3600, 200, dtype=(int))
for i,t in enumerate(slices):
    out_file  = out_dir + "time_slice%s.te" % (str(i).zfill(3))
    with open(out_file, "wb") as f:
        for k in segs.keys():
            hdr = b"> -Z%f\n" % (segs[k].ID)
            f.write(hdr)
            arr = np.column_stack((
                time[:t+1]/3.15e10,
                z[segs[k].ID][:t+1,xs[k]] ))
            np.savetxt(f, arr)
    out_file  = out_dir + "time_slice_circles%s.te" % (str(i).zfill(3))
    with open(out_file, "wb") as f:
        for k in segs.keys():
            circs = lag[segs[k].ID]['obs_tps'][xs[k]][np.where(lag[segs[k].ID]['obs_tps'][xs[k]] <= t)]
            arr = np.column_stack(( time[circs]/3.15e10, z[segs[k].ID][circs,xs[k]], [segs[k].ID]*len(circs) ))
            np.savetxt(f, arr)
    filename = out_dir + "time_slice%s.de" % (str(i).zfill(3))
    with open(filename, "wb") as f:
        for seg in net.list_of_LongProfile_objects:
            hdr = b"> -Z%i\n" % seg.ID
            f.write(hdr)
            arr = np.column_stack(( seg.x/1000., z[seg.ID][t,:] ))
            np.savetxt(f, arr)
    out_file  = out_dir + "time_slice_circles%s.de" % (str(i).zfill(3))
    with open(out_file, "wb") as f:
        for k in segs.keys():
            arr = np.column_stack(( segs[k].x[xs[k]]/1000., z[segs[k].ID][t,xs[k]], segs[k].ID ))
            np.savetxt(f, arr)
    out_file  = out_dir + "scale%s.ts" % (str(i).zfill(3))
    with open(out_file, "wb") as f:
        arr = np.column_stack(( time[:t+1]/3.15e10, Qs0*scale[:t+1]*1000. ))
        # arr = np.column_stack(( time[:s+1]/3.15e10, Qw*scale[:s+1] ))
        np.savetxt(f, arr)
    out_file = out_dir + "scale_circles%s.ts" % (str(i).zfill(3))
    with open(out_file, "wb") as f:
        circs = lag[0]['scl_tps'][np.where(lag[0]['scl_tps'] <= t)]
        arr = np.column_stack(( time[circs]/3.15e10, Qs0*scale[circs]*1000. ))
        # arr = np.column_stack(( time[circs]/3.15e10, Qw*scale[circs] ))
        np.savetxt(f, arr)
    out_file  = out_dir + "Qs_out%s.ts" % (str(i).zfill(3))
    with open(out_file, "wb") as f:
        arr = np.column_stack(( time[:t+1]/3.15e10, Qs[0][:t+1,-1]*1000. ))
        np.savetxt(f, arr)
    out_file = out_dir + "Qs_out_circles%s.ts" % (str(i).zfill(3))
    with open(out_file, "wb") as f:
        circs = Qs_lag[0]['obs_tps'][-1][np.where(Qs_lag[0]['obs_tps'][-1] <= t)]
        arr = np.column_stack(( time[circs]/3.15e10, Qs[0][circs,-1]*1000. ))
        np.savetxt(f, arr)

with open(out_dir + "grid2.ts", "wb") as f:
    for tp in lag[0]['scl_tps']:
        hdr = b">\n"
        f.write(hdr)
        arr = np.column_stack(( [time[tp]/3.15e10]*2, [0,Qs0*scale[tp]*1000] ))
        np.savetxt(f, arr)
with open(out_dir + "grid2.te", "wb") as f:
    for tp in lag[0]['scl_tps']:
        hdr = b">\n"
        f.write(hdr)
        arr = np.column_stack(( [time[tp]/3.15e10]*2, [0,1000] ))
        np.savetxt(f, arr)

with open(out_dir + "grid.de", "wb") as f:
    for k in segs.keys():
        hdr = b"> -Z%f\n" % (segs[k].ID)
        f.write(hdr)
        arr = np.column_stack(( [segs[k].x[xs[k]]/1000., 110.], [z[segs[k].ID][0,xs[k]]]*2 ))
        np.savetxt(f, arr)
with open(out_dir + "grid.te", "wb") as f:
    for k in segs.keys():
        hdr = b"> -Z%f\n" % (segs[k].ID)
        f.write(hdr)
        arr = np.column_stack(( [-time[-1]/3.15e10, time[-1]/3.15e10], [z[segs[k].ID][0,xs[k]]]*2 ))
        np.savetxt(f, arr)

with open(out_dir + "steady_state.de", "wb") as f:
    arr = np.column_stack(( lp.x/1000., lp.z ))
    np.savetxt(f, arr)
    
with open(out_dir + "planform.d", "wb") as f:
    for k in planform.keys():
        hdr = b"> -Z%i\n" % k
        f.write(hdr)
        arr = np.column_stack(( planform[k]['x'], planform[k]['y'] ))
        np.savetxt(f, arr)



out_dir = "../periodic_output_networks/slow/"
with open(out_dir + "network.dg", "wb") as f:
    for seg in net.list_of_LongProfile_objects:
        hdr = b"> -Z%i\n" % seg.ID
        f.write(hdr)
        arr = np.column_stack(( seg.x/1000., gain[seg.ID] ))
        np.savetxt(f, arr)
        
with open(out_dir + "network.dl", "wb") as f:
    for seg in net.list_of_LongProfile_objects:
        hdr = b"> -Z%i\n" % seg.ID
        f.write(hdr)
        l = (lag[seg.ID]['plags']+lag[seg.ID]['tlags'])/(2.*period)
        arr = np.column_stack(( seg.x/1000., l ))
        np.savetxt(f, arr)

with open(out_dir + "linear.dg", "wb") as f:
    arr = np.column_stack(( lp.x/1000., lp.compute_z_gain(period) ))
    np.savetxt(f, arr)

with open(out_dir + "linear.dl", "wb") as f:
    arr = np.column_stack(( lp.x/1000., lp.compute_z_lag(period)/period ))
    np.savetxt(f, arr)

out_dir = "../periodic_output_networks/sweep/"
with open(out_dir + "single_network.pg", "ab") as f:
    arr = np.column_stack((
        period/3.15e12,
        gain[0][-1],
        mag,
        gain[0][-1] - np.array(gain).flatten().min(),
        np.array(gain).flatten().max() - gain[0][-1]
    ))
    np.savetxt(f, arr)
    
with open(out_dir + "single_network.pl", "ab") as f:
    arr = np.column_stack((
        period/3.15e12,
        lag_simple[0][-1],
        mag,
        lag_simple[0][-1] - np.array(lag_simple).flatten().min(),
        np.array(lag_simple).flatten().max() - lag_simple[0][-1]
    ))
    np.savetxt(f, arr)