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
from ...util import interpolate







def plot(ocd,
         calib,
         file_name = "test.jpg",
         interpolation = False):
    fig = plt.figure(figsize=(12,6))
    ax1 = plt.subplot(111)
    plt.xlabel("{} - Calibrated date (BC)".format(ocd.name), fontsize=18)
    plt.ylabel("Radiocarbon determination (BP)", fontsize=18)


    plt.text(0., 0.99,"pyC14 v0.1; Xtof; Bellevue 2008-2012",
         horizontalalignment='left',
         verticalalignment='bottom',
         transform = ax1.transAxes,
         size=9,
         bbox=dict(facecolor='white', alpha=1, lw=0))


    # Calendar Age
    ax2 = plt.twinx()

    calib_0 = (ocd.likelihood.array)
    calib_1 = (ocd.posterior.array)
    if(interpolation):
        calib_0 = interpolate(calib_0)
        calib_1 = interpolate(calib_1)

    max_prob_ref = max(calib_0[:,1])
    min_prob_ref = min(calib_0[:,1])
    max_prob_calib = max(calib_1[:,1])
    min_prob_calib = min(calib_1[:,1])

    beta = ocd.adjust_comparaison()

    ax2.fill(
        calib_0[:,0],
        calib_0[:,1] + max(max_prob_ref, max_prob_calib)*0.3,
        'k',
        alpha=0.2,
        )
    ax2.plot(
        calib_0[:,0],
        calib_0[:,1] + max(max_prob_ref, max_prob_calib)*0.3,
        'k:',
        alpha=0.5
        )

    # Calendar Age bis
    ax2b = plt.twinx()


    ax2b.fill(
        calib_1[:,0],
        calib_1[:,1]/beta + max(max_prob_ref, max_prob_calib)*0.3,
        'k',
        alpha=0.5,
        )
    ax2b.plot(
        calib_1[:,0],
        calib_1[:,1]/beta + max(max_prob_ref, max_prob_calib)*0.3,
        'k',
        alpha=0.5
        )

    #print(min_prob_ref, min_prob_calib)
    #print(max_prob_ref, max_prob_calib)

    ax2.set_ybound(
        min(min_prob_ref, min_prob_calib), 
        max(max_prob_ref, max_prob_calib)*3)
    ax2b.set_ybound(
        min(min_prob_ref, min_prob_calib), 
        max(max_prob_ref, max_prob_calib)*3)
    ax2.set_axis_off()
    ax2b.set_axis_off()

    # Radiocarbon Age
    sample_interval = np.arange(ocd.date-4*ocd.error, ocd.date+4*ocd.error,1.)
    sample_curve = normpdf(sample_interval, ocd.date, ocd.error)
    max_sample_curve = max(sample_curve)

    line_x = np.array([0, max_sample_curve*3])
    line_y = np.array([ocd.date, ocd.date])

    ax3 = plt.twiny(ax1)
    for i in range(-1,2,1):
        ax3.plot(
            line_x,
            line_y+i*ocd.error,
            'k--',
            alpha=0.5-0.2*abs(i),
            lw=2-abs(i)
            )
    ax3.fill(
        sample_curve,
        sample_interval,
        'r',
        alpha=0.4
        )
    ax3.plot(
        sample_curve,
        sample_interval,
        'r',
        alpha=0.5
        )
    ax3.set_xbound(0,max_sample_curve*4)
    ax3.set_axis_off()


    # Calibration Curve
    xs, ys = mlab.poly_between(calib.array[:,0],
                               calib.array[:,1] - calib.array[:,2],
                               calib.array[:,1] + calib.array[:,2])
    ax1.fill(xs, ys, 'b', alpha=0.3)
    ax1.plot(
        calib.array[:,0],
        calib.array[:,1],
        'b',
        alpha=0.5,
        lw=1
        )

    # Confidence intervals

    ymin=[0.075, 0.05, 0.025]
    if(ocd.posterior.used):
        calibrated = ocd.posterior
    else:
        calibrated = ocd.likelihood

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
                ymin=ymin[j]+0.02,
                ymax=ymin[j]+0.07,
                facecolor='w',
                edgecolor='w',
                lw=2)

    comments = ocd.ref + "\n"
    comments += calib.ref + "\n"

    plt.text(0.55, 0.90,'{}'.format(comments),
         horizontalalignment='left',
         verticalalignment='center',
         transform = ax1.transAxes,
         bbox=dict(facecolor='white', alpha=0.9, lw=0))

    plt.text(0.745, 0.68,'{}'.format(calibrated.get_meta("",False)),
         horizontalalignment='left',
         verticalalignment='center',
         transform = ax1.transAxes,
         bbox=dict(facecolor='white', alpha=0.9, lw=0))

    # FIXME the following values 10 and 5 are arbitrary and could be probably
    # drawn from the f_m value itself, while preserving their ratio
    tl = len(ocd.likelihood.array[:,0])
    ax1.set_ybound(ocd.date - ocd.error * 8, ocd.date + ocd.error * 8)
    ax1.set_xbound(ocd.likelihood.array[0,0],ocd.likelihood.array[-1,0])

    #plt.savefig('image_%d±%d.pdf' %(f_m, sigma_m))
    plt.savefig(file_name)
    fig = plt.gcf()
    fig.clear()

