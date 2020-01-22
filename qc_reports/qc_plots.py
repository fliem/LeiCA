__author__ = 'franzliem'



import pylab as plt
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec
from matplotlib.backends.backend_pdf import FigureCanvasPdf as FigureCanvas
import seaborn as sns


def include_png(in_file, title=None, figsize=(11.7,8.3)):
    fig = plt.figure(figsize=figsize)
    img = plt.imread(in_file)
    plt.imshow(img)
    plt.grid(False)
    plt.tick_params(labelbottom='off', labeltop='off', labelleft='off', labelright='off')
    plt.title(title, fontsize='10')
    plt.close()
    return fig


def plot_vline(cur_val, label, ax):
    ax.axvline(cur_val)
    ylim = ax.get_ylim()
    vloc = (ylim[0] + ylim[1]) / 2.0
    xlim = ax.get_xlim()
    pad = (xlim[0] + xlim[1]) / 100.0
    ax.text(cur_val - pad, vloc, label, color="blue", rotation=90, verticalalignment='center', horizontalalignment='right')

def plot_distribution_of_values(ax, distribution, xlabel, subject_value=None, subject_value_label=''):


    h = sns.distplot(distribution, kde=None, ax=ax)
    ax.set_xlabel(xlabel)
    if subject_value:
        label = "%s %g"%(subject_value_label, subject_value)
        plot_vline(subject_value, label, ax=ax)
    return h

def plot_2_distributions(distribution1,  xlabel1, distribution2,  xlabel2, subject_value1=None, subject_value_label1='',
                           subject_value2=None, subject_value_label2='', title='', figsize=(8.3, 7)):

    fig = Figure(figsize=figsize)
    FigureCanvas(fig)

    gs = GridSpec(2, 1)
    ax = fig.add_subplot(gs[0, 0])
    plot_distribution_of_values(ax, distribution1, xlabel1, subject_value=subject_value1, subject_value_label=subject_value_label1)
    ax = fig.add_subplot(gs[1, 0])
    plot_distribution_of_values(ax, distribution2, xlabel2, subject_value=subject_value2, subject_value_label=subject_value_label2)
    fig.suptitle(title)
    return fig

def plot_motion(FD_ts, mean_FD_distribution, n_spikes, spikes_distribution, title='', figsize=(8.3, 10)):

    fig = Figure(figsize=figsize)
    FigureCanvas(fig)

    grid = GridSpec(3, 4)


    ax = fig.add_subplot(grid[0,:-1])
    ax.plot(FD_ts)
    ax.set_xlim((0, len(FD_ts)))
    ax.set_ylabel("Frame Displacement [mm]")
    ax.set_xlabel("Frame number")
    ylim = ax.get_ylim()

    ax = fig.add_subplot(grid[0,-1])
    sns.distplot(FD_ts, vertical=True, ax=ax)
    ax.set_ylim(ylim)


    ax = fig.add_subplot(grid[1,:])
    sns.distplot(mean_FD_distribution, kde=None, ax=ax)


    ax.set_xlabel("Mean Frame Dispalcement (over all subjects) [mm]")
    MeanFD = FD_ts.mean()
    label = "MeanFD = %g"%MeanFD
    plot_vline(MeanFD, label, ax=ax)

    ax = fig.add_subplot(grid[2,:])
    sns.distplot(spikes_distribution, ax=ax)
    ax.set_xlabel("n Spikes (over all subjects)")
    label = "n_spikes = %g"%n_spikes
    plot_vline(n_spikes, label, ax=ax)

    fig.suptitle(title)
    return fig


