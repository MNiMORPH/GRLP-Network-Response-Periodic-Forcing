"""
This script performs the analysis presented in Figure 13 of McNab et al. (2025,
EGUsphere); produces a rough version of the Figure; and, optionally, generates
output files for plotting the final Figure in GMT.

The purpose of the script/figure is to show how patterns of aggradation and
incision can vary throughout a network. We show plots of gain and lag on
schematic network planform, and show time series of elevation for selected
segments.

Code for plotting coloured lines in matplotlib adapted from:
nbviewer.org/github/dpsanders/matplotlib-examples/blob/master/colorline.ipynb
"""


# ---- Import functions

# External packages
import numpy as np
import matplotlib.pyplot as plt
import copy
import grlp
import scipy.signal as sig

# Extra functions etc. for plotting
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
from mpl_toolkits.axes_grid1 import make_axes_locatable

# Local packages
import grlp_extras as grlpx


# ---- Variables
output_gmt = False
indir = "../../Output/Network/MC_N1_40/"
neti = 177
Pi = 3


# ---- Read data
print("Reading results.")
nets, hacks, gains, lags = grlpx.read_MC(indir, cases=['UUU'])


# ---- Measure gain and lag with period equal to network equilibration time
print("Evolving network.")

# Predict network Teq
Teq = gains[neti]['UUU']['Teq']
L_eff = np.sqrt(Teq*nets[neti]['UUU'].mean_diffusivity)

# Evolve to ensure steady state
nets[neti]['UUU'].evolve_threshold_width_river_network(nt=100, dt=3.154e10)

# Evolve with sinusoisal variation in sediment supply and period equal to
# equilibration time.
periodic = grlpx.evolve_network_periodic(
    net=copy.deepcopy(nets[neti]['UUU']),
    period=Teq,
    A_Qs=0.2,
    A_Q=0.
    )


# # ---- Some plots to help decide which segments to plot in the main figure.
# 
# plan = grlp.plot_network(nets[neti]['UUU'], show=False)
# for i,seg in enumerate(nets[neti]['UUU'].list_of_LongProfile_objects):
#     plt.plot(plan[i]['x'], plan[i]['y'], "0.5")
#     plt.text(plan[i]['x'][:-1].mean(), plan[i]['y'][:-1].mean(), i)
# plt.show()
# 
# for i,seg in enumerate(nets[neti]['UUU'].list_of_LongProfile_objects):
#     plt.plot(seg.x/1.e3, lags[neti]['UUU']['lag_z']['Qs'][Pi][i], "0.5")
#     plt.text(
#         seg.x.mean()/1.e3, lags[neti]['UUU']['lag_z']['Qs'][Pi][i].mean(), i
#         )
# plt.show()


# ---- List of segments to plot, and on which panels to plot their time series
segs_to_plot = [
    nets[neti]['UUU'].find_downstream_IDs(34),
    [78, 76],
    [6, 5],
    [69, 67, 65, 64, 63, 61, 49],
    [43, 41, 39],
    [2],
    [36],
    ]
seg_panels = [0, 2, 2, 1, 2, 1, 1]


# ---- Plot

fig, axs = plt.subplots(2, 3, sharex="row", sharey="row")

plan = grlp.plot_network(nets[neti]['UUU'], show=False)

