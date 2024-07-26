import matplotlib.pyplot as plt
import numpy as np

import grlp
import grlp_extras as grlpx

from copy import deepcopy
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap

# initial set up
lp = grlp.LongProfile()
lp.basic_constants()
lp.bedload_lumped_constants()
lp.set_hydrologic_constants()

# ---- Reference properties
x0 = 50.e3
L = 100.e3
p__x_A = 1./0.54 # global mean from He et al. (2024)
k__x_A = 2.1*1.e3/(1.e6**0.55) # global mean from He et al. (2024), converted to m & m^2
P = 1.e3 / 1.e3 / 3.154e7 # precipitation rate in m/s
C_R = 0.4 # runoff coefficient
Qw_mean = P * C_R * k__x_A * ((L+x0)**(p__x_A+1.) - x0**(p__x_A+1.)) / (L * (p__x_A+1.))
Qs_mean = Qw_mean * 1.e-4
Teq = 3.154e12
diffusivity = L**2. / Teq
S0 = (Qs_mean/(lp.k_Qs*Qw_mean))**(6./7.)
B_mean = (7./6.) * (lp.k_Qs * Qw_mean * S0**(1./6.)) / (diffusivity * (1. - lp.lambda_p))
D = 0.1

# ---- grlp object
net_wo_B = grlpx.set_up_long_profile(L, Qw_mean, Qs_mean, B_mean, p__x_A, p__x_A, 0., x0=x0, dx=5.e2, evolve=True)
net_w_B = grlpx.set_up_long_profile(L, Qw_mean, Qs_mean, B_mean, p__x_A, p__x_A, p__x_A, x0=x0, dx=5.e2, evolve=True)

# ---- evolve periodic
periods = np.logspace(-2, 2, 25) * 3.154e12
periodic_wo_B = []
periodic_w_B = []
periodic_wo_B_Qw = []
periodic_w_B_Qw = []
for period in periods:
    print(period/3.154e12)
    periodic_wo_B.append( grlpx.evolve_network_periodic(deepcopy(net_wo_B), period, 0.2, 0.) )
    periodic_w_B.append( grlpx.evolve_network_periodic(deepcopy(net_w_B), period, 0.2, 0.) )
    periodic_wo_B_Qw.append( grlpx.evolve_network_periodic(deepcopy(net_wo_B), period, 0., 0.2) )
    periodic_w_B_Qw.append( grlpx.evolve_network_periodic(deepcopy(net_w_B), period, 0., 0.2) )

# ---- plot
periods_to_plot = [0, 6, 12, 18, 24]

fig, axs = plt.subplots(2, len(periods_to_plot), sharey='row', sharex=True)

for i,p in enumerate(periods_to_plot):

    axs[0,i].plot(
        net_wo_B.list_of_LongProfile_objects[0].x/1000., 
        net_wo_B.list_of_LongProfile_objects[0].compute_z_gain(periods[p]),
        ":")
    axs[0,i].plot(
        net_wo_B.list_of_LongProfile_objects[0].x/1.e3,
        periodic_wo_B[p]['G_z'][0],
        "-."
        )
    axs[0,i].plot(
        net_w_B.list_of_LongProfile_objects[0].x/1.e3,
        periodic_w_B[p]['G_z'][0]
        )
    axs[0,i].set_title(r'$P/T_{eq}$ = %.2f' % (periods[p]/3.154e12))
    if i==0:
        axs[0,i].set_ylabel(r'$G_{z,L}$ [-]')

    axs[1,i].plot(
        net_wo_B.list_of_LongProfile_objects[0].x/1000., 
        net_wo_B.list_of_LongProfile_objects[0].compute_z_lag(periods[p], nsum=1000)/periods[p],
        ":")
    axs[1,i].plot(
        net_wo_B.list_of_LongProfile_objects[0].x/1.e3,
        periodic_wo_B[p]['lag_z'][0],
        "-."
        )
    axs[1,i].plot(
        net_w_B.list_of_LongProfile_objects[0].x/1.e3,
        periodic_w_B[p]['lag_z'][0]
        )
    if i==0:
        axs[1,i].set_ylabel(r'${\varphi}_{z,L}$ [-]')
    axs[1,i].set_xlabel(r'$x$ [km]')

for ax in axs:
    for a in ax:
        a.set_box_aspect(1)
        
axs[1,0].set_ylim(-0.01, 0.41)
plt.show()


lin_periods = np.logspace(-2., 2., 51) * 3.154e12

fig, axs = plt.subplots(2, 3, sharex=True)

