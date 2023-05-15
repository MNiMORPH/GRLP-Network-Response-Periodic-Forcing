from grlp import *
from extras import *
from copy import deepcopy
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap

from bokeh.io import curdoc
from bokeh.layouts import column, row, gridplot
from bokeh.models import ColumnDataSource, Slider, TextInput
from bokeh.plotting import figure

# ---- River properties
x0 = 10.e3
L = 100.e3
mean_Qw = 10.
mean_Qs = 0.001
B = 98.1202038813591
hack_p = 1./0.55 # Hack
lp = set_up_long_profile(L, mean_Qw, mean_Qs, hack_p, B, dx=1.e2, evolve=True)


# ---- Evolve
lp_Qs = deepcopy(lp)
lp_Qw = deepcopy(lp)
Qw_x = deepcopy(lp.Q)
mean_Qs0 = deepcopy(lp.Q_s_0)
mean_ssd = deepcopy(lp.ssd)
mean_ssd_Qs = deepcopy(lp.Q_s)
mean_slope = deepcopy(lp.S)
period = lp.equilibration_time
A = 0.2
time = np.arange(0., 6.*period, period/1000.)
scale = 1. + A*np.sin(2.*np.pi*time/period)
z = np.zeros((len(time), len(lp.x)))
slope = np.zeros((len(time), len(lp.x)))
Qs = np.zeros((len(time), len(lp.x)))
z_Qw = np.zeros((len(time), len(lp.x)))
Qs_Qw = np.zeros((len(time), len(lp.x)))
for j,s in enumerate(scale):

    lp_Qs.set_Qs_input_upstream(mean_Qs0 * s)
    lp_Qs.set_source_sink_distributed(mean_ssd * s)
    lp_Qs.evolve_threshold_width_river(nt=1, dt=period/1000.)
    lp_Qs.compute_Q_s()
    z[j,:] = lp_Qs.z.copy()
    slope[j,:] = lp_Qs.S.copy()
    Qs[j,:] = lp_Qs.Q_s.copy()

    lp_Qw.set_Q(Qw_x * s)
    lp_Qw.evolve_threshold_width_river(nt=1, dt=period/1000.)
    lp_Qw.compute_Q_s()
    z_Qw[j,:] = lp_Qw.z.copy()
    Qs_Qw[j,:] = lp_Qw.Q_s.copy()

G_zs = (z[4000:,:].max(axis=0) - z[4000:,:].min(axis=0)) / \
    (2. * A * (L - lp.x) * (mean_Qs/(lp.k_Qs*mean_Qw))**(6./7.))
G_Qss = (Qs[4000:,:].max(axis=0) - Qs[4000:,:].min(axis=0)) / \
    (2. * A * mean_ssd_Qs)
G_Qs_Qws = (Qs_Qw[4000:,:].max(axis=0) - Qs_Qw[4000:,:].min(axis=0)) / \
    (2. * A * mean_ssd_Qs)

lag_zs = find_lag_times_x_corr(z[2000:,:], scale[2000:], time[:4000], period) / period
lag_Qss = find_lag_times_x_corr(Qs[2000:,:], scale[2000:], time[:4000], period) / period
lag_Qs_Qws = find_lag_times_x_corr(Qs_Qw[2000:,:], scale[2000:], time[:4000], period) / period



p = figure(x_axis_label='Time [kyr]', y_axis_label='Qs / Qs0')
Qs0_line = ColumnDataSource(data=dict(x=time/3.15e10, y=scale))
Qs_line = ColumnDataSource(data=dict(x=time/3.15e10, y=Qs[:,0]/mean_ssd_Qs[0]))
slope_line = ColumnDataSource(data=dict(x=time/3.15e10, y=slope[:,0]/mean_slope[0]))
t_circ = ColumnDataSource(data=dict(x=[0],y=[Qs[0,0]/mean_ssd_Qs[0]]))
p.line('x', 'y', source=Qs0_line, line_width=4)
p.line('x', 'y', source=Qs_line, line_dash="4 4", line_color="red", line_width=4)
p.line('x', 'y', source=slope_line, line_dash="2 2", line_color="grey", line_width=4)
p.circle('x', 'y', source=t_circ, radius=10)

p2 = figure(x_axis_label='Distance [km]', y_axis_label='Elevation [km]')
z_line = ColumnDataSource(data=dict(x=lp.x/1000., y=lp.z))
z_ss_line = ColumnDataSource(data=dict(x=lp.x/1000., y=lp.z))
z_circ = ColumnDataSource(data=dict(x=[lp.x[0]/1000.],y=[lp.z[0]]))
p2.line('x', 'y', source=z_line, line_width=4)
p2.line('x', 'y', source=z_ss_line, line_width=4, line_color="grey", line_dash="4 4")
p2.circle('x', 'y', source=z_circ, radius=1)

p3 = figure(x_axis_label='Distance [km]', y_axis_label='Gain')
G_line = ColumnDataSource(data=dict(x=lp.x/1000., y=G_zs))
G_circ = ColumnDataSource(data=dict(x=[lp.x[0]/1000.],y=[G_zs[0]]))
p3.line('x', 'y', source=G_line, line_width=4)
p3.circle('x', 'y', source=G_circ, radius=1)

p4 = figure(x_axis_label='Distance [km]', y_axis_label='Lag')
lag_line = ColumnDataSource(data=dict(x=lp.x/1000., y=lag_zs))
lag_circ = ColumnDataSource(data=dict(x=[lp.x[0]/1000.],y=[lag_zs[0]]))
p4.line('x', 'y', source=lag_line, line_width=4)
p4.circle('x', 'y', source=lag_circ, radius=1)


dist_slider = Slider(start=lp.x.min()/1000., end=lp.x.max()/1000., value=lp.x.min()/1000., step=0.1, title="Downstream distance [km]")
def update_dist(attrname, old, new):

    i = int(dist_slider.value*10)-1
    x = time/3.15e10
    y = Qs[:,i]/mean_ssd_Qs[i]
    y2 = slope[:,i]/mean_slope[i]
    Qs_line.data = dict(x=x, y=y)
    slope_line.data = dict(x=x, y=y2)
    
    t = int(time_slider.value * 3.15e10 / period * 1000)    
    x3 = [lp.x[i]/1000.]
    y3 = [z[t,i]]
    z_circ.data = dict(x=x3, y=y3)
    
    y4 = [G_zs[i]]
    G_circ.data = dict(x=x3, y=y4)
    
    y5 = [lag_zs[i]]
    lag_circ.data = dict(x=x3, y=y5)
dist_slider.on_change('value', update_dist)

time_slider = Slider(start=0., end=time[-1]/3.15e10, value=0., step=0.1, title="Time [kyr]")
def update_time(attr, old, new):
    t = int(time_slider.value * 3.15e10 / period * 1000)
    x = [time[t]/3.15e10]
    y = [scale[t]]
    t_circ.data = dict(x=x,y=y)
    
    i = int(dist_slider.value*10)-1
    x2 = lp.x/1000.
    y2 = z[t,:]
    z_line.data = dict(x=x2, y=y2)
    
    x3 = [lp.x[i]/1000.]
    y3 = [z[t,i]]
    z_circ.data = dict(x=x3, y=y3)
time_slider.on_change('value', update_time)

col1 = column(dist_slider,time_slider,p)
col2 = column(p2)
rows = row(col1, col2)
grid = gridplot([[dist_slider, time_slider, None, None], [p, p2, p3, p4]])
# show(column(dist,p))
curdoc().add_root(grid)
# curdoc().title = "Sliders"