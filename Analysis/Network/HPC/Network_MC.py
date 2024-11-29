"""
This script analyses the response of a network to sinusoidal variation in
sediment and water supply. It uses Python's multiprocessing package to run
different versions of the network in parallel (expecting eight cores to be
available).

Specifically, we randomly generate a network topology, and then create eight
network versions. The eight versions represent combinations of three binary
options, which we denote with a three letter code:
    - Uniform / non-uniform segment lengths                                [U/N]
        Segment lengths are either constant through the network or drawn
        from a gamma distribution with shape parameter equal to two (see
        Shreve, 1969, J. Geol.; Shreve, 1974, WRR).
    - Upstream / along stream supply of sediment and water                 [U/A]
        In the upstream supply case, sediment and water are only supplied
        at the valley inlets. In the along stream supply case, sediment
        and water are also added along stream.
    - Uniform / non-uniform valley width                                   [U/N]
        Valley width is either constant throughout the network or
        increases downstream at the same rate as water discharge.

We then evolve the networks with sinusoidal variation in sediment and water
supply, measure gain and lag in elevation throughout the network, and measure
gain and lag in sediment discharge at the outlet. We further use the gain in
sediment discharge at the outlet as a function of period to determine
empirically a valley response time.

The script expects some information as standard input. To run it, at the
command line type:

python3 Network_MC.py i N1 outdir

where:
    - i is an integer code for the network.
    - N1 is the number of valley inlet segments desired for the network.
    - outdir is a path to the desired output directory.
"""

# -------- Import functions

# External packages
import numpy as np
import scipy.stats as sts
import copy
import pickle
import os
import matplotlib.pyplot as plt
from datetime import datetime
import sys
import multiprocessing as mp

# Local packages
import grlp
import grlp_extras as grlpx


# -------- Define functions

def analyse_network(iter):
    """
    Analyse response of a network to sinusoidal variation in sediment and
    water supply.
    
    Expects a single iterable containing the necessary objects/information (for
    use with multiprocessing). It should include:
        - net: the network object to test.
        - lin_net: an equivalent single segment network to compare against.
        - outdir: path to the desired output directory.
        
    We test the response at different periods, use the outcome to calibrate
    a network response time, compute a best-fitting hack exponent, and save
    all the results. 
    """
    
    # ---- Unpack iterable input
    net = iter[0]
    lin_net = iter[1]
    outdir = iter[2]
    
    # ---- Get linear-equivalent equilibration time, compute periods to analyse
    T_eq = lin_net.list_of_LongProfile_objects[0].equilibration_time    
    periods = np.logspace(-2., 2., 7) * T_eq
    
    # ---- Prepare output
    G_z = {'Qs': [], 'Qw': []}
    lag_z = {'Qs': [], 'Qw': []}
    G_Qs = {'Qs': [], 'Qw': []}
    lag_Qs = {'Qs': [], 'Qw': []}
    
    # ---- Loop over periods, analyse
    for period in periods:
        
        # Loop over sediment forcing and water forcing
        for lab, A_Qs, A_Qw in zip(['Qs', 'Qw'], [0.2, 0.], [0., 0.2]):
            
            # Run, compute metrics
            neti = copy.deepcopy(net)
            periodic = grlpx.evolve_network_periodic(
                neti, period, A_Qs, A_Qw
                )
            
            # Record gain
            G_z[lab].append(periodic['G_z'])
            G_Qs[lab].append(periodic['G_Qs'])
            
            # Record lag
            lag_z[lab].append(periodic['lag_z'])
            lag_Qs[lab].append(periodic['lag_Qs'])

    # ---- Compute best fitting equilibration times
    net_Teq = grlpx.find_network_equilibration_time(
        [g[0][-1] for g in G_Qs['Qs']], 
        periods,
        lin_net
        )
        
    # ---- Hack
    hack = grlp.find_network_hack_parameters(net)

    # ---- Output
    os.makedirs(outdir)
    with open(outdir + "props.obj", "wb") as f:
        pickle.dump({
            'x_bl': net.list_of_LongProfile_objects[0].x_ext[0][-1],
            'z_bl': 0.,
            'S0': [
                seg.S0 
                for seg in net.list_of_LongProfile_objects
                if seg.S0 is not None
                ],
            'upstream_segment_IDs': [
                seg.upstream_segment_IDs
                for seg in net.list_of_LongProfile_objects
                ],
            'downstream_segment_IDs': [
                seg.downstream_segment_IDs
                for seg in net.list_of_LongProfile_objects
                ],
            'x_ls': [
                seg.x
                for seg in net.list_of_LongProfile_objects
                ],
            'z_ls': [
                seg.z
                for seg in net.list_of_LongProfile_objects
                ],
            'Q_ls': [
                seg.Q
                for seg in net.list_of_LongProfile_objects
                ],
            'dQ_ls': [
                seg.Q[1] - seg.Q[0]
                for seg in net.list_of_LongProfile_objects
                ],
            'B_ls': [
                seg.B
                for seg in net.list_of_LongProfile_objects
                ],
            'ssd_ls': [
                seg.ssd
                for seg in net.list_of_LongProfile_objects
                ]                                    
            }, 
            f
            )
    with open(outdir + "hack.obj", "wb") as f:
        pickle.dump(hack, f)
    with open(outdir + "gain.obj", "wb") as f:
        pickle.dump(
            {'P': periods, 'G_z': G_z, 'G_Qs': G_Qs, 'Teq': net_Teq},
            f
            )
    with open(outdir + "lag.obj", "wb") as f:
        pickle.dump(
            {'P': periods, 'lag_z': lag_z, 'lag_Qs': lag_Qs},
            f
            )


