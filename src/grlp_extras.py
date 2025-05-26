# ---- Import packages
import numpy as np
import scipy.signal as sig
import os
import pickle
import grlp
import copy
from scipy.optimize import minimize

# ---- Functions

def find_lag_time(forcing, response, time, period, can_lead=False):
    """
    Find lag time between a forcing and a response (quasi-sinusoidal) time
    series.
    
    Pairs peaks and troughs in the two time series and measures average time
    between them. If one or fewer pairs are identified, nan is returned. 
    Negative lag (i.e. leading of the response over the forcing) is allowed,
    but nan is returned if the measured lag is below negative one quarter of the
    specified period; this result implies peaks/troughs in the response time
    series before the beginning of the time series, usually meaning something
    has gone wrong (e.g. too many response peaks/troughs identified).
    
    Parameters
    ----------
    forcing : np.ndarray
        Values for the forcing time series.
    response : np.ndarray
        Values for the response time series.
    time : np.ndarray
        Time array for the two time series.
    period : np.ndarray
        The period of the two (quasi-sinusoidal) time series.
    can_lead : bool
        Whether or not the response should be allowed to lead the forcing
        (i.e. whether negative lag times are allowed/expected).
        
    Returns
    -------
    lag_time : float
        The measured lag time.
    """
    
    # ---- Identify peaks and troughs in forcing
    # Use scipy's find_peaks function to find peaks and troughs separately,
    # then combine to give all turning points.
    forcing_peaks, __ = sig.find_peaks(forcing)
    forcing_troughs, __ = sig.find_peaks(-forcing)
    forcing_tps = np.sort( np.hstack(( forcing_peaks, forcing_troughs )) )

    # ---- Identify peaks and troughs in response
    # Use scipy's find_peaks function to find peaks and troughs separately,
    # then combine to give all turning points.
    # Sometimes lag times are systematically different for peaks compared to
    # troughs. We want to average across this difference, so we make sure we
    # use an equal number of peaks and troughs.
    response_peaks, __ = sig.find_peaks(response)
    response_troughs, __ = sig.find_peaks(-response)
    min_tps = min(len(response_peaks), len(response_troughs))
    response_tps = np.sort(
        np.hstack(( response_peaks[:min_tps], response_troughs[:min_tps] )) 
        )

    # ---- Check whether turning points in response preceed those in forcing
    # Sometimes we get turning points at the very beginning of the time series
    # due to small numerical effects or transient parts of the response. These
    # mess up our measurement. But sometimes we turning points in the response
    # before those in the forcing that are real. This is difficult to deal with
    # so we include the "can_lead" flag. For scenarios where the user does not
    # expect the response to lead the forcing, they can impose that.
    if not can_lead:
        response_tps = response_tps[np.where( response_tps >= forcing_tps[0] )]    

    # ---- Attach response TPs to forcing TPs, measure lag
    # Loop over turning points, compare turning point i in forcing to turning
    # point i in response; measure time difference.
    # We can only compute a lag time if we have both a forcing and a response
    # peak.
    lag_times = np.zeros( min(len(response_tps), len(forcing_tps)), dtype=int )
    for i in range(len(lag_times)):
        lag_times[i] = time[response_tps[i]] - time[forcing_tps[i]]

    # ---- Average the lag times
    # We ignore the first two turning points, which can be influenced by
    # transient parts of the response. We also want to average at least one
    # peak and one trough. So we need at least four points; otherwise we return
    # nan.
    if len(lag_times) > 3:
        lag_time = np.array(lag_times[2:]).mean()
    else:
        lag_time = np.nan

    # ---- Check the lag time is physically plausible
    # Assuming the forcing is (quasi-)sinusoidal, a lag time less than negative
    # one quarter of the forcing period implies peaks/troughs before the
    # start of the time series. This usually points to something going wrong,
    # e.g. noise in the response being picked up as peaks and troughs. So
    # we also return nan in that case. We use a cut-off of -0.3*period to allow
    # for some noise.
    if lag_time < -0.3*period:
        lag_time = np.nan

    return lag_time


