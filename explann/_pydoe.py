import numpy as np
from pyDOE.doe_star import star
from pyDOE.doe_union import union
from pyDOE.doe_repeat_center import repeat_center


def fullfact(levels):
    """
    Create a general full-factorial design
    
    Parameters
    ----------
    levels : array-like
        An array of integers that indicate the number of levels of each input
        design factor.
    
    Returns
    -------
    mat : 2d-array
        The design matrix with coded levels 0 to k-1 for a k-level factor
    
    Example
    -------
    ::
    
        >>> fullfact([2, 4, 3])
        array([[ 0.,  0.,  0.],
               [ 1.,  0.,  0.],
               [ 0.,  1.,  0.],
               [ 1.,  1.,  0.],
               [ 0.,  2.,  0.],
               [ 1.,  2.,  0.],
               [ 0.,  3.,  0.],
               [ 1.,  3.,  0.],
               [ 0.,  0.,  1.],
               [ 1.,  0.,  1.],
               [ 0.,  1.,  1.],
               [ 1.,  1.,  1.],
               [ 0.,  2.,  1.],
               [ 1.,  2.,  1.],
               [ 0.,  3.,  1.],
               [ 1.,  3.,  1.],
               [ 0.,  0.,  2.],
               [ 1.,  0.,  2.],
               [ 0.,  1.,  2.],
               [ 1.,  1.,  2.],
               [ 0.,  2.,  2.],
               [ 1.,  2.,  2.],
               [ 0.,  3.,  2.],
               [ 1.,  3.,  2.]])
               
    """
    n = len(levels)  # number of factors
    nb_lines = np.prod(levels)  # number of trial conditions
    H = np.zeros((nb_lines, n))
    
    level_repeat = 1
    range_repeat = np.prod(levels)
    for i in range(n):
        range_repeat /= levels[i]
        lvl = []
        for j in range(levels[i]):
            lvl += [j]*level_repeat
        rng = lvl*int(range_repeat)
        level_repeat *= levels[i]
        H[:, i] = rng
     
    return H

def ff2n(n):
    """
    Create a 2-Level full-factorial design
    
    Parameters
    ----------
    n : int
        The number of factors in the design.
    
    Returns
    -------
    mat : 2d-array
        The design matrix with coded levels -1 and 1
    
    Example
    -------
    ::
    
        >>> ff2n(3)
        array([[-1., -1., -1.],
               [ 1., -1., -1.],
               [-1.,  1., -1.],
               [ 1.,  1., -1.],
               [-1., -1.,  1.],
               [ 1., -1.,  1.],
               [-1.,  1.,  1.],
               [ 1.,  1.,  1.]])
       
    """
    return 2*fullfact([2]*n) - 1