axs[0,0].plot(
    lin_periods/3.154e12,
    [net_wo_B.list_of_LongProfile_objects[0].compute_z_gain(p)[-1]
        for p in lin_periods],
    ":")
axs[0,0].plot(
    periods/3.15e12,
    [periodic['G_z'][0][-1] for periodic in periodic_wo_B],
    "-."
    )
axs[0,0].plot(
    periods/3.15e12,
    [periodic['G_z'][0][-1] for periodic in periodic_w_B],
    )
axs[0,0].set_ylabel(r'$G$ [-]')
axs[0,0].set_ylim(-0.05,1.25)
axs[0,0].set_title('$\delta z$')

axs[1,0].plot(
    lin_periods/3.154e12,
    [net_wo_B.list_of_LongProfile_objects[0].compute_z_lag(p, nsum=1000)[-1]/p
        for p in lin_periods],
    ":")
axs[1,0].plot(
    periods/3.15e12,
    [periodic['lag_z'][0][-1] for periodic in periodic_wo_B],
    "-."
    )
axs[1,0].plot(
    periods/3.15e12,
    [periodic['lag_z'][0][-1] for periodic in periodic_w_B],
    )
axs[1,0].set_ylabel(r'$\varphi$ [-]')
axs[1,0].set_xlabel(r'$P / T_{eq}$ [-]')
axs[1,0].set_ylim(-0.01, 0.21)

axs[0,1].plot(
    lin_periods/3.154e12,
    [net_wo_B.list_of_LongProfile_objects[0].compute_Qs_gain(p, A_Qs=0.2)[-1]
        for p in lin_periods],
    ":")
axs[0,1].plot(
    periods/3.15e12,
    [periodic['G_Qs'][0][-1] for periodic in periodic_wo_B],
    "-."
    )
axs[0,1].plot(
    periods/3.15e12,
    [periodic['G_Qs'][0][-1] for periodic in periodic_w_B],
    )
axs[0,1].set_ylim(-0.05,1.25)
axs[0,1].set_title('$\delta Q_s$: $Q_{s,0}$ forcing')

axs[1,1].plot(
    lin_periods/3.154e12,
    [net_wo_B.list_of_LongProfile_objects[0].compute_Qs_lag(p, A_Qs=0.2, nsum=1000)[-1]/p
        for p in lin_periods],
    ":")
axs[1,1].plot(
    periods/3.15e12,
    [periodic['lag_Qs']/periods[p] for p,periodic in enumerate(periodic_wo_B)],
    "-."
    )
axs[1,1].plot(
    periods/3.15e12,
    [periodic['lag_Qs']/periods[p] for p,periodic in enumerate(periodic_w_B)],
    )
axs[1,1].set_xlabel(r'$P / T_{eq}$ [-]')
axs[1,1].set_ylim(-0.01, 0.21)

axs[0,2].plot(
    lin_periods/3.154e12,
    [net_wo_B.list_of_LongProfile_objects[0].compute_Qs_gain(p, A_Q=0.2)[-1]
        for p in lin_periods],
    ":")
axs[0,2].plot(
    periods/3.15e12,
    [periodic['G_Qs'][0][-1] for periodic in periodic_wo_B_Qw],
    "-."
    )
axs[0,2].plot(
    periods/3.15e12,
    [periodic['G_Qs'][0][-1] for periodic in periodic_w_B_Qw],
    )
axs[0,2].set_ylim(-0.05,1.25)
axs[0,2].set_title('$\delta Q_s$: $Q_w$ forcing')

axs[1,2].plot(
    lin_periods/3.154e12,
    [net_wo_B.list_of_LongProfile_objects[0].compute_Qs_lag(p, A_Q=0.2, nsum=1000)[-1]/p
        for p in lin_periods],
    ":")
axs[1,2].plot(
    periods/3.15e12,
    [periodic['lag_Qs']/periods[p] for p,periodic in enumerate(periodic_wo_B_Qw)],
    "-."
    )
axs[1,2].plot(
    periods/3.15e12,
    [periodic['lag_Qs']/periods[p] for p,periodic in enumerate(periodic_w_B_Qw)],
    )
axs[1,2].set_xlabel(r'$P / T_{eq}$ [-]')

axs[0,0].set_xscale('log')

for ax in axs:
    for a in ax:
        a.set_box_aspect(1)
        
plt.show()


period_to_plot = 0
xs_to_plot = [0, 39, 79, 119, 159, 199]

for x in xs_to_plot:
    plt.plot(
        periodic_wo_B[period_to_plot]['time']/3.154e12,
        periodic_wo_B[period_to_plot]['z'][0][:,x]
        )
plt.show()