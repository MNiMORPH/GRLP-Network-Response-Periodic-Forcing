import numpy as np
import matplotlib.pyplot as plt
import copy as cp

import grlp
import grlp_extras as grlpx


sweep_nets, sweep_hacks, sweep_gains, sweep_lags = grlpx.read_sweep("../output/network/m40_rnd_seg_length_w_internal/")

i = 40
net = cp.deepcopy(sweep_nets[i])
net.evolve_threshold_width_river_network(nt=100, dt=3.154e11)
periodics = grlpx.evolve_network_periodic(
    net=cp.deepcopy(net),
    period=sweep_lags[i]['P'][-1],
    A_Qs=0.,
    A_Q=0.2
    )



# def find_lag_time_single(val, time, scale, threshold=0., can_lead=False):
# 
#     scl_peaks, __ = find_peaks(scale)
#     scl_troughs, __ = find_peaks(-scale)
#     scl_tps = np.sort( np.hstack(( scl_peaks, scl_troughs )) )
# 
#     obs_peaks, __ = find_peaks(val)
#     obs_troughs, __ = find_peaks(-val)
#     obs_tps = np.sort( np.hstack(( obs_peaks, obs_troughs )) )
#     if not can_lead:
#         obs_tps = obs_tps[ np.where( obs_tps >= scl_tps[0] ) ]
# 
#     obs_tps_attached = np.zeros( len(obs_tps), dtype=int )
#     obs_lag_time = np.zeros( len(obs_tps), dtype=int )
# 
#     for j,tp in enumerate(obs_tps):
#         if j > len(scl_tps)-1:
#             continue
#         obs_tps_attached[j] = scl_tps[j]
#         obs_lag_time[j] = time[tp] - time[scl_tps[j]]
# 
#     peak_lags_i = []
#     trough_lags_i = []
# 
#     for k,tp in enumerate(obs_tps_attached):
# 
#         if obs_lag_time[k] != 0.:
#             if any(scl_peaks == tp):
#                 peak_lags_i.append( obs_lag_time[k].copy() )
#             else:
#                 trough_lags_i.append( obs_lag_time[k].copy() )
# 
#     if len(peak_lags_i) > 1:
#         peak_lags = np.array(peak_lags_i[1:]).mean()
#     else:
#         peak_lags = np.nan
# 
#     if len(trough_lags_i) > 1:
#         trough_lags = np.array(trough_lags_i[1:]).mean()
#     else:
#         trough_lags = np.nan
# 
#     average_lag = (peak_lags + trough_lags)/2.
#     if average_lag < -0.25:
#         average_lag = np.nan
# 
#     return average_lag