# -------- Unpack standard input
i = int(sys.argv[1])        # network index
N1 = int(sys.argv[2])       # number of valley-inlet segments
outdir = str(sys.argv[3])   # output directory


# -------- Report begin
begin = datetime.now()
print(str(i) + ": Starting: " + begin.strftime("%H:%M:%S"))


# -------- Valley properties
# Define properties to use when constructing the single segment valleys.
# Correspond to precipitation rate of c. 1 m/yr for a catchment with Hack
# exponent of 1.8 and runoff coefficent of 0.4; and an equilibration time of
# 100 kyr.
# See ../Compute_River_Properties.py for details.
x0 = 50.e3
Q_mean = 26.
Qs_mean = Q_mean * 1.e-4
B_mean = 254.


# -------- Network properties
mean_segment_length = 5.e3
segment_length = sts.gamma(2., scale=mean_segment_length/2.)
segment_length_area_ratio = 1.
supply_area = 10.e3


# -------- Set up networks: Uniform width
nets = {}

# ---- Base network
net, topo = grlp.generate_random_network(
    magnitude=N1,
    segment_length=mean_segment_length,
    approx_dx=2.e2,
    min_nxs=4,
    mean_discharge=Q_mean,
    sediment_discharge_ratio=1.e4,
    mean_width=B_mean,
    topology=None,
    evolve=True
    )
net.compute_network_properties()
nets['UUU'] = {'net': net, 'topo': topo}

# ---- Along stream supply
net, topo = grlp.generate_random_network(
    magnitude=N1,
    segment_length=mean_segment_length,
    segment_length_area_ratio=segment_length_area_ratio,
    supply_area=supply_area,
    approx_dx=2.e2,
    min_nxs=4,
    mean_discharge=Q_mean,
    sediment_discharge_ratio=1.e4,
    mean_width=B_mean,
    topology=nets['UUU']['topo'].links,
    evolve=True
    )
net.compute_network_properties()
nets['UAU'] = {'net': net, 'topo': topo}

# ---- Random segment lengths
net, topo = grlp.generate_random_network(
    magnitude=N1,
    segment_length=segment_length,
    approx_dx=2.e2,
    min_nxs=4,
    mean_discharge=Q_mean,
    sediment_discharge_ratio=1.e4,
    mean_width=B_mean,
    topology=nets['UUU']['topo'].links,
    evolve=True
    )
