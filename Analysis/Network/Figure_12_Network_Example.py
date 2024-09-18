"""
This script performs the analysis presented in Figure 12 of McNab et al. (2024,
EGUsphere); produces a rough version of the Figure; and, optionally, generates
output files for plotting the final Figure in GMT.

The purpose of the script/figure is to .

nbviewer.org/github/dpsanders/matplotlib-examples/blob/master/colorline.ipynb
"""


# ---- Define functions
def compute_origin_gradient(x, y):
    x = np.array(x)
    y = np.array(y)
    return x.dot(y) / x.dot(x)


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
neti = 0
Pi = 3


# ---- Read data
print("Reading results.")
nets, hacks, gains, lags = grlpx.read_MC(indir)


# ---- Measure gain and lag with period equal to network equilibration time
print("Evolving networks.")

# Predict network Teq
L_eff = nets[neti]['UUU'].mean_downstream_distance * 1.2
Teq = (L_eff**2.) / nets[neti]['UUU'].mean_diffusivity

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


# ---- Segments to plot

plan = grlp.plot_network(nets[neti]['UUU'], show=False)
for i,seg in enumerate(nets[neti]['UUU'].list_of_LongProfile_objects):
    plt.plot(plan[i]['x'], plan[i]['y'], "0.5")
    plt.text(plan[i]['x'][:-1].mean(), plan[i]['y'][:-1].mean(), i)
plt.show()
    

trunk_segs = nets[neti]['UUU'].find_downstream_IDs(38)
trunk_x_stack = np.hstack(( [nets[neti]['UUU'].list_of_LongProfile_objects[i].x/1.e3 for i in trunk_segs] ))
trunk_y_stack = np.hstack(( [plan[i]['y'][:-1] for i in trunk_segs] ))
trunk_z_stack = np.hstack(( [periodic['z'][i] for i in trunk_segs] ))
nodes_to_plot = np.arange(0, len(trunk_x_stack)-1, 6).astype(int)

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
    
axs[0,0].plot(trunk_x_stack[nodes_to_plot], trunk_y_stack[nodes_to_plot], "o", ms=4, mec='k', mfc='none')

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

for k in nodes_to_plot:
    axs[1,0].plot(
        periodic['time']/3.154e10,
        trunk_z_stack[:,k]
        )
    pks = sig.find_peaks(trunk_z_stack[:,k])[0]
    trs = sig.find_peaks(-trunk_z_stack[:,k])[0]
    tps = np.hstack((pks, trs))
    axs[1,0].plot(
        periodic['time'][tps]/3.154e10,
        trunk_z_stack[tps,k],
        'o'
        )

for i,row in enumerate(axs):
    for ax in row:
        ax.set_box_aspect(1)
        if i==0:
            ax.set_xlabel(r"Downstream distance, $x$ [km]")
plt.show()