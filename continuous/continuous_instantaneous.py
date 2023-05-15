from grlp import *
from extras import *
from copy import deepcopy
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap


# ---- River properties
x0 = 10.e3
L = 100.e3
mean_Qw = 10.
mean_Qs = 0.001
B = 98.1202038813591


# ---- Evolve
ps = np.array([0., 0.5, 1., 1.5, 2., 2.5, 3.])
zs = []
Qss = []
ts = []
for p in ps:
    lp = set_up_long_profile(L, mean_Qw, mean_Qs, p, B, dx=1.e2, evolve=True)
    # lp.set_Q(lp.Q * 2.)
    lp.set_Qs_input_upstream(mean_Qs0 * 0.5)
    lp.set_source_sink_distributed(mean_ssd * 0.5)
    lp.compute_diffusivity()
    e_folding = (4. * (lp.L**2.)) / ((np.pi**2.) * lp.diffusivity.mean())
    mean_Qs0 = deepcopy(lp.Q_s_0)
    mean_ssd = deepcopy(lp.ssd)
    mean_ssd_Qs = deepcopy(lp.Q_s)
    print(p, e_folding/3.15e10)
    time, dt = np.linspace(0., 6.*e_folding, 6000, retstep=True)
    z = np.zeros((len(time), len(lp.x)))
    Qs = np.zeros((len(time), len(lp.x)))
    for i,t in enumerate(time):
        lp.evolve_threshold_width_river(nt=1, dt=dt)
        lp.compute_Q_s()
        z[i,:] = lp.z.copy()
        Qs[i,:] = lp.Q_s.copy()
    zs.append(z)
    Qss.append(Qs)
    ts.append(time)
    
# ---- Fit
def exponential_decay(time, amplitude, time_scale):
    return amplitude * np.exp(-time/time_scale)


# ---- Plot

Z = 3

fig, axs = plt.subplots(1,2,sharey=True)

for t in [0, 500, 1000, 1500, 2000, 2500, 3000]:
    axs[0].plot(lp.x/1.e3, zs[Z][t,:])
    
for x in [0, 200, 400, 600, 800]:
    axs[1].plot(ts[Z]/3.15e10, zs[Z][:,x])
    axs[1].plot(ts[Z]/3.15e10, zs[Z][-1,x]+exponential_decay(time, zs[Z][0,x]-zs[Z][-1,x], e_folding), "--")

plt.show()




fig, axs = plt.subplots(2, 1, sharex=True)
for i,z in enumerate(zs):
    axs[0].plot(ts[i]/3.15e10, z[:,0])
axs[0].plot(time/3.15e10, zs[0][-1,0]+exponential_decay(time, zs[0][0,0]-zs[0][-1,0], e_folding), "--")
axs[0].set_ylabel(r"Elevation, $z$ [m]")

for i,Qs in enumerate(Qss):
    axs[1].plot(ts[i]/3.15e10, Qs[:,-1]/Qs[-1,-1])
axs[1].plot(time/3.15e10, 1+exponential_decay(time, 1, e_folding), "--")
axs[1].set_ylabel(r"Sediment output, $Q_s$ [m]")
axs[1].set_xlabel(r"Time, $t$ [kyr]")

plt.show()