from grlp import *
from grlp_extras import *
from scipy.optimize import minimize
import random
import copy
import pickle
import os

def analyse_network(i):

    print("Working on network " + str(i) + ".")

    # ---- Basic lp object to get k_Qs
    lp = LongProfile()
    lp.basic_constants()
    lp.bedload_lumped_constants()
    lp.set_hydrologic_constants()

    # ---- River properties
    L = 100.e3
    mean_Q = 10.
    mean_Qs = 0.001
    B = 98.1202038813591
    S0 = (mean_Qs / (lp.k_Qs * mean_Q))**(6./7.)
    dx = 5.e2
    
    # ---- Simple example
    lin_net = Network()
    lin_net.initialize(
        config_file = None,
        x_bl = L,
        z_bl = 0.,
        S0 = [S0],
        upstream_segment_IDs = [[]],
        downstream_segment_IDs = [[]],
        x = [np.arange(0,L,dx)],
        z = [(L-np.arange(0,L,dx))*S0],
        Q = [np.full(int(L//dx),mean_Q)],
        B = [np.full(int(L//dx),B)],
        overwrite = False
        )
    lin_net.set_niter(3)
    lin_net.get_z_lengths()
    lin_net.evolve_threshold_width_river_network(nt=100, dt=3.15e11)
    lin_net.list_of_LongProfile_objects[0].compute_equilibration_time()

    # lp = LongProfile()
    # lp.basic_constants()
    # lp.bedload_lumped_constants()
    # lp.set_hydrologic_constants()
    # lp.set_x(x_ext=np.arange(0., L+5.e2, 5.e2))
    # lp.set_Q(Q=mean_Q)
    # lp.set_B(B=B)
    # lp.set_z(S0=-(mean_Qs/(lp.k_Qs*mean_Q))**(6./7.))
    # lp.set_Qs_input_upstream(mean_Qs)
    # lp.set_z_bl(0.)
    # lp.set_uplift_rate(0.)
    # lp.set_niter(3)
    # lp.compute_Q_s()
    # lp.compute_equilibration_time()
    
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
    mag = 20
    # mag = int(random.choice(magnitude_choices))
    net, net_topo = generate_random_network(mag, L, B, mean_Q, mean_Qs, evolve=True)
    
    # ---- Hack
    hack = find_network_hack_parameters(net)
    
    # ---- Periodic
    periods = np.logspace(-2.,2.,7) * lin_net.list_of_LongProfile_objects[0].equilibration_time
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
    outdir = "./../../output/network_sweep_v2_m20" + str(i) + "/"
    
    os.makedirs(outdir)
    with open(outdir + "props.obj", "wb") as f:
        pickle.dump(
            {'topology': net_topo.links,
            'Q_mean': mean_Q,
            'Qs_mean': mean_Qs,
            'B': B,
            'L': L}, 
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