def find_along_stream_lag_times(forcing, response, time, period, can_lead=False):
    """
    Find lag time between a forcing and a set of response (quasi-sinusoidal)
    time series along stream.
    
    Uses fing_lag_times() to measure lag times for the individual time series.
    Then looks for cycle skipping along stream. Jumps of more than half a
    period between nodes are assumed to be cycle skipping. In this case,
    lag times are adjusted by one period at a time until jumps do not exceed
    half a period.
    
    Parameters
    ----------
    forcing : np.ndarray
        Values for the forcing time series.
    response : np.ndarray
        Values for the response time series. Dimensions expected to be
        (len(time), N), for N points along stream.
    time : np.ndarray
        Time array for the two time series.
    period : np.ndarray
        The period of the two (quasi-sinusoidal) time series.
        
    Returns
    -------
    lag_times : np.ndarray
        Lag times for each point along stream.
    """
    
    # ---- Measure lags for each point along stream
    lag_times = np.zeros( len(response[0,:]) )
    for i in range(len(response[0,:])):
        lag_times[i] = find_lag_time(
            forcing,
            response[:,i],
            time,
            period,
            can_lead=can_lead)

    # ---- Deal with NaNs
    # Sections that have nans on both sides cannot be reliably corrected for
    # cycle skipping (which involves checking difference between lag times of
    # adjacent nodes). We therefore also set such sections to nan.
    nans = np.where(np.isnan(lag_times))[0]
    for i in range(len(lag_times)):
        if np.isnan(lag_times[:i]).any() and np.isnan(lag_times[i+1:]).any():
            lag_times[i] = np.nan

    # ---- Check for cycle skipping
    # Move from upstream end downstream, then from downstream end upstream,
    # looking for jumps in lag time of more than half about half a period. We
    # use 0.25*period as a threshold because some difference is expected from
    # node to node. If identified, correct by subtracting period until jump is
    # removed. We adjust the relevent node and all preceeding nodes (back to
    # the last nan).
    nans = np.where(np.isnan(lag_times))[0]
    if period:
        for i in range(1,len(response[0,:])):
            while lag_times[i] - lag_times[i-1] > 0.4*period:
                up_nans = nans[nans > i]
                if up_nans.size > 0:
                    next_nan = up_nans[0]
                else:
                    next_nan = len(lag_times)
                lag_times[i:next_nan] -= 0.5*period
        for i in range(len(response[0,:])-2,-1,-1):
            while lag_times[i] - lag_times[i+1] > 0.4*period:
                down_nans = nans[nans < i]
                if down_nans.size > 0:
                    next_nan = down_nans[-1]
                else:
                    next_nan = 0
                lag_times[next_nan:i+1] -= 0.5*period

    return lag_times

def compute_power_law_coefficient(mean, p, L, x0):
    """
    Compute power law coefficient needed to obtain specified mean for given
    exponent, length, and intial value.
    
    Parameters
    ----------
    mean : float
        The desired mean value of the power law.
    p : float
        The power law exponent.
    L : float
        The length of the domain.
    x0 : float
        The initial value of the domain.
        
    Returns
    -------
    The coefficient value.
    """
    return mean * L * (p+1.) / ((L+x0)**(p+1.) - x0**(p+1.))

