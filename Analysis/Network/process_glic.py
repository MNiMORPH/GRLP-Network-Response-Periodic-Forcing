from grlp import *
from grlp_extras import *
import scipy
import os
import pickle

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
# indir = "./glic/output_170523/"
# indir = "./glic/output_061123/"
# indir = "./glic/output_071123/"
indir = "./glic/output_081123/"
# indir = "./glic/output_101123/"
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
        net.compute_network_properties()
        nets.append(net)
    with open(indir + netdir + "/gain.obj", "rb") as f:
        gain = pickle.load(f)
        gains.append(gain)
    with open(indir + netdir + "/lag.obj", "rb") as f:
        lag = pickle.load(f)
        lags.append(lag)
            
# import sys
# sys.exit()

# # ---- Example

# period = 0
# for i,net in enumerate(nets):
#     print(i)
#     for seg in net.list_of_LongProfile_objects:
#         plt.plot(
#             seg.x/1.e3, lags[i]['lag_Qs'][period][seg.ID]
#         )
#     plt.show()

# netID = 0
# period = 0
# for seg in nets[netID].list_of_LongProfile_objects:
#     plt.plot(
#         seg.x/1.e3, lags[netID]['lag_Qs'][period][seg.ID]
#     )
# plt.show()

# # rerun for debugging
# periods = np.logspace(-2.,2.,7) * lp.equilibration_time
# period = periods[0]
# neti = copy.deepcopy(nets[netID])
# # neti.evolve_threshold_width_river_network(nt=1000, dt=3.15e11)
# print("starting")
# z, Qs, time, scale = evolve_network_periodic2(neti, period, 0.2, 0.)
# z_gain = compute_network_z_gain(neti, z, 0.2, 0., S0)
# Qs_gain = compute_network_Qs_gain(neti, Qs, 0.2, 0., [q[0,:] for q in Qs])
# z_lag = find_network_lag2(neti, z, time, scale, period)
# Qs_lag = find_network_lag2(neti, Qs, time, scale, period)

# fig, axs = plt.subplots(1,2)
# for seg in neti.list_of_LongProfile_objects:
#     # fig, axs = plt.subplots(1,2)
#     axs[0].plot(
#         seg.x/1.e3, z_lag[seg.ID]
#     )
#     axs[1].plot(
#         seg.x/1.e3, Qs_lag[seg.ID]
#     )
# # plt.show()
# 
# import sys
# sys.exit()

# orders = np.arange(1,len(nets[netID].order_counts)+1,1)
# 
# # Rb
# plt.plot(orders, nets[netID].bifurcation_ratio**(max(orders)-orders), "--")
# plt.scatter(
#     orders, 
#     [nets[netID].order_counts[o] for o in nets[netID].orders])
# 
# # Rl
# plt.plot(orders,
#     nets[netID].order_lengths[1]/1.e3*(nets[netID].length_ratio**(orders-1)), "--")
# plt.scatter(
#     orders, 
#     np.array([nets[netID].order_lengths[o] for o in nets[netID].orders])/1.e3)
# 
# # Ra
# plt.plot(orders, nets[netID].order_discharges[1]*(nets[netID].discharge_ratio**(orders-1)), "--")
# plt.scatter(
#     orders, 
#     [nets[netID].order_discharges[o] for o in nets[netID].orders])
# 
# plt.yscale("log")
# plt.show()

# ---- Network props

fig, axs = plt.subplots(2,3,sharey=True)

axs[0,0].hist([n.bifurcation_ratio for n in nets])
axs[0,0].set_xlabel("Bifurcation ratio")
axs[0,0].set_ylabel("Count")

axs[0,1].hist([n.length_ratio for n in nets])
axs[0,1].set_xlabel("Length ratio")

axs[0,2].hist([n.discharge_ratio for n in nets])
axs[0,2].set_xlabel("Discharge ratio")

h = axs[1,0].hist([n.max_topological_length for n in nets])
axs[1,0].plot([2+int(np.log(20))]*2, [0, h[0].max()], ":")
axs[1,0].plot([20]*2, [0, h[0].max()], ":")
axs[1,0].plot([expected_lengths[19]]*2, [0, h[0].max()], ":")
axs[1,0].set_xlabel("Maximum topological length")
axs[1,0].set_ylabel("Count")

axs[1,1].hist([n.mean_downstream_distance/100.e3 for n in nets])
axs[1,1].set_xlabel("Mean length")

