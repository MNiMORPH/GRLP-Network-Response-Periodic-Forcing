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
lps = {}
for p in [0., 0.5, 1., 1.5, 2., 2.5, 3.]:
    print(p)
    lp = set_up_long_profile(L, mean_Qw, mean_Qs, p, B, dx=1.e2, evolve=True)
    lps[p] = lp
S = (mean_Qs / (lps[0].k_Qs * mean_Qw))**(6./7.)


# ---- Plots

fig, axs = plt.subplots(2, 1, sharex=True)

for p in lps.keys():
    axs[0].plot(lps[p].x/1000., lps[p].z)
axs[0].plot(lps[0].x/1000., S * (lps[p].L - lps[p].x), "--")

for p in lps.keys():
    axs[1].plot(lps[p].x/1000., lps[p].Q/mean_Qw)
    axs[1].plot(lps[p].x/1000., lps[p].Q_s/mean_Qs, ":")

plt.show()


# ---- Save

out_dir = "output/setup/"

with open(out_dir + "numerical_profile.de", "wb") as f:
    hdr = b"> -Z2\n"
    f.write(hdr)
    arr = np.column_stack(( lps[2].x/1000., lps[2].z ))
    np.savetxt(f, arr)

with open(out_dir + "analytical_profile.de", "wb") as f:
    arr = np.column_stack(( lps[0.5].x/1000., S * (lps[p].L - lps[p].x) ))
    np.savetxt(f, arr)
    
with open(out_dir + "water.dq", "wb") as f:
    for p in lps.keys():
        hdr = b"> -Z%f\n" % p
        f.write(hdr)
        arr = np.column_stack(( lps[p].x/1000., lps[p].Q ))
        np.savetxt(f, arr)
        
with open(out_dir + "sediment.dq", "wb") as f:
    for p in lps.keys():
        hdr = b"> -Z%f\n" % p
        f.write(hdr)
        arr = np.column_stack(( lps[p].x/1000., lps[p].Q_s*1000. ))
        np.savetxt(f, arr)
        
with open(out_dir + "constant.dq", "wb") as f:
    arr = np.column_stack(( [0., 100.], [10., 10.] ))
    np.savetxt(f, arr)