def generate_single_segment_network(L, Q_mean, Qs_mean, B_mean, p_Q, p_B,
    x0=10.e3, dx=1.e3, evolve=True):
    """
    Set up a single segment GRLP network.
    
    Uses power laws to set variation in water discharge and valley width.
    Sediment discharge is set to vary along stream to balance variation in
    water discharge. Specify desired mean values and power-law exponent.
    Optionally evolve the network for a while, aiming for steady state.
    
    Parameters
    ----------
    L : float
        Desired segment length.
    Q_mean : float
        Desired mean water discharge.
    Qs_mean : float
        Desired mean sediment discharge.
    B_mean : float
        Desired mean valley width.
    p_Q : float
        Desired power-exponent for water discharge.
    p_B : float
        Desired power-exponent for valley width.
    x_0 : float
        Distance downstream at the value inlet. Only used to set inlet water,
        sediment and width values; the x-domain of the network object starts at
        0.
    dx : float
        Desired spatial node spacing.
    evolve : bool
        If true, evolve the network for a while, aiming for steady state.
        
    Returns
    -------
    net : grlp.Network
        The network object.
    """
    
    # ---- Set up a basic long profile object to access constants
    lp = grlp.LongProfile()
    lp.basic_constants()
    lp.bedload_lumped_constants()
    lp.set_hydrologic_constants()
    
    # ---- Set up the x domain
    # x_ext needed to set SSD term (see below).
    x = np.arange(0,L,dx)
    x_ext = np.arange(-dx,L+dx,dx)

    # ---- Set up water discharge
    # Q_ext is needed to set SSD term (see below). We set outer nodes of Q_ext
    # to the same values of the inlet/outlet nodes, to avoid artefacts from
    # outside the domain.
    k_x_Q = compute_power_law_coefficient(Q_mean, p_Q, L, x0)
    Q = k_x_Q * ((x+x0)**p_Q)
    Q_ext = k_x_Q * ((x_ext+x0)**p_Q)
    Q_ext[0] = Q_ext[1]
    Q_ext[-1] = Q_ext[-2]
    
    # ---- Set up valley width
    k_x_B = compute_power_law_coefficient(B_mean, p_B, L, x0)
    B = k_x_B*((x+x0)**p_B)

    # ---- Set up source-sink-distributed term.
    # Internal source of sediment. Sediment supply per unit distance along
    # stream and per unit valley width. To balance effects of variation in
    # water discharge, set to derivative of water discharge.
    ssd = (
        (Q_ext[2:] - Q_ext[:-2])/(x_ext[2:] - x_ext[:-2]) / 
        (B * (1.-lp.lambda_p)) / 
        (Q_mean/Qs_mean)
        )

    # ---- Set initial slope
    S0=(Qs_mean/(lp.k_Qs * Q_mean))**(6./7.)

    # ---- Initialize the Network object
    net = grlp.Network()
    net.initialize(
        config_file = None,
        x_bl = L,
        z_bl = 0.,
        S0 = [S0],
        upstream_segment_IDs = [[]],
        downstream_segment_IDs = [[]],
        x = [x],
        z = [(L-x)*S0],
        Q = [Q],
        B = [B],
        overwrite = False
        )
    net.set_niter(3)
    net.get_z_lengths()
    net.list_of_LongProfile_objects[0].set_source_sink_distributed(ssd)


    # ---- Optionally evolve for a while, aiming for steady state
    if evolve:
        net.evolve_threshold_width_river_network(nt=100, dt=3.15e11)
    
    # ---- Compute Qs (hence slope), and estimate equilibration_time
    for seg in net.list_of_LongProfile_objects:
        seg.compute_Q_s()
    net.list_of_LongProfile_objects[0].compute_equilibration_time()
    
    return net

