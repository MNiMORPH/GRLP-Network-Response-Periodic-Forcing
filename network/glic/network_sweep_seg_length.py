import numpy as np
import scipy.stats as sts
import random
import copy
import pickle
import os
import yaml

import grlp
import grlp_extras as grlpx


def analyse_network(iter):
    
    i = iter[0]
    setup_file = iter[1]
    
    with open(setup_file, 'r') as f:
        props = yaml.safe_load(f)
    
    print("Working on network " + str(i) + ".")
        
    # ---- Make choices for magnitude
    try:
        min_mag = props['magnitude'][0]
        max_mag = props['magnitude'][1]
        magnitude_choices = np.array([], dtype=int)
        for mag in range(min_mag,max_mag+1):
            if mag==2:
                possible_length_range = 1
            else:
                possible_length_range = 1 + np.log2(mag - int(1. + np.log2(mag)))
            magnitude_choices = np.hstack(( 
                magnitude_choices, 
                np.full(int(possible_length_range), mag) ))
        magnitude = int(random.choice(magnitude_choices))
    except TypeError:
        magnitude = props['magnitude']

    # ---- Set up random segment length/area generators
    try:
        segment_length = sts.gamma(2., scale=props['segment_length']['mean']/2.)
    except TypeError:
        segment_length = props['segment_length']
    try:
        segment_length_area_ratio = sts.norm(
            loc=props['segment_length_area_ratio']['mean'],
            scale=props['segment_length_area_ratio']['sd'])
    except TypeError:
        segment_length_area_ratio = props['segment_length_area_ratio']
    try:
        supply_area = sts.norm(
            loc=props['supply_area']['mean'],
            scale=props['supply_area']['sd'])
    except TypeError:
        supply_area = props['supply_area'] 

    # ---- Network topology
    net, net_topo = grlp.generate_random_network(
        magnitude=magnitude,
        max_length=props['max_length'],
        segment_length=segment_length,
        segment_length_area_ratio=segment_length_area_ratio,
        supply_area=supply_area,
        approx_dx=props['approx_dx'],
        min_nxs=props['min_nxs'],
        mean_discharge=props['mean_discharge'],
        effective_rainfall=props['effective_rainfall'],
        sediment_discharge_ratio=props['sediment_discharge_ratio'],
        mean_width=props['mean_width'],
        variable_width=props['variable_width'],
        topology=None,
        evolve=True
        )
    net.compute_network_properties()

    # ---- Hack
    hack = grlpx.find_network_hack_parameters(net)

    # ---- Liear version
    lin_net = grlpx.set_up_long_profile(
        props['max_length'],
        props['mean_discharge'],
        props['mean_discharge']/props['sediment_discharge_ratio'],
        props['mean_width'],
        0.,
        0.,
        0.
        )
    lin_net.list_of_LongProfile_objects[0].compute_equilibration_time()
    
    # ---- Periodic
    periods = np.logspace(-2.,2.,7) * lin_net.list_of_LongProfile_objects[0].equilibration_time
    z_gains = {'Qs': [], 'Qw': []}
    z_lags = {'Qs': [], 'Qw': []}
    Qs_gains = {'Qs': [], 'Qw': []}
    Qs_lags = {'Qs': [], 'Qw': []}
    for period in periods:
        
        for lab, A_Qs, A_Qw, can_lead in zip(['Qs', 'Qw'], [0.2, 0.], [0., 0.2], [False, True]):
            
            # Run, compute metrics
            neti = copy.deepcopy(net)
            periodic = grlpx.evolve_network_periodic(neti, period, A_Qs, A_Qw)
            
            # z_gain = grlpx.compute_network_gain(periodic['z'], 0.2)
            # Qs_gain = grlpx.compute_network_gain(periodic['Qs'], 0.2)
            # z_lag = grlpx.find_network_lag(net, periodic['z'], periodic['time'], periodic['S_scale'], period)
            # Qs_lag = grlpx.find_lag_time_single(periodic['Qs'][0][:,-1], periodic['time'], periodic['S_scale'], period, can_lead=can_lead)/period
            
            # Record gain
            z_gains[lab].append(periodic['G_z'])
            Qs_gains[lab].append(periodic['G_Qs'])
            
            # Record lag
            z_lags[lab].append(periodic['lag_z'])
            Qs_lags[lab].append(periodic['lag_Qs'])

    # ---- Compute best fitting equilibration times
    net_Teq = grlpx.find_network_equilibration_time(
        [g[0][-1] for g in z_gains['Qs']],
        periods,
        lin_net)
    net_Teq_Qs = grlpx.find_network_equilibration_time_Qs(
        [g[0][-1] for g in Qs_gains['Qs']], 
        periods,
        lin_net)

    # ---- Output
    outdir = props['outdir'] + str(i) + "/"
    os.makedirs(outdir)
    with open(outdir + "props.obj", "wb") as f:
        pickle.dump({
            'topology': net_topo.links,
            'nx_list': [len(seg.x) for seg in net.list_of_LongProfile_objects], 
            'dxs': [seg.x[1]-seg.x[0] for seg in net.list_of_LongProfile_objects], 
            'lengths': net_topo.segment_lengths,
            'source_areas': net_topo.source_areas,
            'segment_areas': net_topo.segment_areas,
            'mean_discharge': props['mean_discharge'],
            'supply_discharges': [
                seg.Q[0] if not seg.upstream_segment_IDs else 0. \
                    for seg in net.list_of_LongProfile_objects
                ],
            'internal_discharges': [
                seg.Q[-1]-seg.Q[0] for seg in net.list_of_LongProfile_objects
                ],
            'sediment_discharge_ratio': props['sediment_discharge_ratio'],
            'mean_width': props['mean_width'],
            'variable_width': props['variable_width']
            }, 
            f
        )
    with open(outdir + "hack.obj", "wb") as f:
        pickle.dump(hack, f)
    with open(outdir + "gain.obj", "wb") as f:
        pickle.dump(
            {'P': periods,
             'G_z': z_gains, 'G_Qs': Qs_gains,
             'Teq_z': net_Teq, 'Teq_Qs': net_Teq_Qs},
            f
        )
    with open(outdir + "lag.obj", "wb") as f:
        pickle.dump(
            {'P': periods, 'lag_z': z_lags, 'lag_Qs': Qs_lags},
            f
        )
    
    return i


if __name__ == "__main__":
    
    import sys
    i = int(sys.argv[1])
    j = int(sys.argv[2])
    setup_file = sys.argv[3]
    
    from datetime import datetime
    print("Starting: " + datetime.now().strftime("%H:%M:%S"))
    
    import multiprocessing as mp
    with mp.Pool(processes=2) as pool:
        results = pool.map(
            analyse_network, 
            [(k, setup_file) for k in range(i,j+1)]
            )
    
    print("Finished: " + datetime.now().strftime("%H:%M:%S"))