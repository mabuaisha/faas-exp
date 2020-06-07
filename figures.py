import numpy as np
import matplotlib.pyplot as plt


def plot_figure(
        k8s,
        nomad,
        swarm,
        metric,
        xlabel,
        xtick_labels,
        figure_path
):
    ind = np.arange(len(xtick_labels))
    width = 0.27

    fig = plt.figure()
    ax = fig.add_subplot(111)

    k8s_rects = ax.bar(ind, k8s, width, color='r')
    nomad_rects = ax.bar(ind+width, nomad, width, color='g')
    swarm_rects = ax.bar(ind+width*2, swarm, width, color='b')

    ax.set_ylabel('{0} (Median)'.format(metric))
    ax.set_xlabel(xlabel)
    ax.set_xticks(ind+width)
    ax.set_xticklabels(xtick_labels)
    ax.legend(
        (k8s_rects[0], nomad_rects[0], swarm_rects[0]),
        ('k8s', 'nomad', 'swarm')
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
    _auto_label(nomad_rects)
    _auto_label(swarm_rects)

    plt.savefig('{0}.png'.format(figure_path))
    plt.close(fig)