def evolve_network(net, time, Qs_scale, Q_scale, S_scale):
    """
    Evolve a network object through time.
    
    Takes time series of scaling factors for sediment supply, water supply and
    inlet slope, and evolves the network accordingly. Returns time series of
    elevation and sediment discharge.
    
    Parameters
    ----------
    net : grlp.Network
        Network object to evolve.
    time : np.ndarray
        Time array.
    Qs_scale : nd.array
        Values by which to scale the initial sediment supply through time.
    Q_scale : nd.array
        Values by which to scale the initial water supply through time.
    S_scale : nd.array
        Values by which to scale the initial inlet slope through time.
        
    Returns
    -------
    z : list of np.ndarrays
        List of arrays of elevation through time and space, one for each
        segment, each with dimensions (len(time), N), where N is number of
        spatial nodes in the segment.
    Qs : list of np.ndarrays
        List of arrays of sediment discharge through time and space, one for
        each segment, each with dimensions (len(time), N), where N is number of
        spatial nodes in the segment.
    """
    
    # ---- Set up arrays for output
    z = [np.zeros(( len(time), len(seg.z) ))
            for seg in net.list_of_LongProfile_objects]
    Qs = [np.zeros(( len(time), len(seg.Q_s) ))
            for seg in net.list_of_LongProfile_objects]

    # ---- Initial sediment and water supplies
    S0 = net.list_of_LongProfile_objects[
        net.list_of_channel_head_segment_IDs[0]
        ].S0
    Q0 = [np.zeros(len(seg.Q)) for seg in net.list_of_LongProfile_objects]
    dQ0 = [seg.dQ_up_jcn for seg in net.list_of_LongProfile_objects]
    for seg in net.list_of_LongProfile_objects:
        Q0[seg.ID] = seg.Q.copy()
    ssd0 = [seg.ssd.copy() for seg in net.list_of_LongProfile_objects]

    # ---- Loop over time, evolve the network and record its state
    for i,t in enumerate(time):
        
        # Skip the first entry
        if i > 1:
            
            # Time step
            dt = time[i] - time[i-1]
        
            # Update the source-sink-distributed term
            for seg in net.list_of_LongProfile_objects:
                seg.set_source_sink_distributed(ssd0[seg.ID] * Qs_scale[i])

            # Update the water discharges
            new_Q = [
                Q0[j] * Q_scale[i]
                for j in range(len(net.list_of_LongProfile_objects))
                ]
            net.update_Q(new_Q)
            for seg in net.list_of_LongProfile_objects:
                seg.dQ_up_jcn = [dQ*Q_scale[i] for dQ in dQ0[seg.ID]]
            net.create_Q_ext_lists()
            net.update_Q_ext_from_Q()
            net.update_Q_ext_internal()
            net.update_Q_ext_external_upstream()
            net.update_Q_ext_external_downstream()
            net.update_dQ_ext_2cell()

            # Update the sediment supplies
            net.update_z_ext_external_upstream(
                S0 = np.full(
                    len(net.list_of_channel_head_segment_IDs), 
                    S0 * S_scale[i]
                    ) 
                )
            
            # Evolve the network
            net.evolve_threshold_width_river_network(nt=1, dt=dt)
        
        # Save elevations and sediment discharges
        for seg in net.list_of_LongProfile_objects:
            z[seg.ID][i,:] = seg.z.copy()
            seg.compute_Q_s()
            Qs[seg.ID][i,:] = seg.Q_s.copy()
            
    return z, Qs

def evolve_network_periodic(net, period, A_Qs, A_Q, nperiods=4):
    """
    Evolve a network with periodic variation in sediment and/or water supply.
    
    Given a forcing period, number of periods for which to evolve, and scaling
    amplitudes for sediment and water supply, evolves the network using
    evolve_network(). Also computes elevation gain and lag throughout the
    network, and sediment-discharge gain and lag at the network outlet.
    
    Parameters
    ----------
    net : grlp.Network
        Network object to evolve.
    period : float
        The forcing period to use.
    A_Qs : float
        The scaling amplitude for sediment supply. Should be a value between
        0 and 1.
    A_Q : float
        The scaling amplitude for water supply. Should be a value between
        0 and 1.
    nperiods : int
        The number of periods for which to evolve.
        
    Returns
    -------
    A dictionary containing: 'z' and 'Qs', lists of arrays containing time
    series of elevation and sediment discharge for each network segment; 'time',
    an array of times at which elevation and sediment discharge are recorded;
    'Qs_scale', 'Q_scale' and 'S_scale', time series of scaling factors for
    sediment supply, water supply and inlet slope; 'G_z' and 'lag_z', lists of
    arrays of elevation gain and lag for each network segment; 'G_Qs' and
    'lag_Qs', values of sediment-discharge gain and lag at the network outlet.
    """
    
    # ---- Set up time domain
    time = np.linspace(0., period*nperiods, 1000*nperiods)
    Qs_scale = 1 + A_Qs*np.sin(2. * np.pi * time / period)
    Q_scale = 1 + A_Q*np.sin(2. * np.pi * time / period)
    S_scale = (Qs_scale/Q_scale)**(6./7.)
    
    # ---- Evolve
    z, Qs = evolve_network(net, time, Qs_scale, Q_scale, S_scale)
    
    # ---- Compute gains
    # To avoid transient effects, we focus on the second half of the time
    # series.
    G_z = compute_network_gain([zi[2000:,:] for zi in z], max([A_Qs, A_Q]))
    G_Qs = compute_network_gain([Qsi[2000:,:] for Qsi in Qs], max([A_Qs, A_Q]))
    
    # ---- Compute lags
    # We scale the lag time by the forcing period before returning.
    # If forcing with water discharge, Qs signal could lead the forcing.
    lag_z = [
        l/period 
        for l in find_network_lag_times(net, z, time, S_scale, period)
        ]
    if A_Q > 0.:
        can_lead=True
    else:
        can_lead=False
    lag_Qs = find_lag_time(S_scale, Qs[0][:,-1], time, period, can_lead)/period

    return {'z': z, 'Qs': Qs, 'time': time, 'Qs_scale': Qs_scale,
        'Q_scale': Q_scale, 'S_scale': S_scale, 'G_z': G_z, 'G_Qs': G_Qs, 
        'lag_z': lag_z, 'lag_Qs': lag_Qs}