axs[1,2].hist([1./h['p'] for h in hacks])
axs[1,2].set_xlabel("Hack exponent")

# axs[1,2].hist([g['Teq_z'][0]/3.15e12 for g in gains])
# axs[1,2].hist([g['Teq_Qs']/3.15e12 for g in gains])
# axs[1,2].set_xlabel(r"Effective $T_{eq}$")

plt.show()


# ---- Teq Qs vs Teq z
plt.plot([0.5,1.5],[0.5,1.5],":")
plt.scatter(
    [g['Teq_z'][0]/3.15e12 for g in gains],
    [g['Teq_Qs']/3.15e12 for g in gains]
)
plt.xlabel(r"Effective $T_{eq}$ ($G_z$)")
plt.ylabel(r"Effective $T_{eq}$ ($G_{Q_s}$)")
plt.show()


# ---- Effective length vs Mean length

fig, axs = plt.subplots(2,3,sharey=True)
# eff_length = [ np.sqrt(g['Teq_z'][0]*lp.diffusivity.mean())/100.e3 for g in gains]
eff_length = [ np.sqrt(g['Teq_z'][0]*diff)/100.e3 for g in gains]

axs[0,0].scatter([n.bifurcation_ratio for n in nets], eff_length, c=[max(n.segment_orders) for n in nets])
axs[0,0].set_xlabel("Bifurcation ratio")
axs[0,0].set_ylabel("Effective length / Maximum length")

axs[0,1].scatter([n.length_ratio for n in nets], eff_length, c=[max(n.segment_orders) for n in nets])
axs[0,1].set_xlabel("Length ratio")

axs[0,2].scatter([n.discharge_ratio for n in nets], eff_length, c=[max(n.segment_orders) for n in nets])
axs[0,2].set_xlabel("Discharge ratio")

axs[1,0].scatter([n.max_topological_length for n in nets], eff_length, c=[max(n.segment_orders) for n in nets])
axs[1,0].set_xlabel("Maximum topological length")
axs[0,0].set_ylabel("Effective length / Maximum length")

axs[1,1].scatter([1/h['p'] for h in hacks], eff_length, c=[max(n.segment_orders) for n in nets])
axs[1,1].set_xlabel("Hack exponent")

reg = np.polyfit(
    np.array([n.mean_downstream_distance for n in nets if len(n.list_of_channel_head_segment_IDs)])/100.e3,
    [l for i,l in enumerate(eff_length) if len(nets[i].list_of_channel_head_segment_IDs)],
    1)
Ls = np.linspace(0.4,1.,10)
axs[1,2].plot(Ls, reg[0]*Ls + reg[1], "--")
axs[1,2].scatter(
    np.array([n.mean_downstream_distance for n in nets])/100.e3,
    eff_length, c=[max(n.segment_orders) for n in nets])
axs[1,2].set_xlabel("Mean length / Maximum length")

plt.show()


# ---- Effective length / Mean length

fig, axs = plt.subplots(1,2)
axs[0].hist(
    np.array(eff_length)[:,0] /
    np.array([n.mean_downstream_distance/100.e3 for n in nets])
    )
axs[0].set_xlabel("Effective length / Mean length")
axs[0].set_ylabel("Count")
axs[1].scatter(
    [len(n.list_of_channel_head_segment_IDs) for n in nets],
    np.array(eff_length)[:,0] / np.array([n.mean_downstream_distance/100.e3 for n in nets])
    )
plt.show()


# # ---- Hack vs other stuff
# plt.scatter(eff_length, [1./h['p'] for h in hacks])
# plt.show()



# ---- Gain
periods = np.logspace(-2.,2.,7) * lp.equilibration_time
lin_periods = np.logspace(-2.5,2.5,81) * lp.equilibration_time
fig, axs = plt.subplots(2,2,sharex=True,sharey="row")
axs[0,0].plot(
    lin_periods/lp.equilibration_time, 
    [lp.compute_z_gain(p)[-1] for p in lin_periods])
axs[0,1].plot(
    lin_periods/lp.equilibration_time, 
    [lp.compute_z_gain(p)[-1] for p in lin_periods])
axs[1,0].plot(
    lin_periods/lp.equilibration_time, 
    [lp.compute_Qs_gain(p, A_Qs=0.2)[-1] for p in lin_periods])
axs[1,1].plot(
    lin_periods/lp.equilibration_time, 
    [lp.compute_Qs_gain(p, A_Qs=0.2)[-1] for p in lin_periods])
