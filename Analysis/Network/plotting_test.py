import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as sts

import grlp
import grlp_extras as grlpx



import copy

def plot_network(net, show=True):
    """
    Generate a plotable network planform from a network object.
    """

    def check_for_segment_conflicts(ID, segs_by_topo_length, net, ys):
        """
        Check for segments that overlap with the given segment.
        """
        
        seg = net.list_of_LongProfile_objects[ID]
        x_max = seg.x_ext[0].max()
        x_min = seg.x_ext[0].min()
        y = ys[ID]

        for other_topo_length in segs_by_topo_length.keys():
            for other_ID in segs_by_topo_length[other_topo_length]:
                if other_ID != ID:
                    
                    other_seg = net.list_of_LongProfile_objects[other_ID]
                    other_x_max = other_seg.x_ext[0].max()
                    other_x_min = other_seg.x_ext[0].min()
                    other_y = ys[other_ID]
                    
                    if (
                        (other_x_min <= x_min <= other_x_max) or 
                        (other_x_min <= x_max <= other_x_max)
                        ):
                        if y == other_y:
                            return other_ID
                    
                    if other_seg.downstream_segment_IDs:
                        down_y = ys[other_seg.downstream_segment_IDs[0]]
                        if (
                            (x_min <= other_x_max <= x_max) and
                            (min(other_y,down_y) <= y <= max(other_y,down_y))
                            ):
                            return other_ID
                    
                    # # Don't think I need this bit...
                    # if seg.downstream_segment_IDs:
                    #     down_ID = seg.downstream_segment_IDs[0]
                    #     if down_ID != other_ID:
                    #         down_y = ys[down_ID]
                    #         if (
                    #             (other_x_min <= x_max <= other_x_max) and 
                    #             (min(y,down_y) <= other_y <= max(y,down_y))
                    #             ):
                    #             return other_ID
                            
        return False

    def create_planform(net, ys):
        """
        Generate the final x and y coordinates to plot.
        """
        
        planform = {}
        for i,seg in enumerate(net.list_of_LongProfile_objects):
            if not seg.downstream_segment_IDs:
                x = np.hstack(( seg.x, seg.x_ext[0][-1], seg.x_ext[0][-1] ))/1000.
                y = np.hstack(( np.full(len(seg.x),ys[i]), ys[i], ys[i] ))
            else:
                x = np.hstack(( seg.x, seg.x_ext[0][-1], seg.x_ext[0][-1] ))/1000.
                y = np.hstack(( 
                    np.full(len(seg.x),ys[i]), 
                    ys[i], 
                    ys[seg.downstream_segment_IDs[0]]
                    ))
            planform[i] = {'x': x, 'y': y}
        return planform
        
    def plot_planform(planform):
        """
        Plot the planform.
        """
        
        for i in planform:
            plt.plot(planform[i]['x'], planform[i]['y'])
        plt.show()
            
    # ---- Organise segments by distance upstream (topological length)
    # Used later to check for conflicts between segments.
    segs_by_topo_length = {0: [], net.max_topological_length+2: []}
    for i in range(1,net.max_topological_length+2):
        segs_by_topo_length[i] = []
    for i,seg in enumerate(net.list_of_LongProfile_objects):
        topo_length = len(net.find_downstream_IDs(seg.ID))
        segs_by_topo_length[topo_length].append(seg.ID)
    
    # ---- Set up arrays to fill
    ys = np.full( len(net.list_of_LongProfile_objects), np.nan )
    sides = np.full( len(net.list_of_LongProfile_objects), 0)
    up_sides = np.full( len(net.list_of_LongProfile_objects), -1)
    connections = [
        [np.nan,np.nan] for i in range(len(net.list_of_LongProfile_objects))
        ]
    
    # ---- Loop over segments building planform
    for i,seg in enumerate(net.list_of_LongProfile_objects):
        
        # ---- Check if outlet
        if not seg.downstream_segment_IDs:
            ys[i] = 0.
            connections[i][1] = copy.copy(ys[i])
        
        # ---- Otherwise, add segment on to downstream one
        else:
            
            # Some info about the segment
            down_ID = seg.downstream_segment_IDs[0]
            topo_length = len(net.find_downstream_IDs(seg.ID))

            # Add segment based on relationship to downstream segment
            # Record what side of downstream segment the segment is on
            # Update "up_sides" so that next segment goes on the other side
            ys[i] = ys[down_ID] + up_sides[down_ID]
            sides[i] = copy.copy(up_sides[down_ID])
            up_sides[down_ID] *= -1
            
            # Check for conflict
            conflicting_id = check_for_segment_conflicts(
                seg.ID, segs_by_topo_length, net, ys)
            
            # If there is a conflict, move downstream until reaching a segment
            # with the right direction to fix the conflict
            if conflicting_id:
                seg_to_adjust = seg.ID
                if seg.x.max() >= net.list_of_LongProfile_objects[conflicting_id].x.max():
                    while sides[conflicting_id] != sides[seg_to_adjust]:
                        seg_to_adjust = (
                            net.list_of_LongProfile_objects[seg_to_adjust]. \
                            downstream_segment_IDs[0])
                else:
                    while sides[seg.ID] == sides[seg_to_adjust]:
                        seg_to_adjust = (
                            net.list_of_LongProfile_objects[seg_to_adjust]. \
                            downstream_segment_IDs[0])
            
            # Move everything upstream of that segment out the way until the
            # conflict is addressed
            while check_for_segment_conflicts(
                seg.ID, segs_by_topo_length, net, ys):
                up_IDs_down_ID = net.find_upstream_IDs(seg_to_adjust)
                ys[up_IDs_down_ID] += sides[seg_to_adjust]

    # ---- Get everything starting from zero and positive
    ys -= ys.min() - 1.

    # ---- Create final planform
    planform = create_planform(net, ys)
    if show:
        plot_planform(planform)

    return planform





net, net_topo = grlp.generate_random_network(
    magnitude=40,
    max_length=100.e3,
    segment_length=sts.gamma(2., scale=1./2.),
    approx_dx=5.e2,
    min_nxs=5,
    mean_discharge=10.,
    segment_length_area_ratio=1,
    supply_area=1,
    sediment_discharge_ratio= 1.e4,
    mean_width=10.,
    variable_width=False,
    topology=None,
    evolve=False
    )
net.compute_network_properties()






# sweep_nets, sweep_hacks, sweep_gains, sweep_lags = grlpx.read_sweep(
#     "../output/network/m40_rnd_seg_length_no_internal/"
#     )
# 
__ = plot_network(net)






