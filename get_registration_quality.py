


import pandas as pd
import numpy as np
from scipy import stats

import seaborn as sns
import os


from variables import working_dir, fig_dir, subjects_list

out_dir = os.path.join(fig_dir, 'registrations_comparison')
if not os.path.isdir(out_dir):
    os.mkdir(out_dir)

regs_list = ['bbr', 'flirt6', 'flirt7','flirt9', 'flirt12', 'flirt6MI', 'bbrMI']
metrics_list = ['mi','nmi','cr']

def read_reg_file(in_file, subject_id):
    print in_file
    d = np.genfromtxt(in_file)
    mi, nmi, cr = d
    numdata = np.concatenate([mi, nmi, cr])
    data = [subject_id]
    data += list(numdata)
    header = ['ID']
    for m in metrics_list:
        for r in regs_list:
            header += [r + '_' + m]
    #print header
    #print data
    df = pd.DataFrame(data=data) #, columns=header)
    df = df.T
    df.columns = header
    df = df.set_index(df.ID)
    return df




df = pd.DataFrame()

for subject in subjects_list:
    in_file = os.path.join(working_dir, 'LeiCA_resting/rsfMRI_preproc_wf/registration/_TR_id_645/_subject_id_' + subject,'write_file/similarity.txt')
    df_ss = read_reg_file(in_file, subject)
    df = pd.concat([df, df_ss])
    
df.to_pickle(os.path.join(out_dir, 'registrations_similarity_df.pkl'))



for m in metrics_list:
    header = []
    for r in regs_list:
        header += [r + '_' + m]
    #print df[header]
    b = sns.boxplot(df[header], names=regs_list, join_rm=True)
    b.set(title=m.upper())
    fig = b.get_figure()
    fig.savefig(os.path.join(out_dir, m + '.png'))
    b.set(ylim=(0, None))
    fig = b.get_figure()
    fig.savefig(os.path.join(out_dir, m + '_0ax.png'))
    fig.clear()



#sns.boxplot([.2, .5])