for g in gains:
    G_z_out = [p[0][-1] for p in g['G_z']]
    G_Qs_out = [p[0][-1] for p in g['G_Qs']]
    axs[0,0].scatter(periods/lp.equilibration_time, G_z_out)
    axs[0,1].scatter(periods/g['Teq_z'], G_z_out)
    axs[1,0].scatter(periods/lp.equilibration_time, G_Qs_out)
    axs[1,1].scatter(periods/g['Teq_Qs'], G_Qs_out)
axs[0,0].set_ylabel(r"$G_z$")
axs[1,0].set_ylabel(r"$G_{Q_s}$")
axs[1,0].set_xlabel(r"$P$ / $T_{eq}$")
axs[1,1].set_xlabel(r"$P$ / $T_{eq}$")
axs[1,0].set_xscale("log")
plt.show()


# ---- Lag
fig, axs = plt.subplots(2,2,sharex=True,sharey=True)
axs[0,0].plot(
    lin_periods/lp.equilibration_time, 
    [lp.compute_z_lag(p,nsum=1000)[-1]/p for p in lin_periods])
axs[0,1].plot(
    lin_periods/lp.equilibration_time, 
    [lp.compute_z_lag(p,nsum=1000)[-1]/p for p in lin_periods])
axs[1,0].plot(
    lin_periods/lp.equilibration_time, 
    [lp.compute_Qs_lag(p,nsum=1000, A_Qs=0.2)[-1]/p for p in lin_periods])
axs[1,1].plot(
    lin_periods/lp.equilibration_time, 
    [lp.compute_Qs_lag(p,nsum=1000, A_Qs=0.2)[-1]/p for p in lin_periods])
for l,g in zip(lags,gains):
    lag_z_out = [p[0][-1] for p in l['lag_z']]
    lag_Qs_out = [p[0][-1] for p in l['lag_Qs']]
    axs[0,0].scatter(periods/lp.equilibration_time, lag_z_out)
    axs[0,1].scatter(periods/g['Teq_z'], lag_z_out)
    axs[1,0].scatter(periods/lp.equilibration_time, lag_Qs_out)
    axs[1,1].scatter(periods/g['Teq_Qs'], lag_Qs_out)
axs[0,0].set_ylabel(r"${\varphi}_z$")
axs[1,0].set_ylabel(r"${\varphi}_{Q_s}$")
axs[1,0].set_xlabel(r"$P$ / $T_{eq}$")
axs[1,1].set_xlabel(r"$P$ / $T_{eq}$")
axs[1,0].set_xscale("log")
plt.show()


import sys
sys.exit()

# ---- Export: network examples
outdir = "../output/network_example/"
netID = 11
planform = plot_network(nets[netID], show=False)
orders = np.arange(1,len(nets[netID].order_counts)+1,1)

with open(outdir + "info.txt", "wb") as f:
    arr = np.column_stack(( 
        max([planform[i]['y'].max() for i in planform.keys()])+1,
        5*round(max(hacks[netID]['Q'])/5) + 5,
        len(nets[netID].sources),
        nets[netID].max_topological_length ))
    np.savetxt(f, arr, fmt="%d")
    
with open(outdir + "flt_info.txt", "wb") as f:
    arr = np.column_stack(( 
        (1./hacks[netID]['k'])**(1./hacks[netID]['p']),
        1./hacks[netID]['p'],
        nets[netID].bifurcation_ratio,
        nets[netID].length_ratio,
        nets[netID].discharge_ratio ))
    np.savetxt(f, arr, fmt="%.2f")

with open(outdir + "planform.d", "wb") as f:
    for seg in nets[netID].list_of_LongProfile_objects:
        hdr = b"> -Z%f\n" % (nets[netID].segment_orders[seg.ID]+1)
        f.write(hdr)
        arr = np.column_stack(( planform[seg.ID]['x'], planform[seg.ID]['y'] ))
        np.savetxt(f, arr)
        
with open(outdir + "discharge.dq", "wb") as f:
    arr = np.column_stack((
        np.array(hacks[netID]['d'])/1000.,
        hacks[netID]['Q'],
        nets[netID].segment_orders+1
        ))
    np.savetxt(f, arr)
    
