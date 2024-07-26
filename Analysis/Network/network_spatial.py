import numpy as np
import scipy.signal as sig
import matplotlib.pyplot as plt
import copy as cp

import grlp
import grlp_extras as grlpx

output_gmt = False

indirs = {
    "m40_no_int": "../output/network/m40_fix_seg_length_no_internal/",
    "m40_w_int": "../output/network/m40_fix_seg_length_w_internal/",
    "m40_rnd_no_int": "../output/network/m40_rnd_seg_length_no_internal/",
    "m40_rnd_w_int": "../output/network/m40_rnd_seg_length_w_internal/",
    "m40_no_int_var_width": "../output/network/m40_fix_seg_length_no_internal_var_width/",
    "m40_w_int_var_width": "../output/network/m40_fix_seg_length_w_internal_var_width/",
    "m40_rnd_no_int_var_width": "../output/network/m40_rnd_seg_length_no_internal_var_width/",
    "m40_rnd_w_int_var_width": "../output/network/m40_rnd_seg_length_w_internal_var_width/"
    }
    
nets = {}
hacks = {}
gains = {}
for sweep in indirs.keys():
    sweep_nets, sweep_hacks, sweep_gains, sweep_lags = grlpx.read_sweep(indirs[sweep])
    nets[sweep] = sweep_nets
    hacks[sweep] = sweep_hacks
    gains[sweep] = sweep_gains


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

# ---- Run

net_is = {
    "m40_no_int": 0, "m40_w_int": 0, "m40_rnd_no_int": 0, "m40_rnd_w_int": 0,
    "m40_no_int_var_width": 0, "m40_w_int_var_width": 0, "m40_rnd_no_int_var_width": 0, "m40_rnd_w_int_var_width": 0
    }
periodics = {}
lin_nets = {}
cont_nets = {}
cont_periodics = {}
for i,sweep in enumerate(net_is.keys()):
    print(sweep)
    
    net = cp.deepcopy(nets[sweep][net_is[sweep]])
    if "var_width" in sweep:
        L_eff = 0.9 * net.mean_downstream_distance
    else:
        L_eff = 1.2 * net.mean_downstream_distance
    Teq = (L_eff**2.) / net.mean_diffusivity
    
    # periodics[sweep] = grlpx.evolve_network_periodic(
    #     net=cp.deepcopy(net),
    #     period=Teq,
    #     A_Qs=0.2,
    #     A_Q=0.
    #     )

    x0 = 50.e3
    Q_mean = 26.
    Qs_mean = Q_mean * 1.e-4
    B_mean = 254.
    lin_nets[sweep] = grlpx.set_up_long_profile(
        L=L_eff,
        Q_mean=Q_mean,
        Qs_mean=Qs_mean,
        B_mean=B_mean,
        p_Q=0,
        p_Qs=0,
        p_B=0,
        x0=x0,
        dx=5.e2,
        evolve=True
        )

    x0 = 50.e3
    Q_mean = 26.
    Qs_mean = Q_mean * 1.e-4
    B_mean = 254.
    if "var_width" in sweep:
        cont_nets[sweep] = grlpx.set_up_long_profile(
            L=100.e3,
            Q_mean=Q_mean,
            Qs_mean=Qs_mean,
            B_mean=B_mean,
            p_Q=hacks[sweep][net_is[sweep]]['p'],
            p_Qs=hacks[sweep][net_is[sweep]]['p'],
            p_B=hacks[sweep][net_is[sweep]]['p'],
            x0=x0,
            dx=5.e2,
            evolve=True
            )
    else:
        cont_nets[sweep] = grlpx.set_up_long_profile(
            L=100.e3,
            Q_mean=Q_mean,
            Qs_mean=Qs_mean,
            B_mean=B_mean,
            p_Q=hacks[sweep][net_is[sweep]]['p'],
            p_Qs=hacks[sweep][net_is[sweep]]['p'],
            p_B=0,
            x0=x0,
            dx=5.e2,
            evolve=True
            )

    cont_periodics[sweep] = grlpx.evolve_network_periodic(
        net=cp.deepcopy(cont_nets[sweep]),
        period=Teq,
        A_Qs=0.2,
        A_Q=0.
        )


