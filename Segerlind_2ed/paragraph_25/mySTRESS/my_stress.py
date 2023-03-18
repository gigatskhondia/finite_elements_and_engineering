from sfepy.mechanics.matcoefs import stiffness_from_youngpoisson_mixed

filename_mesh = 'my_stress.mesh'

materials = {
    'solid': ({'D': stiffness_from_youngpoisson_mixed(dim=2, young=20e6, poisson=0.25, plane='stress')},),
    'load': ({'.coef': [0,  -150000]},),
}

regions = {
    'Omega': 'all',
    'Top1' : ('vertices in (y > 29.99) & (x<1)', 'vertex'),
    'Top2': ('vertices in (y > 29.99) & (x>9) & (x<11)', 'vertex'),
    'bottom': ('vertices in (y < 0.1)', 'vertex'),
    'left': ('vertices in (x < 0.1)', 'vertex'),
}

fields = {
    'displacement': ('real', 'vector', 'Omega', 1),

}

variables = {
    'u': ('unknown field', 'displacement', 0),
    'v': ('test field', 'displacement', 'u'),
}

ebcs = {
    'Fixed1': ('bottom', {'u.1': 0.0}),
    'Fixed2': ('left', {'u.0': 0.0}),
}

integrals = {
    'i':  2,
    'i0': 0
}

equations = {
     'balance_of_forces' : """dw_lin_elastic.i.Omega(solid.D, v, u) = dw_point_load.i0.Top1(load.coef, v)
    + dw_point_load.i0.Top2(load.coef, v)""",
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
    'nls': 'newton',
    'ls': 'ls',
}

# TODO - the answer is not the same as in the book (although at the same orders of magnitude as in the book results)