with open(outdir + "discharge_fit.dq", "wb") as f:
    d = np.linspace(0., L+10.e3, 100)
    Q = hacks[netID]['k'] * (d**hacks[netID]['p'])
    arr = np.column_stack(( d/1000., Q ))
    np.savetxt(f, arr)

with open(outdir + "bifurcation.on", "wb") as f:
    arr = np.column_stack((
        nets[netID].orders,
        [nets[netID].order_counts[o] for o in nets[netID].orders],
        nets[netID].bifurcation_ratio**(max(nets[netID].orders)-nets[netID].orders)
        ))
    np.savetxt(f, arr)
    
with open(outdir + "length.ol", "wb") as f:
    arr = np.column_stack((
        nets[netID].orders,
        [nets[netID].order_lengths[o]/1.e3 for o in nets[netID].orders],
        # nets[netID].order_lengths[1]/1.e3*(nets[netID].length_ratio**(np.array(nets[netID].orders)-1))
        nets[netID].length_scale/1.e3*(nets[netID].length_ratio**(np.array(nets[netID].orders)-1))
        ))
    np.savetxt(f, arr)
    
with open(outdir + "discharge.oq", "wb") as f:
    arr = np.column_stack((
        nets[netID].orders,
        [nets[netID].order_discharges[o] for o in nets[netID].orders],
        # nets[netID].order_discharges[1]*(nets[netID].discharge_ratio**(np.array(nets[netID].orders)-1))
        nets[netID].discharge_scale*(nets[netID].discharge_ratio**(np.array(nets[netID].orders)-1))
        ))
    np.savetxt(f, arr)
    
with open(outdir + "gain.dg", "wb") as f:
    for seg in nets[netID].list_of_LongProfile_objects:
        hdr = b"> -Z%d\n" % (nets[netID].segment_orders[seg.ID]+1)
        f.write(hdr)
        arr = np.column_stack((
            seg.x/1.e3, gains[netID]['G_z'][3][seg.ID]
            ))
        np.savetxt(f, arr)
        
with open(outdir + "lin_gain.dg", "wb") as f:
    arr = np.column_stack((
        lp.x/1.e3, lp.compute_z_gain(periods[3])
        ))
    np.savetxt(f, arr)
    
# ---- Export: network sweep
outdir = "../output/network_sweep_m20_v2/"
# outdir = "../output/network_sweep_m40/"
# outdir = "../output/network_sweep_m2-m60/"
eff_length = [ np.sqrt(g['Teq_z'][0]*lp.diffusivity.mean())/100.e3 for g in gains]
lin_periods = np.logspace(-2.5,2.5,81) * lp.equilibration_time
periods = np.logspace(-2.,2.,7) * lp.equilibration_time

# with open(outdir + "props.dat", "wb") as f:
#     arr = np.column_stack((
#         [n.bifurcation_ratio for n in nets],
#         [n.length_ratio for n in nets],
#         [n.discharge_ratio for n in nets],
#         [n.max_topological_length for n in nets],
#         [1./h['p'] for h in hacks],
#         [n.mean_downstream_distance/L for n in nets],
#         eff_length,
#         [len(n.sources) for n in nets]
#         ))
#     np.savetxt(f, arr)
    
with open(outdir + "Le_fit.dat", "wb") as f:
    reg = np.polyfit(
        np.array([n.mean_downstream_distance for n in nets])/100.e3,
        eff_length,
        1)
    Ls = np.linspace(0.,1.,10)
    arr = np.column_stack(( Ls, reg[0]*Ls + reg[1] ))
    np.savetxt(f, arr)

with open(outdir + "z_gain_poly.pg", "wb") as f:
    ps = np.hstack(( lin_periods, lin_periods[::-1] )) / lp.equilibration_time
    gs = np.hstack((
        [lp.compute_z_gain(p)[-1] for p in lin_periods],
        [lp.compute_z_gain(p)[0] for p in lin_periods][::-1]
    ))
    arr = np.column_stack(( ps, gs ))
    np.savetxt(f, arr)

with open(outdir + "z_gain_out.pg", "wb") as f:
    arr = np.column_stack(( 
        lin_periods/lp.equilibration_time, 
        [lp.compute_z_gain(p)[-1] for p in lin_periods] ))
    np.savetxt(f, arr)

with open(outdir + "z_lag_poly.pl", "wb") as f:
    ps = np.hstack(( lin_periods, lin_periods[::-1] )) / lp.equilibration_time
    gs = np.hstack((
        [lp.compute_z_lag(p, nsum=1000)[-1]/p for p in lin_periods],
        [lp.compute_z_lag(p, nsum=1000)[0]/p for p in lin_periods][::-1]
    ))
    arr = np.column_stack(( ps, gs ))
    np.savetxt(f, arr)

