from grlp import *
from grlp_extras import *
import random

from scipy.stats import skewnorm, gamma

# mean = 0.255
# variance = 0.0388
# shp = 20
# delta = shp/np.sqrt(1.+(shp**2.))
# scl = np.sqrt( variance / (1. - (2./np.pi)*(delta**2.)) )
# loc = mean - scl*delta*np.sqrt(2./np.pi)
# mean2 = loc + scl*delta*np.sqrt(2./np.pi)
# var2 = (scl**2.) * (1. - (2.*(delta**2.))/np.pi)
# sk = skewnorm(shp, loc=loc, scale=scl)
# x = np.linspace(-0.2,1,1000)
# r = sk.rvs(size=10000)
# plt.hist(r, density=True)
# plt.plot(x, sk.pdf(x))
# plt.show()

# alpha = 2
# mean = 255.
# rate = alpha / mean
# gam = gamma(alpha,scale=1./rate)
# x = np.linspace(0.,5.,1000)
# r = gam.rvs(size=100000)
# plt.hist(r, density=True)
# plt.plot(x, gam.pdf(x))
# plt.show()
# 
# 
# import sys
# sys.exit()


class NormalVariable:
    def __init__(self, mean: float, sd: float):
        self.mean = mean
        self.sd = sd
    def draw(self):
        return random.gauss(self.mean, self.sd)
        
class GammaVariable:
    def __init__(self, mean: float, shape: float = 2.):
        from scipy.stats import skewnorm, gamma
        self.mean = mean
        self.shape = shape
        self.rate = shape / mean
        self.gamma = gamma(shape, scale=1/self.rate)
    def draw(self):
        return self.gamma.rvs(size=1)[0]
        
        
# ---- Network props
# ext_link_length = NormalVariable(0.255 * 1.e3, np.sqrt(0.0388 * 1.e3))
# int_link_length = NormalVariable(0.267 * 1.e3, np.sqrt(0.0388 * 1.e3))
ext_link_length = GammaVariable(0.255 * 1.e3)
int_link_length = GammaVariable(0.267 * 1.e3)
length_area_scl = NormalVariable(0.5 * 1.e3, 0.1 * 1.e3)
rainfall = 1e3 * 3.171e-11
Cr = 0.4
B = 100.
sediment_discharge_ratio = 1.e4

# ---- Test link properties
length = []
area = []
for i in range(200):
    length.append( ext_link_length.draw() )
    area.append( length[-1] * length_area_scl.draw() )
plt.scatter(np.array(area)/1.e6, np.array(length)/1.e3)
plt.show()

# import sys
# sys.exit()

# ---- Network topology

net_topo = Shreve_Random_Network(magnitude=10)
downstream_segment_list = net_topo.downstream_segment_IDs
upstream_segment_list = net_topo.upstream_segment_IDs

sources = []
for i in range(len(net_topo.downstream_segment_IDs)):
    if not net_topo.upstream_segment_IDs[i]:
        sources.append(i)

lengths = {}
discharges = {}
nxs = {}
dxs = {}
for i in range(len(net_topo.upstream_segment_IDs)):
    if i in sources:
        lengths[i] = ext_link_length.draw()
        discharges[i] = lengths[i] * length_area_scl.draw() * rainfall * 0.4
    else:
        lengths[i] = int_link_length.draw()
        discharges[i] = None
    nxs[i] = 5
    dxs[i] = lengths[i] / nxs[i]


# ---- Basic lp object to get k_Qs for later
lp = LongProfile()
lp.basic_constants()
lp.bedload_lumped_constants()
lp.set_hydrologic_constants()

# ---- Loop over segments filling lists for network
x_ls = []
z_ls = []
Q_ls = []
B_ls = []
S0_ls = []
for i,nx in enumerate(nxs):
    
    # # Set up x domain
    # down_IDs = downstream_IDs(downstream_segment_list, i)[1:]
    # down_nx = sum([nxs[j] for j in down_IDs])
    # x0 = - down_nx - nxs[i]
    # x1 = x0 + nxs[i]
    # x = np.arange( x0, x1, 1. ) * dxs[i]
    # x_ls.append(x)
    
    # Set up x domain
    down_IDs = downstream_IDs(net_topo.downstream_segment_IDs, i)[1:]
    down_x = sum([lengths[i] for i in down_IDs])
    x0 = - down_x - lengths[i]
    x1 = x0 + lengths[i]
    x = x0 + np.arange( 0, nxs[i], 1 )*dxs[i]
    x_ls.append(x)
    
    # set width
    B_ls.append(B)
    
    # Set discharges
    if i in sources:
        # if segment is a mountain source, set Q input values
        Q_ls.append(np.full(len(x), discharges[i]))
    else:
        # otherwise set Q based on upstream sources
        # Qs will be set by input from upstream segments
        up_IDs = upstream_IDs(net_topo.upstream_segment_IDs, i)
        up_discharge = sum([discharges[j] for j in up_IDs if j in sources])
        Q_ls.append(np.full(len(x), up_discharge))

    # S0
    S0 = (1./(lp.k_Qs*sediment_discharge_ratio))**(6./7.)

    # Set initial z
    z = (x.max()-x)*S0
    
    # if not mouth, reset downstream elevation to that of downstream segment
    # needs lists to work backwards from downstream end
    if downstream_segment_list[i]:
        z += z_ls[downstream_segment_list[i][0]][0] + dxs[i]*S0
    z_ls.append(z)
    
    if i in sources:
        S0_ls.append(S0)
        