# ---- Plot
# segs_to_plot = {
#     "m40_no_int": [43, 14, 31]
#     }

fig, axs = plt.subplots(3, 8, sharex=True)
for i,sweep in enumerate(net_is.keys()):
    net = cp.deepcopy(nets[sweep][net_is[sweep]])
    plan = grlp.plot_network(net, show=False)   
    for seg in net.list_of_LongProfile_objects:
        axs[0,i].plot(
            plan[seg.ID]['x'],
            plan[seg.ID]['y']
            )
        axs[1,i].plot(
            seg.x/1.e3,
            periodics[sweep]['G_z'][seg.ID]
            )
        axs[2,i].plot(
            seg.x/1.e3,
            periodics[sweep]['lag_z'][seg.ID]
            )
        # if seg.ID in segs_to_plot[sweep]:
        #     axs[0].text(
        #         seg.x.mean()/1.e3,
        #         plan[seg.ID]['y'].mean(),
        #         seg.ID, 
        #         horizontalalignment='center',
        #         verticalalignment='center')
        #     axs[1].text(
        #         seg.x.mean()/1.e3,
        #         periodic['G_z'][seg.ID].mean(),
        #         seg.ID, 
        #         horizontalalignment='center',
        #         verticalalignment='center')
        #     axs[2].text(
        #         seg.x.mean()/1.e3,
        #         periodic['lag_z'][seg.ID].mean(),
        #         seg.ID, 
        #         horizontalalignment='center',
        #         verticalalignment='center')

    lin_seg = lin_nets[sweep].list_of_LongProfile_objects[0]
    axs[1,i].plot(
        lin_seg.x/1.e3 + (100-lin_seg.x.max()/1.e3),
        lin_seg.compute_z_gain(lin_seg.equilibration_time),
        "k--"
        )
    axs[2,i].plot(
        lin_seg.x/1.e3 + (100.-lin_seg.x.max()/1.e3),
        lin_seg.compute_z_lag(lin_seg.equilibration_time)/lin_seg.equilibration_time,
        "k--"
        )
        
    cont_seg = cont_nets[sweep].list_of_LongProfile_objects[0]
    axs[1,i].plot(
        cont_seg.x/1.e3,
        cont_periodics[sweep]['G_z'][0],
        "k:"
        )
    axs[2,i].plot(
        cont_seg.x/1.e3,
        cont_periodics[sweep]['lag_z'][0],
        "k:"
        )
        
plt.show()

import sys
sys.exit()

sweep = "m40_no_int"
trunk_segs_to_plot = {
    sweep: nets[sweep][net_is[sweep]].find_downstream_IDs(32)
    }
trib_segs_to_plot = {
    sweep: [[43], [77, 76, 74], [63, 62], [25, 24]]
    }

for i,sweep in enumerate(trunk_segs_to_plot.keys()):
    net = cp.deepcopy(nets[sweep][net_is[sweep]])
    plan = grlp.plot_network(net, show=False)   
    for seg in net.list_of_LongProfile_objects:
        plt.plot(
            plan[seg.ID]['x'],
            plan[seg.ID]['y']
            )
        if seg.ID in trunk_segs_to_plot[sweep] or seg.ID in [id for trib in trib_segs_to_plot[sweep] for id in trib]:
            plt.text(
                seg.x.mean()/1.e3,
                plan[seg.ID]['y'][:-1].mean(),
                seg.ID, 
                horizontalalignment='center',
                verticalalignment='center')
    plt.show()


