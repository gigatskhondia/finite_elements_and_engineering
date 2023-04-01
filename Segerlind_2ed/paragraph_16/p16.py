import numpy as np

filename_mesh = 'p16.mesh'

num = 1209/(20*15-10*5/2)*1*1  # sink is shared by more than one element

materials = {
    'D1': ({'val': 2},),
    'coef': ({'val': -200/num},),
    'D2': ({'val': 5},),
    'M': ({'val': -2},),
    'S': ({'val': 10/2},),
}


def incline(coors, domain=None):
    shift=0.5

    X=coors[:,0]
    Y=coors[:,1]
    
    y = -2*X + 45-shift
    
    return np.where(Y>y)[0]


functions = {
    'my_incline': (incline,),
}


regions = {
    
    'Omega' : 'all',
    'Omega_Left': 'vertices in (x<=10)',
    'Omega_Right': 'vertices in (x>10)',
    
    'Gamma_Left_B': ('vertices in (x < 0.00001)', 'facet'),
    'Gamma_Right_B': ('vertices in (x > 19.99999)', 'facet'),
    'Gamma_Inc': ('vertices by my_incline', 'facet'),
    
    'Source': 'vertices in (y > 4.5)&(y<5.5)&(x>9.5)&(x<10.5)',
}

fields = {
    'temperature': ('real', 1, 'Omega', 1),
}


variables = {
    't': ('unknown field', 'temperature', 0),
    's': ('test field', 'temperature', 't'),
}

ebcs = {
    'T1': ('Gamma_Left_B', {'t.0': 20}),
}

integrals = {
    'i':  2,
}

equations = {
      'Temperature': """dw_laplace.i.Omega_Left(D1.val, s, t ) +
      dw_laplace.i.Omega_Right(D2.val, s, t )+
      dw_volume_integrate.i.Source(coef.val, s) = 
      dw_bc_newton.i.Gamma_Right_B(M.val, S.val, s, t)+
      dw_bc_newton.i.Gamma_Inc(M.val, S.val, s, t)""",
  
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

# TODO - the answer is not the same as in the book, although on the same order of magnitude