# ---- Update x coordinates to run from 0 at furthest upstream point, record max
x_min = min([min(x) for x in x_ls])
for i,nx in enumerate(nxs):
    x_ls[i] -= x_min
# AW guess: take max x value and add an increment dx for base-level boundary
x_max = max([max(x) + (x[-1]-x[-2]) for x in x_ls])
# Then add on some vertical distance to make a straight line to base level
dz_for_bl = dxs[i]*S0
for _z in z_ls:
    _z += dz_for_bl

net = Network()
net.initialize(
    config_file = None,
    x_bl = x_max,
    z_bl = 0.,
    S0 = S0_ls,
    upstream_segment_IDs = upstream_segment_list,
    downstream_segment_IDs = downstream_segment_list,
    x = x_ls,
    z = z_ls,
    Q = Q_ls,
    B = B_ls,
    overwrite = False
    )
net.set_niter(3)
net.get_z_lengths()
net.compute_network_properties()













# 
# 
# segments = []
# for i in range(len(net_topo.upstream_segment_IDs)):
# 
#     # Some basic set up
#     lp = LongProfile()
#     lp.set_ID(i)
#     lp.set_upstream_segment_IDs(net_topo.upstream_segment_IDs[i])
#     lp.set_downstream_segment_IDs(net_topo.downstream_segment_IDs[i])
#     lp.set_intermittency(1)
#     lp.basic_constants()
#     lp.bedload_lumped_constants()
#     lp.set_hydrologic_constants()
#     lp.set_niter()
#     lp.set_uplift_rate(0)
# 
#     # Set up x domain
#     down_IDs = downstream_IDs(net_topo.downstream_segment_IDs, i)[1:]
#     down_x = sum([lengths[i] for i in down_IDs])
#     x0 = - down_x - lengths[i]
#     x1 = x0 + lengths[i]
#     x = x0 + np.arange( -1, nxs[i]+1, 1 )*dxs[i]
#     lp.set_x(x_ext=x)
# 
#     # set width
#     lp.set_B(B)
# 
#     # Set initial z
#     S0 = (1. / (lp.k_Qs * sediment_discharge_ratio))**(6./7.)
#     lp.set_z(S0=-S0, z1=0.)
# 
#     if i in sources:
#         # if segment is a source, set Q and Qs to input values
#         lp.set_Q(Q=discharges[i])
#         lp.set_Qs_input_upstream(discharges[i]/sediment_discharge_ratio)
#     else:
#         # otherwise set Q based on upstream sources
#         # Qs will be set by input from upstream segments
#         up_IDs = upstream_IDs(net_topo.upstream_segment_IDs, i)
#         up_discharge = sum([discharges[j] for j in up_IDs if j in sources])
#         lp.set_Q(Q=up_discharge)
# 
#     if lp.downstream_segment_IDs:
#         # if not mouth, reset downstream elevation to that of downstream segment
#         lp.z += segments[lp.downstream_segment_IDs[0]].z_ext[0]
#         lp.z_ext += segments[lp.downstream_segment_IDs[0]].z_ext[0]
#     else:
#         # otherwise set network base level to zero
#         lp.set_z_bl(0.)
# 
#     # add LongProfile object to segment list
#     segments.append(lp)
# 
# # ---- Update x coordinates to run from 0 at furthest upstream point
# x_min = min([min(lp.x) for lp in segments])
# for i,seg in enumerate(segments):
#     segments[i].set_x(x_ext=segments[i].x_ext-x_min)
# 
# # ---- Initialise and set up network object with list of LongProfile objects
# net = Network(segments)
# net.get_z_lengths()
# net.set_niter()
# net.build_ID_list()
# net.compute_network_properties()


for seg in net.list_of_LongProfile_objects:
    plt.plot(seg.x/1.e3, seg.z)
plt.show()
__ = plot_network(net)
