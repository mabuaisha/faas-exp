import numpy as np
import matplotlib.pyplot as plt

N = 4
ind = np.arange(N)  # the x locations for the groups
width = 0.27       # the width of the bars

fig = plt.figure()
ax = fig.add_subplot(111)

yvals = [4, 9, 2, 5]
rects1 = ax.bar(ind, yvals, width, color='r')
zvals = [1,2,3, 6]
rects2 = ax.bar(ind+width, zvals, width, color='g')
kvals = [11,12,13, 40]
rects3 = ax.bar(ind+width*2, kvals, width, color='b')

ax.set_ylabel('Response Time (Median)')
ax.set_xlabel('Replicas')
ax.set_xticks(ind+width)
ax.set_xticklabels( ('5', '10', '20') )
ax.legend( (rects1[0], rects2[0], rects3[0]), ('k8s', 'swarm', 'nomad') )


def autolabel(rects):
    for rect in rects:
        h = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*h, '%d'%int(h),
                ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)
autolabel(rects3)

plt.show()