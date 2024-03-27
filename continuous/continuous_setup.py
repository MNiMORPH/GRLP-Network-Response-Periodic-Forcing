from grlp import *
from grlp_extras import *
# from extras import *
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
for p in np.array([1.4, 1.8, 2.2, 2.6]):
    print(p)
    net = set_up_long_profile(L, mean_Qw, mean_Qs, p, B, dx=1.e2, evolve=True)
    lps[p] = net
# S = (mean_Qs / (lps[1.4].list_of_LongProfile_objects[0].k_Qs * mean_Qw))**(6./7.)
lp_ref = set_up_long_profile(L, mean_Qw, mean_Qs, 0, B, dx=1.e2, evolve=True)

# ---- Plots

fig, axs = plt.subplots(1, 2, sharex=True)

for p in lps.keys():
    axs[0].plot(lps[p].list_of_LongProfile_objects[0].x/1000., lps[p].list_of_LongProfile_objects[0].Q/mean_Qw)
    axs[0].plot(lps[p].list_of_LongProfile_objects[0].x/1000., lps[p].list_of_LongProfile_objects[0].Q_s/mean_Qs, ":")
axs[0].plot(lp_ref.list_of_LongProfile_objects[0].x/1000., lp_ref.list_of_LongProfile_objects[0].Q/mean_Qw, "--")

for p in lps.keys():
    axs[1].plot(lps[p].list_of_LongProfile_objects[0].x/1000., lps[p].list_of_LongProfile_objects[0].z)
axs[1].plot(lp_ref.list_of_LongProfile_objects[0].x/1000., lp_ref.list_of_LongProfile_objects[0].z, "--")

plt.show()


# ---- Save

out_dir = "../output/continuous/setup/"

with open(out_dir + "numerical_profile.de", "wb") as f:
    for p in list(lps.keys())[::-1]:
        hdr = b"> -Z%f\n" % p
        f.write(hdr)
        arr = np.column_stack((
            lps[p].list_of_LongProfile_objects[0].x/1000.,
            lps[p].list_of_LongProfile_objects[0].z))
        np.savetxt(f, arr)

with open(out_dir + "analytical_profile.de", "wb") as f:
    arr = np.column_stack((
        lp_ref.list_of_LongProfile_objects[0].x/1000., 
        lp_ref.list_of_LongProfile_objects[0].z ))
    np.savetxt(f, arr)

with open(out_dir + "water.dq", "wb") as f:
    for p in lps.keys():
        hdr = b"> -Z%f\n" % p
        f.write(hdr)
        arr = np.column_stack((
            lps[p].list_of_LongProfile_objects[0].x/1000.,
            lps[p].list_of_LongProfile_objects[0].Q ))
        np.savetxt(f, arr)

with open(out_dir + "sediment.dq", "wb") as f:
    for p in lps.keys():
        hdr = b"> -Z%f\n" % p
        f.write(hdr)
        arr = np.column_stack((
            lps[p].list_of_LongProfile_objects[0].x/1000.,
            lps[p].list_of_LongProfile_objects[0].Q_s*1000. ))
        np.savetxt(f, arr)

with open(out_dir + "constant.dq", "wb") as f:
    arr = np.column_stack(( [0., L/1.e3], [mean_Qw, mean_Qw] ))
    np.savetxt(f, arr)