for i,seg in enumerate(nets[neti]['UUU'].list_of_LongProfile_objects):
    
    points = np.array([plan[i]['x'], plan[i]['y']]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    
    
    order = np.full(len(plan[i]['x']), nets[neti]['UUU'].segment_orders[i]+1)
    order_lc = LineCollection(
        segments,
        array=order,
        cmap="viridis_r",
        norm=plt.Normalize(
            nets[neti]['UUU'].segment_orders.min()+1,
            nets[neti]['UUU'].segment_orders.max()+1
            )
        )
    order_cmap = axs[0,0].add_collection(order_lc)

    gain = np.hstack(( periodic['G_z'][i], periodic['G_z'][i][-1] ))
    gain_lc = LineCollection(
        segments,
        array=gain,
        cmap="plasma",
        norm=plt.Normalize(
            min([g.min() for g in periodic['G_z']]),
            max([g.max() for g in periodic['G_z']])
            )
        )
    gain_cmap = axs[0,1].add_collection(gain_lc)

    lag = np.hstack(( periodic['lag_z'][i], periodic['lag_z'][i][-1] ))
    lag_lc = LineCollection(
        segments,
        array=lag,
        cmap="Blues",
        norm=plt.Normalize(
            min([l.min() for l in periodic['lag_z']]),
            max([l.max() for l in periodic['lag_z']])
            )
        )
    lag_cmap = axs[0,2].add_collection(lag_lc)
    

divider = make_axes_locatable(axs[0,0])
cax = divider.append_axes('top', size='3%', pad=0.05)
fig.colorbar(
    order_cmap,
    cax=cax,
    orientation='horizontal',
    label='Order'
    )

divider = make_axes_locatable(axs[0,1])
cax = divider.append_axes('top', size='3%', pad=0.05)
fig.colorbar(
    gain_cmap,
    cax=cax,
    orientation='horizontal',
    label=r'Gain, $G_z$'
    )

divider = make_axes_locatable(axs[0,2])
cax = divider.append_axes('top', size='3%', pad=0.05)
fig.colorbar(
    lag_cmap,
    cax=cax,
    orientation='horizontal',
    label=r'Lag, ${\varphi}_z$ / $P$'
    )

axs[0,0].set_xlim(-10,110)
axs[0,0].set_ylim(0,max([seg['y'].max() for seg in plan.values()])+1)

for j,segs in enumerate(segs_to_plot):
    
    x_stack = np.hstack((
        [nets[neti]['UUU'].list_of_LongProfile_objects[i].x[:-1]/1.e3
            for i in segs]
        ))
    y_stack = np.hstack(( [plan[i]['y'][:-3] for i in segs] ))
    z_stack = np.hstack(( [periodic['z'][i][:,:-1] for i in segs] ))
    nodes_to_plot = np.hstack((
        np.arange(0, len(x_stack)-1, 12), len(x_stack)-2
        )).astype(int)    
    
    axs[0,0].plot(
        x_stack[nodes_to_plot],
        y_stack[nodes_to_plot],
        "o", ms=4, mec='k', mfc='none'
        )
    
    for k in nodes_to_plot:
    
        axs[1,seg_panels[j]].plot(
            periodic['time']/3.154e10,
            z_stack[:,k]
            )
        pks = sig.find_peaks(z_stack[:,k])[0]
        trs = sig.find_peaks(-z_stack[:,k])[0]
        tps = np.hstack((pks, trs))
        axs[1,seg_panels[j]].plot(
            periodic['time'][tps]/3.154e10,
            z_stack[tps,k],
            'o'
            )

for i,row in enumerate(axs):
    for ax in row:
        ax.set_box_aspect(1)
        if i==0:
            ax.set_xlabel(r"Downstream distance, $x$ [km]")
plt.show()


# ---- Save

if output_gmt:

    basedir = "../../Output/Network/Figure_13_Network_Example/"

    with open(basedir + "planform.d", "wb") as f:
        plan = grlp.plot_network(nets[neti]['UUU'], show=False)
        for seg in plan.keys():
            hdr = b"> -Z%f\n" % (nets[neti]['UUU'].segment_orders[seg])
            f.write(hdr)
            arr = np.column_stack(( plan[seg]['x'], plan[seg]['y'] ))
            np.savetxt(f, arr)
            
    with open(basedir + "planform_select.d", "wb") as f:
        for j,segs in enumerate(segs_to_plot):
            hdr = b">\n"
            f.write(hdr)
            arr = np.column_stack((
                np.hstack(( [plan[i]['x'][:-1] for i in segs] )),
                np.hstack(( [plan[i]['y'][:-1] for i in segs] ))
                ))
            np.savetxt(f, arr)

    with open(basedir + "planform_nodes.d", "wb") as f:
        for j,segs in enumerate(segs_to_plot):
            x_stack = np.hstack((
                [nets[neti]['UUU'].list_of_LongProfile_objects[i].x[:-1]/1.e3
                    for i in segs]
                ))
            y_stack = np.hstack(( [plan[i]['y'][:-3] for i in segs] ))
            nodes_to_plot = np.hstack((
                np.arange(0, len(x_stack)-1, 12),
                len(x_stack)-2
                )).astype(int)    
            arr = np.column_stack((
                np.hstack(( x_stack[nodes_to_plot] )),
                np.hstack(( y_stack[nodes_to_plot] ))
                ))
            np.savetxt(f, arr)
            
    with open(basedir + "planform_gain.dg", "wb") as f:
        plan = grlp.plot_network(nets[neti]['UUU'], show=False)
        for seg in plan.keys():
            for i in range(len(plan[seg]['x'])-1):
                if i <= len(periodic['G_z'][seg])-2:
                    hdr = b"> -Z%f\n" % ((periodic['G_z'][seg][i]+periodic['G_z'][seg][i+1])/2)
                elif i == len(periodic['G_z'][seg])-1:
                    hdr = b"> -Z%f\n" % periodic['G_z'][seg][i]
                else:
                    hdr = b"> -Z%f\n" % periodic['G_z'][seg][i-1]
                f.write(hdr)
                arr = np.column_stack((
                    [plan[seg]['x'][i], plan[seg]['x'][i+1]],
                    [plan[seg]['y'][i], plan[seg]['y'][i+1]]
                    ))
                np.savetxt(f, arr)

    with open(basedir + "planform_lag.dl", "wb") as f:
        plan = grlp.plot_network(nets[neti]['UUU'], show=False)
        for seg in plan.keys():
            for i in range(len(plan[seg]['x'])-1):
                if i <= len(periodic['lag_z'][seg])-2:
                    hdr = b"> -Z%f\n" % ((periodic['lag_z'][seg][i]+periodic['lag_z'][seg][i+1])/2)
                elif i == len(periodic['lag_z'][seg])-1:
                    hdr = b"> -Z%f\n" % periodic['lag_z'][seg][i]
                else:
                    hdr = b"> -Z%f\n" % periodic['lag_z'][seg][i-1]
                f.write(hdr)
                arr = np.column_stack((
                    [plan[seg]['x'][i], plan[seg]['x'][i+1]],
                    [plan[seg]['y'][i], plan[seg]['y'][i+1]]
                    ))
                np.savetxt(f, arr)

    with open(basedir + "force_tps.te", "wb") as f:
        tps = [250 + 500*i for i in range(8)]*2
        for tp in tps:
            hdr = b">\n"
            f.write(hdr)
            arr = np.column_stack((
                [periodic['time'][tp]/3.154e10]*2,
                [0, 1.e3]
                ))
            np.savetxt(f, arr)

    for panel in np.unique(seg_panels):
        filename = basedir + "panel%i.te" % panel
        
        with open(filename, "wb") as f:
            for j,segs in enumerate(segs_to_plot):
                if seg_panels[j] == panel:
                    
                    o_stack = np.hstack(( [
                        np.full(
                            len(nets[neti]['UUU'].list_of_LongProfile_objects[i].x[:-1]),
                            nets[neti]['UUU'].segment_orders[i]
                            )
                        for i in segs
                        ] ))
                    z_stack = np.hstack((
                        [periodic['z'][i][:,:-1] for i in segs]
                        ))
                    nodes_to_plot = np.hstack((
                        np.arange(0, len(z_stack[0,:])-1, 12),
                        len(z_stack[0,:])-1
                        )).astype(int)
                    
                    for k in nodes_to_plot:
                        arr = np.column_stack((
                            periodic['time']/3.154e10,
                            z_stack[:,k]
                            ))

                        hdr = b"> -Z%i\n" % o_stack[k]
                        f.write(hdr)
                        np.savetxt(f, arr)
                        
        filename = basedir + "panel_tps%i.te" % panel
        with open(filename, "wb") as f:
            for j,segs in enumerate(segs_to_plot):
                if seg_panels[j] == panel:
                    
                    o_stack = np.hstack(( [
                        np.full(
                            len(nets[neti]['UUU'].list_of_LongProfile_objects[i].x[:-1]),
                            nets[neti]['UUU'].segment_orders[i]
                            )
                        for i in segs
                        ] ))
                    z_stack = np.hstack(([periodic['z'][i][:,:-1] for i in segs]))
                    nodes_to_plot = np.hstack((
                        np.arange(0, len(z_stack[0,:])-1, 12),
                        len(z_stack[0,:])-1
                        )).astype(int)

                    for k in nodes_to_plot:
                        pks = sig.find_peaks(z_stack[:,k])[0]
                        trs = sig.find_peaks(-z_stack[:,k])[0]
                        tps = np.hstack((pks, trs))
                        arr = np.column_stack((
                            periodic['time'][tps]/3.154e10,
                            z_stack[tps,k],
                            np.full(len(tps), o_stack[k])
                            ))
                        np.savetxt(f, arr)