def compute_network_gain(prop, A_forcing):
    """
    Compute gain for a network property (e.g. elevation or sediment discharge).
    
    Gain is defined as the ampltitude of the property time series divided by
    the imposed forcing amplitude and the property mean.
    
    Properties
    ----------
    prop : list of np.ndarrays
        List of arrays of property time series for each segment. Arrays should
        have dimensions (len(time), N), where N is number of spatial nodes in
        the segment.
    A_forcing : float
        The imposed forcing amplitude.
        
    Returns
    -------
    gain : list of np.ndarrays
        List of arrays of gain for each segment. Arrays will have length N.
    """
    
    # ---- Set up the list to save gain results
    gain = [np.zeros(len(p[:,0])) for p in prop]
    
    # ---- Loop over segments, compute gain
    for i,propi in enumerate(prop):
        A_prop = (propi.max(axis=0) - propi.min(axis=0)) / 2.
        gain[i] = A_prop / (A_forcing*propi.mean(axis=0))
        
    return gain

def find_network_lag_times(net, prop, time, forcing, period, can_lead=False):
    """
    Compute lag for a network property (e.g. elevation or sediment discharge).
    
    Uses the function find_along_stream_lag_times() to compute lag along each
    of the network segments. Then additionally looks for cycle skipping at
    the junctions between segments. Jumps of more than half a period between
    segments are assumed to be cycle skipping. In this case, lag times are
    adjusted by one period at a time until jumps do not exceed half a period.
    
    Parameters
    ----------
    net : grlp.Network
        Network object to evolve.
    prop : list of np.ndarrays
        List of arrays of property time series for each segment. Arrays should
        have dimensions (len(time), N), where N is number of spatial nodes in
        the segment.
    time : np.ndarray
        The times corresponding to property time series.
    forcing : np.ndarray
        The forcing time series to compare with.
    period : np.ndarray
        The forcing period.
        
    Returns
    -------
    lag_times : list of np.ndarrays
        List of arrays of lag for each segment. Arrays will have length N.
    """
    
    def first_nan_last_nan(arr):
        """
        Check array for nans and return first and last occurence.
        """
        nans = np.where(np.isnan(arr))[0]
        if nans.any():
            first_nan = nans[0]
            last_nan = nans[-1]
        else:
            first_nan = len(arr)
            last_nan = -1
        return first_nan, last_nan
    
    def move_upstream(net, segID):
        """
        Move recursively upstream from a given segment checking for big jumps
        between segments and correcting.
        """
        
        # ---- Extract segment
        seg = net.list_of_LongProfile_objects[segID]
    
        # ---- Loop over upstream segments, if there are any
        if seg.upstream_segment_IDs:
            for upID in seg.upstream_segment_IDs:
    
                # Check for nans.
                first_nan, last_nan = first_nan_last_nan(LAG_TIMES[upID])
    
                # Correct any cycle skipping.
                while LAG_TIMES[upID][-1]-LAG_TIMES[segID][0] > 0.4*period:
                    LAG_TIMES[upID][last_nan+1:] -= 0.5*period
                while LAG_TIMES[upID][-1]-LAG_TIMES[segID][0] < -0.4*period:
                    LAG_TIMES[upID][last_nan+1:] += 0.5*period
    
                # Update corrected segments.
                CHECKED[upID][last_nan+1:] = True
    
                # If no nans present, we continue upstream.
                # NaNs mean we cannot determine whether jumps occur in the lag
                # times, so we cannot reliably check for cycle skipping.
                if not np.isnan(LAG_TIMES[upID]).any():
                    move_upstream(net, upID)
    
    def move_downstream(net, segID):
    
        # ---- Extract segment
        seg = net.list_of_LongProfile_objects[segID]
    
        # ---- If the upstream point is not NaN, we start working upstream
        if not np.isnan(LAG_TIMES[segID][0]):
            move_upstream(net, segID)
    
        # ---- If there are any NaNs, we stop moving downstream
        if not np.isnan(LAG_TIMES[segID]).any():
    
            # Check there is something downstream
            if seg.downstream_segment_IDs:
    
                # Identify downstream segment
                downID = seg.downstream_segment_IDs[0]
    
                # Check for NaNs.
                first_nan, last_nan = first_nan_last_nan(LAG_TIMES[downID])
    
                # Correct any cycle skipping.
                while LAG_TIMES[downID][0]-LAG_TIMES[segID][-1] > 0.4*period:
                    LAG_TIMES[downID][:first_nan] -= 0.5*period
                while LAG_TIMES[downID][0]-LAG_TIMES[segID][-1] < -0.4*period:
                    LAG_TIMES[downID][:first_nan] += 0.5*period
    
                # Update checked record.
                CHECKED[downID][:first_nan] = True
    
                # Continue downstream.
                move_downstream(net, downID)

    # ---- First attempt to compute lag times along each segment
    lag_times = [
        np.zeros(len(seg.x)) for seg in net.list_of_LongProfile_objects
        ]
    for seg in net.list_of_LongProfile_objects:
        lag_times[seg.ID] = find_along_stream_lag_times(
            forcing,
            prop[seg.ID],
            time,
            period,
            can_lead=can_lead
            )
            
    # ---- Create global-ish variables for use in cycle skipping functions
    # We create the "CORRECTED" list of arrays to keep track of which nodes
    # we have been able to connect back to a channel head. Those that are
    # surrounded by NaNs cannot be checked and will be set to NaN at the end.
    LAG_TIMES = copy.deepcopy(lag_times)
    CHECKED = [np.full(len(seg.x), False)
        for seg in net.list_of_LongProfile_objects]
    
    # ---- Work downstream from each channel head
    # We assume that the lag at the channel heads is small (i.e. less than
    # half a forcing period). Then we work through the network from each head
    # (first downstream then also upstream from downstream nodes). If we
    # encounter NaNs, we stop.
    for segID in net.list_of_channel_head_segment_IDs:
    
        # Extract segment.
        seg = net.list_of_LongProfile_objects[segID]
    
        # Check for NaNs.
        first_nan, last_nan = first_nan_last_nan(LAG_TIMES[segID])
    
        # First force all channel heads to have positive lag.
        # Thinking mainly about z here.
        # If applied with Qs, maybe negative lag is possible...
        while LAG_TIMES[segID][0] < 0.:
            LAG_TIMES[segID][:first_nan] += 0.5*period
    
        # Also force all channel heads to have lag below 0.5.
        # For the scenarios we test, do not expect such long lag times at the
        # inlet. So longer lags indicate cycle skipping.
        while LAG_TIMES[segID][0] > 0.5*period:
            LAG_TIMES[segID][:first_nan] -= 0.5*period
    
        # Updated checked record
        CHECKED[segID][:first_nan] = True
    
        # Start working downstream
        move_downstream(net, segID)
    
    # ---- Set sections that couldn't be checked to NaN
    for segID in range(len(net.list_of_LongProfile_objects)):
        LAG_TIMES[segID][~CHECKED[segID]] = np.nan
    
    # ---- Finished!
    return LAG_TIMES
    
