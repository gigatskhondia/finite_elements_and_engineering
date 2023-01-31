import numpy as nm

# TODO - the answer is not the same as in the book

filename_mesh = 'p11_5.mesh'

num = 96/(2*6)*2*0.5  # sink is shared by more than one element

materials = {
    'k': ({'val': 0.018},),
    'coef': ({'val': 0.05},),
    'M':({'val':0.0034},),
    'S': ({'val': -0.017},),
}

regions = {
    'Omega' : 'all', 
    'Gamma_Left': ('vertices in (x < 0.00001)', 'facet'),
    'Gamma_Right': ('vertices in (x > 1.99999)', 'facet'),
    'Gamma_Down': ('vertices in (y < 0.00001)', 'facet'),
    'Gamma_Up': ('vertices in (y > 5.99999)', 'facet'),
    'Source': 'vertices in (y > 3.0)&(y<5.5)&(x>0)&(x<1.0)',
}

fields = {
    'heating': ('real', 1, 'Omega', 1)
}

variables = {
    't': ('unknown field', 'heating', 0),
    's': ('test field', 'heating', 't'),
}

ebcs = {
    # 't1': ('Gamma_Left', {'t.0': 200}),
    # 't2': ('Gamma_Right', {'t.0': 200}),
    # 't3': ('Gamma_Up', {'t.0': -5}),
    't4': ('Gamma_Down', {'t.0': 0}),
}

integrals = {
    'i':  2,
}

equations = {
    'Temperature': """dw_laplace.i.Omega(k.val, s, t ) -
     dw_volume_integrate.i.Source(coef.val, s) = dw_integrate.i.Gamma_Up(-M.val*t+S.val, s)""",
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

