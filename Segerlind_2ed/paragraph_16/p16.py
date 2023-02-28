filename_mesh = 'p16.mesh'

num = 160/(20*15)*2*2  # sink is shared by more than one element

materials = {
    'D1': ({'val': 2},),
    'coef_s': ({'val': -200/num},),
    'D2': ({'val': 5},),
    'coef': ({'val': 5},),
    'M': ({'val': 2},),
    'S': ({'val': -10/2},),
}

regions = {
    
    'Omega1': 'vertices in (y >=0)&(y<=15)&(x>=0)&(x<10)',
    'Omega2': 'vertices in (y >=0)&(y<=15)&(x>=10)&(x<=20)',
    'Gamma_Left1': ('vertices in (x < 0.00001)', 'facet'),
    'Gamma_Right1': ('vertices in (x > 9.99999)', 'facet'),
    'Gamma_Left2': ('vertices in (x < 10.00001)', 'facet'),
    'Gamma_Right2': ('vertices in (x > 19.99999)', 'facet'),
    'Gamma_Down': ('vertices in (y < 0.00001)', 'facet'),
    'Gamma_Up': ('vertices in (y > 14.99999)', 'facet'),
    # 'Source': 'cell 21',
    'Source1': 'vertices in (y > 3)&(y<7)&(x>6)&(x<10)',
    'Source2': 'vertices in (y > 3)&(y<7)&(x>10)&(x<14)',
}

fields = {
    'temperature1': ('real', 1, 'Omega1', 1),
    'temperature2': ('real', 1, 'Omega2', 1),
}


variables = {
    't1': ('unknown field', 'temperature1', 0),
    's1': ('test field', 'temperature1', 't1'),
    't2': ('unknown field', 'temperature2', 1),
    's2': ('test field', 'temperature2', 't2'),
}

ebcs = {
    'T1': ('Gamma_Left1', {'t1.0': 20}),
    'T2': ('Gamma_Up', {'t1.0': 0, 't2.0': 0}),
    'T3': ('Gamma_Down', {'t1.0': 0, 't2.0': 0})
}

integrals = {
    'i':  2,
}

equations = {
     'komp1': """dw_laplace.i.Omega1(D1.val, s1, t1 ) +
      dw_volume_integrate.i.Source1(coef_s.val, s1) = 0""",
     'komp2': """dw_laplace.i.Omega2(D2.val, s2, t2 ) 
     = dw_bc_newton.i.Gamma_Right2(M.val, S.val, s2, t2)""",
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
    # 'split_results_by': 'region',
}

# TODO - the answer is not the same as in the book
# TODO - the left material does not see the right material
