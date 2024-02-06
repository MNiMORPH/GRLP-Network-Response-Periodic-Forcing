from grlp import *
from grlp_extras import *
import scipy
import os
import pickle
import scipy.stats as  sts

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

indirs = {
    "m20": "./glic/output_071123/",
    "m40": "./glic/output_081123/",
    "m2-100": "./glic/output_101123/"
    }
nets = {}
hacks = {}
for sweep in indirs.keys():
    netdirs = next(os.walk(indirs[sweep]))[1]
    sweep_nets = []
    sweep_hacks = []
    for netdir in netdirs:
        with open(indirs[sweep] + netdir + "/hack.obj", "rb") as f:
            hack = pickle.load(f)
            sweep_hacks.append(hack)
        with open(indirs[sweep] + netdir + "/props.obj", "rb") as f:
            prop = pickle.load(f)
            net, net_topo = generate_random_network(
                magnitude=20, 
                max_length=100.e3,
                approx_dx=5.e2,
                min_nxs=5,
                mean_discharge=prop['Q_mean'],
                sediment_discharge_ratio=1.e4,
                width=98.1202038813591,
                topology=prop['topology']
                )
            net.compute_network_properties()
            sweep_nets.append(net)

    nets[sweep] = sweep_nets
    hacks[sweep] = sweep_hacks
    
indir = "./glic/test/"
netdirs = next(os.walk(indir))[1]
sweep_nets = []
sweep_hacks = []
for netdir in netdirs:
    with open(indir + netdir + "/hack.obj", "rb") as f:
        hack = pickle.load(f)
        sweep_hacks.append(hack)
    with open(indir + netdir + "/props.obj", "rb") as f:
        prop = pickle.load(f)
        net, net_topo = generate_random_network(
            magnitude=None, 
            segment_lengths=prop['lengths'],
            supply_discharges=prop['supply_discharges'],
            internal_discharges=prop['internal_discharges'],
            approx_dx=5.e2,
            min_nxs=5,
            sediment_discharge_ratio=prop['sediment_discharge_ratio'],
            width=98.1202038813591,
            topology=prop['topology']
            )
        net.compute_network_properties()
        sweep_nets.append(net)
nets['m40_var'] = sweep_nets
hacks['m40_var'] = sweep_hacks

# ------------------------- EXAMPLE ------------------------------------------ #

net_is = {"m20": 0, "m40": 0, "m40_var": 0}

fig, axs = plt.subplots(3,5)
i = 0

for sweep in net_is.keys():
    
    planform = plot_network(nets[sweep][net_is[sweep]], show=False)
    net = nets[sweep][net_is[sweep]]
    
    for seg in planform:
        axs[i,0].plot(planform[seg]['x'], planform[seg]['y'])
    
    for seg in nets[sweep][net_is[sweep]].list_of_LongProfile_objects:
        if seg.downstream_segment_IDs:
            downID = seg.downstream_segment_IDs[0]
            x = np.hstack(( seg.x_ext[0][1:]/1.e3, seg.x_ext[0][-1]/1.e3 ))
            Q = np.hstack(( seg.Q, seg.Q[-1], nets[sweep][net_is[sweep]].list_of_LongProfile_objects[downID].Q[0] ))
        else:
            x = seg.x/1.e3
            Q = seg.Q
        axs[i,1].plot(x, Q)
                
        axs[i,4].plot(seg.x/1.e3, seg.z)

    hack = hacks[sweep][net_is[sweep]]
    d = np.linspace(0,max(hack['d']), 100)
    Q = hack['k'] * (d**hack['p'])
    axs[i,2].plot(d/1.e3, Q, "--")
    axs[i,2].scatter(np.array(hack['d'])/1.e3, hack['Q'])

    orders = np.linspace(1, max(net.orders), 10)
    axs[i,3].plot(orders, net.bifurcation_ratio**(orders.max()-orders), "--")
    axs[i,3].scatter(
        nets[sweep][net_is[sweep]].orders,
        [nets[sweep][net_is[sweep]].order_counts[i] for i in nets[sweep][net_is[sweep]].orders])
    axs[i,3].plot(orders, net.length_scale*net.length_ratio**(orders-1), "--")
    axs[i,3].scatter(
        nets[sweep][net_is[sweep]].orders,
        [nets[sweep][net_is[sweep]].order_lengths[i] for i in nets[sweep][net_is[sweep]].orders])
    axs[i,3].plot(orders, net.discharge_scale*net.discharge_ratio**(orders-1), "--")
    axs[i,3].scatter(
        nets[sweep][net_is[sweep]].orders,
        [nets[sweep][net_is[sweep]].order_discharges[i] for i in nets[sweep][net_is[sweep]].orders])
    axs[i,3].set_yscale("log")
     
    i += 1
    
plt.show()
    
# ------------------------------- PROP DISTRIBUTIONS ------------------------- #

fig, axs = plt.subplots(4,3,sharex='col')

for i,sweep in enumerate(nets.keys()):

    axs[i,0].hist(
        [n.bifurcation_ratio for n in nets[sweep]]
        )
    axs[i,0].hist(
        [n.length_ratio for n in nets[sweep]]
        )
    axs[i,0].hist(
        [n.discharge_ratio for n in nets[sweep]]
        )
        
    axs[i,1].hist(
        [1./h['p'] for h in hacks[sweep]]
        )
        
    axs[i,2].hist(
        [n.mean_downstream_distance/1.e3 for n in nets[sweep]]
        )

plt.show()



