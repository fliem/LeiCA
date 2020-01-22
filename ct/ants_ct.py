def ants_ct_wf(subjects_id,
            preprocessed_data_dir,
            working_dir,
            ds_dir,
            template_dir,
            plugin_name):
    import os
    from nipype import config
    from nipype.pipeline.engine import Node, Workflow, MapNode
    import nipype.interfaces.utility as util
    import nipype.interfaces.io as nio
    from nipype.interfaces.freesurfer.utils import ImageInfo



    #####################################
    # GENERAL SETTINGS
    #####################################
    wf = Workflow(name='ants_ct')
    wf.base_dir = os.path.join(working_dir)

    nipype_cfg = dict(logging=dict(workflow_level='DEBUG'), execution={'stop_on_first_crash': True,
                                                                       'remove_unnecessary_outputs': True,
                                                                       'job_finished_timeout': 120})
    config.update_config(nipype_cfg)
    wf.config['execution']['crashdump_dir'] = os.path.join(working_dir, 'crash')

    ds = Node(nio.DataSink(base_directory=ds_dir), name='ds')



    #####################################
    # GET DATA
    #####################################
    # GET SUBJECT SPECIFIC STRUCTURAL DATA
    in_data_templates = {
        't1w': '{subject_id}/raw_niftis/sMRI/t1w_reoriented.nii.gz',
    }

    in_data = Node(nio.SelectFiles(in_data_templates,
                                       base_directory=preprocessed_data_dir),
                       name="in_data")
    in_data.inputs.subject_id = subjects_id


    # GET NKI ANTs templates
    ants_templates_templates = {
        'brain_template': 'NKI/T_template.nii.gz',
        'brain_probability_mask': 'NKI/T_templateProbabilityMask.nii.gz',
        'segmentation_priors': 'NKI/Priors/*.nii.gz',
        't1_registration_template': 'NKI/T_template_BrainCerebellum.nii.gz'

    }

    ants_templates = Node(nio.SelectFiles(ants_templates_templates,
                                       base_directory=template_dir),
                       name="ants_templates")