with open(outdir + "z_lag_out.pl", "wb") as f:
    arr = np.column_stack(( 
        lin_periods/lp.equilibration_time, 
        [lp.compute_z_lag(p, nsum=1000)[-1]/p for p in lin_periods] ))
    np.savetxt(f, arr)

with open(outdir + "Qs_gain_poly.pg", "wb") as f:
    ps = np.hstack(( lin_periods, lin_periods[::-1] )) / lp.equilibration_time
    gs = np.hstack((
        [lp.compute_Qs_gain(p, A_Qs=0.2)[-1] for p in lin_periods],
        [lp.compute_Qs_gain(p, A_Qs=0.2)[0] for p in lin_periods][::-1]
    ))
    arr = np.column_stack(( ps, gs ))
    np.savetxt(f, arr)

with open(outdir + "Qs_gain_out.pg", "wb") as f:
    arr = np.column_stack(( 
        lin_periods/lp.equilibration_time, 
        [lp.compute_Qs_gain(p, A_Qs=0.2)[-1] for p in lin_periods] ))
    np.savetxt(f, arr)

with open(outdir + "Qs_lag_poly.pl", "wb") as f:
    ps = np.hstack(( lin_periods, lin_periods[::-1] )) / lp.equilibration_time
    ls = []
    for p in lin_periods:
        l = lp.compute_Qs_lag(p, A_Qs=0.2, nsum=10000)/p
        if l[0] > 0.5:
            l -= 0.5
        ls.append(l[-1])
    for p in lin_periods[::-1]:
        l = lp.compute_Qs_lag(p, A_Qs=0.2, nsum=10000)/p
        if l[0] > 0.5:
            l -= 0.5
        ls.append(l[0])
    arr = np.column_stack(( ps, ls ))
    np.savetxt(f, arr)

with open(outdir + "Qs_lag_out.pl", "wb") as f:
    arr = np.column_stack(( 
        lin_periods/lp.equilibration_time, 
        [lp.compute_Qs_lag(p, A_Qs=0.2, nsum=10000)[-1]/p for p in lin_periods] ))
    np.savetxt(f, arr)

with open(outdir + "net_z_gain_out.pg", "wb") as f:
    for i,g in enumerate(gains):
        arr = np.column_stack(( 
            periods/lp.equilibration_time,
            periods/g['Teq_z'],
            [p[0][-1] for p in g['G_z']],
            [p[0][-1] - min(np.array(p).flatten()) for p in g['G_z']],
            [max(np.array(p).flatten()) - p[0][-1] for p in g['G_z']],
            np.full(len(periods), i)
            ))
        np.savetxt(f, arr)
        
with open(outdir + "net_z_lag_out.pg", "wb") as f:
    for l,g in zip(lags,gains):
        arr = np.column_stack(( 
            periods/lp.equilibration_time,
            periods/g['Teq_z'],
            [p[0][-1] for p in l['lag_z']],
            [p[0][-1] - min(np.array(p).flatten()) for p in l['lag_z']],
            [max(np.array(p).flatten()) - p[0][-1] for p in l['lag_z']],
            ))
        np.savetxt(f, arr)
        
with open(outdir + "net_Qs_gain_out.pg", "wb") as f:
    for i,g in enumerate(gains):
        arr = np.column_stack(( 
            periods/lp.equilibration_time,
            periods/g['Teq_z'],
            [p[0][-1] for p in g['G_Qs']],
            [p[0][-1] - min(np.array(p).flatten()) for p in g['G_Qs']],
            [max(np.array(p).flatten()) - p[0][-1] for p in g['G_Qs']],
            np.full(len(periods), i)
            ))
        np.savetxt(f, arr)
        
with open(outdir + "net_Qs_lag_out.pg", "wb") as f:
    for l,g in zip(lags,gains):
        arr = np.column_stack(( 
            periods/lp.equilibration_time,
            periods/g['Teq_z'],
            [p[0][-1] for p in l['lag_Qs']],
            [p[0][-1] - min(np.array(p).flatten()) for p in l['lag_Qs']],
            [max(np.array(p).flatten()) - p[0][-1] for p in l['lag_Qs']],
            ))
        np.savetxt(f, arr)