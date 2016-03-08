#!/usr/bin/env python3

from collections import namedtuple
from colour.plotting import CIE_1931_chromaticity_diagram_plot
import matplotlib.pyplot as plt
from pandas import read_csv
from numpy  import array, transpose

def readpattern(filename):
    value = array(read_csv(filename))
    return transpose(value)

Blackbody = readpattern('./datasets/BlackBody_xy.csv')
CIE_1931_chromaticity_diagram_plot(standalone = False)

legend = dict()
ColorPoint = namedtuple('ColorPoint', ['x', 'y', 'label'])
legend['ro'] = ColorPoint(0.464, 0.523, 'LE174-H00-N50-2A CW7 DOE')
legend['mo'] = ColorPoint(0.511, 0.477, 'LE174-H00-N30 (PC Cover CW8) DOE')
legend['bo'] = ColorPoint(0.531, 0.464, 'LE174-H00-N30-2A CW9 DOE')
legend['wo'] = ColorPoint(0.562, 0.432, 'PC Converted Amber LED')
legend['co'] = ColorPoint(0.450, 0.410, '3000K Blackbody Source')
legend['go'] = ColorPoint(0.350, 0.355, '5000K Blackbody Source')

def createPlot(**legend):
    plt.xlabel('x', fontsize=20)
    plt.ylabel('y', fontsize=20)
    plt.tick_params(axis='x', labelsize=15)
    plt.tick_params(axis='y', labelsize=15)

    for key in legend:
        point = legend[key]
        plt.plot(point.x, point.y, key,
                 markersize=10,
                 label=point.label)

    plt.plot(Blackbody[0], Blackbody[1], '--', color = 'black', linewidth = 0.5)

    plt.grid(True)
    plt.legend(loc=1, fontsize=15, numpoints=1)
    plt.xlim(-.1,.9), plt.ylim(-.1,.9)

    plt.show()

createPlot(**legend)
