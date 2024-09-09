"""
This script performs the analysis presented in Figure 10 of McNab et al. (2024,
EGUsphere); produces a rough version of the Figure; and, optionally, generates
output files for plotting the final Figure in GMT.

The purpose of the script/figure is to .
"""

# ---- Define functions
def compute_origin_gradient(x, y):
    x = np.array(x)
    y = np.array(y)
    return x.dot(y) / x.dot(x)

# ---- Import functions

# External packages
import numpy as np
import matplotlib.pyplot as plt
import copy
import grlp

# Local packages
import grlp_extras as grlpx


# ---- Variables
output_gmt = False
indir = "../../Output/Network/MC_N1_40/"


# ---- Read data
print("Reading results.")
nets, hacks, gains, lags = grlpx.read_MC(indir)


# ---- Regressions
regressions = {'UUU': {}, 'NUU': {}, 'UAU': {}, 'NAU': {}}
for case in ['UUU', 'NUU', 'UAU', 'NAU']:
    
    regressions[case]['eff_lengths'] = np.sqrt([
            g[case]['Teq']*nets[i][case].mean_diffusivity
            for i,g in enumerate(gains)
            ])
        
    regressions[case]['coeffs'] = {}
    regressions[case]['grads'] = {}
    
    regressions[case]['coeffs']['p'] = np.corrcoef(
        [h[case]['p'] for h in hacks],
        regressions[case]['eff_lengths']
        )[0,1]
    regressions[case]['grads']['p'] = compute_origin_gradient(
        [h[case]['p'] for h in hacks],
        regressions[case]['eff_lengths']
        )

    regressions[case]['coeffs']['R_B'] = np.corrcoef(
        [n[case].bifurcation_ratio for n in nets],
        regressions[case]['eff_lengths']
        )[0,1]
    regressions[case]['grads']['R_B'] = compute_origin_gradient(
        [n[case].bifurcation_ratio for n in nets],
        regressions[case]['eff_lengths']
        )

    regressions[case]['coeffs']['R_L'] = np.corrcoef(
        [n[case].length_ratio for n in nets],
        regressions[case]['eff_lengths']
        )[0,1]
    regressions[case]['grads']['R_L'] = compute_origin_gradient(
        [n[case].length_ratio for n in nets],
        regressions[case]['eff_lengths']
        )
        
    regressions[case]['coeffs']['R_Q'] = np.corrcoef(
        [n[case].discharge_ratio for n in nets],
        regressions[case]['eff_lengths']
        )[0,1]
    regressions[case]['grads']['R_Q'] = compute_origin_gradient(
        [n[case].discharge_ratio for n in nets],
        regressions[case]['eff_lengths']
        )
        
    regressions[case]['coeffs']['K'] = np.corrcoef(
        [n[case].tokunaga['K_mean'] for n in nets],
        regressions[case]['eff_lengths']
        )[0,1]
    regressions[case]['grads']['K'] = compute_origin_gradient(
        [n[case].tokunaga['K_mean'] for n in nets],
        regressions[case]['eff_lengths']
        )
        
    regressions[case]['coeffs']['<L>'] = np.corrcoef(
        [n[case].mean_downstream_distance for n in nets],
        regressions[case]['eff_lengths']
        )[0,1]
    regressions[case]['grads']['<L>'] = compute_origin_gradient(
        [n[case].mean_downstream_distance for n in nets],
        regressions[case]['eff_lengths']
        )
    
    regressions[case]['coeffs']['<L>_50'] = np.corrcoef(
        [n[case].median_downstream_distance for n in nets],
        regressions[case]['eff_lengths']
        )[0,1]
    regressions[case]['grads']['<L>_50'] = compute_origin_gradient(
        [n[case].median_downstream_distance for n in nets],
        regressions[case]['eff_lengths']
        )


# ---- Labels
labels = {
    'p': r'$p_{x,Q}$',
    'R_B': r'$R_B$',
    'R_L': r'$R_L$',
    'R_Q': r'$R_Q$',
    'K': r'$K$',
    '<L>': r'$\langle L \rangle$',
    '<L>_50': r'$\langle L \rangle_{50}$'
    }