def find_network_equilibration_time(net_gain, periods, single_seg_net):
    """
    Estimate a network's equilibration time.
    
    Works by comparing the network's outlet sediment-discharge gain as a
    function of forcing period to that predicted for a single segment network.
    We seek the network equilibration time that minimises the difference
    between gains for the network and the single as a function, once period has
    been scaled by their respective equilibration times.
    
    Parameters
    ----------
    net_gain : np.ndarray
        Sediment-discharge gain at the network outlet as a function of forcing
        period.
    periods : np.ndarray
        The periods at which gain is calculated.
    single_seg_net : grlp.Network
        Single segment network object to compare against.
        
    Returns
    -------
    net_Teq : float
        The estimated network equilibration time.
    """
    
    # ---- Define a misfit function
    # The function takes an estimate of a scaling between the single segment
    # equilibration time and network equilibration time; computes the
    # corresponding gain for the single segment case; and calculates a
    # root-mean-square misfit between the network and single segment gain.
    
    def gain_misfit(Teq_scale, net_gain, periods, single_seg_net):
        
        # Get the equilibration time of the single segment network
        lp = single_seg_net.list_of_LongProfile_objects[0]
        
        # Scale to get the estimate of network equilibration time to test
        net_Teq = Teq_scale * lp.equilibration_time
        
        # Compute the gain for the single segment case.
        # We compute gain at a set of periods such that the scaled periods
        # (period/equilibraton time) match the scaled network periods for this
        # estimate of network equilibration time.
        lin_gain = [
            lp.compute_Qs_gain(p, A_Qs=0.2)[-1]
            for p in periods / lp.equilibration_time * net_Teq
            ]
        
        # Compute the RMS misfit between the network and single segment gains.
        misfit = np.sqrt(
            (1./len(net_gain)) * sum((np.array(net_gain) - lin_gain)**2.)
            )
        return misfit
    
    # ---- Optimize the misfit function
    # Gives us the scaling between the single segment and network equilibration
    # times. Initial guess (1) that the two have the same equilibration time.
    fit = minimize(
        fun=gain_misfit, 
        x0=1.,
        args=(net_gain,periods,single_seg_net,)
        )
    
    # ---- Unscale the result
    # Use the optmized result to scale the single segment equilibration time to
    # the network equilibration time.
    net_Teq = (
        single_seg_net.list_of_LongProfile_objects[0].equilibration_time /
        fit.x[0]
        )
        
    return net_Teq

