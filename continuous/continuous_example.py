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
p = 1.8
net = set_up_long_profile(L, mean_Qw, mean_Qs, p, B, dx=5.e2, evolve=True)
ref_net = set_up_long_profile(L, mean_Qw, mean_Qs, 0, B, dx=5.e2, evolve=True)
ref_net.list_of_LongProfile_objects[0].compute_equilibration_time()

# ---- Evolve

periods = np.array([0.1, 1., 10.]) * ref_net.list_of_LongProfile_objects[0].equilibration_time

evolutions_Qs = []
ref_evolutions_Qs = []
spinups_Qs = []
ref_spinups_Qs = []

for i,period in enumerate(periods):

    spinup_time, dt = np.linspace(-period/4., 0., 250, retstep=True)
    spinup_z = np.zeros((len(spinup_time), len(net.list_of_LongProfile_objects[0].x)))
    spinup_Qs = np.zeros((len(spinup_time), len(net.list_of_LongProfile_objects[0].x)))
    for i,t in enumerate(spinup_time):
        net.evolve_threshold_width_river_network(nt=1, dt=dt)
        net.list_of_LongProfile_objects[0].compute_Q_s()
        spinup_z[i,:] = net.list_of_LongProfile_objects[0].z
        spinup_Qs[i,:] = net.list_of_LongProfile_objects[0].Q_s
    spinups_Qs.append({
        'time': spinup_time,
        'z': spinup_z,
        'Qs': spinup_Qs
    })
    
    ref_spinup_z = np.zeros((len(spinup_time), len(ref_net.list_of_LongProfile_objects[0].x)))
    ref_spinup_Qs = np.zeros((len(spinup_time), len(ref_net.list_of_LongProfile_objects[0].x)))
    for i,t in enumerate(spinup_time):
        ref_net.evolve_threshold_width_river_network(nt=1, dt=dt)
        ref_net.list_of_LongProfile_objects[0].compute_Q_s()
        ref_spinup_z[i,:] = ref_net.list_of_LongProfile_objects[0].z
        ref_spinup_Qs[i,:] = ref_net.list_of_LongProfile_objects[0].Q_s
    ref_spinups_Qs.append({
        'time': spinup_time,
        'z': ref_spinup_z,
        'Qs': ref_spinup_Qs
    })
    
    # evolve periodic
    z, Qs, time, scale = evolve_network_periodic(
        net=deepcopy(net),
        period=period,
        A_Qs=0.2,
        A_Q=0.)
    ref_z, ref_Qs, ref_time, ref_scale = evolve_network_periodic(
        net=deepcopy(ref_net),
        period=period,
        A_Qs=0.2,
        A_Q=0.)

    # save
    evolutions_Qs.append({
        'z': z,
        'Qs': Qs,
        'time': time,
        'scale': scale
        })
    ref_evolutions_Qs.append({
        'z': ref_z,
        'Qs': ref_Qs,
        'time': ref_time,
        'scale': ref_scale
        })


evolutions_Qw = []
ref_evolutions_Qw = []
spinups_Qw = []
ref_spinups_Qw = []

for i,period in enumerate(periods):

    spinup_time, dt = np.linspace(-period/4., 0., 250, retstep=True)
    spinup_z = np.zeros((len(spinup_time), len(net.list_of_LongProfile_objects[0].x)))
    spinup_Qs = np.zeros((len(spinup_time), len(net.list_of_LongProfile_objects[0].x)))
    for i,t in enumerate(spinup_time):
        net.evolve_threshold_width_river_network(nt=1, dt=dt)
        net.list_of_LongProfile_objects[0].compute_Q_s()
        spinup_z[i,:] = net.list_of_LongProfile_objects[0].z
        spinup_Qs[i,:] = net.list_of_LongProfile_objects[0].Q_s
    spinups_Qw.append({
        'time': spinup_time,
        'z': spinup_z,
        'Qs': spinup_Qs
    })
    
    ref_spinup_z = np.zeros((len(spinup_time), len(ref_net.list_of_LongProfile_objects[0].x)))
    ref_spinup_Qs = np.zeros((len(spinup_time), len(ref_net.list_of_LongProfile_objects[0].x)))
    for i,t in enumerate(spinup_time):
        ref_net.evolve_threshold_width_river_network(nt=1, dt=dt)
        ref_net.list_of_LongProfile_objects[0].compute_Q_s()
        ref_spinup_z[i,:] = ref_net.list_of_LongProfile_objects[0].z
        ref_spinup_Qs[i,:] = ref_net.list_of_LongProfile_objects[0].Q_s
    ref_spinups_Qw.append({
        'time': spinup_time,
        'z': ref_spinup_z,
        'Qs': ref_spinup_Qs
    })
    
    # evolve periodic
    z, Qs, time, scale = evolve_network_periodic(
        net=deepcopy(net),
        period=period,
        A_Qs=0.,
        A_Q=0.2)
    ref_z, ref_Qs, ref_time, ref_scale = evolve_network_periodic(
        net=deepcopy(ref_net),
        period=period,
        A_Qs=0.,
        A_Q=0.2)

    # save
    evolutions_Qw.append({
        'z': z,
        'Qs': Qs,
        'time': time,
        'scale': scale
        })
    ref_evolutions_Qw.append({
        'z': ref_z,
        'Qs': ref_Qs,
        'time': ref_time,
        'scale': ref_scale
        })


