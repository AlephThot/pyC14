# -*- coding: utf-8 -*-

"""

    Part of the pyC14 scripts set, used to calibrate C14 data.

    @author Christophe Le Bourlot, MATEIS - INSA LYON - UMR CNRS 5510 
    @date 10/01/2014
    @version 0.1

    Copyright © 2014 INSA Lyon - MATEIS

    This file is part of pyC14.

    pyC14 is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    pyC14 is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with pyC14.  If not, see <http://www.gnu.org/licenses/>.

"""


from __future__ import print_function

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

from pylab import normpdf

import numpy as np

from ...pyC14 import OxCalData, Calibration


def plot(ocd,
        calib,
        file_name = "test.jpg",
        use_model = True):

    fig = plt.figure(figsize=(8,2))
    ax1 = plt.subplot(111)
    plt.ylabel("C14 age (BP)", fontsize=11)

    plt.text(-0.14, -0.11,"Date (BC)",
         horizontalalignment='left',
         verticalalignment='bottom',
         transform = ax1.transAxes,
         size=11)

    plt.text(0.0, 0.97,"pyC14 v0.1; Xtof; Ard-team",
         horizontalalignment='left',
         verticalalignment='bottom',
         transform = ax1.transAxes,
         size=7,
         bbox=dict(facecolor='white', alpha=1, lw=0))

    comments = ""
    comments += ocd.ref + "\n"
    comments += calib.ref + "\n"

    plt.text(0.55, 0.85,'{}'.format(comments),
         horizontalalignment='left',
         verticalalignment='center',
         transform = ax1.transAxes,
         size=8,
         bbox=dict(facecolor='white', alpha=0.9, lw=0))


    alphaY = 8
    if(ocd.posterior.used and use_model):
        calibrated = ocd.posterior
        alphaY = 6
    else:
        calibrated = ocd.likelihood

    # Calendar Age
    # imitate OxCal
    ax2 = plt.twinx()

    ax2.fill(
        calibrated.calibAxis,
        calibrated.prob + max(calibrated.prob)*0.3,
        'k',
        alpha=0.3
        )
    ax2.plot(
        calibrated.calibAxis,
        calibrated.prob + max(calibrated.prob)*0.3,
        'k',
        alpha=0.8
        )

    ax2.set_ybound(min(calibrated.prob),max(calibrated.prob)*1.7)
    tl = len(calibrated.calibAxis)
    ax2.set_xbound(calibrated.array[0,0],calibrated.array[-1,0])
    ax2.set_axis_off()

    # Radiocarbon Age
    sample_interval = np.arange(ocd.date-4*ocd.error, ocd.date+4*ocd.error,1.)
    sample_curve = normpdf(sample_interval, ocd.date, ocd.error)
    line_x = np.array([0, 1])
    line_y = np.array([ocd.date, ocd.date])

    ax3 = plt.twiny(ax1)
    for i in range(-1,2,1):
        ax3.plot(
            line_x,
            line_y+i*ocd.error,
            'k--',
            alpha=0.5-0.2*abs(i),
            lw=1.5-abs(i)
            )
    ax3.fill(
        sample_curve,
        sample_interval,
        'r',
        alpha=0.3
        )
    ax3.plot(
        sample_curve,
        sample_interval,
        'r',
        alpha=0.3,
        label='Radiocarbon determination (BP)'
        )
    ax3.set_xbound(0,max(sample_curve)*4)
    ax3.set_axis_off()

    # Calibration Curve
    xs, ys = mlab.poly_between(calib.array[:,0],
                               calib.array[:,1] - calib.array[:,2],
                               calib.array[:,1] + calib.array[:,2])
    ax1.fill(xs, ys, 'b', alpha=0.3)

    # Confidence intervals
    ymin=[0.14, 0.10, 0.06]

    for j in range(2,-1,-1):
        for i in calibrated.range[j]:
            ax1.axvspan(
                i[0], i[1],
                ymin=ymin[j],
                ymax=ymin[j]+0.07,
                facecolor='none',
                alpha=0.8)
            ax1.axvspan(
                i[0], i[1],
                ymin=ymin[j]+0.03,
                ymax=ymin[j]+0.07,
                facecolor='w',
                edgecolor='w',
                lw=2)

    # FIXME the following values 10 and 5 are arbitrary and could be probably
    # drawn from the f_m value itself, while preserving their ratio
    detla_BP = ocd.likelihood.mean - calibrated.mean
    ax1.set_ybound(ocd.date - ocd.error*alphaY + detla_BP, ocd.date + ocd.error*alphaY + detla_BP)
    ax1.set_xbound(calibrated.array[0,0],calibrated.array[-1,0])

    #plt.savefig('image_%d±%d.pdf' %(f_m, sigma_m))
    plt.savefig(file_name)
    fig = plt.gcf()
    fig.clear()
