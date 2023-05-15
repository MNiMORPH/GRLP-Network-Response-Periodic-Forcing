from grlp import *
from extras import *
import scipy
import os
import pickle

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
    
    # Initial attempt
    lag = [np.zeros(len(seg.x)) for seg in net.list_of_LongProfile_objects]
    for seg in net.list_of_LongProfile_objects:
        lag[seg.ID] = find_lag_times(prop[seg.ID], time, scale, period=period) / period
    
    # Check for cycle-skipped segment
    completed_segs = []
    for segID in net.sources:
        while net.list_of_LongProfile_objects[segID].downstream_segment_IDs:
            down_segID = net.list_of_LongProfile_objects[segID].downstream_segment_IDs[0]
            if down_segID not in completed_segs:
                if (lag[down_segID][0] - lag[segID][-1]) > 0.5:
                    lag[down_segID] -= 1.
                completed_segs.append(down_segID)
            segID = down_segID
    
    return lag

def find_lag_times(val, time, scale, threshold=0., can_lead=False, period=False, full=False):


    peak_lags = np.zeros( len(val[0,:]) )
    trough_lags = np.zeros( len(val[0,:]) )

    tps = []

    scl_peaks, __ = find_peaks(scale)
    scl_troughs, __ = find_peaks(-scale)
    scl_tps = np.sort( np.hstack(( scl_peaks, scl_troughs )) )

    for i in range(len(val[0,:])):

        if ( val[:,i].max() - val[:,i].min() ) < threshold:
            peak_lags[i] = np.nan
            trough_lags[i] = np.nan
            continue

        obs_peaks, __ = find_peaks(val[:,i])
        obs_troughs, __ = find_peaks(-val[:,i])
        obs_tps = np.sort( np.hstack(( obs_peaks, obs_troughs )) )
        if not can_lead:
            obs_tps = obs_tps[ np.where( obs_tps >= scl_tps[0] ) ]

        obs_tps_attached = np.zeros( len(obs_tps), dtype=int )
        obs_lag_time = np.zeros( len(obs_tps), dtype=int )

        for j,tp in enumerate(obs_tps):
            if j > len(scl_tps)-1:
                continue
            obs_tps_attached[j] = scl_tps[j]
            obs_lag_time[j] = time[tp] - time[scl_tps[j]]

        peak_lags_i = []
        trough_lags_i = []

        for k,tp in enumerate(obs_tps_attached):

            if obs_lag_time[k] != 0.:
                if any(scl_peaks == tp):
                    peak_lags_i.append( obs_lag_time[k].copy() )
                else:
                    trough_lags_i.append( obs_lag_time[k].copy() )

        if len(peak_lags_i) > 1:
            peak_lags[i] = np.array(peak_lags_i[1:]).mean()
        else:
            peak_lags[i] = np.nan

        if len(trough_lags_i) > 1:
            trough_lags[i] = np.array(trough_lags_i[1:]).mean()
        else:
            trough_lags[i] = np.nan

        tps.append( obs_tps )

    if period:
        for i in range(1,len(val[0,:])):
            while (peak_lags[i] - peak_lags[i-1]) > 0.5*period:
                peak_lags[i] -= period
            while (trough_lags[i] - trough_lags[i-1]) > 0.5*period:
                trough_lags[i] -= period
        for i in range(len(val[0,:])-2,-1,-1):
            while (peak_lags[i] - peak_lags[i+1]) > 0.5*period:
                peak_lags[i] -= period
            while (trough_lags[i] - trough_lags[i+1]) > 0.5*period:
                trough_lags[i] -= period

    if full:
        return {'plags': peak_lags, 'tlags': trough_lags, 'obs_tps': tps, 'scl_tps': scl_tps, 'scl_p': scl_peaks, 'scl_t': scl_troughs}
    else:
        return (peak_lags + trough_lags)/2.

# ---- Load expected lengths
arr = np.loadtxt("./expected_length/expected_lengths.dat")
magnitudes = arr[:,0]
expected_lengths = arr[:,1]


# ---- Linear part
L = 100.e3
mean_Q = 10.
mean_Qs = 0.001
B = 98.1202038813591
S0 = (mean_Qs / (0.040987384904837776 * mean_Q))**(6./7.)
lp = LongProfile()
lp.basic_constants()
lp.bedload_lumped_constants()
lp.set_hydrologic_constants()
lp.set_x(x_ext=np.arange(0., L+5.e2, 1.e3))
lp.set_Q(Q=mean_Q)
lp.set_B(B=B)
lp.set_z(S0=-(mean_Qs/(lp.k_Qs*mean_Q))**(6./7.))
lp.set_Qs_input_upstream(mean_Qs)
lp.set_z_bl(0.)
lp.set_uplift_rate(0.)
lp.set_niter()
lp.compute_Q_s()
lp.compute_equilibration_time()


# ---- Unpack network results
indir = "./glic/output_170423/"
# indir = "./glic/output_200423/"
# indir = "./glic/output_210423/"
netdirs = next(os.walk(indir))[1]
hacks = []
nets = []
gains = []
lags = []
for netdir in netdirs:
    with open(indir + netdir + "/hack.obj", "rb") as f:
        hack = pickle.load(f)
        hacks.append(hack)
    with open(indir + netdir + "/props.obj", "rb") as f:
        prop = pickle.load(f)
        net, net_topo = generate_random_network(
            24, 
            prop['L'], 
            prop['B'], 
            prop['Q_mean'], 
            prop['Qs_mean'], 
            evolve=False, 
            topology=prop['topology']
        )
        nets.append(net)
    with open(indir + netdir + "/gain.obj", "rb") as f:
        gain = pickle.load(f)
        gains.append(gain)
    with open(indir + netdir + "/lag.obj", "rb") as f:
        lag = pickle.load(f)
        lags.append(lag)



# ---- evolve
i=2
nets[i].evolve_threshold_width_river_network(nt=1000, dt=3.15e10)
for seg in nets[i].list_of_LongProfile_objects: seg.compute_Q_s()

period = lp.equilibration_time/100.

neti = copy.deepcopy(nets[i])

z, Qs, time, scale = evolve_network_periodic(neti, period, 0.2, 0.)
z_gain = compute_network_z_gain(neti, z, 0.2, 0., S0)
Qs_gain = compute_network_Qs_gain(neti, Qs, 0.2, 0., [q[0,:] for q in Qs])
z_lag = find_network_lag(neti, z, time, scale, period)
Qs_lag = find_network_lag(neti, Qs, time, scale, period)

for j,seg_l in enumerate(z_lag):
    if (seg_l > 1).any():
        print(j)
    plt.plot(neti.list_of_LongProfile_objects[j].x/1000., seg_l)
plt.show()