# ---- Plot
fig, axs = plt.subplots(2, 4, sharey="row", sharex="row")
for i,case in enumerate(['UUU', 'NUU', 'UAU', 'NAU']):
    
    axs[0,i].bar(
        np.arange(len(regressions[case]['coeffs'])),
        list(regressions[case]['coeffs'].values())
        )

    rng = np.array([
        min([n[case].mean_downstream_distance for n in nets]),
        max([n[case].mean_downstream_distance for n in nets])
        ])
    axs[1,i].plot(rng/1.e3, rng*regressions[case]['grads']['<L>']/1.e3, "k--")
    axs[1,i].plot(
        [n[case].mean_downstream_distance/1.e3 for n in nets],
        np.array(regressions[case]['eff_lengths'])/1.e3,
        "o",
        alpha=0.2
        )

axs[0,0].set_ylabel(r'Correlation coefficient, $r$')
axs[0,0].set_xticks(
    np.arange(len(regressions[case]['coeffs'])),
    labels.values()
    )
    
axs[1,0].set_ylabel(r'Effective length, $\widehat{L}$ [km]')
for ax in axs[1,:]:
    ax.set_xlabel(r'Mean length, $\langle L \rangle$ [km]')
    
for row in axs:
    for ax in row:
        ax.set_box_aspect(1)

plt.show()


# ---- save