def read_MC(indir, cases=None, toread=['nets', 'hacks', 'gains', 'lags']):
    """
    Read and unpack the results of a Monte Carlo simulation.
    """
    
    # Get list of topology directories.
    topodirs = next(os.walk(indir))[1]

    # Set up lists for output.
    out = {}
    for data in toread:
        out[data] = []
    
    # Loop over topology directories.
    for topodir in topodirs:
        
        # If cases not specified, get list from directory.
        if cases is None:
            cases = next(os.walk(indir + topodir))[1]
        
        for data in toread:
            out[data].append({})
                
        # Loop over networks.
        for case in cases:
            
            # Read the Hack object.
            if 'hacks' in toread:
                with open(indir + topodir + "/" + case + "/hack.obj", "rb") as f:
                    out['hacks'][-1][case] = pickle.load(f)
            
            # Read the network properties and create network instance.
            if 'nets' in toread:
                with open(indir + topodir + "/" + case + "/props.obj", "rb") as f:
                    props = pickle.load(f)
                    out['nets'][-1][case] = grlp.Network()
                    out['nets'][-1][case].initialize(
                        config_file = None,
                        x_bl = props['x_bl'],
                        z_bl = props['z_bl'],
                        S0 = props['S0'],
                        upstream_segment_IDs = props['upstream_segment_IDs'],
                        downstream_segment_IDs = props['downstream_segment_IDs'],
                        x = props['x_ls'],
                        z = props['z_ls'],
                        Q = props['Q_ls'],
                        dQ = props['dQ_ls'],
                        B = props['B_ls'],
                        overwrite = False
                        )
                    out['nets'][-1][case].set_niter(3)
                    out['nets'][-1][case].get_z_lengths()
                    for i,seg in enumerate(
                        out['nets'][-1][case].list_of_LongProfile_objects
                        ):
                        seg.set_source_sink_distributed(props['ssd_ls'][i])
                    for seg in out['nets'][-1][case].list_of_LongProfile_objects:
                        seg.compute_Q_s()
                    out['nets'][-1][case].compute_network_properties()

            
            # Read the gain object.
            if 'gains' in toread:
                with open(indir + topodir + "/" + case + "/gain.obj", "rb") as f:
                    out['gains'][-1][case] = pickle.load(f)
            
            # Read the lag object.
            if 'lags' in toread:
                with open(indir + topodir + "/" + case + "/lag.obj", "rb") as f:
                    out['lags'][-1][case] = pickle.load(f)
        
        out_ls = []
        for data in toread:
            out_ls.append(out[data])
        
    return out_ls