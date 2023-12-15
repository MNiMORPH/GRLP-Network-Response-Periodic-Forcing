from grlp import *
from grlp_extras import *
from scipy.stats import  gamma, norm
from scipy.optimize import minimize
import random
import copy
import pickle
import os

def analyse_network(i):
    
    print("Working on network " + str(i) + ".")

    # ---- Network props
    ext_link_length = gamma(2., scale=255./2.)
    int_link_length = gamma(2., scale=267./2.)
    ext_length_area_scl = norm(loc=127.e3/255., scale=127.e3/255.*0.1)
    int_length_area_scl = norm(loc=814.e2/267., scale=814.e2/267.*0.1)
    rainfall = 1.e3 / 3.154e10
    Cr = 0.4
    B = 100.
    sediment_discharge_ratio = 1.e4

    # ---- Network topology
    net_topo = Shreve_Random_Network(
        magnitude=40, 
        segment_length=(ext_link_length, int_link_length),
        segment_length_area_ratio=(ext_length_area_scl, int_length_area_scl)
        )
    net = set_up_network_object(
        nx_list = [5 for i in range(len(net_topo.downstream_segment_IDs))], 
        dxs = np.array(net_topo.segment_lengths)/5, 
        segment_lengths = net_topo.segment_lengths, 
        upstream_segment_list =  net_topo.upstream_segment_IDs,
        downstream_segment_list = net_topo.downstream_segment_IDs, 
        discharge_list = [area*rainfall*0.4 for area in net_topo.segment_areas], 
        sediment_discharge_ratio = sediment_discharge_ratio, 
        B = B, 
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
    mean_Qw = np.array([seg.Q for seg in net.list_of_LongProfile_objects]).mean()
    mean_S = np.array([seg.S for seg in net.list_of_LongProfile_objects]).mean()
    mean_B = np.array([seg.B for seg in net.list_of_LongProfile_objects]).mean()
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
    periods = np.logspace(-2.,2.,5) * lin_net.list_of_LongProfile_objects[0].equilibration_time
    z_gains = []
    z_lags = []
    Qs_gains = []
    Qs_lags = []
    for period in periods:
        print(period)
        
        # Run, compute metrics
        neti = copy.deepcopy(net)
        z, Qs, time, scale = evolve_network_periodic(neti, period, 0.2, 0.)
        z_gain = compute_network_z_gain(neti, z, 0.2, 0., S0)
        Qs_gain = compute_network_Qs_gain(neti, Qs, 0.2, 0., [q[0,:] for q in Qs])
        z_lag = find_network_lag(net, z, time, scale, period)
        Qs_lag = find_network_lag(net, Qs, time, scale, period)
        
        # Record gain
        z_gains.append(z_gain)
        Qs_gains.append(Qs_gain)
        
        # Record lag
        z_lags.append(z_lag)
        Qs_lags.append(Qs_lag)

    # ---- Compute best fitting equilibration times
    net_Teq = find_network_equilibration_time(
        [g[0][-1] for g in z_gains],
        periods,
        lin_net)
    net_Teq_Qs = find_network_equilibration_time_Qs(
        [g[0][-1] for g in Qs_gains], 
        periods,
        lin_net)

    # ---- Output
    outdir = "/home/mcnab/grlp_network_analysis/network/glic/output_161223/" + str(i) + "/"
    
    os.makedirs(outdir)
    with open(outdir + "props.obj", "wb") as f:
        pickle.dump(
            {'topology': net_topo.links,
            'nx_list': [5 for i in range(len(net_topo.downstream_segment_IDs))], 
            'dxs': np.array(net_topo.segment_lengths)/5, 
            'lengths': net_topo.segment_lengths,
            'areas': net_topo.segment_areas,
            'discharges': [area*rainfall*0.4 for area in net_topo.segment_areas], 
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