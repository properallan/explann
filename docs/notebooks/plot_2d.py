import pyvista as pv
import numpy as np

def plot_property(prop, unseeing_path, surrogate_solution, hfdh, clim=None, solid=True):
    pv.set_jupyter_backend("static")

    p = pv.Plotter(shape=(1, 3), notebook=True, border=False, line_smoothing=True, window_size=[1800,600])

    p.subplot(0, 0)
    
    unseeing=pv.read(unseeing_path)
    
    p.add_mesh(unseeing[0][0][0], scalars= f'{prop}', clim=clim, scalar_bar_args={'title': f'{prop}', 'width' : 0.75})
    if solid: p.add_mesh(unseeing[1][0][0], scalars= f'{prop}', clim=clim, scalar_bar_args={'title': f'{prop}', 'width' : 0.75})

    p.view_xy()
    
    clear_unseeing=pv.read(unseeing_path)
    clear_unseeing[0][0][0].clear_data()
    if solid:clear_unseeing[1][0][0].clear_data()

    clear_unseeing[0][0][0][f'{prop}']=hfdh(surrogate_solution)[f'{prop}']
    if solid: clear_unseeing[1][0][0][f'{prop}']=hfdh(surrogate_solution)[f'{prop}_Solid']

    p.subplot(0, 1)

    p.add_mesh(clear_unseeing[0][0][0], scalars=f'{prop}', clim=clim, scalar_bar_args={'title':  f'{prop} Surrogate', 'width' : 0.75})
    if solid: p.add_mesh(clear_unseeing[1][0][0], scalars=f'{prop}', clim=clim, scalar_bar_args={'title':  f'{prop} Surrogate', 'width' : 0.75})

    p.view_xy()

    error=pv.read(unseeing_path)
    error[0][0][0].clear_data()
    error[1][0][0].clear_data()
    
    error[0][0][0][f'{prop}']=np.abs(unseeing[0][0][0][f'{prop}']-clear_unseeing[0][0][0][f'{prop}'])
    if solid: error[1][0][0][f'{prop}']=np.abs(unseeing[1][0][0][f'{prop}']-clear_unseeing[1][0][0][f'{prop}'])

    p.subplot(0, 2)

    p.add_mesh(error[0][0][0], scalars=f'{prop}', clim=clim, scalar_bar_args={'title': 'Absolute Error', 'width' : 0.75})
    if solid: p.add_mesh(error[1][0][0], scalars=f'{prop}', clim=clim, scalar_bar_args={'title': 'Absolute Error', 'width' : 0.75})

    p.view_xy()

    p.show()
