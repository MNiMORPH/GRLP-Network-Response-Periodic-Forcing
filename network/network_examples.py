from grlp import *
from grlp_extras import *

indirs = {
    "m20": "./glic/output_071123/",
    "m40": "./glic/output_081123/",
    "m40_var": "../output/network/m40_rnd_seg_length/"
    }
nets = {}
hacks = {}
for sweep in indirs.keys():
    sweep_nets, sweep_hacks, sweep_gains, sweep_lags = read_sweep(indirs[sweep])
    nets[sweep] = sweep_nets
    hacks[sweep] = sweep_hacks
    
# ------------------------- EXAMPLE ------------------------------------------ #

net_is = {"m20": 0, "m40": 0, "m40_var": 443}

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
    axs[i,3].plot(orders, net.length_scale*net.length_ratio**(orders-1)/1.e3, "--")
    axs[i,3].scatter(
        nets[sweep][net_is[sweep]].orders,
        [nets[sweep][net_is[sweep]].order_lengths[i]/1.e3 for i in nets[sweep][net_is[sweep]].orders])
    axs[i,3].plot(orders, net.discharge_scale*net.discharge_ratio**(orders-1), "--")
    axs[i,3].scatter(
        nets[sweep][net_is[sweep]].orders,
        [nets[sweep][net_is[sweep]].order_discharges[i] for i in nets[sweep][net_is[sweep]].orders])
    axs[i,3].set_yscale("log")
     
    i += 1
    
plt.show()

# ---- Write output

basedir = "../output/network/examples/"

outdirs = {
    "m20": "m20_fix_seg_length/",
    "m40": "m40_fix_seg_length/",
    "m40_var": "m40_rnd_seg_length/"
    }
    
for i,sweep in enumerate(indirs.keys()):
    
    net = nets[sweep][net_is[sweep]]
    # net.evolve_threshold_width_river_network(nt=100, dt=3.15e11)
    
    # Planform
    planform = plot_network(net, show=False)
    with open(basedir + outdirs[sweep] + "planform.d", "wb") as f:
        for j,seg in enumerate(net.list_of_LongProfile_objects):
            hdr = b"> -Z%i\n" % (net.segment_orders[j]+1)
            f.write(hdr)
            arr = np.column_stack(( planform[j]['x'], planform[j]['y'] ))
            np.savetxt(f, arr)

    # Discharge
    with open(basedir + outdirs[sweep] + "discharge.dq", "wb") as f:
        for j,seg in enumerate(net.list_of_LongProfile_objects):
            if seg.downstream_segment_IDs:
                downID = seg.downstream_segment_IDs[0]
                x = np.hstack(( seg.x_ext[0][1:]/1.e3, seg.x_ext[0][-1]/1.e3 ))
                Q = np.hstack((
                    seg.Q, 
                    seg.Q[-1], 
                    net.list_of_LongProfile_objects[downID].Q[0] ))
            else:
                x = seg.x/1.e3
                Q = seg.Q
            hdr = b"> -Z%i\n" % (net.segment_orders[j]+1)
            f.write(hdr)
            arr = np.column_stack(( x, Q ))
            np.savetxt(f, arr)
            
    # Hack
    hack = hacks[sweep][net_is[sweep]]
    with open(basedir + outdirs[sweep] + "hack_fit.dq", "wb") as f:
        d = np.linspace(0,max(hack['d']), 100)
        Q = hack['k'] * (d**hack['p'])
        arr = np.column_stack(( d/1.e3, Q ))
        np.savetxt(f, arr)
    with open(basedir + outdirs[sweep] + "hack.dq", "wb") as f:
        arr = np.column_stack(( 
            np.array(hack['d'])/1.e3,
            hack['Q'],
            net.segment_orders+1
            ))
        np.savetxt(f, arr)

    # # Profile
    # with open(basedir + outdirs[sweep] + "profile.de", "wb") as f:
    #     for j,seg in enumerate(net.list_of_LongProfile_objects):
    #         hdr = b"> -Z%i\n" % (net.segment_orders[j]+1)
    #         f.write(hdr)
    #         arr = np.column_stack(( seg.x/1.e3, seg.z ))
    #         np.savetxt(f, arr)
            
    # Ratios
    with open(basedir + outdirs[sweep] + "counts.oc", "wb") as f:
        arr = np.column_stack((
            net.orders,
            [net.order_counts[i] for i in net.orders]
            ))
        np.savetxt(f, arr)
    with open(basedir + outdirs[sweep] + "count_fit.oc", "wb") as f:
        arr = np.column_stack((
            net.orders,
            net.bifurcation_ratio**(max(net.orders)-net.orders)
            ))
        np.savetxt(f, arr)
    with open(basedir + outdirs[sweep] + "lengths.oc", "wb") as f:
        arr = np.column_stack((
            net.orders,
            [net.order_lengths[i]/1.e3 for i in net.orders]
            ))
        np.savetxt(f, arr)
    with open(basedir + outdirs[sweep] + "length_fit.oc", "wb") as f:
        arr = np.column_stack((
            net.orders,
            net.length_scale*net.length_ratio**(np.array(net.orders)-1)/1.e3
            ))
        np.savetxt(f, arr)
    with open(basedir + outdirs[sweep] + "discharges.oc", "wb") as f:
        arr = np.column_stack((
            net.orders,
            [net.order_discharges[i] for i in net.orders]
            ))
        np.savetxt(f, arr)
    with open(basedir + outdirs[sweep] + "discharge_fit.oc", "wb") as f:
        arr = np.column_stack((
            net.orders,
            net.discharge_scale*net.discharge_ratio**(np.array(net.orders)-1)
            ))
        np.savetxt(f, arr)   

    with open(basedir + outdirs[sweep] + "info.i", "wb") as f:
        arr = np.column_stack((
            net.bifurcation_ratio,
            net.length_ratio,
            net.discharge_ratio,
            1./hacks[sweep][net_is[sweep]]['p']
            ))
        np.savetxt(f, arr)