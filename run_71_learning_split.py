import os
import pandas as pd

# # LeiCA modules
from LeiCA_LIFE.learning.learning_predict_data_wf import learning_predict_data_2samp_wf
from variables_learning import in_data_name_list, subjects_selection_crit_dict, \
    subjects_selection_crit_names_list, target_list

wd_root_path = PATH
ds_root_path = PATH

working_dir = os.path.join(wd_root_path, 'wd_learning')
ds_dir = os.path.join(ds_root_path, 'learning_out')
aggregated_subjects_dir = os.path.join(ds_dir, 'vectorized_aggregated_data')

use_n_procs = 5
plugin_name = 'MultiProc'

# in_data_name_list = [['msdl_abide_BP']]

learning_predict_data_2samp_wf(working_dir=working_dir,
                               ds_dir=ds_dir,
                               in_data_name_list=in_data_name_list,
                               subjects_selection_crit_dict=subjects_selection_crit_dict,
                               subjects_selection_crit_names_list=subjects_selection_crit_names_list,
                               aggregated_subjects_dir=aggregated_subjects_dir,
                               target_list=target_list,
                               use_n_procs=use_n_procs,
                               plugin_name=plugin_name,
                               confound_regression=[False],
                               run_cv=True,
                               n_jobs_cv=5,
                               run_tuning=False,
                               run_2sample_training=False,
                               aggregated_subjects_dir_nki=None,
                               subjects_selection_crit_dict_nki=None,
                               subjects_selection_crit_name_nki=None)
