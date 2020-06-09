import numpy as np
import matplotlib.pyplot as plt


def plot_bar_figure(
        k8s,
        nomad,
        swarm,
        ylabel,
        xlabel,
        xtick_labels,
        figure_path
):
    ind = np.arange(len(xtick_labels))
    width = 0.27

    fig = plt.figure()
    ax = fig.add_subplot(111)
    k8s_rects = ax.bar(ind, k8s, width, color='r')
    if nomad:
        nomad_rects = ax.bar(ind + width, nomad, width, color='g')
    swarm_rects = ax.bar(ind + width * 2, swarm, width, color='b')

    legend_title = ('k8s', 'swarm')
    if nomad:
        legend_title = ('k8s', 'nomad', 'swarm',)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_xticks(ind + width)
    ax.set_xticklabels(xtick_labels)
    ax.legend(
        legend_title,
        bbox_to_anchor=(0, 1.05, 1, 0.2), loc="lower left",
        fancybox=True, shadow=True, ncol=5, mode="expand"
    )

    def _auto_label(rects):
        for rect in rects:
            h = rect.get_height()
            ax.text(
                rect.get_x() + rect.get_width() / 2.,
                1.05 * h, '%d' % int(h),
                ha='center', va='bottom'
            )

    _auto_label(k8s_rects)
    if nomad:
        _auto_label(nomad_rects)
    _auto_label(swarm_rects)

    plt.savefig('{0}.png'.format(figure_path))
    plt.close(fig)
