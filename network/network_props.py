from grlp import *
from grlp_extras import *

indirs = {
    "m20": "./glic/output_071123/",
    "m40": "./glic/output_081123/",
    "m2-100": "./glic/output_101123/",
    "m40_var": "../output/network/m40_rnd_seg_length/"
    }
nets = {}
hacks = {}
for sweep in indirs.keys():
    sweep_nets, sweep_hacks, sweep_gains, sweep_lags = read_sweep(indirs[sweep])
    nets[sweep] = sweep_nets
    hacks[sweep] = sweep_hacks
    
# ------------------------------- PROP DISTRIBUTIONS ------------------------- #

fig, axs = plt.subplots(4,3,sharex='col')

for i,sweep in enumerate(nets.keys()):

    axs[i,0].hist(
        [n.bifurcation_ratio for n in nets[sweep]]
        )
    axs[i,0].hist(
        [n.length_ratio for n in nets[sweep]]
        )
    axs[i,0].hist(
        [n.discharge_ratio for n in nets[sweep]]
        )
        
    axs[i,1].hist(
        [1./h['p'] for h in hacks[sweep]]
        )
        
    axs[i,2].hist(
        [n.mean_downstream_distance/1.e3 for n in nets[sweep]]
        )

plt.show()

# ---- SAVE

basedir = "../output/network/props/"

outdirs = {
    "m20": "m20_fix_seg_length/",
    "m40": "m40_fix_seg_length/",
    "m2-100": "m2-100_fix_seg_length/",
    "m40_var": "m40_rnd_seg_length/"
    }

for i,sweep in enumerate(indirs.keys()):
    
    with open(basedir + outdirs[sweep] + "Rb.c", "wb") as f:
        np.savetxt(
            f,
            [n.bifurcation_ratio for n in nets[sweep]]
            )

    with open(basedir + outdirs[sweep] + "Rl.c", "wb") as f:
        np.savetxt(
            f,
            [n.length_ratio for n in nets[sweep]]
            )  

    with open(basedir + outdirs[sweep] + "Rq.c", "wb") as f:
        np.savetxt(
            f,
            [n.discharge_ratio for n in nets[sweep]]
            )     

    with open(basedir + outdirs[sweep] + "h.c", "wb") as f:
        np.savetxt(
            f,
            [1./h['p'] for h in hacks[sweep]]
            )
            
    with open(basedir + outdirs[sweep] + "Le.c", "wb") as f:
        np.savetxt(
            f,
            [n.mean_downstream_distance/1.e3 for n in nets[sweep]]
            )      