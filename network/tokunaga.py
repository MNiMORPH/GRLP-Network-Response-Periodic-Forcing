from grlp import *
from grlp_extras import *
import scipy.stats as sts

# Network props
effective_rainfall = 1.e4*0.4/3.154e10
B = 98.1202038813591
sediment_discharge_ratio = 1.e4

# ---- Read in expected topological lengths
expected_topological_lengths = np.loadtxt("./expected_length/expected_lengths.dat")

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
mag = 50
# mag = int(random.choice(magnitude_choices))

# # Shreve numbers
# segment_length = sts.gamma(2., scale=260./2.)
# segment_length_area_ratio = sts.norm(loc=300., scale=30.)
# supply_area = sts.norm(loc=52000., scale=5200.)

# My numbers
mean_total_length = 100.e3
expected_topological_length = expected_topological_lengths[mag-1,1]
mean_segment_length = 100.e3 / expected_topological_length
mean_segment_length_area_ratio = 300. # from Shreve
mean_supply_area = mean_segment_length * mean_segment_length_area_ratio / 2.
segment_length = sts.gamma(2., scale=mean_segment_length/2.)
segment_length_area_ratio = sts.norm(loc=mean_segment_length_area_ratio, scale=mean_segment_length_area_ratio/10.)
supply_area = sts.norm(loc=mean_supply_area, scale=mean_supply_area/10.)    

# Recreate Pelletier & Turcotte example (hopefully)
topo = [
    0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1,
    1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1,
    1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1,
    0, 1, 1, 1, 0, 1, 0, 1, 1, 1
    ]

# ---- Network topology
net, net_topo = generate_random_network(
    magnitude=mag,
    max_length=100.e3,
    segment_length=False,
    segment_length_area_ratio=False,
    supply_area=False,
    approx_dx=5.e2,
    min_nxs=5,
    mean_discharge=10.,
    effective_rainfall=False,
    sediment_discharge_ratio=sediment_discharge_ratio,
    width=B,
    topology=topo,
    evolve=False
    )
net.compute_network_properties()

# ---- Tokunaga

def tokunaga(net):

    # Count numbers of streams of order i that join streams of order j
    N = np.zeros(( net.orders[-1]-1, net.orders[-1] ))
    for i in net.orders[:-1]:
        for stream in net.streams_by_order[i]:
            for ID in stream:
                downID = net.list_of_LongProfile_objects[ID].downstream_segment_IDs[0]
                if downID not in stream:
                    adjacentID = [id for id in net.list_of_LongProfile_objects[downID].upstream_segment_IDs if id != ID][0]
                    adjacent_order = net.segment_orders[adjacentID]+1
                    N[i-1,adjacent_order-1] += 1

    # Get averages by dividing by number of streams j
    T = np.zeros(( net.orders[-1]-1, net.orders[-1]-1 ))
    for i in net.orders[1:]:
        T[:i-1,i-2] = N[:i-1,i-1] / net.order_counts[i]

    # Tokunaga's e_k - Average number of streams i flowing into streams of i+k
    e_k = np.zeros(max(net.orders)-1)
    for k in range(1,max(net.orders)):
        e_k[k-1] = T.diagonal(k-1).mean()

    # Ratios of e_k / e_k-1
    K = e_k[1:]/e_k[:-1]
    
    k = [k for k in range(1,max(net.orders))]
    
    return np.array(k), e_k, K
    
k, e_k, K = tokunaga(net)

# Plot it
plt.plot(k, e_k, "bo")
plt.plot(k, e_k[0]*(K.mean()**(k-1)), "r-")
plt.yscale("log")
plt.show()