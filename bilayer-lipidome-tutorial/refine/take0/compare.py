#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import scipy.interpolate
import matplotlib.pyplot as plt
from sys import argv

INTERPOLATION_ORDER = 'cubic'  # Specifies the kind of interpolation as a string (‘linear’, \
#  ‘nearest’, ‘zero’, ‘slinear’, ‘quadratic, ‘cubic’ where ‘slinear’, ‘quadratic’ and ‘cubic’\ 
#  refer to a spline interpolation of first, second or third order) or as an integer specifying\
#  the order of the spline interpolator to use.
INTERPOLATION_POINTS = 2000


def read_xvg(file_name):
    #return np.loadtxt(file_name, comments = '@', dtype=np.float)
    #Let's assume simply tabulated data for now (x y\nx y\nx y...)
    data = []
    comment_chars = ('#', '@')
    with open(file_name, 'r') as file_handle:
        for line in file_handle:
            line = split_comments(line, comment_chars)[0].strip()
            if not line:
                continue
            data.append(list(map(float, line.split())))
    return np.array(data, dtype=float)


def split_comments(line, comment_chars):
    find = lambda char: (line.find(char), char) if char in line else (len(line), char)
    comment_start, char = min(map(find, comment_chars), key=lambda x: x[0])
    return line[:comment_start], line[comment_start + len(char):]


def R_squared(x1, y1, x2, y2):
    min_x = max((np.min(x1), np.min(x2)))
    max_x = min((np.max(x1), np.max(x2)))
    interp_x = np.linspace(min_x, max_x, INTERPOLATION_POINTS)

    interp_y1 = scipy.interpolate.interp1d(x1, y1, kind=INTERPOLATION_ORDER)(interp_x)
    interp_y2 = scipy.interpolate.interp1d(x2, y2, kind=INTERPOLATION_ORDER)(interp_x)

    ss_y1 = np.sum((interp_y1 - np.mean(interp_y1))**2)
    ss_diff = np.sum((interp_y1-interp_y2)**2)
    return 1 - (ss_diff/ss_y1)


def compare(data1, data2, color, show=False):
    x = data2[:, 0]
    y = data2[:, 1]

    interp_x = np.linspace(np.min(x), np.max(x), INTERPOLATION_POINTS)
    f = scipy.interpolate.interp1d(x, y, kind=INTERPOLATION_ORDER)

    plt.plot(data1[:, 0], data1[:, 1], 'bo')  # blue dots
    plt.plot(interp_x, f(interp_x), color=color, linestyle='-')
    if show:
        plt.show()
    return R_squared(data1[:, 0], data1[:, 1], x, y)

reference = read_xvg(argv[1])

other_data = []
names = []

for filename in argv[2:]:
    other_data.append(read_xvg(filename))
    names.append(filename)

colors = ('red', 'green', 'cyan', 'magenta', 'black', 'yellow')  # Not blue

print('R-squared is:')
for data, color, name in zip(other_data, colors, names):
    R = compare(reference, data, color)
    print('{} ({}): {}'.format(name, color, R))

plt.show()
