from grlp import *
from grlp_extras import *
import scipy
import os
import pickle
import scipy.stats as  sts
from copy import deepcopy

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
# B = [np.full(len(x),B)]
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
    B = [np.full(len(x),B)],
    overwrite = False
    )
net.set_niter(3)
net.get_z_lengths()
diff = (7./6.) * lp.k_Qs * mean_Q * (S0[0]**(1./6.)) / (B[0] * (1. - lp.lambda_p))
lp = net.list_of_LongProfile_objects[0]
lp.compute_equilibration_time()

indirs = {
    "m20": "./glic/output_071123/",
    "m40": "./glic/output_081123/",
    "m40_var": "../output/network/m40_rnd_seg_length/"
    }
nets = {}
hacks = {}
gains = {}
lags = {}
for sweep in indirs.keys():
    sweep_nets, sweep_hacks, sweep_gains, sweep_lags = read_sweep(indirs[sweep])
    nets[sweep] = sweep_nets
    hacks[sweep] = sweep_hacks
    gains[sweep] = sweep_gains
    lags[sweep] = sweep_lags

# ---- Effective length
eff_lengths = {}
for i,sweep in enumerate(indirs.keys()):
    ls = []
    for j in range(len(gains[sweep])):
        diffs = []
        for seg in nets[sweep][j].list_of_LongProfile_objects:
            seg.compute_diffusivity()
            diffs.append(seg.diffusivity)
        ls.append( np.sqrt(gains[sweep][j]['Teq_Qs']*np.mean(np.hstack(diffs))) )
    eff_lengths[sweep] = ls

# ---- Plot

net_is = {"m20": 0, "m40": 0, "m40_var": 443}

new_gains = {}
new_lags = {}
linear_lps = {}
cont_lps = {}
cont_gains = {}
cont_lags = {}

for i,sweep in enumerate(net_is.keys()):
    
    print(sweep)
    
    net = nets[sweep][net_is[sweep]]
    
    # # Do evolutions
    # net.evolve_threshold_width_river_network(nt=1000, dt=3.15e10)
    # net.compute_network_properties()
    Teq = gains[sweep][net_is[sweep]]['Teq_Qs']
    # net_gains = []
    # net_lags = []
    # 
    # neti = deepcopy(net)
    # z, Qs, time, scale = evolve_network_periodic(neti, Teq, 0.2, 0.)
    # z_gain = compute_network_z_gain(neti, z, 0.2, 0., [seg.S for seg in net.list_of_LongProfile_objects])
    # z_lag = find_network_lag(neti, z, time, scale, Teq)
    # net_gains.append(z_gain)
    # net_lags.append(z_lag)
    # 
    # new_gains[sweep] = net_gains
    # new_lags[sweep] = net_lags

    # diffusivity, mean Q, mean Qs
    Q = []
    Qs = []
    diffs = []
    for seg in net.list_of_LongProfile_objects:
        Q.append(seg.Q)
        Qs.append(seg.Q_s)
        seg.compute_diffusivity()
        diffs.append(seg.diffusivity)
    diff = np.mean(np.hstack(diffs))
    mean_Q = np.mean(np.hstack(Q))
    mean_Qs = np.mean(np.hstack(Qs))
    
    # effective length
    Le = np.sqrt(Teq * diff)
    
    # linear equivalent
    x, dx = np.linspace(0., Le, 100, retstep=True)
    x = [x[:-1]]
    S0 = [(mean_Qs/(lp.k_Qs*mean_Q))**(6./7.)]
    upstream_segment_IDs = [[]]
    downstream_segment_IDs = [[]]
    z = [(x[0].max()-x[0])*S0]
    Q = [np.full(len(x),mean_Q)]
    # B = [np.full(len(x),B)]
    lin_net = Network()
    lin_net.initialize(
        config_file = None,
        x_bl =Le,
        z_bl = 0.,
        S0 = S0,
        upstream_segment_IDs = upstream_segment_IDs,
        downstream_segment_IDs = downstream_segment_IDs,
        x = x,
        z = z,
        Q = Q,
        B = [np.full(len(x),B)],
        overwrite = False
        )
    lin_net.set_niter(3)
    lin_net.get_z_lengths()
    lp = lin_net.list_of_LongProfile_objects[0]
    lp.compute_equilibration_time()
    
    # save
    linear_lps[sweep] = lp
    
    # continuous
    p = hacks[sweep][net_is[sweep]]['p']
    L = net.list_of_LongProfile_objects[0].x[-1]
    cont_lp = set_up_long_profile(L, mean_Q, mean_Qs, p, B, dx=1.e3, evolve=True)
    z, Qs, time, scale = evolve_network_periodic(deepcopy(cont_lp), Teq, 0.2, 0.)
    z_gain = compute_network_z_gain(deepcopy(cont_lp), z, 0.2, 0., [S0[0]])
    z_lag = find_network_lag(deepcopy(cont_lp), z, time, scale, Teq)
    
    # save
    cont_lps[sweep] = cont_lp
    cont_gains[sweep] = z_gain[0]
    cont_lags[sweep] = z_lag[0]