for i,sweep in enumerate(trunk_segs_to_plot.keys()):
    net = cp.deepcopy(nets[sweep][net_is[sweep]])
    fig, axs = plt.subplots(1, 2, sharex=True, sharey=True)
    
    peaks = np.arange(250, 4000, 500)
    for ax in axs:
        for peak in peaks:
            ax.plot(
                [periodics[sweep]['time'][peak]/3.15e10]*2,
                [0, 700],
                ":",
                color="gray"
                )
    
    for j,ID in enumerate(trunk_segs_to_plot[sweep]):
        seg = net.list_of_LongProfile_objects[ID]
        if j == 0:
            trunk_x_stack = seg.x/1.e3
            trunk_z_stack = periodics[sweep]['z'][ID]
        else:
            trunk_x_stack = np.hstack(( trunk_x_stack, seg.x/1.e3 ))
            trunk_z_stack = np.hstack(( trunk_z_stack, periodics[sweep]['z'][ID] ))
        
    nodes_to_plot = np.arange(0, len(trunk_x_stack)-1, 6).astype(int)
    for k in nodes_to_plot:
        axs[0].plot(
            periodics[sweep]['time']/3.154e10,
            trunk_z_stack[:,k]
            )
        pks = sig.find_peaks(trunk_z_stack[:,k])[0]
        trs = sig.find_peaks(-trunk_z_stack[:,k])[0]
        tps = np.hstack((pks, trs))
        axs[0].plot(
            periodics[sweep]['time'][tps]/3.154e10,
            trunk_z_stack[tps,k],
            'o'
            )

    for j,trib in enumerate(trib_segs_to_plot[sweep]):

        for k,ID in enumerate(trib):
            seg = net.list_of_LongProfile_objects[ID]
            if k == 0:
                trib_x_stack = seg.x/1.e3
                trib_z_stack = periodics[sweep]['z'][ID]
            else:
                trib_x_stack = np.hstack(( trib_x_stack, seg.x/1.e3 ))
                trib_z_stack = np.hstack(( trib_z_stack, periodics[sweep]['z'][ID] ))

        n_nodes = int(len(trib_x_stack)/6) + 1
        nodes_to_plot = np.linspace(0, len(trib_x_stack)-1, n_nodes).astype(int)
        for k in nodes_to_plot:
            axs[1].plot(
                periodics[sweep]['time']/3.154e10,
                trib_z_stack[:,k]
                )
            pks = sig.find_peaks(trib_z_stack[:,k])[0]
            trs = sig.find_peaks(-trib_z_stack[:,k])[0]
            tps = np.hstack((pks, trs))
            axs[1].plot(
                periodics[sweep]['time'][tps]/3.154e10,
                trib_z_stack[tps,k],
                'o'
                )

    plt.show()
    
    

# ---- Write output

