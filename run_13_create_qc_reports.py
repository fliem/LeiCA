
__author__ = 'franzliem'
import os
import shutil

import numpy as np
import pandas as pd
from nipype.pipeline.engine import Node, Workflow
import nipype.interfaces.utility as util

from utils import get_condor_exit_status, check_if_wf_crashed, load_subjects_list
from qc_reports.create_qc_report_pdf import create_qc_report_pdf
from variables import ds_dir, report_base_dir, subjects_dir
from variables import TR_list, full_subjects_list, subjects_file_prefix
from variables import plugin_name, use_n_procs


#fixme
plugin_name = 'MultiProc'
use_n_procs = 25


subjects_list = full_subjects_list
subjects_missing_files_list = load_subjects_list(subjects_dir, subjects_file_prefix + '_excluded.txt')


report_str = 'rsfMRI_preprocessing'


wf = Workflow('qc_reports_wf')
wf.base_dir = report_base_dir
wf.config['execution']['crashdump_dir'] = os.path.join(report_base_dir, 'crash')
wf.config['execution']['stop_on_first_crash'] = False

# collect dfs
df = pd.DataFrame()


for TR in TR_list:
    rel_report_dir = os.path.join(report_str + '_TR_%s'%TR)
    os.chdir(report_base_dir)
    if os.path.isdir(rel_report_dir):
        shutil.rmtree(rel_report_dir)
    os.mkdir(rel_report_dir)
    os.chdir(rel_report_dir)
    os.mkdir('reports')

    for subject_id in subjects_list:
        print(subject_id)
        df_ss_file = os.path.join(ds_dir, subject_id, 'rsfMRI_preprocessing/QC/df', 'TR_%s'%TR, 'qc_values.pkl')
        #fixme
        if os.path.exists(df_ss_file):
            df_ss = pd.read_pickle(df_ss_file)
        else:
            header = ['subject_id', 'similarity_epi_struct', 'similarity_struct_MNI', 'mean_FD_Power', 'n_spikes',
                      'median_tsnr']
            data = np.hstack( (subject_id, np.repeat(np.nan, len(header)-1)))
            df_ss = pd.DataFrame([data], columns=header)
            df_ss = df_ss.set_index(df_ss.subject_id)


        # link to report pdf:
        rel_report_dir = os.path.join(report_str + '_TR_%s'%TR)
        subject_reports_dir = os.path.join(rel_report_dir, 'reports')
        report_file = os.path.join(subject_reports_dir, subject_id + '.pdf')
        df_ss['report_file'] = report_file

        # get condor exit status
        batch_dir =os.path.join(ds_dir, subject_id, 'condor', 'LeiCA_resting_preprocessing', 'batch')
        if os.path.exists(batch_dir):
            condor_exitcode, condor_n_jobs_failed = get_condor_exit_status(batch_dir)
        else:
            condor_exitcode = np.nan
            condor_n_jobs_failed = np.nan
        df_ss['condor_exitcode'] = condor_exitcode
        df_ss['condor_n_jobs_failed'] = condor_n_jobs_failed


        # check if wf has crashed
        crash_dir = os.path.join(ds_dir, subject_id, 'condor', 'LeiCA_resting_preprocessing', 'crash')
        wf_crashed = check_if_wf_crashed(crash_dir)
        df_ss['wf_crashed'] = wf_crashed

        ######

        df = pd.concat([df, df_ss])

    df.to_pickle('group.QC.pkl')
    df.to_csv('group.QC.csv', sep='\t')
    df.to_excel('group.QC.xlsx')

    # CREAT FILE THAT CAN BE USED TO EDIT & MARK BAD QC SUBJECTS
    all_subjects_list = subjects_list + subjects_missing_files_list
    header = ['subject_excluded','reason', 'comment']
    n_good = len(subjects_list)
    n_bad = len(subjects_missing_files_list)
    subject_excluded = np.concatenate((np.zeros(n_good),np.ones(n_bad)))
    reason = ['']*n_good + ['files missing']*n_bad
    comment = ['']*n_good + ['automatically excluded before analysis']*n_bad
    data = {'subject_excluded':subject_excluded, 'reason':reason, 'comment':comment}
    df_to_edit = pd.DataFrame(data, columns=header, index=all_subjects_list)
    df_to_edit.to_excel('group.QC.to_edit.xlsx') #.csv', sep='\t')



