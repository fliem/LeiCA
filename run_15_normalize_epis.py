__author__ = 'franzliem'
'''
how to run

'''


import os

# # LeiCA modules
from preprocessing import normalize

from variables import working_dir, ds_dir, preprocessed_data_dir, template_dir
from variables import full_subjects_list, TR_list
# from variables import use_n_procs, plugin_name

#fixme
full_subjects_list=full_subjects_list[400:]
##############################

working_dir = "PATH"
preprocessed_data_dir = "PATH"
ref_file = "PATH"
ds_dir ="PATH"
##############################

use_n_procs = 50
plugin_name = 'MultiProc'
# plugin_name = 'CondorDAGMan'

# fixme
# ignore warning from np.rank
import warnings

selectfiles_templates = {
    'epi_2_MNI_warp': '{subject_id}/rsfMRI_preprocessing/registration/epi_2_MNI_warp/TR_{TR_id}/*.nii.gz',
    'preproc_epi_full_spectrum': '{subject_id}/rsfMRI_preprocessing/epis/01_denoised/TR_{TR_id}/*.nii.gz',
    'preproc_epi_bp_tNorm': '{subject_id}/rsfMRI_preprocessing/epis/03_denoised_BP_tNorm/TR_{TR_id}/*.nii.gz',
}

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    normalize.normalize_epi(subjects_list=full_subjects_list,
                            TR_list=TR_list,
                            preprocessed_data_dir=preprocessed_data_dir,
                            selectfiles_templates=selectfiles_templates,
                            ref_file=ref_file,
                            working_dir=working_dir,
                            ds_dir=ds_dir,
                            plugin_name=plugin_name,
                            use_n_procs=use_n_procs)
