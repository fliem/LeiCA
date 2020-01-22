'''
'''
import os
from LeiCA_LIFE.freesurfer.downsample_surfs import downsampel_surfs
from variables import full_subjects_list

metrics_root_path =PATH
wd_root_path =PATH

subjects_list = full_subjects_list
#fixme
subjects_list = subjects_list[300:]

working_dir_base = os.path.join(wd_root_path, 'wd_fs')
ds_dir_base = os.path.join(metrics_root_path, 'metrics')

fresurfer_dir = PATH


use_n_procs = 1
#plugin_name = 'MultiProc'
plugin_name = 'CondorDAGMan'


for subject_id in subjects_list:
    working_dir = os.path.join(working_dir_base, subject_id)
    ds_dir = os.path.join(ds_dir_base, subject_id)
    print('\nsubmitting %s'%subject_id)
    downsampel_surfs(subject_id=subject_id,
                     working_dir=working_dir,
                     freesurfer_dir=fresurfer_dir,
                     ds_dir=ds_dir,
                     plugin_name=plugin_name,
                     use_n_procs=use_n_procs)
