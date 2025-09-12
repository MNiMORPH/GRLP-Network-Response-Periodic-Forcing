"""
Run some network simulations and save the output for plotting in GMT and
ultimately combining in an animated GIF.
"""

# ---- Import functions

# External packages
import numpy as np
import matplotlib.pyplot as plt
import copy
import grlp
import scipy.signal as sig

# Local packages
import grlp_extras as grlpx


# ---- Variables
output_gmt = False
indir = "../../Output/Network/MC_N1_40/"
neti = 177
Pi = 3


# ---- Read data
print("Reading results.")
nets, hacks, gains, lags = grlpx.read_MC(indir, cases=['UUU'])


# ---- Measure gain and lag with period equal to network equilibration time
print("Evolving network.")

# Predict network Teq
Teq = gains[neti]['UUU']['Teq']
L_eff = np.sqrt(Teq*nets[neti]['UUU'].mean_diffusivity)

# Evolve to ensure steady state
nets[neti]['UUU'].evolve_threshold_width_river_network(nt=100, dt=3.154e10)

# Evolve with sinusoisal variation in sediment supply and period equal to
# equilibration time.
periodics = []
for p in [0.1, 1., 10.]:
    print(p)
    periodics.append(grlpx.evolve_network_periodic(
        net=copy.deepcopy(nets[neti]['UUU']),
        period=Teq*p,
        A_Qs=0.2,
        A_Q=0.
        ))
    
    
# ---- Save

for p,lab in enumerate(["fast/", "medium/", "slow/"]):

    basedir = "./Output/" + lab

    with open(basedir + "planform.d", "wb") as f:
        plan = grlp.plot_network(nets[neti]['UUU'], show=False)
        for seg in plan.keys():
            hdr = b"> -Z%f\n" % (nets[neti]['UUU'].segment_orders[seg])
            f.write(hdr)
            arr = np.column_stack(( plan[seg]['x'], plan[seg]['y'] ))
            np.savetxt(f, arr)
            
    with open(basedir + "force_tps.te", "wb") as f:
        tps = [250 + 500*i for i in range(8)]*2
        for tp in tps:
            hdr = b">\n"
            f.write(hdr)
            arr = np.column_stack((
                [periodics[p]['time'][tp]/3.154e10]*2,
                [0, 1.e3]
                ))
            np.savetxt(f, arr)
            
    with open(basedir + "force.tq", "wb") as f:
            arr = np.column_stack((
                periodics[p]['time']/3.154e10,
                periodics[p]['Qs_scale']
                ))
            np.savetxt(f, arr)


    frames = np.linspace(0, len(periodics[p]['time'])-1, 161).astype(int)

    for fr,frame in enumerate(frames):
        
        filename = basedir + "frame%s_Qs_out.tq" % (str(fr).zfill(3))
        with open(filename, "wb") as f:
                arr = np.column_stack((
                    periodics[p]['time'][:frame]/3.154e10,
                    periodics[p]['Qs'][0][:frame,-1]/periodics[p]['Qs'][0][0,-1]
                    ))
                np.savetxt(f, arr)

        filename = basedir + "frame%s_Qs_out_tps.tq" % (str(fr).zfill(3))
        with open(filename, "wb") as f:
            pks = sig.find_peaks(periodics[p]['Qs'][0][:frame,-1])[0]
            trs = sig.find_peaks(-periodics[p]['Qs'][0][:frame,-1])[0]
            tps = np.hstack((pks, trs))
            arr = np.column_stack((
                periodics[p]['time'][tps]/3.154e10,
                periodics[p]['Qs'][0][tps,-1]/periodics[p]['Qs'][0][0,-1],
                ))
            np.savetxt(f, arr)

        filename = basedir + "frame%s_force.tq" % (str(fr).zfill(3))
        with open(filename, "wb") as f:
                arr = np.column_stack((
                    periodics[p]['time'][:frame]/3.154e10,
                    periodics[p]['Qs_scale'][:frame]
                    ))
                np.savetxt(f, arr)

        filename = basedir + "frame%s_force_tps.tq" % (str(fr).zfill(3))
        with open(filename, "wb") as f:
            tps = [250 + 500*i for i in range(8) if 250 + 500*i <= frame]*2
            arr = np.column_stack((
                periodics[p]['time'][tps]/3.154e10,
                periodics[p]['Qs_scale'][tps]
                ))
            np.savetxt(f, arr)
            
        filename = basedir + "frame%s_z.de" % (str(fr).zfill(3))
        with open(filename, "wb") as f:
            plan = grlp.plot_network(nets[neti]['UUU'], show=False)
            for seg in plan.keys():
                for i in range(len(plan[seg]['x'])-1):
                    if i <= len(periodics[p]['z'][seg][frame,:])-1:
                        hdr = b"> -Z%f\n" % (periodics[p]['z'][seg][frame,i])
                    else:
                        hdr = b"> -Z%f\n" % (periodics[p]['z'][seg][frame,-1])
                    f.write(hdr)
                    arr = np.column_stack((
                        plan[seg]['x'][i:i+2],
                        plan[seg]['y'][i:i+2]
                        ))
                    np.savetxt(f, arr)
                    
        filename = basedir + "frame%s_dz.de" % (str(fr).zfill(3))
        with open(filename, "wb") as f:
            plan = grlp.plot_network(nets[neti]['UUU'], show=False)
            for seg in plan.keys():
                for i in range(len(plan[seg]['x'])-1):
                    if i <= len(periodics[p]['z'][seg][frame,:])-1:
                        hdr = b"> -Z%f\n" % (
                            (periodics[p]['z'][seg][frame,i] -
                            periodics[p]['z'][seg][0,i]) / 
                            periodics[p]['z'][seg][0,i]
                            )
                    else:
                        hdr = b"> -Z%f\n" % (
                            (periodics[p]['z'][seg][frame,-1] - 
                            periodics[p]['z'][seg][0,-1]) / 
                            periodics[p]['z'][seg][0,-1]
                            )
                    f.write(hdr)
                    arr = np.column_stack((
                        plan[seg]['x'][i:i+2],
                        plan[seg]['y'][i:i+2]
                        ))
                    np.savetxt(f, arr)