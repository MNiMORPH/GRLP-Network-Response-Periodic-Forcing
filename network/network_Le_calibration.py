from grlp import *
from grlp_extras import *
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
x = [np.arange(0., L, dx)]
S0 = [(mean_Qs/(lp.k_Qs*mean_Q))**(6./7.)]
upstream_segment_IDs = [[]]
downstream_segment_IDs = [[]]
z = [(x[0].max()-x[0])*S0]
Q = [np.full(len(x),mean_Q)]
B = [np.full(len(x),B)]
net = Network()
net.initialize(
    config_file = None,
    x_bl =L,
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

# indirs = {
#     "m40": "./glic/output_081123/",
#     "m2-100": "./glic/output_101123/",
#     "m40_w_int": "../output/network/m40_fix_seg_length_w_internal/",
#     "m2-100_w_int": "../output/network/m2-100_fix_seg_length_w_internal/",
#     "m40_var_no_int": "../output/network/m40_rnd_seg_length_no_internal/",
#     "m40_var": "../output/network/m40_rnd_seg_length/",
#     "m2-100_var": "../output/network/m2-100_rnd_seg_length/"
#     }
indirs = {"m40": "./glic/test/"}
nets = {}
hacks = {}
gains = {}
for sweep in indirs.keys():
    sweep_nets, sweep_hacks, sweep_gains, sweep_lags = read_sweep(indirs[sweep])
    nets[sweep] = sweep_nets
    hacks[sweep] = sweep_hacks
    gains[sweep] = sweep_gains

# ---- LINEAR GAIN
lin_periods = np.logspace(-2.5, 2.5, 81) * lp.equilibration_time
lin_gain_Qs = [lp.compute_Qs_gain(p, A_Qs=0.2)[-1] for p in lin_periods]
lin_gain_Qs_Qw = [lp.compute_Qs_gain(p, A_Q=0.2)[-1] for p in lin_periods]

# # ---- Continuous Gain
# continuous_gains = {}
# continuous_ps = [0.5, 1.]
# continuous_periods = np.logspace(-2.5, 2.5, 21) * lp.equilibration_time
# for i,p in enumerate(continuous_ps):
#     net = set_up_long_profile(L, mean_Q, mean_Qs, 1/p, B[0], dx=1.e3, evolve=True)
#     gs = []
#     for period in continuous_periods:
#         print(p,period)
#         z, Qs, time, scale = evolve_network_periodic(deepcopy(net), period, 0.2, 0.)
#         Qs_gain = compute_network_Qs_gain(net, Qs, 0.2, 0., [q[0,:] for q in Qs])
#         gs.append(Qs_gain[0][-1])
#     continuous_gains[p] = gs


# ---- Teq_max_L
Teq_max_Ls = {}
for i,sweep in enumerate(indirs.keys()):
    Teqs = []
    for j in range(len(gains[sweep])):
        L = nets[sweep][j].list_of_LongProfile_objects[0].x_ext[0][-1]
        Teqs.append((L**2.)/nets[sweep][j].mean_diffusivity)
    Teq_max_Ls[sweep] = Teqs

# ---- Stacks
stacks = {}
for i,sweep in enumerate(indirs.keys()):
    for j in range(len(gains[sweep])):
        periods1 = gains[sweep][j]['P']/Teq_max_Ls[sweep][j]
        periods2 = gains[sweep][j]['P']/gains[sweep][j]['Teq_Qs']
        if i>=0:
            gain = [gains[sweep][j]['G_Qs']['Qs'][k][0][-1] for k in range(len(gains[sweep][j]['P']))]
        else:
            gain = [gains[sweep][j]['G_Qs'][k][0][-1] for k in range(len(gains[sweep][j]['P']))]
        mag = np.full(len(periods1), len(nets[sweep][j].streams_by_order[1]))
        combine = np.column_stack(( periods1, periods2, gain, mag ))
        if j==0:
            arr = combine
        else:
            arr = np.vstack(( arr, combine ))
        stacks[sweep] = arr

fig, axs = plt.subplots(max(2,len(indirs.keys())),2,sharex=True,sharey=True)

for axs_i in axs:
    for ax_ij in axs_i:
        # ax_ij.fill(
        #     np.hstack(( continuous_periods, continuous_periods[::-1] ))/lp.equilibration_time,
        #     np.hstack(( continuous_gains[0.5], continuous_gains[1][::-1] )),
        #     c="lightgrey"
        #     )
        # ax_ij.plot(
        #     continuous_periods/lp.equilibration_time,
        #     continuous_gains[0.5], "--", c="grey")
        # ax_ij.plot(
        #     continuous_periods/lp.equilibration_time,
        #     continuous_gains[1], "--", c="grey")
        ax_ij.plot(lin_periods/lp.equilibration_time, lin_gain_Qs, c="black")        

for k,sweep in enumerate(indirs.keys()):

    for i in range(len(gains[sweep])):
    
        axs[k,0].scatter(
            stacks[sweep][:,0],
            stacks[sweep][:,2],
            c="red",
            # alpha=0.01
            )
        axs[k,1].scatter(
            stacks[sweep][:,1],
            stacks[sweep][:,2],
            c="red",
            # alpha=0.01
            )

axs[0,0].set_xscale("log")

plt.show()

import sys
sys.exit()

# ---- Save

basedir = "../output/network/calibration/"

with open(basedir + "linear_gain.pg", "wb") as f:
    arr = np.column_stack(( lin_periods/lp.equilibration_time, lin_gain_Qs ))
    np.savetxt(f, arr)
    
with open(basedir + "continuous_gain.pg", "wb") as f:
    arr = np.column_stack(( 
        np.hstack(( continuous_periods, continuous_periods[::-1] ))/lp.equilibration_time,
        np.hstack(( continuous_gains[0.5], continuous_gains[1][::-1] ))
        ))
    np.savetxt(f, arr)
    
outdirs = {
    "m20": "m20_fix_seg_length/",
    "m40": "m40_fix_seg_length/",
    "m2-100": "m2-100_fix_seg_length/",
    "m40_var": "m40_rnd_seg_length/"
    }

for i,sweep in enumerate(indirs.keys()):
    
    with open(basedir + outdirs[sweep] + "gain_L.pg", "wb") as f:
        arr = np.column_stack(( stacks[sweep][:,0], stacks[sweep][:,2], stacks[sweep][:,3] ))
        np.savetxt(f, arr)
        
    with open(basedir + outdirs[sweep] + "gain_Le.pg", "wb") as f:
        arr = np.column_stack(( stacks[sweep][:,1], stacks[sweep][:,2], stacks[sweep][:,3] ))
        np.savetxt(f, arr)