for TR in TR_list:
    print ('***********')
    print('TR: %s'%TR)
    print ('***********')
    rel_report_dir = os.path.join(report_str + '_TR_%s'%TR)
    subject_reports_dir = os.path.join(report_base_dir, rel_report_dir, 'reports')
    os.chdir(subject_reports_dir)

    for subject_id in subjects_list:
        print('%s generate report'%subject_id)
        file_dict = {}
        file_dict['report_file'] = os.path.join(subject_reports_dir, subject_id + '.pdf')
        file_dict['mean_epi'] = os.path.join(ds_dir, subject_id, 'rsfMRI_preprocessing/QC/initial_mean_epi_moco/TR_%s/initial_mean_epi_moco.nii.gz'%TR)
        file_dict['brain_mask_epiSpace'] = os.path.join(ds_dir, subject_id, 'rsfMRI_preprocessing/masks/brain_mask_epiSpace/TR_%s/brain_mask_epiSpace.nii.gz'%TR)
        file_dict['csf_mask_epiSpace'] = os.path.join(ds_dir, subject_id, 'rsfMRI_preprocessing/masks/csf_mask_lat_ventr_epiSpace/TR_%s/csf_mask_epiSpace.nii.gz'%TR)
        file_dict['wm_mask_epiSpace'] = os.path.join(ds_dir, subject_id, 'rsfMRI_preprocessing/masks/wm_mask_epiSpace/TR_%s/wm_mask_epiSpace.nii.gz'%TR)
        file_dict['tsnr'] = os.path.join(ds_dir, subject_id, 'rsfMRI_preprocessing/QC/tsnr/TR_%s/tsnr.nii.gz'%TR)
        file_dict['subject_tsnr_np_file'] = os.path.join(ds_dir, subject_id, 'rsfMRI_preprocessing/QC/tsnr/TR_%s/tsnr.npy'%TR)
        file_dict['struct_brain_epiSpace'] = os.path.join(ds_dir, subject_id, 'rsfMRI_preprocessing/QC/struct_brain_epiSpace/TR_%s/struct_brain_epiSpace.nii.gz'%TR)
        file_dict['slices_epi_structSpace'] = os.path.join(ds_dir, subject_id, 'rsfMRI_preprocessing/QC/slices/epi_structSpace/TR_%s/slices.png'%TR)
        file_dict['slices_struct_MNIspace'] = os.path.join(ds_dir, subject_id, 'rsfMRI_preprocessing/QC/slices/struct_MNIspace/slices.png')
        file_dict['slices_epi_MNIspace'] = os.path.join(ds_dir, subject_id, 'rsfMRI_preprocessing/QC/slices/epi_MNIspace/TR_%s/slices.png'%TR)
        file_dict['FD_ts'] = os.path.join(ds_dir, subject_id, 'rsfMRI_preprocessing/QC/FD/FD_ts/TR_%s/FD.1D'%TR)


        # CHECK IF ALL FILES EXIST
        def check_if_out_files_exist(check_file_dict):
            for file in check_file_dict.values():
                if not os.path.exists(file):
                    raise Exception('file missing: %s'%file)

        check_file_dict = file_dict.copy()
        check_file_dict.pop('report_file')
        check_if_out_files_exist(check_file_dict)

        report = Node(util.Function(input_names=['subject_id', 'file_dict', 'df'],
                                    output_names=[],
                                    function=create_qc_report_pdf),
                      name='report_%s_%s'%(TR, subject_id))
        report.inputs.subject_id = subject_id
        report.inputs.file_dict = file_dict
        report.inputs.df = df

        wf.add_nodes([report])

# fixme
# ignore warning from np.rank
import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    if plugin_name == 'CondorDAGMan':
        wf.run(plugin=plugin_name)
    if plugin_name == 'MultiProc':
        wf.run(plugin=plugin_name, plugin_args={'n_procs': use_n_procs})