if output_gmt:

    basedir = "../output/network/controls/"
    outfiles = {
        "m40_no_int": "m40_fix_seg_length_no_internal.dat",
        "m40_w_int": "m40_fix_seg_length_w_internal.dat",
        "m40_rnd_no_int": "m40_rnd_seg_length_no_internal.dat",
        "m40_rnd_w_int": "m40_rnd_seg_length_w_internal.dat",
        "m2-150_no_int": "m2-150_fix_seg_length_no_internal.dat",
        "m2-150_w_int": "m2-150_fix_seg_length_w_internal.dat",
        "m2-150_rnd_no_int": "m2-150_rnd_seg_length_no_internal.dat",
        "m2-150_rnd_w_int": "m2-150_rnd_seg_length_w_internal.dat",
        "m40_no_int_var_width": "m40_fix_seg_length_no_internal_var_width.dat",
        "m40_w_int_var_width": "m40_fix_seg_length_w_internal_var_width.dat",
        "m40_rnd_no_int_var_width": "m40_rnd_seg_length_no_internal_var_width.dat",
        "m40_rnd_w_int_var_width": "m40_rnd_seg_length_w_internal_var_width.dat",
        "m2-150_no_int_var_width": "m2-150_fix_seg_length_no_internal_var_width.dat",
        "m2-150_w_int_var_width": "m2-150_fix_seg_length_w_internal_var_width.dat",
        "m2-150_rnd_no_int_var_width": "m2-150_rnd_seg_length_no_internal_var_width.dat",
        "m2-150_rnd_w_int_var_width": "m2-150_rnd_seg_length_w_internal_var_width.dat"
        }
    corr_outfiles = {
        "m40_no_int": "corr_m40_fix_seg_length_no_internal.dat",
        "m40_w_int": "corr_m40_fix_seg_length_w_internal.dat",
        "m40_rnd_no_int": "corr_m40_rnd_seg_length_no_internal.dat",
        "m40_rnd_w_int": "corr_m40_rnd_seg_length_w_internal.dat",
        "m2-150_no_int": "corr_m2-150_fix_seg_length_no_internal.dat",
        "m2-150_w_int": "corr_m2-150_fix_seg_length_w_internal.dat",
        "m2-150_rnd_no_int": "corr_m2-150_rnd_seg_length_no_internal.dat",
        "m2-150_rnd_w_int": "corr_m2-150_rnd_seg_length_w_internal.dat",
        "m40_no_int_var_width": "corr_m40_fix_seg_length_no_internal_var_width.dat",
        "m40_w_int_var_width": "corr_m40_fix_seg_length_w_internal_var_width.dat",
        "m40_rnd_no_int_var_width": "corr_m40_rnd_seg_length_no_internal_var_width.dat",
        "m40_rnd_w_int_var_width": "corr_m40_rnd_seg_length_w_internal_var_width.dat",
        "m2-150_no_int_var_width": "corr_m2-150_fix_seg_length_no_internal_var_width.dat",
        "m2-150_w_int_var_width": "corr_m2-150_fix_seg_length_w_internal_var_width.dat",
        "m2-150_rnd_no_int_var_width": "corr_m2-150_rnd_seg_length_no_internal_var_width.dat",
        "m2-150_rnd_w_int_var_width": "corr_m2-150_rnd_seg_length_w_internal_var_width.dat"
        }
        
    fit_outfiles = {
        "m40_no_int": "fit_m40_fix_seg_length_no_internal.dat",
        "m40_w_int": "fit_m40_fix_seg_length_w_internal.dat",
        "m40_rnd_no_int": "fit_m40_rnd_seg_length_no_internal.dat",
        "m40_rnd_w_int": "fit_m40_rnd_seg_length_w_internal.dat",
        "m2-150_no_int": "fit_m2-150_fix_seg_length_no_internal.dat",
        "m2-150_w_int": "fit_m2-150_fix_seg_length_w_internal.dat",
        "m2-150_rnd_no_int": "fit_m2-150_rnd_seg_length_no_internal.dat",
        "m2-150_rnd_w_int": "fit_m2-150_rnd_seg_length_w_internal.dat",
        "m40_no_int_var_width": "fit_m40_fix_seg_length_no_internal_var_width.dat",
        "m40_w_int_var_width": "fit_m40_fix_seg_length_w_internal_var_width.dat",
        "m40_rnd_no_int_var_width": "fit_m40_rnd_seg_length_no_internal_var_width.dat",
        "m40_rnd_w_int_var_width": "fit_m40_rnd_seg_length_w_internal_var_width.dat",
        "m2-150_no_int_var_width": "fit_m2-150_fix_seg_length_no_internal_var_width.dat",
        "m2-150_w_int_var_width": "fit_m2-150_fix_seg_length_w_internal_var_width.dat",
        "m2-150_rnd_no_int_var_width": "fit_m2-150_rnd_seg_length_no_internal_var_width.dat",
        "m2-150_rnd_w_int_var_width": "fit_m2-150_rnd_seg_length_w_internal_var_width.dat"
        }
        
    for i,grp in enumerate(sweep_grps.keys()):
        
        with open(basedir + outfiles[grp], "wb") as f:
            arr = np.column_stack((
                [n.bifurcation_ratio for sweep in sweep_grps[grp] for n in nets[sweep]],
                [n.length_ratio for sweep in sweep_grps[grp] for n in nets[sweep]],
                [n.discharge_ratio for sweep in sweep_grps[grp] for n in nets[sweep]],
                [1./h['p'] for sweep in sweep_grps[grp] for h in hacks[sweep]],
                [n.mean_downstream_distance/1.e3 for sweep in sweep_grps[grp] for n in nets[sweep]],
                [n.median_downstream_distance/1.e3 for sweep in sweep_grps[grp] for n in nets[sweep]],
                np.array([eff_length for sweep in sweep_grps[grp] for eff_length in eff_lengths[sweep]])/1.e3,
                [len(n.streams_by_order[1]) for sweep in sweep_grps[grp] for n in nets[sweep]]
                ))
            np.savetxt(f, arr)
            
        with open(basedir + corr_outfiles[grp], "wb") as f:
            arr = np.column_stack((
                np.arange(len(grp_corrs[grp])),
                grp_corrs[grp]
                ))
            np.savetxt(f, arr)
        
        with open(basedir + fit_outfiles[grp], "wb") as f:
            arr = np.column_stack((
                grp_L_mean_grad[grp]['L_mean'],
                grp_L_mean_grad[grp]['eff_length']
                ))
            np.savetxt(f, arr)    
        