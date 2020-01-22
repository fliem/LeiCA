'''
wd ca 170MB/subj
'''

# fixme
# check tr in fullspectrum (for bp this is not important, scince only afni is getting tr from header

import os
from LeiCA_LIFE.metrics.calc_metrics import calc_local_metrics
from variables import full_subjects_list

subjects_list = full_subjects_list

brain_mask = 'PATH/Templates/MNI_resampled_brain_mask.nii'
template_dir = 'PATH/templates/parcellations'
in_data_root_path = 'PATH/results'
metrics_root_path = 'PATH/metrics'
wd_root_path = 'PATH/LeiCA_NKI_wd'
selectfiles_templates = {
    'epi_MNI_BP': '{subject_id}/rsfMRI_preprocessing/epis_MNI_3mm/03_denoised_BP_tNorm/TR_645/residual_filt_norm_warp.nii.gz',
    'epi_MNI_fullspectrum': '{subject_id}/rsfMRI_preprocessing/epis_MNI_3mm/01_denoised/TR_645/preprocessed_fullspectrum_MNI_3mm.nii.gz',
    'moco_parms_file': '{subject_id}/rsfMRI_preprocessing/QC/rest_realigned.nii.gz.par',
    'jenkinson_file': '{subject_id}/rsfMRI_preprocessing/QC/rest_realigned.nii.gz_rel.rms',
    'rest2anat_cost_file': '{subject_id}/rsfMRI_preprocessing/QC/similarity/struct_MNI/similarity.txt',
}

working_dir_base = os.path.join(wd_root_path, 'wd_metrics')
ds_dir_base = os.path.join(metrics_root_path)

# con mat parameters
bp_freq_list = [(0.01, 0.1)]
TR = 0.645

parcellations_dict = {}
parcellations_dict['craddock_205'] = {
    'nii_path': os.path.join(template_dir,
                             'craddock_2012/scorr_mean_single_resolution/scorr_mean_parc_n_21_k_205_rois.nii.gz'),
    'is_probabilistic': False}

parcellations_dict['craddock_788'] = {
    'nii_path': os.path.join(template_dir,
                             'craddock_2012/scorr_mean_single_resolution/scorr_mean_parc_n_43_k_788_rois.nii.gz'),
    'is_probabilistic': False}

parcellations_dict['gordon'] = {
    'nii_path': os.path.join(template_dir,
                             'Gordon_2014_Parcels/Parcels_MNI_111_sorted.nii.gz'),
    'is_probabilistic': False}

parcellations_dict['msdl_abide'] = {
    'nii_path': os.path.join(template_dir,
                             'msdl_abide_2016/MSDL_ABIDE/maps.nii'),
    'is_probabilistic': True}

use_n_procs = 5
# plugin_name = 'MultiProc'
plugin_name = 'CondorDAGMan'

for subject_id in subjects_list:
    working_dir = os.path.join(working_dir_base, subject_id)
    ds_dir = os.path.join(ds_dir_base, subject_id)

    print('\n\nsubmitting %s' % subject_id)
    calc_local_metrics(brain_mask=brain_mask,
                       preprocessed_data_dir=in_data_root_path,
                       subject_id=subject_id,
                       parcellations_dict=parcellations_dict,
                       bp_freq_list=bp_freq_list,
                       TR=TR,
                       selectfiles_templates=selectfiles_templates,
                       working_dir=working_dir,
                       ds_dir=ds_dir,
                       use_n_procs=use_n_procs,
                       plugin_name=plugin_name)
