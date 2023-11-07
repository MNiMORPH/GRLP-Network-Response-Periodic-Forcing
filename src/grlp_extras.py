from grlp import *
from scipy.signal import find_peaks


def compute_coeff_internal_external(lp, A_Q=0., A_Qs=0., A_Qs_i=0.):
    
    internal = A_Qs_i * (lp.Q_s[-1] - lp.Q_s[0])/lp.L
    internal += A_Q*lp.k_Qs*((lp.Q[-1]-lp.Q[0])/lp.L)*((lp.z[0]-lp.z[-1])/lp.L)**(7./6.)
    internal *= lp.L
    
    external = lp.k_Qs * lp.Q.mean() * (lp.S.mean()**(7./6.)) * abs(A_Q - A_Qs)
    
    coeff = internal / external 
    
    return coeff

def find_lag_times_x_corr(val, scale, time, period):
    lags = np.zeros(val.shape[1])
    dt = np.linspace(-time[-1], time[-1], 2*len(time)-1)
    for i in range(val.shape[1]):
        x_corr = np.correlate(
            (scale - scale.mean())/scale.std(), 
            (val[:,i] - val[:,i].mean())/val[:,i].std(),
            "full")
        lags[i] = -dt[x_corr.argmax()]
        
    for i in range(1,len(val[0,:])):
        if (lags[i] - lags[i-1]) > 0.5*period:
            lags[i:] -= period
    for i in range(len(val[0,:])-2,0,-1):
        if (lags[i] - lags[i+1]) > 0.5*period:
            lags[:i+1] -= period
            
    if abs(lags[0])/period > 0.5:
        lags -= np.sign(lags[0])*period
            
    return lags
        

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
        for i in range(len(val[0,:])-2,0,-1):
            while (peak_lags[i] - peak_lags[i+1]) > 0.5*period:
                peak_lags[i] -= period
            while (trough_lags[i] - trough_lags[i+1]) > 0.5*period:
                trough_lags[i] -= period

    if full:
        return {'plags': peak_lags, 'tlags': trough_lags, 'obs_tps': tps, 'scl_tps': scl_tps, 'scl_p': scl_peaks, 'scl_t': scl_troughs}
    else:
        return (peak_lags + trough_lags)/2.


def compute_power_law_coefficient(mean, p, L, x0):
    return mean * L * (p+1.) / ((L+x0)**(p+1.) - x0**(p+1.))

def set_up_long_profile(L, mean_Qw, mean_Qs, p, B, x0=10.e3, dx=1.e3, evolve=True):
    
    # initial set up
    lp = LongProfile()
    lp.basic_constants()
    lp.bedload_lumped_constants()
    lp.set_hydrologic_constants()
    lp.set_x(x_ext=np.arange(0., L+dx, dx))
    lp.set_B(B=B)
    lp.set_uplift_rate(0.)
    lp.set_niter(3)
    
    # Qw
    k_x_Qw = compute_power_law_coefficient(mean_Qw, p, L, x0)
    Qw = k_x_Qw*((lp.x+x0)**p)
    lp.set_Q(Q=Qw)
    
    # Qs
    k_x_Qs = compute_power_law_coefficient(mean_Qs, p, L, x0)
    ssd = p * k_x_Qs * (lp.x+x0)**(p-1.) / (B * (1. - lp.lambda_p))
    lp.set_source_sink_distributed(ssd)

    # z
    lp.set_z(S0=(mean_Qs/(lp.k_Qs * mean_Qw))**(6./7.))
    # lp.set_z_bl(0.)
    lp.set_Qs_input_upstream(k_x_Qs * (x0**p))

    if evolve:
        lp.evolve_threshold_width_river(nt=10000, dt=3.15e10)
    lp.compute_Q_s()
    
    # properties
    lp.compute_equilibration_time()
    
    return lp

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
    S0 = net.list_of_LongProfile_objects[net.list_of_channel_head_segment_IDs[0]].S0
    Qw0 = [np.zeros(len(seg.Q)) for seg in net.list_of_LongProfile_objects]
    for seg in net.list_of_LongProfile_objects:
        Qw0[seg.ID] = seg.Q.copy()
    
    # ---- Evolve
    for i,s in enumerate(scale):
        # for seg in net.list_of_LongProfile_objects:
        #     seg.set_Q(Qw0[seg.ID] * (1. + A_Q*s))
        #     if seg.ID in net.list_of_channel_head_segment_IDs:
                # seg.set_Qs_input_upstream(S0 * ((1. + A_Qs*s)**(6./7.)))
        net.update_z_ext_external_upstream( S0 = np.full(len(net.list_of_channel_head_segment_IDs), S0 * ((1. + A_Qs*s)**(6./7.))) )
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
                (net.list_of_LongProfile_objects[0].x_ext[0].max() - seg.x) *
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
    for segID in net.list_of_channel_head_segment_IDs:
        while net.list_of_LongProfile_objects[segID].downstream_segment_IDs:
            down_segID = net.list_of_LongProfile_objects[segID].downstream_segment_IDs[0]
            if down_segID not in completed_segs:
                if (lag[down_segID][0] - lag[segID][-1]) > 0.5:
                    lag[down_segID] -= 1.
                completed_segs.append(down_segID)
            segID = down_segID
    
    return lag
    
def find_network_equilibration_time(net_gain, net_periods, lin_net):
    
    def gain_misfit(scaled_Teq, net_gain, net_periods, lin_net):
        Teq = scaled_Teq * lin_net.list_of_LongProfile_objects[0].equilibration_time
        lin_gain = [
            lin_net.list_of_LongProfile_objects[0].compute_z_gain(p)[-1]
            for p in net_periods / lin_net.list_of_LongProfile_objects[0].equilibration_time * Teq
            ]
        misfit = np.sqrt( (1./len(net_gain)) * sum((np.array(net_gain) - lin_gain)**2.) )
        return misfit
    
    fit = minimize(
        fun=gain_misfit, 
        x0=1.,
        args=(net_gain,net_periods,lin_net,))
        
    return lin_net.list_of_LongProfile_objects[0].equilibration_time / fit.x
    
def find_network_equilibration_time_Qs(net_gain, net_periods, lin_net):
    
    def gain_misfit(scaled_Teq, net_gain, net_periods, lin_net):
        Teq = scaled_Teq * lin_net.list_of_LongProfile_objects[0].equilibration_time
        lin_gain = [
            lin_net.list_of_LongProfile_objects[0].compute_Qs_gain(p, A_Qs=0.2)[-1]
            for p in net_periods / lin_net.list_of_LongProfile_objects[0].equilibration_time * Teq
            ]
        misfit = np.sqrt( (1./len(net_gain)) * sum((np.array(net_gain) - lin_gain)**2.) )
        return misfit
    
    fit = minimize(
        fun=gain_misfit, 
        x0=1.,
        args=(net_gain,net_periods,lin_net,))
        
    return lin_net.list_of_LongProfile_objects[0].equilibration_time / fit.x[0]