net.compute_network_properties()
nets['NUU'] = {'net': net, 'topo': topo}

# ---- Random segment lengths & Along stream supply
net, topo = grlp.generate_random_network(
    magnitude=N1,
    segment_lengths=nets['NUU']['topo'].segment_lengths,
    segment_length_area_ratio=segment_length_area_ratio,
    supply_area=supply_area,
    approx_dx=2.e2,
    min_nxs=4,
    mean_discharge=Q_mean,
    sediment_discharge_ratio=1.e4,
    mean_width=B_mean,
    topology=nets['UUU']['topo'].links,
    evolve=True
    )
net.compute_network_properties()
nets['NAU'] = {'net': net, 'topo': topo}


# -------- Set up networks: Non-uniform width

# ---- Base network
net, topo = grlp.generate_random_network(
    magnitude=N1,
    segment_length=mean_segment_length,
    approx_dx=2.e2,
    min_nxs=4,
    mean_discharge=Q_mean,
    sediment_discharge_ratio=1.e4,
    mean_width=B_mean,
    variable_width=True,
    topology=nets['UUU']['topo'].links,
    evolve=True
    )
net.compute_network_properties()
nets['UUN'] = {'net': net, 'topo': topo}

# ---- Along stream supply
net, topo = grlp.generate_random_network(
    magnitude=N1,
    segment_length=mean_segment_length,
    segment_length_area_ratio=segment_length_area_ratio,
    supply_area=supply_area,
    approx_dx=2.e2,
    min_nxs=4,
    mean_discharge=Q_mean,
    sediment_discharge_ratio=1.e4,
    mean_width=B_mean,
    variable_width=True,
    topology=nets['UUU']['topo'].links,
    evolve=True
    )
net.compute_network_properties()
nets['UAN'] = {'net': net, 'topo': topo}

# ---- Random segment lengths
net, topo = grlp.generate_random_network(
    magnitude=N1,
    segment_lengths=nets['NUU']['topo'].segment_lengths,
    approx_dx=2.e2,
    min_nxs=4,
    mean_discharge=Q_mean,
    sediment_discharge_ratio=1.e4,
    mean_width=B_mean,
    variable_width=True,
    topology=nets['UUU']['topo'].links,
    evolve=True
    )
net.compute_network_properties()
nets['NUN'] = {'net': net, 'topo': topo}

# ---- Random segment lengths & Along stream supply
net, topo = grlp.generate_random_network(
    magnitude=N1,
    segment_lengths=nets['NUU']['topo'].segment_lengths,
    segment_length_area_ratio=segment_length_area_ratio,
    supply_area=supply_area,
    approx_dx=2.e2,
    min_nxs=4,
    mean_discharge=Q_mean,
    sediment_discharge_ratio=1.e4,
    mean_width=B_mean,
    variable_width=True,
    topology=nets['UUU']['topo'].links,
    evolve=True
    )
net.compute_network_properties()
nets['NAN'] = {'net': net, 'topo': topo}


# -------- Single segment version
ss_nets = {}
for case in nets.keys():
    ss_nets[case] = grlpx.generate_single_segment_network(
        nets[case]['net'].list_of_LongProfile_objects[0].x.max(),
        Q_mean,
        Qs_mean,
        B_mean,
        0.,
        0.,
        0.
        )


# -------- Use multiprocessing to analyse each case in parallel
with mp.Pool(processes=8) as pool:
    results = pool.map(
        analyse_network, 
        [(nets[case]['net'], ss_nets[case], outdir + str(i) + "/" + case + "/")
            for case in nets.keys()]
        )


# -------- Report completion
finish = datetime.now()
print(
    str(i) +
    ": Finished: " + finish.strftime("%H:%M:%S") +
    ". Elapsed time: " + str(finish-begin) + "."
    )