def ccdesign(n, center=(4, 4), alpha='orthogonal', face='circumscribed'):
    """
    Central composite design
    
    Parameters
    ----------
    n : int
        The number of factors in the design.
    
    Optional
    --------
    center : int array
        A 1-by-2 array of integers, the number of center points in each block
        of the design. (Default: (4, 4)).
    alpha : str
        A string describing the effect of alpha has on the variance. ``alpha``
        can take on the following values:
        
        1. 'orthogonal' or 'o' (Default)
        
        2. 'rotatable' or 'r'
        
    face : str
        The relation between the start points and the corner (factorial) points.
        There are three options for this input:
        
        1. 'circumscribed' or 'ccc': This is the original form of the central
           composite design. The star points are at some distance ``alpha``
           from the center, based on the properties desired for the design.
           The start points establish new extremes for the low and high
           settings for all factors. These designs have circular, spherical,
           or hyperspherical symmetry and require 5 levels for each factor.
           Augmenting an existing factorial or resolution V fractional 
           factorial design with star points can produce this design.
        
        2. 'inscribed' or 'cci': For those situations in which the limits
           specified for factor settings are truly limits, the CCI design
           uses the factors settings as the star points and creates a factorial
           or fractional factorial design within those limits (in other words,
           a CCI design is a scaled down CCC design with each factor level of
           the CCC design divided by ``alpha`` to generate the CCI design).
           This design also requires 5 levels of each factor.
        
        3. 'faced' or 'ccf': In this design, the star points are at the center
           of each face of the factorial space, so ``alpha`` = 1. This 
           variety requires 3 levels of each factor. Augmenting an existing 
           factorial or resolution V design with appropriate star points can 
           also produce this design.
    
    Notes
    -----
    - Fractional factorial designs are not (yet) available here.
    - 'ccc' and 'cci' can be rotatable design, but 'ccf' cannot.
    - If ``face`` is specified, while ``alpha`` is not, then the default value
      of ``alpha`` is 'orthogonal'.
        
    Returns
    -------
    mat : 2d-array
        The design matrix with coded levels -1 and 1
    
    Example
    -------
    ::
    
        >>> ccdesign(3)
        array([[-1.        , -1.        , -1.        ],
               [ 1.        , -1.        , -1.        ],
               [-1.        ,  1.        , -1.        ],
               [ 1.        ,  1.        , -1.        ],
               [-1.        , -1.        ,  1.        ],
               [ 1.        , -1.        ,  1.        ],
               [-1.        ,  1.        ,  1.        ],
               [ 1.        ,  1.        ,  1.        ],
               [ 0.        ,  0.        ,  0.        ],
               [ 0.        ,  0.        ,  0.        ],
               [ 0.        ,  0.        ,  0.        ],
               [ 0.        ,  0.        ,  0.        ],
               [-1.82574186,  0.        ,  0.        ],
               [ 1.82574186,  0.        ,  0.        ],
               [ 0.        , -1.82574186,  0.        ],
               [ 0.        ,  1.82574186,  0.        ],
               [ 0.        ,  0.        , -1.82574186],
               [ 0.        ,  0.        ,  1.82574186],
               [ 0.        ,  0.        ,  0.        ],
               [ 0.        ,  0.        ,  0.        ],
               [ 0.        ,  0.        ,  0.        ],
               [ 0.        ,  0.        ,  0.        ]])
        
       
    """
    # Check inputs
    assert isinstance(n, int) and n>1, '"n" must be an integer greater than 1.'
    assert alpha.lower() in ('orthogonal', 'o', 'rotatable', 
        'r'), 'Invalid value for "alpha": {:}'.format(alpha)
    assert face.lower() in ('circumscribed', 'ccc', 'inscribed', 'cci',
        'faced', 'ccf'), 'Invalid value for "face": {:}'.format(face)
    
    try:
        nc = len(center)
    except:
        raise TypeError('Invalid value for "center": {:}. Expected a 1-by-2 array.'.format(center))
    else:
        if nc!=2:
            raise ValueError('Invalid number of values for "center" (expected 2, but got {:})'.format(nc))

    # Orthogonal Design
    if alpha.lower() in ('orthogonal', 'o'):
        H2, a = star(n, alpha='orthogonal', center=center)
    
    # Rotatable Design
    if alpha.lower() in ('rotatable', 'r'):
        H2, a = star(n, alpha='rotatable')
    
    # Inscribed CCD
    if face.lower() in ('inscribed', 'cci'):
        H1 = ff2n(n)
        H1 = H1/a  # Scale down the factorial points
        H2, a = star(n)
    
    # Faced CCD
    if face.lower() in ('faced', 'ccf'):
        H2, a = star(n)  # Value of alpha is always 1 in Faced CCD
        H1 = ff2n(n)
    
    # Circumscribed CCD
    if face.lower() in ('circumscribed', 'ccc'):
        H1 = ff2n(n)
    
    C1 = repeat_center(n, center[0])
    C2 = repeat_center(n, center[1])

    H1 = union(H1, C1)
    H2 = union(H2, C2)
    H = union(H1, H2)

    return H