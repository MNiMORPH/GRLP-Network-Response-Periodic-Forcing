from grlp import *
from grlp_extras import *
import scipy.stats as sts
from scipy.optimize import minimize
import random
import copy
import pickle
import os

def analyse_network(i):
    
    print("Working on network " + str(i) + ".")
    
    # Network props
    effective_rainfall = 1.e3*0.4/3.154e10
    B = 98.1202038813591
    sediment_discharge_ratio = 1.e4
    
    # ---- Read in expected topological lengths
    expected_topological_lengths = np.loadtxt("../expected_length/expected_lengths.dat")
    
    # ---- Make choices for random magnitude
    min_mag = 2
    max_mag = 100
    magnitude_choices = np.array([], dtype=int)
    for mag in range(min_mag,max_mag+1):
        if mag==2:
            possible_length_range = 1
        else:
            possible_length_range = 1 + np.log2(mag - int(1. + np.log2(mag)))
        magnitude_choices = np.hstack(( 
            magnitude_choices, 
            np.full(int(possible_length_range), mag) ))
    
    # ---- Set up network
    mag = 40
    # mag = int(random.choice(magnitude_choices))
    
    # # Shreve numbers
    # segment_length = sts.gamma(2., scale=260./2.)
    # segment_length_area_ratio = sts.norm(loc=300., scale=30.)
    # supply_area = sts.norm(loc=52000., scale=5200.)
    
    # My numbers
    mean_total_length = 100.e3
    expected_topological_length = expected_topological_lengths[mag-1,1]
    mean_segment_length = 100.e3 / expected_topological_length
    mean_segment_length_area_ratio = 300. # from Shreve
    mean_supply_area = mean_segment_length * mean_segment_length_area_ratio / 2.
    segment_length = sts.gamma(2., scale=mean_segment_length/2.)
    segment_length_area_ratio = sts.norm(loc=mean_segment_length_area_ratio, scale=mean_segment_length_area_ratio/10.)
    supply_area = sts.norm(loc=mean_supply_area, scale=mean_supply_area/10.)    
    
    # ---- Network topology
    # net, net_topo = generate_random_network(
    #     magnitude=mag, 
    #     segment_length=segment_length,
    #     segment_length_area_ratio=segment_length_area_ratio,
    #     supply_area=supply_area,
    #     approx_dx=5.e2,
    #     min_nxs=5,
    #     mean_discharge=False,
    #     effective_rainfall=effective_rainfall,
    #     sediment_discharge_ratio=sediment_discharge_ratio,
    #     width=B,
    #     topology=False,
    #     evolve=True
    #     )
    net, net_topo = generate_random_network(
        magnitude=mag, 
        segment_length=segment_length,
        segment_length_area_ratio=False,
        supply_area=False,
        approx_dx=5.e2,
        min_nxs=5,
        mean_discharge=10.,
        effective_rainfall=False,
        sediment_discharge_ratio=sediment_discharge_ratio,
        width=B,
        topology=False,
        evolve=True
        )
    net.compute_network_properties()

    # ---- Basic lp object to get k_Qs for later
    lp = LongProfile()
    lp.basic_constants()
    lp.bedload_lumped_constants()
    lp.set_hydrologic_constants()

    # ---- Liear version
    L_eff = 0.7 * net.mean_downstream_distance
    dx = L_eff / 100.
    S0 = (1./(lp.k_Qs*sediment_discharge_ratio))**(6./7.)
    mean_Qw = np.hstack([seg.Q for seg in net.list_of_LongProfile_objects]).mean()
    mean_S = np.hstack([seg.S for seg in net.list_of_LongProfile_objects]).mean()
    mean_B = np.hstack([seg.B for seg in net.list_of_LongProfile_objects]).mean()
    lin_net = Network()
    lin_net.initialize(
        config_file = None,
        x_bl = L_eff,
        z_bl = 0.,
        S0 = [S0],
        upstream_segment_IDs = [[]],
        downstream_segment_IDs = [[]],
        x = [np.arange(0,L_eff,dx)],
        z = [(L_eff-np.arange(0,L_eff,dx))*S0],
        Q = [np.full(len(np.arange(0,L_eff,dx)),mean_Qw)],
        B = [np.full(len(np.arange(0,L_eff,dx)),mean_B)],
        overwrite = False
        )
    lin_net.set_niter(3)
    lin_net.get_z_lengths()
    lin_net.evolve_threshold_width_river_network(nt=100, dt=3.15e11)
    lin_net.list_of_LongProfile_objects[0].compute_equilibration_time()
    
    # ---- Hack
    hack = find_network_hack_parameters(net)

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
            z, Qs, time, scale = evolve_network_periodic(neti, period, A_Qs, A_Qw)
            z_gain = compute_network_z_gain(neti, z, A_Qs, A_Qw, [seg.S for seg in net.list_of_LongProfile_objects])
            Qs_gain = compute_network_Qs_gain(neti, Qs, A_Qs, A_Qw, [q[0,:] for q in Qs])
            z_lag = find_network_lag(net, z, time, scale, period)
            # Qs_lag = find_network_lag(net, Qs, time, scale, period)
            Qs_lag = find_lag_time_single(Qs[0][:,-1], time, scale, period, can_lead=can_lead)/period
            
            # Record gain
            z_gains[lab].append(z_gain)
            Qs_gains[lab].append(Qs_gain)
            
            # Record lag
            z_lags[lab].append(z_lag)
            Qs_lags[lab].append(Qs_lag)

    # ---- Compute best fitting equilibration times
    net_Teq = find_network_equilibration_time(
        [g[0][-1] for g in z_gains['Qs']],
        periods,
        lin_net)
    net_Teq_Qs = find_network_equilibration_time_Qs(
        [g[0][-1] for g in Qs_gains['Qs']], 
        periods,
        lin_net)

    # ---- Output
    outdir = "/home/mcnab/grlp_network_analysis/output/network/m40_rnd_seg_length_no_internal/" + str(i) + "/"
    # outdir = "./test/" + str(i) + "/"
    
    os.makedirs(outdir)
    with open(outdir + "props.obj", "wb") as f:
        pickle.dump(
            {'topology': net_topo.links,
            'nx_list': [len(seg.x) for seg in net.list_of_LongProfile_objects], 
            'dxs': [seg.x[1]-seg.x[0] for seg in net.list_of_LongProfile_objects], 
            'lengths': net_topo.segment_lengths,
            'source_areas': net_topo.source_areas,
            'segment_areas': net_topo.segment_areas,
            'supply_discharges': [
                area*effective_rainfall for area in net_topo.source_areas
                ],
            'internal_discharges': [
                area*effective_rainfall for area in net_topo.segment_areas
                ],
            'sediment_discharge_ratio': sediment_discharge_ratio,
            'B': B}, 
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
    
    from datetime import datetime
    print("Starting: " + datetime.now().strftime("%H:%M:%S"))
    
    import multiprocessing as mp
    with mp.Pool(processes=10) as pool:
        results = pool.map(analyse_network, range(i,j+1))
    
    print("Finished: " + datetime.now().strftime("%H:%M:%S"))