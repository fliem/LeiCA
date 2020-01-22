''' 
Adaptation of  https://github.com/juhuntenburg/mriqc/blob/lsd_lemon/mriqc/volumes.py
'''

import math
import os
import time
import nibabel as nb
import numpy as np
import seaborn as sns
from matplotlib.figure import Figure
from pylab import cm
from matplotlib.gridspec import GridSpec
from matplotlib.backends.backend_pdf import FigureCanvasPdf as FigureCanvas
import pylab as plt

def _calc_rows_columns(ratio, n_images):
    rows = 1
    for _ in range(100):
        columns = math.floor(ratio * rows)
        total = rows * columns
        if total > n_images:
            break

        columns = math.ceil(ratio * rows)
        total = rows * columns
        if total > n_images:
            break
        rows += 1
    return rows, columns

def plot_mosaic(nifti_file, title=None, overlay_mask=None, bright_mask=False, figsize=(11.7,8.3)):
    if isinstance(nifti_file,str):
        nii = nb.load(nifti_file)
        mean_data = nii.get_data()
    else:
        mean_data = nifti_file
   
    n_images = mean_data.shape[2]
    row, col = _calc_rows_columns(figsize[0]/figsize[1], n_images)
    
    if overlay_mask:
        overlay_data = nb.load(overlay_mask).get_data()

    # create figures
    fig = Figure(figsize=figsize)
    FigureCanvas(fig)
    
    fig.subplots_adjust(top=0.85)
    for image in (range(n_images)):
        ax = fig.add_subplot(row, col, image+1)
        data_mask = np.logical_not(np.isnan(mean_data))
        if overlay_mask:
            ax.set_rasterized(True)
        ax.imshow(np.fliplr(mean_data[:,:,image].T), vmin=np.percentile(mean_data[data_mask], 0.5), 
                   vmax=np.percentile(mean_data[data_mask],99.5), 
                   cmap=cm.Greys_r, interpolation='nearest', origin='lower')  # @UndefinedVariable
        if overlay_mask:
            overlay_data[overlay_data==0]=np.nan
            if bright_mask:
                cmap = cm.rainbow
                cmap._init()
            else:
                cmap = cm.Reds #rainbow #cool #Reds  # @UndefinedVariable
                cmap._init()
                alphas = np.linspace(0, 0.75, cmap.N+3)
                cmap._lut[:,-1] = alphas
            ax.imshow(np.fliplr(overlay_data[:,:,image].T), vmin=0, vmax=1,
                   cmap=cmap, interpolation='nearest', origin='lower')  # @UndefinedVariable
            
        ax.axis('off')
    fig.subplots_adjust(left = 0.05, right = 0.95, bottom = 0.05, top = 0.95, wspace=0.01, hspace=0.1)
    
    if not title:
        _, title = os.path.split(nifti_file)
        title += " (last modified: %s)"%time.ctime(os.path.getmtime(nifti_file))
    fig.suptitle(title, fontsize='13', fontweight='bold')
    
    return fig
    
    
def _get_values_inside_a_mask(main_file, mask_file):
    main_nii = nb.load(main_file)
    main_data = main_nii.get_data()
    nan_mask = np.logical_not(np.isnan(main_data))
    mask = nb.load(mask_file).get_data() > 0
    
    data = main_data[np.logical_and(nan_mask, mask)]
    return data

def get_median_distribution(main_files, mask_files):
    medians = []
    for main_file, mask_file in zip(main_files, mask_files):
        med = np.median(_get_values_inside_a_mask(main_file, mask_file))
        medians.append(med)
    return medians