# # ---- Plots
# fig, axs = plt.subplots(3,3,sharey='row')
# 
# for i,period in enumerate(periods):
# 
#     ev = evolutions[i]
#     ref_ev = ref_evolutions[i]
# 
#     axs[0,i].plot(ev['time']/3.154e10, ev['scale'], color="0.7")
#     axs[0,i].plot(ev['time']/3.154e10, ref_ev['Qs'][0][:,-1]/ref_ev['Qs'][0][:,-1].mean(), "--", color="0.3")
#     axs[0,i].plot(ev['time']/3.154e10, ev['Qs'][0][:,-1]/ev['Qs'][0][:,-1].mean())
# 
#     xs = [0, 40, 80, 120, 160]
#     axs[1,i].plot(ev['time']/3.154e10, ref_ev['z'][0][:,xs], "--", color="0.3")
#     axs[1,i].plot(ev['time']/3.154e10, ev['z'][0][:,xs])
# 
#     ts = [3000,3050,3100,3150,3200,3250]
#     for t in ts:
#         axs[2,i].plot(net.list_of_LongProfile_objects[0].x/1.e3, ev['z'][0][t,:])
#         axs[2,i].plot(net.list_of_LongProfile_objects[0].x/1.e3, ev['z'][0][t,:]-ev['z'][0][0,:], "--")
# 
# plt.show()

# ---- Write output
basedir = "../output/continuous/example/"

labels = ["fast/", "medium/", "slow/"]

for i,period in enumerate(periods):
    
    outdir = basedir + labels[i]

    with open(outdir + "Qs_scale.tq", "wb") as f:
        arr = np.column_stack((
            np.hstack(( spinups_Qs[i]['time'][0], evolutions_Qs[i]['time']))/3.15e10,
            np.hstack(( mean_Qs*1.e3, evolutions_Qs[i]['scale']*mean_Qs*1.e3))
            ))
        np.savetxt(f, arr)
        
    with open(outdir + "Qs_out.tq", "wb") as f:
        arr = np.column_stack((
            np.hstack(( spinups_Qs[i]['time'], evolutions_Qs[i]['time']))/3.15e10,
            np.hstack(( spinups_Qs[i]['Qs'][:,-1], evolutions_Qs[i]['Qs'][0][:,-1]))/spinups_Qs[i]['Qs'][0,-1]
            ))
        np.savetxt(f, arr)
        
    with open(outdir + "ref_Qs_out.tq", "wb") as f:
        arr = np.column_stack((
            np.hstack(( spinups_Qs[i]['time'], evolutions_Qs[i]['time']))/3.15e10,
            np.hstack(( ref_spinups_Qs[i]['Qs'][:,-1], ref_evolutions_Qs[i]['Qs'][0][:,-1]))/ref_spinups_Qs[i]['Qs'][0,-1]
            ))
        np.savetxt(f, arr)

    xs = [0, 40, 80, 120, 160]
    with open(outdir + "profile.te", "wb") as f:
        for x in xs:
            hdr = b"> %.f\n" % (net.list_of_LongProfile_objects[0].x[x]/1.e3)
            f.write(hdr)
            arr = np.column_stack((
                evolutions_Qs[i]['time']/3.15e10,
                evolutions_Qs[i]['z'][0][:,x]
                ))
            np.savetxt(f, arr)

    with open(outdir + "Qw_scale.tq", "wb") as f:
        arr = np.column_stack((
            np.hstack(( spinups_Qw[i]['time'][0], evolutions_Qw[i]['time']))/3.15e10,
            np.hstack(( 1., evolutions_Qw[i]['scale']))
            ))
        np.savetxt(f, arr)
        
    with open(outdir + "Qw_Qs_out.tq", "wb") as f:
        arr = np.column_stack((
            np.hstack(( spinups_Qw[i]['time'], evolutions_Qw[i]['time']))/3.15e10,
            np.hstack(( spinups_Qw[i]['Qs'][:,-1], evolutions_Qw[i]['Qs'][0][:,-1]))/spinups_Qw[i]['Qs'][0,-1]
            ))
        np.savetxt(f, arr)
        
    with open(outdir + "Qw_ref_Qs_out.tq", "wb") as f:
        arr = np.column_stack((
            np.hstack(( spinups_Qw[i]['time'], evolutions_Qw[i]['time']))/3.15e10,
            np.hstack(( ref_spinups_Qw[i]['Qs'][:,-1], ref_evolutions_Qw[i]['Qs'][0][:,-1]))/ref_spinups_Qw[i]['Qs'][0,-1]
            ))
        np.savetxt(f, arr)
        
    
    