if output_gmt:

    basedir = "../output/network/spatial/"

    outdirs = {
        "m40_no_int": "m40_fix_seg_length_no_internal/",
        "m40_w_int": "m40_fix_seg_length_w_internal/",
        "m40_rnd_no_int": "m40_rnd_seg_length_no_internal/",
        "m40_rnd_w_int": "m40_rnd_seg_length_w_internal/",
        "m40_no_int_var_width": "m40_fix_seg_length_no_internal_var_width/",
        "m40_w_int_var_width": "m40_fix_seg_length_w_internal_var_width/",
        "m40_rnd_no_int_var_width": "m40_rnd_seg_length_no_internal_var_width/",
        "m40_rnd_w_int_var_width": "m40_rnd_seg_length_w_internal_var_width/"
        }

    for i,sweep in enumerate(indirs.keys()):
        
        net = nets[sweep][net_is[sweep]]
        L = net.list_of_LongProfile_objects[0].x[-1]
        if "var_width" in sweep:
            L_eff = 0.9 * net.mean_downstream_distance
        else:
            L_eff = 1.2 * net.mean_downstream_distance
        Teq = (L_eff**2.) / net.mean_diffusivity
        lin_seg = lin_nets[sweep].list_of_LongProfile_objects[0]
        cont_seg = cont_nets[sweep].list_of_LongProfile_objects[0]

        with open(basedir + outdirs[sweep] + "gain.dg", "wb") as f:
            for j,seg in enumerate(net.list_of_LongProfile_objects):
                hdr = b"> -Z%i\n" % (net.segment_orders[j]+1)
                f.write(hdr)
                arr = np.column_stack((
                    seg.x/1.e3,
                    periodics[sweep]['G_z'][j]
                    ))
                np.savetxt(f, arr)
                
        with open(basedir + outdirs[sweep] + "lag.dl", "wb") as f:
            for j,seg in enumerate(net.list_of_LongProfile_objects):
                hdr = b"> -Z%i\n" % (net.segment_orders[j]+1)
                f.write(hdr)
                arr = np.column_stack((
                    seg.x/1.e3,
                    periodics[sweep]['lag_z'][j]
                    ))
                np.savetxt(f, arr)
                
        with open(basedir + outdirs[sweep] + "lin_gain.dg", "wb") as f:
            arr = np.column_stack((
                (L - lin_seg.x.max() + lin_seg.x)/1.e3,
                lin_seg.compute_z_gain(Teq)
                ))
            np.savetxt(f, arr)
            
        with open(basedir + outdirs[sweep] + "lin_lag.dl", "wb") as f:
            arr = np.column_stack((
                (L - lin_seg.x.max() + lin_seg.x)/1.e3,
                lin_seg.compute_z_lag(Teq)/Teq
                ))
            np.savetxt(f, arr)
            
        with open(basedir + outdirs[sweep] + "cont_gain.dg", "wb") as f:
            arr = np.column_stack((
                cont_seg.x/1.e3,
                cont_periodics[sweep]['G_z'][0]
                ))
            np.savetxt(f, arr)
            
        with open(basedir + outdirs[sweep] + "cont_lag.dl", "wb") as f:
            arr = np.column_stack((
                cont_seg.x/1.e3,
                cont_periodics[sweep]['lag_z'][0]
                ))
            np.savetxt(f, arr)
            
    for i,sweep in enumerate(trunk_segs_to_plot.keys()):
        net = nets[sweep][net_is[sweep]]
        plan = grlp.plot_network(net, show=False)
        
        with open(basedir + outdirs[sweep] + "plan_gain.dg", "wb") as f:
            for j,seg in enumerate(net.list_of_LongProfile_objects):
                for k in range(len(seg.x)+1):
                    if k < len(seg.x):
                        hdr = b"> -Z%f\n" % (periodics[sweep]['G_z'][j][k:k+2].mean())
                    else:
                        hdr = b"> -Z%f\n" % (periodics[sweep]['G_z'][j][k-1])
                    f.write(hdr)
                    arr = np.column_stack((
                        plan[j]['x'][k:k+2],
                        plan[j]['y'][k:k+2]
                        ))
                    np.savetxt(f, arr)
                    
        with open(basedir + outdirs[sweep] + "plan_lag.dl", "wb") as f:
            for j,seg in enumerate(net.list_of_LongProfile_objects):
                for k in range(len(seg.x)+1):
                    if k < len(seg.x):
                        hdr = b"> -Z%f\n" % (periodics[sweep]['lag_z'][j][k:k+2].mean())
                    else:
                        hdr = b"> -Z%f\n" % (periodics[sweep]['lag_z'][j][k-1])
                    f.write(hdr)
                    arr = np.column_stack((
                        plan[j]['x'][k:k+2],
                        plan[j]['y'][k:k+2]
                        ))
                    np.savetxt(f, arr)
                    
        with open(basedir + outdirs[sweep] + "plan_select.d", "wb") as f:
            for j in trunk_segs_to_plot[sweep]:
                arr = np.column_stack((
                    plan[j]['x'],
                    plan[j]['y']
                    ))
                np.savetxt(f, arr)
            for trib in trib_segs_to_plot[sweep]:
                hdr = b">\n"
                f.write(hdr)
                for j in trib:
                    if j==trib[-1]:
                        arr = np.column_stack((
                            plan[j]['x'][:-1],
                            plan[j]['y'][:-1]
                            ))
                    else:    
                        arr = np.column_stack((
                            plan[j]['x'],
                            plan[j]['y']
                            ))
                    np.savetxt(f, arr)
                      
        for j,ID in enumerate(trunk_segs_to_plot[sweep]):
            seg = net.list_of_LongProfile_objects[ID]
            if j == 0:
                trunk_x_stack = seg.x/1.e3
                trunk_z_stack = periodics[sweep]['z'][ID]
                trunk_o_stack = np.full(len(seg.x), net.segment_orders[ID])
            else:
                trunk_x_stack = np.hstack(( trunk_x_stack, seg.x/1.e3 ))
                trunk_z_stack = np.hstack(( trunk_z_stack, periodics[sweep]['z'][ID] ))
                trunk_o_stack = np.hstack(( trunk_o_stack, np.full(len(seg.x), net.segment_orders[ID]) ))
        
        nodes_to_plot = np.arange(0, len(trunk_x_stack)-1, 6).astype(int)
        
        with open(basedir + outdirs[sweep] + "trunk.te", "wb") as f:
            for k in nodes_to_plot:
                hdr = b"> -Z%f\n" % (trunk_o_stack[k]+1)
                f.write(hdr)
                arr = np.column_stack((
                    periodics[sweep]['time']/3.154e10,
                    trunk_z_stack[:,k]
                    ))
                np.savetxt(f, arr)
                
        with open(basedir + outdirs[sweep] + "trunk_tps.te", "wb") as f:
            for k in nodes_to_plot:
                pks = sig.find_peaks(trunk_z_stack[:,k])[0]
                trs = sig.find_peaks(-trunk_z_stack[:,k])[0]
                tps = np.hstack((pks, trs))
                arr = np.column_stack((
                    periodics[sweep]['time'][tps]/3.154e10,
                    trunk_z_stack[tps,k],
                    np.full(len(tps), trunk_o_stack[k]+1)
                    ))
                np.savetxt(f, arr)
        
        with open(basedir + outdirs[sweep] + "scl_tp_grid.te", "wb") as f:
            peaks = np.arange(250, 4000, 500)
            for peak in peaks:
                hdr = b">\n"
                f.write(hdr)
                arr = np.column_stack((
                    [periodics[sweep]['time'][peak]/3.15e10]*2,
                    [0, 700]
                ))
                np.savetxt(f, arr)

        trib_x_stacks = []
        trib_z_stacks = []
        trib_o_stacks = []
        for j,trib in enumerate(trib_segs_to_plot[sweep]):
            for k,ID in enumerate(trib):
                seg = net.list_of_LongProfile_objects[ID]
                if k == 0:
                    trib_x_stack = seg.x/1.e3
                    trib_z_stack = periodics[sweep]['z'][ID]
                    trib_o_stack = np.full(len(seg.x), net.segment_orders[ID])
                else:
                    trib_x_stack = np.hstack(( trib_x_stack, seg.x/1.e3 ))
                    trib_z_stack = np.hstack(( trib_z_stack, periodics[sweep]['z'][ID] ))
                    trib_o_stack = np.hstack(( trunk_o_stack, np.full(len(seg.x), net.segment_orders[ID]) ))
            trib_x_stacks.append(trib_x_stack)
            trib_z_stacks.append(trib_z_stack)
            trib_o_stacks.append(trib_o_stack)

        with open(basedir + outdirs[sweep] + "trib.te", "wb") as f:
            for j,trib in enumerate(trib_segs_to_plot[sweep]):
                n_nodes = int( len(trib_x_stacks[j])/6) + 1
                nodes_to_plot = np.linspace(0, len(trib_x_stacks[j])-1, n_nodes).astype(int)
                for k in nodes_to_plot:
                    hdr = b"> -Z%f\n" % (trib_o_stacks[j][k]+1)
                    f.write(hdr)
                    arr = np.column_stack((
                        periodics[sweep]['time']/3.154e10,
                        trib_z_stacks[j][:,k]
                        ))
                    np.savetxt(f, arr)
                    
        with open(basedir + outdirs[sweep] + "trib_tps.te", "wb") as f:
            for j,trib in enumerate(trib_segs_to_plot[sweep]):
                n_nodes = int( len(trib_x_stacks[j])/6) + 1
                nodes_to_plot = np.linspace(0, len(trib_x_stacks[j])-1, n_nodes).astype(int)
                for k in nodes_to_plot:
                    pks = sig.find_peaks(trib_z_stacks[j][:,k])[0]
                    trs = sig.find_peaks(-trib_z_stacks[j][:,k])[0]
                    tps = np.hstack((pks, trs))
                    arr = np.column_stack((
                        periodics[sweep]['time'][tps]/3.154e10,
                        trib_z_stacks[j][tps,k],
                        np.full(len(tps), trib_o_stacks[j][k]+1)
                        ))
                    np.savetxt(f, arr)