from sfepy.mechanics.matcoefs import stiffness_from_youngpoisson_mixed
import numpy as np

filename_mesh = 'iso_time_field.mesh'


h = 1.5
T0 = 20
kc = 2

materials = {
    'k': ({'val': kc },),
    'h': ({'val': -h},),
    'f': ({'val': T0},),
}

def get_circle_outer(coors, domain=None):
    r = np.sqrt(coors[:,0]**2.0 + coors[:,1]**2.0)
    return np.where(r > 3.9)[0]


def get_circle_inner(coors, domain=None):
    r = np.sqrt(coors[:,0]**2.0 + (coors[:,1]-1.0)**2.0)
    return np.where(r < 1.1)[0]

functions = {
    'get_out_cir' : (get_circle_outer,),
    'get_in_cir' : (get_circle_inner,),
}


regions = {
    'Omega': 'all',
    'OutCircle' : ('vertices by get_out_cir','facet'),
    'InCircle' : ('vertices by get_in_cir','facet'),
}


fields = {
    'heating': ('real', 1, 'Omega', 1)
}

variables = {
    't': ('unknown field', 'heating', 0),
    's': ('test field', 'heating', 't'),
}

ebcs = {
    't1': ('InCircle', {'t.0': 140}),
}

integrals = {
    'i':  2,
}


equations = {
    'Temperature': """dw_laplace.i.Omega(k.val, s, t ) = dw_bc_newton.i.OutCircle(h.val, f.val, s, t)""",
}

solvers = {
    'ls': ('ls.scipy_direct', {}),
    'newton': ('nls.newton',
               {'i_max': 1,
                'eps_a': 1e-6,
                'eps_r': 1.0,
                })
}

options = {
    'nls' : 'newton',
    'ls' : 'ls',
}


# TODO - the answer is of the same magnitude as in the book, but solution needs verification