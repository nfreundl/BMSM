# -*- coding: utf-8 -*-
"""
Created on Wed May 20 15:51:40 2015

@author: peterkroon
"""
#import fitter
from symfit.api import exp, cos, Variable, Parameter, Fit
import symfit.contrib
import numpy as np
import functools
import matplotlib.pyplot as plt
import argparse
import os
import inspect

kb = 8.3144621e-3  # kJ/mol/K
T = 298


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


def boltzmann(T, V, *args, **kwargs):
    kbT = kb * T
    return exp(-V(*args, **kwargs)/kbT)


def harmonic(x, x0, k):
    return 0.5 * k * (x - x0)**2


def periodic(x, x0, k, n):
    return k*(1+cos(n*x - x0))


funcs = {'harmonic': harmonic, 'periodic': periodic}


def file_readable(file):
    if not os.access(file, os.F_OK | os.R_OK):
        raise argparse.ArgumentTypeError("{} is not readable or does not exist.".format(file))
    return file


parser = argparse.ArgumentParser(description="Fit a function to data.")


parser.add_argument('-f', help='(input) XVG file containing the data to fit to',
                    required=True, metavar='data.xvg', type=file_readable, dest='xvg_file')
function_group = parser.add_mutually_exclusive_group(required=True)

function_group.add_argument('--harmonic', help='use an harmonic functional (V(x) = 0.5 * k * (x - x0)**2)', action='store_const', const=harmonic, dest='func')
function_group.add_argument('--periodic', help='use an periodic functional (V(x) = k * (1 + cos(n*x - x0)))', action='store_const', const=periodic, dest='func')
x0 = parser.add_argument('-x0', help='equilibrium value.', required=True,
                    type=float, dest='x0')
k = parser.add_argument('-k', help='force constant.', required=True,
                    type=float, dest='k')
parser.add_argument('-mink', help='(opt.) minimum value allowed for k.', required=False, default=0, type=float, metavar=0)
parser.add_argument('-maxk', help='(opt.) maximum value allowed for k.', required=False, default=None, type=float, metavar='2*k')
n = parser.add_argument('-n', help='(opt.) periodicity for periodic function.',
                    required=False, type=int, dest='n', metavar=1)
parser.add_argument('--radians', '-rad', help='(opt.) specify whether x0 and the x-axis in your data should be converted to radians. This is usually the case for all angles.',
                    required=False, action='store_const', const=np.pi/180, default=1, dest='factor')
parser.add_argument('-T', help='(opt.) temperature (K).',
                    required=False, default=298, type=float, dest='T', metavar=298)
args = parser.parse_args()

if args.maxk is None:
    args.maxk = args.k * 2

if args.n is None:
    del args.n

if 'n' not in inspect.getargspec(args.func).args and hasattr(args, 'n'):
    raise argparse.ArgumentError(n, 'This function type does not accept -n.')

if not hasattr(args, 'n') and 'n' in inspect.getargspec(args.func).args:
    args.n = 1



data = read_xvg(args.xvg_file)

xs = data[:, 0]
ys = data[:, 1]
ys = ys/np.max(ys)  # Normalize data


harmonic_distribution = functools.partial(boltzmann, args.T, args.func)

argument_dict = {}
x = Variable() * args.factor
x0 = Parameter(value=args.x0, min=np.min(xs), max=np.max(xs)) * args.factor
k = Parameter(value=args.k, min=args.mink, max=args.maxk)
argument_dict['x'] = x
argument_dict['x0'] = x0
argument_dict['k'] = k
if hasattr(args, 'n'):
    n = Parameter(value=args.n, min=0, max=args.n * 2, fixed=True)
    argument_dict['n'] = n



model = harmonic_distribution(**argument_dict)
#fit = fitter.InteractiveFit2D(model, xs, ys)
guess = symfit.contrib.interactive_guess.interactive_guess.InteractiveGuess2D(model, xs, ys) 
#fit.visual_guess(1000)
#result = fit.execute(maxfev=1000)
result = guess.execute()

fit = Fit(model, xs, ys)
result = fit.execute()

print(result)

plt.scatter(xs, ys, color='b')
plt.plot(xs, model(x=xs, **result.params), color='r')
plt.show()
#
#angs = np.array(range(-180, 181), dtype=np.float64)
#probs = model(th=angs, **result.params)
#
#potentials = -kb*T*np.log(probs)
#print(potentials)
#
#potentials[potentials == np.inf] = 50
##print(potentials)
#deriv = -np.gradient(potentials)
#
#table = np.array((angs, potentials, deriv)).T
#print(table)
#plt.plot(angs, potentials)
#plt.show()
#tableoutname = 's_s_bb_ss_table.xvg'
#
#with open(tableoutname, 'w') as tableout:
#    for angle, pot, der in table:
#        print(angle, pot, der)
#        tableout.write("{:3.0f} {:8.3f} {:8.3f}\n".format(angle, pot, der))
##    tableout.write("{:d} {:8.3f} {:8.3f}\n".format(180, potentials[-1], deriv[-1]))
