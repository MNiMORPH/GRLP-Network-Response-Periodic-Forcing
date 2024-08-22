import numpy as np
import scipy.stats as sts
import random
import copy
import pickle
import os
import yaml
import matplotlib.pyplot as plt

import grlp
import grlp_extras as grlpx


def analyse_network(iter):
    
    i = iter[0]
    setup_file = iter[1]    
    
    with open(setup_file, 'r') as f:
        props = yaml.safe_load(f)

    # ---- Valley properties
    # Define properties to use when constructing the single segment valleys.
    # Correspond to precipitation rate of c. 1 m/yr for a catchment with Hack
    # exponent of 1.8 and runoff coefficent of 0.4; and an equilibration time of
    # 100 kyr.
    # See ../Compute_River_Properties.py for details.
    x0 = 50.e3
    L = 100.e3
    Q_mean = 26.
    Qs_mean = Q_mean * 1.e-4
    B_mean = 254.

    # ---- Network properties
    segment_length = sts.gamma(2., scale=1./2.)
    segment_length_area_ratio = 1.
    supply_area = 10.e3

    # ---- Liear version
    lin_net = grlpx.generate_single_segment_network(
        L,
        Q_mean,
        Qs_mean,
        B_mean,
        0.,
        0.,
        0.
        )
    T_eq = lin_net.list_of_LongProfile_objects[0].equilibration_time


    # N1 = 10
    try:
        min_N1 = props['N1'][0]
        max_N1 = props['N1'][1]
        N1_choices = np.hstack(
            [[N1]*np.log2(N1).astype(int) for N1 in range(min_N1,max_N1)]
            )
        N1 = int(random.choice(N1_choices))
    except TypeError:
        N1 = props['N1']
    print(N1)


    nets = {}

    # ---- Base network
    net, topo = grlp.generate_random_network(
        magnitude=N1,
        max_length=L,
        approx_dx=5.e2,
        min_nxs=5,
        mean_discharge=Q_mean,
        sediment_discharge_ratio=1.e4,
        mean_width=B_mean,
        topology=None,
        evolve=True
        )
    net.compute_network_properties()
    nets['UUU'] = {'net': net, 'topo': topo}

    # ---- Along stream supply
    net, topo = grlp.generate_random_network(
        magnitude=N1,
        max_length=L,
        segment_length_area_ratio=segment_length_area_ratio,
        supply_area=supply_area,
        approx_dx=5.e2,
        min_nxs=5,
        mean_discharge=Q_mean,
        sediment_discharge_ratio=1.e4,
        mean_width=B_mean,
        topology=nets['UUU']['topo'].links,
        evolve=True
        )
    net.compute_network_properties()
    nets['UAU'] = {'net': net, 'topo': topo}

    # ---- Random segment lengths
    net, topo = grlp.generate_random_network(
        magnitude=N1,
        max_length=L,
        segment_length=segment_length,
        approx_dx=5.e2,
        min_nxs=5,
        mean_discharge=Q_mean,
        sediment_discharge_ratio=1.e4,
        mean_width=B_mean,
        topology=nets['UUU']['topo'].links,
        evolve=True
        )
    net.compute_network_properties()
    nets['NUU'] = {'net': net, 'topo': topo}

    # ---- Random segment lengths & Along stream supply
    net, topo = grlp.generate_random_network(
        magnitude=N1,
        max_length=L,
        segment_lengths=nets['NUU']['topo'].segment_lengths,
        segment_length_area_ratio=segment_length_area_ratio,
        supply_area=supply_area,
        approx_dx=5.e2,
        min_nxs=5,
        mean_discharge=Q_mean,
        sediment_discharge_ratio=1.e4,
        mean_width=B_mean,
        topology=nets['UUU']['topo'].links,
        evolve=True
        )
    net.compute_network_properties()
    nets['NAU'] = {'net': net, 'topo': topo}

    # --------Variable width

    # ---- Base network
    net, topo = grlp.generate_random_network(
        magnitude=N1,
        max_length=L,
        approx_dx=5.e2,
        min_nxs=5,
        mean_discharge=Q_mean,
        sediment_discharge_ratio=1.e4,
        mean_width=B_mean,
        variable_width=True,
        topology=nets['UUU']['topo'].links,
        evolve=True
        )
    net.compute_network_properties()
    nets['UUN'] = {'net': net, 'topo': topo}

    # ---- Along stream supply
    net, topo = grlp.generate_random_network(
        magnitude=N1,
        max_length=L,
        segment_length_area_ratio=segment_length_area_ratio,
        supply_area=supply_area,
        approx_dx=5.e2,
        min_nxs=5,
        mean_discharge=Q_mean,
        sediment_discharge_ratio=1.e4,
        mean_width=B_mean,
        variable_width=True,
        topology=nets['UUU']['topo'].links,
        evolve=True
        )
    net.compute_network_properties()
    nets['UAN'] = {'net': net, 'topo': topo}

    # ---- Random segment lengths
    segment_length = sts.gamma(2., scale=1./2.)
    net, topo = grlp.generate_random_network(
        magnitude=N1,
        max_length=L,
        segment_lengths=nets['NUU']['topo'].segment_lengths,
        approx_dx=5.e2,
        min_nxs=5,
        mean_discharge=Q_mean,
        sediment_discharge_ratio=1.e4,
        mean_width=B_mean,
        variable_width=True,
        topology=nets['UUU']['topo'].links,
        evolve=True
        )
    net.compute_network_properties()
    nets['NUN'] = {'net': net, 'topo': topo}

    # ---- Random segment lengths & Along stream supply
    net, topo = grlp.generate_random_network(
        magnitude=N1,
        max_length=L,
        segment_lengths=nets['NUU']['topo'].segment_lengths,
        segment_length_area_ratio=segment_length_area_ratio,
        supply_area=supply_area,
        approx_dx=5.e2,
        min_nxs=5,
        mean_discharge=Q_mean,
        sediment_discharge_ratio=1.e4,
        mean_width=B_mean,
        variable_width=True,
        topology=nets['UUU']['topo'].links,
        evolve=True
        )
    net.compute_network_properties()
    nets['NAN'] = {'net': net, 'topo': topo}

    # # ---- Plot
    # fig, axs = plt.subplots(4,8,sharex=True, sharey="row")
    # for i,n in enumerate(['UUU', 'NUU', 'UAU', 'NAU', 'UUN', 'NUN', 'UAN', 'NAN']):
    #     plan = grlp.plot_network(nets[n]['net'], show=False)
    #     for seg in nets[n]['net'].list_of_LongProfile_objects:
    #         axs[0,i].plot(plan[seg.ID]['x'], plan[seg.ID]['y'])
    #         axs[1,i].plot(seg.x/1.e3, seg.Q)
    #         axs[2,i].plot(seg.x/1.e3, seg.B)
    #         axs[3,i].plot(seg.x/1.e3, seg.z)
    # plt.show()
    # 
    # fig, axs = plt.subplots(2,4,sharex=True, sharey="row")
    # for i,n in enumerate(['UUU', 'NUU', 'UAU', 'NAU']):
    #     axs[0,i].plot([0., 100.], [1., 1.], ":")
    #     for seg in nets[n]['net'].list_of_LongProfile_objects:
    #         if not seg.upstream_segment_IDs:
    #             c="black"
    #         else:
    #             c="grey"
    #         axs[0,i].plot(seg.x/1.e3, seg.Q_s/seg.Q*1.e4, c=c)   
    #     if i==0:
    #         axs[0,i].set_ylabel(r"$Q_s$ / Intended $Q_s$") 
    #     axs[0,i].set_title(n)
    # for i,n in enumerate(['UUN', 'NUN', 'UAN', 'NAN']):
    #     axs[1,i].plot([0., 100.], [1., 1.], ":")
    #     for seg in nets[n]['net'].list_of_LongProfile_objects:
    #         if not seg.upstream_segment_IDs:
    #             c="black"
    #         else:
    #             c="grey"
    #         axs[1,i].plot(seg.x/1.e3, seg.Q_s/seg.Q*1.e4, c=c)
    #     axs[1,i].set_xlabel(r"$x$ [km]")
    #     if i==0:
    #         axs[1,i].set_ylabel(r"$Q_s$ / Intended $Q_s$") 
    #     axs[1,i].set_title(n)
    # plt.show()

    # import sys
    # sys.exit()

    # ---- Analyse
    # for n in ['UUU', 'NUU', 'UAU', 'NAU', 'UUN', 'NUN', 'UAN', 'NAN']:
    for n in ['UUU']:
        print(n)

        periods = np.logspace(-2.,2.,3) * T_eq
        G_z = {'Qs': [], 'Qw': []}
        lag_z = {'Qs': [], 'Qw': []}
        G_Qs = {'Qs': [], 'Qw': []}
        lag_Qs = {'Qs': [], 'Qw': []}
        for period in periods:
            
            for lab, A_Qs, A_Qw in zip(['Qs', 'Qw'], [0.2, 0.], [0., 0.2]):
                
                # Run, compute metrics
                neti = copy.deepcopy(nets[n]['net'])
                periodic = grlpx.evolve_network_periodic(
                    neti, period, A_Qs, A_Qw
                    )
                
                # Record gain
                G_z[lab].append(periodic['G_z'])
                G_Qs[lab].append(periodic['G_Qs'])
                
                # Record lag
                lag_z[lab].append(periodic['lag_z'])
                lag_Qs[lab].append(periodic['lag_Qs'])

        # ---- Compute best fitting equilibration times
        net_Teq = grlpx.find_network_equilibration_time(
            [g[0][-1] for g in G_Qs['Qs']], 
            periods,
            lin_net)
            
        # ---- Hack
        hack = grlp.find_network_hack_parameters(nets[n]['net'])

        # ---- Output
        outdir = props['outdir'] + str(i) + "/" + n + "/"
        os.makedirs(outdir)
        with open(outdir + "props.obj", "wb") as f:
            pickle.dump({
                'x_bl': L,
                'z_bl': 0.,
                'S0': [
                    seg.S0 
                    for seg in nets[n]['net'].list_of_LongProfile_objects
                    if seg.S0 is not None
                    ],
                'upstream_segment_IDs': [
                    seg.upstream_segment_IDs
                    for seg in nets[n]['net'].list_of_LongProfile_objects
                    ],
                'downstream_segment_IDs': [
                    seg.downstream_segment_IDs
                    for seg in nets[n]['net'].list_of_LongProfile_objects
                    ],
                'x_ls': [
                    seg.x
                    for seg in nets[n]['net'].list_of_LongProfile_objects
                    ],
                'z_ls': [
                    seg.z
                    for seg in nets[n]['net'].list_of_LongProfile_objects
                    ],
                'Q_ls': [
                    seg.Q
                    for seg in nets[n]['net'].list_of_LongProfile_objects
                    ],
                'B_ls': [
                    seg.B
                    for seg in nets[n]['net'].list_of_LongProfile_objects
                    ],
                'ssd_ls': [
                    seg.ssd
                    for seg in nets[n]['net'].list_of_LongProfile_objects
                    ]                                    
                }, 
                f
            )
        with open(outdir + "hack.obj", "wb") as f:
            pickle.dump(hack, f)
        with open(outdir + "gain.obj", "wb") as f:
            pickle.dump(
                {'P': periods, 'G_z': G_z, 'G_Qs': G_Qs, 'Teq': net_Teq},
                f
            )
        with open(outdir + "lag.obj", "wb") as f:
            pickle.dump(
                {'P': periods, 'lag_z': lag_z, 'lag_Qs': lag_Qs},
                f
            )
            
if __name__ == "__main__":
    
    import sys
    i = int(sys.argv[1])
    j = int(sys.argv[2])
    setup_file = sys.argv[3]
    
    from datetime import datetime
    print("Starting: " + datetime.now().strftime("%H:%M:%S"))
    
    import multiprocessing as mp
    with mp.Pool(processes=3) as pool:
        results = pool.map(
            analyse_network, 
            [(k, setup_file) for k in range(i,j+1)]
            )
    
    print("Finished: " + datetime.now().strftime("%H:%M:%S"))