fig, axs = plt.subplots(2,3,sharex=True,sharey="row")

for i,sweep in enumerate(net_is.keys()):
    
    net = nets[sweep][net_is[sweep]]
    lp = linear_lps[sweep]
    Teq = gains[sweep][net_is[sweep]]['Teq_Qs']
    L = net.list_of_LongProfile_objects[0].x[-1]
    cont_lp = cont_lps[sweep]
    
    axs[0,i].plot(
        # (L - lp.x.mean() + lp.x)/1.e3,
        (L - lp.x.max() + lp.x)/1.e3,
        lp.compute_z_gain(Teq),
        "--",
        c="dimgrey"
        )
    axs[1,i].plot(
        # (L/2 - lp.x.mean() + lp.x)/1.e3,
        (L - lp.x.max() + lp.x)/1.e3,
        lp.compute_z_lag(Teq)/Teq,
        "--",
        c="dimgrey"
        )
        
    axs[0,i].plot(
        cont_lp.list_of_LongProfile_objects[0].x/1.e3,
        cont_gains[sweep],
        ":",
        c="dimgrey"
        )
    axs[1,i].plot(
        cont_lp.list_of_LongProfile_objects[0].x/1.e3,
        cont_lags[sweep],
        ":",
        c="dimgrey"
        )

    for j,seg in enumerate(net.list_of_LongProfile_objects):
    
        axs[0,i].plot(
            seg.x/1.e3,
            new_gains[sweep][0][j]
            )

        axs[1,i].plot(
            seg.x/1.e3,
            new_lags[sweep][0][j]
            )

plt.show()

# ---- Write output

basedir = "../output/network/spatial/"

outdirs = {
    "m20": "m20_fix_seg_length/",
    "m40": "m40_fix_seg_length/",
    "m40_var": "m40_rnd_seg_length/"
    }

for i,sweep in enumerate(indirs.keys()):
    
    net = nets[sweep][net_is[sweep]]
    lp = linear_lps[sweep]
    Teq = gains[sweep][net_is[sweep]]['Teq_Qs']
    L = net.list_of_LongProfile_objects[0].x[-1]

    with open(basedir + outdirs[sweep] + "gain.dg", "wb") as f:
        for j,seg in enumerate(net.list_of_LongProfile_objects):
            hdr = b"> -Z%i\n" % (net.segment_orders[j]+1)
            f.write(hdr)
            arr = np.column_stack(( seg.x/1.e3, new_gains[sweep][0][j] ))
            np.savetxt(f, arr)
            
    with open(basedir + outdirs[sweep] + "lag.dl", "wb") as f:
        for j,seg in enumerate(net.list_of_LongProfile_objects):
            hdr = b"> -Z%i\n" % (net.segment_orders[j]+1)
            f.write(hdr)
            arr = np.column_stack(( seg.x/1.e3, new_lags[sweep][0][j] ))
            np.savetxt(f, arr)
            
    with open(basedir + outdirs[sweep] + "lin_gain.dg", "wb") as f:
        arr = np.column_stack((
            (L - lp.x.max() + lp.x)/1.e3,
            lp.compute_z_gain(Teq)
            ))
        np.savetxt(f, arr)
        
    with open(basedir + outdirs[sweep] + "lin_lag.dl", "wb") as f:
        arr = np.column_stack((
            (L - lp.x.max() + lp.x)/1.e3,
            lp.compute_z_lag(Teq)/Teq
            ))
        np.savetxt(f, arr)