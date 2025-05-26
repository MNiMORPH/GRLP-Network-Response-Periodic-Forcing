import numpy as np
import grlp

# ---- Set up LongProfile object for access to standard parameter values
lp = grlp.LongProfile()
lp.basic_constants()
lp.bedload_lumped_constants()
lp.set_hydrologic_constants()


# ---- Properties to specify

# Geometry
x0 = 50.e3
L = 100.e3

# Hack's law
# Global mean values from He et al. (2024), converted to m & m^2
p__x_A = 1./0.54
k__x_A = 2.1*1.e3/(1.e6**0.54)

# Hydrology
P = 1.e3 / 1.e3 / 3.154e7 # precipitation rate in m/s
C_R = 0.4 # runoff coefficient

# Ratio of sediment to water discharge
Qs_to_Q = 1.e-4

# Desired equilibration time
Teq = 100. * 3.154e10


# ---- Properties to calculate

# Compute average discharge with precipitation rate, runoff coefficient,
# Hack's law, geometry. Sediment discharge then some fraction.
Q_mean = P * C_R * k__x_A * ((L+x0)**(p__x_A+1.) - x0**(p__x_A+1.)) / (L * (p__x_A+1.))
Qs_mean = Q_mean * Qs_to_Q

# Use length and desired equilibration time to get mean width.
diffusivity = L**2. / Teq
S0 = (Qs_mean/(lp.k_Qs*Q_mean))**(6./7.)
B_mean = (
    (7./6.) * (lp.k_Qs * Q_mean * S0**(1./6.)) / 
    (diffusivity * (1. - lp.lambda_p))
    )


# ---- Print
print("Mean discharge, Q = %f m3/s" % Q_mean)
print("Mean sediment discharge, Qs = %f m3/s" % Qs_mean)
print("Mean width, B = %f m" % B_mean)