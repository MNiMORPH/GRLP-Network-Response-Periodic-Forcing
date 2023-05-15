from grlp import *
from extras import *
from scipy.optimize import minimize
import random
import copy
import pickle
import os

def evolve_network_periodic(net, period, A_Qs, A_Q):
    
    # ---- Set up time domain
    time, dt = np.linspace(0., period*4., 4000, retstep=True)
    scale = np.sin(2. * np.pi * time / period)
    
    # ---- Set up arrays for output
    z = [np.zeros(( len(time), len(seg.z) ))
            for seg in net.list_of_LongProfile_objects]
    Qs = [np.zeros(( len(time), len(seg.Q_s) ))
            for seg in net.list_of_LongProfile_objects]
    
    # ---- Initial sediment and water supplies
    Qs0 = net.list_of_LongProfile_objects[net.sources[0]].Q_s_0
    Qw0 = [np.zeros(len(seg.Q)) for seg in net.list_of_LongProfile_objects]
    for seg in net.list_of_LongProfile_objects:
        Qw0[seg.ID] = seg.Q.copy()
    
    # ---- Evolve
    for i,s in enumerate(scale):
        for seg in net.list_of_LongProfile_objects:
            seg.set_Q(Qw0[seg.ID] * (1. + A_Q*s))
            if seg.ID in net.sources:
                seg.set_Qs_input_upstream(Qs0 * (1. + A_Qs*s))
        net.evolve_threshold_width_river_network(nt=1, dt=dt)
        for seg in net.list_of_LongProfile_objects:
            z[seg.ID][i,:] = seg.z.copy()
            seg.compute_Q_s()
            Qs[seg.ID][i,:] = seg.Q_s.copy()
    
    return z, Qs, time, (1. + (A_Qs-A_Q)*scale)
    
def compute_network_z_gain(net, z, A_Qs, A_Q, S0):
    gain = [np.zeros(len(seg.z)) for seg in net.list_of_LongProfile_objects]
    for seg in net.list_of_LongProfile_objects:
        amp = (
            z[seg.ID][2000:,:].max(axis=0) - 
            z[seg.ID][2000:,:].min(axis=0)
            ) / 2.
        gain[seg.ID] = (
            amp / (
                S0 * 
                (net.list_of_LongProfile_objects[0].x_ext.max() - seg.x) *
                abs(A_Qs-A_Q) ) 
            )
    return gain
    
def compute_network_Qs_gain(net, Qs, A_Qs, A_Q, Qs0):
    gain = [np.zeros(len(seg.Q_s)) for seg in net.list_of_LongProfile_objects]
    for seg in net.list_of_LongProfile_objects:
        amp = (
            Qs[seg.ID][2000:,:].max(axis=0) - 
            Qs[seg.ID][2000:,:].min(axis=0)
            ) / 2.
        gain[seg.ID] = amp / ( Qs0[seg.ID] * abs(A_Qs-A_Q) )
    return gain

def find_network_lag(net, prop, time, scale, period):
    lag = [np.zeros(len(seg.x)) for seg in net.list_of_LongProfile_objects]
    for seg in net.list_of_LongProfile_objects:
        lag[seg.ID] = find_lag_times(prop[seg.ID], time, scale) / period
    return lag
    
def find_network_equilibration_time(net_gain, net_periods, lp):
    
    def gain_misfit(scaled_Teq, net_gain, net_periods, lp):
        Teq = scaled_Teq * lp.equilibration_time
        lin_gain = [
            lp.compute_z_gain(p)[-1]
            for p in net_periods / lp.equilibration_time * Teq
            ]
        misfit = np.sqrt( (1./len(net_gain)) * sum((np.array(net_gain) - lin_gain)**2.) )
        return misfit
    
    fit = minimize(
        fun=gain_misfit, 
        x0=1.,
        args=(net_gain,net_periods,lp,))
        
    return lp.equilibration_time / fit.x
    
def find_network_equilibration_time_Qs(net_gain, net_periods, lp):
    
    def gain_misfit(scaled_Teq, net_gain, net_periods, lp):
        Teq = scaled_Teq * lp.equilibration_time
        lin_gain = [
            lp.compute_Qs_gain(p, A_Qs=0.2)[-1]
            for p in net_periods / lp.equilibration_time * Teq
            ]
        misfit = np.sqrt( (1./len(net_gain)) * sum((np.array(net_gain) - lin_gain)**2.) )
        return misfit
    
    fit = minimize(
        fun=gain_misfit, 
        x0=1.,
        args=(net_gain,net_periods,lp,))
        
    return lp.equilibration_time / fit.x[0]

def analyse_network(i):

    print("Working on network " + str(i) + ".")

    # ---- River properties
    L = 100.e3
    mean_Q = 10.
    mean_Qs = 0.001
    B = 98.1202038813591
    S0 = (mean_Qs / (0.040987384904837776 * mean_Q))**(6./7.)

    # ---- Linear
    lp = LongProfile()
    lp.basic_constants()
    lp.bedload_lumped_constants()
    lp.set_hydrologic_constants()
    lp.set_x(x_ext=np.arange(0., L+5.e2, 5.e2))
    lp.set_Q(Q=mean_Q)
    lp.set_B(B=B)
    lp.set_z(S0=-(mean_Qs/(lp.k_Qs*mean_Q))**(6./7.))
    lp.set_Qs_input_upstream(mean_Qs)
    lp.set_z_bl(0.)
    lp.set_uplift_rate(0.)
    lp.set_niter()
    lp.compute_Q_s()
    lp.compute_equilibration_time()
    
    # ---- Load expected lengths
    arr = np.loadtxt("./expected_lengths.dat")
    magnitudes = arr[:,0]
    expected_lengths = arr[:,1]
    
    # ---- Make choices for random magnitude
    min_mag = 2
    max_mag = 60
    magnitude_choices = np.array([])
    for mag in range(min_mag,max_mag+1):
        expected_length = expected_lengths[mag-1]
        magnitude_choices = np.hstack(( 
            magnitude_choices, 
            np.full(int(expected_length), mag) ))
    
    # ---- Set up network
    # mag = 40
    mag = int(random.choice(magnitude_choices))
    net, net_topo = generate_random_network(mag, L, B, mean_Q, mean_Qs, evolve=True)
    
    # ---- Hack
    hack = find_network_hack_parameters(net)
    
    # ---- Periodic
    periods = np.logspace(-2.,2.,7) * lp.equilibration_time
    z_gains = []
    z_lags = []
    Qs_gains = []
    Qs_lags = []
    for period in periods:
        
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
        lp)
    net_Teq_Qs = find_network_equilibration_time_Qs(
        [g[0][-1] for g in Qs_gains], 
        periods,
        lp)

    # ---- Output
    outdir = "/home/mcnab/output/network" + str(i) + "/"
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
    with mp.Pool(processes=8) as pool:
        results = pool.map(analyse_network, range(i,j+1))
    
    print("Finished: " + datetime.now().strftime("%H:%M:%S"))