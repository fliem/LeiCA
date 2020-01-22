__author__ = 'franzliem'


def create_qc_report_pdf(subject_id, file_dict, df):

    import gc
    import pylab as plt
    from matplotlib.backends.backend_pdf import PdfPages
    from collections import OrderedDict
    import numpy as np

    from qc_reports.qc_plots import plot_2_distributions, include_png, plot_motion
    from qc_reports.volumes import plot_mosaic


    report = PdfPages(file_dict['report_file'])

    fig = plot_mosaic(file_dict['mean_epi'], title='%s\nMean EPI'%subject_id, figsize=(8.3, 11.7)) #r'\textbf{%s}\nMean EPI'
    report.savefig(fig, dpi=300)
    fig.clf()
    plt.close()

    fig = plot_mosaic(file_dict['mean_epi'], title="Mean EPI w brain mask", overlay_mask=file_dict['brain_mask_epiSpace'], figsize=(8.3, 11.7))
    report.savefig(fig, dpi=300)
    fig.clf()
    plt.close()

    fig = plot_mosaic(file_dict['tsnr'], title="tSNR", figsize=(8.3, 11.7))
    report.savefig(fig, dpi=300)
    fig.clf()
    plt.close()

    fig = plot_mosaic(file_dict['struct_brain_epiSpace'], title="CSF mask", overlay_mask=file_dict['csf_mask_epiSpace'],bright_mask=True, figsize=(8.3, 11.7))
    report.savefig(fig, dpi=300)
    fig.clf()
    plt.close()

    fig = plot_mosaic(file_dict['struct_brain_epiSpace'], title="WM mask", overlay_mask=file_dict['wm_mask_epiSpace'],bright_mask=True, figsize=(8.3, 11.7))
    report.savefig(fig, dpi=300)
    fig.clf()
    plt.close()

    data1 = np.load(file_dict['subject_tsnr_np_file'])
    data2 = df['median_tsnr']
    xlabel1 = 'subject %s: tSNR inside mask' % subject_id
    xlabel2 = 'median tSNR over subjects'
    subject_value2 = df.at[subject_id, 'median_tsnr']
    subject_value_label2 = '%s\n median tsnr ='%subject_id
    fig = plot_2_distributions(data1, xlabel1, data2,  xlabel2,
                               subject_value2=subject_value2, subject_value_label2=subject_value_label2,
                               title='tSNR')
    report.savefig(fig, dpi=300)
    fig.clf()
    plt.close()


    data1 = df['similarity_epi_struct']
    data2 = df['similarity_struct_MNI']
    xlabel1 = 'similarity: epi -> struct'
    xlabel2 = 'similarity: struct -> MNI'
    subject_value1 = df.at[subject_id, 'similarity_epi_struct']
    subject_value2 = df.at[subject_id, 'similarity_struct_MNI']
    subject_value_label1 = '%s\n similarity ='%subject_id
    subject_value_label2 = '%s\n similarity ='%subject_id
    fig = plot_2_distributions(data1, xlabel1, data2,  xlabel2,
                               subject_value1=subject_value1, subject_value_label1=subject_value_label1,
                               subject_value2=subject_value2, subject_value_label2=subject_value_label2,
                               title='Similarity')
    report.savefig(fig, dpi=300)
    fig.clf()
    plt.close()


    FD_ts = np.genfromtxt(file_dict['FD_ts'])
    mean_FD_distribution = df['mean_FD_Power']
    n_spikes = df.at[subject_id, 'n_spikes']
    spikes_distribution = df['n_spikes']
    fig = plot_motion(FD_ts, mean_FD_distribution, n_spikes, spikes_distribution, title='Motion')
    report.savefig(fig, dpi=300)
    fig.clf()
    plt.close()



    slices_dict = OrderedDict()
    slices_dict['slices_epi_structSpace'] = file_dict['slices_epi_structSpace']
    slices_dict['slices_struct_MNIspace'] = file_dict['slices_struct_MNIspace']
    slices_dict['slices_epi_MNIspace']= file_dict['slices_epi_MNIspace']

    for slices_name, slices_file in slices_dict.items():
        fig = include_png(slices_file, slices_name)
        report.savefig(fig)
        fig.clf()
        plt.close()

    report.close()
    gc.collect()
    plt.close()


