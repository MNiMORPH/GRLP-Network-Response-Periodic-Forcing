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
    "m40": "./glic/output_081123/"
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
            net = generate_random_network(
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
    
# indir = "./glic/output_161223/"
# netdirs = next(os.walk(indirs[sweep]))[1]
# sweep_nets = []
# for netdir in netdirs:
#     with open(indirs[sweep] + netdir + "/props.obj", "rb") as f:
#         prop = pickle.load(f)
#         net = generate_random_network2(
#             magnitude=20, 
#             max_length=100.e3,
#             approx_dx=5.e2,
#             min_nxs=5,
#             mean_discharge=prop['Q_mean'],
#             sediment_discharge_ratio=1.e4,
#             width=98.1202038813591,
#             topology=prop['topology']
#             )
#         net.compute_network_properties()
#         sweep_nets.append(net)
# nets[sweep] = sweep_nets

net_is = {"m20": 0, "m40": 0}

fig, axs = plt.subplots(2,4,sharex=True)
i = 0

for sweep in net_is.keys():
    
    planform = plot_network(nets[sweep][net_is[sweep]], show=False)
    
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
                
        axs[i,3].plot(seg.x/1.e3, seg.z)

    hack = hacks[sweep][net_is[sweep]]
    d = np.linspace(0,100.e3, 100)
    Q = hack['k'] * (d**hack['p'])
    axs[i,2].plot(d/1.e3, Q, "--")
    axs[i,2].scatter(np.array(hack['d'])/1.e3, hack['Q'])

    i += 1
    
plt.show()
    
    


# net = generate_random_network2(
#     magnitude=20, 
#     max_length=False,
#     segment_length=sts.gamma(2., scale=260./2.),
#     segment_length_area_ratio=sts.norm(loc=300., scale=30.),
#     supply_area=sts.norm(loc=52000., scale=5200.),
#     approx_dx=1.e2,
#     min_nxs=5,
#     mean_discharge=False,
#     effective_rainfall=1.e3*0.4/3.154e10,
#     sediment_discharge_ratio=1.e4,
#     width=98.1202038813591,
#     topology=False,
#     evolve=True
#     )
# net.compute_network_properties()
# 
# __ = plot_network(net)
# for seg in net.list_of_LongProfile_objects:
#     plt.plot(seg.x, seg.Q)
#     plt.plot(seg.x, seg.Q_s*1.e4, ":")
# plt.show()