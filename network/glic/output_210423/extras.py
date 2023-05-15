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
            if (peak_lags[i] - peak_lags[i-1]) > 0.5*period:
                peak_lags[i] -= period
            if (trough_lags[i] - trough_lags[i-1]) > 0.5*period:
                trough_lags[i] -= period
        for i in range(len(val[0,:])-2,0,-1):
            if (peak_lags[i] - peak_lags[i+1]) > 0.5*period:
                peak_lags[i] -= period
            if (trough_lags[i] - trough_lags[i+1]) > 0.5*period:
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
    lp.set_niter()
    
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
    lp.set_z_bl(0.)
    lp.set_Qs_input_upstream(k_x_Qs * (x0**p))

    if evolve:
        lp.evolve_threshold_width_river(nt=10000, dt=3.15e10)
    lp.compute_Q_s()
    
    # properties
    lp.compute_equilibration_time()
    
    return lp
