import numpy as np
import scipy.stats as sts
import random
import copy
import pickle
import os
import yaml
import matplotlib.pyplot as plt

import grlp
import grlp_extras as grlpx

# from grlp import *
# from grlp_extras import *

# ---- Initial set up
lp = grlp.LongProfile()
lp.basic_constants()
lp.bedload_lumped_constants()
lp.set_hydrologic_constants()


# ---- Reference properties
x0 = 50.e3
L = 100.e3
p__x_A = 1./0.54 # global mean from He et al. (2024)
k__x_A = 2.1*1.e3/(1.e6**0.55) # global mean from He et al. (2024), converted to m & m^2
P = 1.e3 / 1.e3 / 3.154e7 # precipitation rate in m/s
C_R = 0.4 # runoff coefficient
Qw_mean = P * C_R * k__x_A * ((L+x0)**(p__x_A+1.) - x0**(p__x_A+1.)) / (L * (p__x_A+1.))
Qs_mean = Qw_mean * 1.e-4
Teq = 3.154e12
diffusivity = L**2. / Teq
S0 = (Qs_mean/(lp.k_Qs*Qw_mean))**(6./7.)
B_mean = (7./6.) * (lp.k_Qs * Qw_mean * S0**(1./6.)) / (diffusivity * (1. - lp.lambda_p))


# ---- Network topology
net, net_topo = grlp.generate_random_network(
    magnitude=20,
    max_length=100.e3,
    approx_dx=5.e2,
    min_nxs=5,
    mean_discharge=Qw_mean,
    # segment_length_area_ratio=1,
    # supply_area=1,
    sediment_discharge_ratio= 1.e4,
    mean_width=B_mean,
    variable_width=False,
    topology=None,
    evolve=False
    )
net.compute_network_properties()



net_B, __ = grlp.generate_random_network(
    magnitude=20,
    max_length=100.e3,
    approx_dx=5.e2,
    min_nxs=5,
    mean_discharge=Qw_mean,
    # segment_length_area_ratio=1,
    # supply_area=1,
    sediment_discharge_ratio=1.e4,
    mean_width=B_mean,
    variable_width=True,
    topology=net_topo.links,
    evolve=False
    )
net_B.compute_network_properties()


for seg in net_B.list_of_LongProfile_objects:
    plt.plot(seg.x, seg.Q/Qw_mean)
    plt.plot(seg.x, seg.B/B_mean, ":")
plt.show()


import sys
sys.exit()

# ---- Evolve
period = ((1.25 * net.mean_downstream_distance)**2.) / net.mean_diffusivity
periodic = grlpx.evolve_network_periodic(copy.deepcopy(net), period, 0.2, 0.)
periodic_B = grlpx.evolve_network_periodic(copy.deepcopy(net_B), period, 0.2, 0.)


# ---- Plot
fig, axs = plt.subplots(2, 2, sharex=True, sharey="row")

for i,seg in enumerate(net.list_of_LongProfile_objects):
    axs[0,0].plot(seg.x/1.e3, periodic['G_z'][i])
    axs[1,0].plot(seg.x/1.e3, periodic['lag_z'][i])
    
for i,seg in enumerate(net_B.list_of_LongProfile_objects):
    axs[0,1].plot(seg.x/1.e3, periodic_B['G_z'][i])
    axs[1,1].plot(seg.x/1.e3, periodic_B['lag_z'][i])

axs[0,0].set_ylabel(r"$G_z$")
axs[1,0].set_ylabel(r"$\varphi_z$")
axs[1,0].set_xlabel(r"$x$, [km]")
axs[1,1].set_xlabel(r"$x$, [km]")

for ax in axs:
    for a in ax:
        a.set_box_aspect(1)
plt.show()