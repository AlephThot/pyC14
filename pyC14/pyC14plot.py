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

from pyC14 import OxCalData, Calibration







def plot_single_expend(ocd,
                calib,
                file_name = "test.jpg"):
    fig = plt.figure(figsize=(12,6))
    ax1 = plt.subplot(111)
    plt.xlabel("{} - Calibrated date (BC)".format(ocd.name), fontsize=15)
    plt.ylabel("Radiocarbon determination (BP)", fontsize=15)


    plt.text(0., 0.99,"pyC14 v0.1; Xtof; Bellevue 2008-2012",
         horizontalalignment='left',
         verticalalignment='bottom',
         transform = ax1.transAxes,
         size=9,
         bbox=dict(facecolor='white', alpha=1, lw=0))


    # Calendar Age
    ax2 = plt.twinx()

    max_prob = max(ocd.likelihood.prob)

    ax2.fill(
        ocd.likelihood.calibAxis,
        ocd.likelihood.prob + max_prob*0.3,
        'k',
        alpha=0.3,
        label='Calendar Age'
        )
    ax2.plot(
        ocd.likelihood.calibAxis,
        ocd.likelihood.prob + max_prob*0.3,
        'k',
        alpha=0.8
        )

    ax2.set_ybound(min(ocd.likelihood.prob),max_prob*3)
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
        alpha=0.5,
        label='Radiocarbon determination (BP)'
        )
    ax3.set_xbound(0,max(sample_curve)*4)
    ax3.set_axis_off()


    # Calibration Curve

    mlab_low  = [ calib.bp[i]-calib.sigma[i] for i in range(len(calib.sigma)) ]
    mlab_high = [ calib.bp[i]+calib.sigma[i] for i in range(len(calib.sigma)) ]

    xs, ys = mlab.poly_between(calib.calibAxis,
                               mlab_low,
                               mlab_high)
    ax1.fill(xs, ys, 'b', alpha=0.3)

    # Confidence intervals

    ymin=[0.075, 0.05, 0.025]

    for j in range(2,-1,-1):
        for i in ocd.likelihood.range[j]:
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

    plt.text(0.745, 0.68,'{}'.format(ocd.likelihood.get_meta("",False)),
         horizontalalignment='left',
         verticalalignment='center',
         transform = ax1.transAxes,
         bbox=dict(facecolor='white', alpha=0.9, lw=0))

    # FIXME the following values 10 and 5 are arbitrary and could be probably
    # drawn from the f_m value itself, while preserving their ratio
    tl = len(ocd.likelihood.calibAxis)
    ax1.set_ybound(ocd.date - ocd.error * 8, ocd.date + ocd.error * 8)
    ax1.set_xbound(ocd.likelihood.calibAxis[0],ocd.likelihood.calibAxis[tl-1])

    #plt.savefig('image_%d±%d.pdf' %(f_m, sigma_m))
    plt.savefig(file_name)
    fig = plt.gcf()
    fig.clear()




def plot_single_simple(ocd,
                calib,
                file_name = "test.jpg"):
    fig = plt.figure(figsize=(8,2))
    ax1 = plt.subplot(111)
    plt.ylabel("C14 age (BP)")

    plt.text(-0.12, -0.11,"Date (BC)",
         horizontalalignment='left',
         verticalalignment='bottom',
         transform = ax1.transAxes,
         size=11)

    plt.text(0.0, 0.97,"pyC14 v0.1; Xtof; Ard-team",
         horizontalalignment='left',
         verticalalignment='bottom',
         transform = ax1.transAxes,
         size=7,
         bbox=dict(facecolor='white', alpha=0.9, lw=0))

    comments = ""
    comments += ocd.ref + "\n"
    comments += calib.ref + "\n"

    plt.text(0.55, 0.85,'{}'.format(comments),
         horizontalalignment='left',
         verticalalignment='center',
         transform = ax1.transAxes,
         size=8,
         bbox=dict(facecolor='white', alpha=0.9, lw=0))

    # Calendar Age
    ax2 = plt.twinx()

    # imitate OxCal
    ax2.fill(
        ocd.likelihood.calibAxis,
        ocd.likelihood.prob + max(ocd.likelihood.prob)*0.3,
        'k',
        alpha=0.3,
        label='Calendar Age'
        )
    ax2.plot(
        ocd.likelihood.calibAxis,
        ocd.likelihood.prob + max(ocd.likelihood.prob)*0.3,
        'k',
        alpha=0.8
        )

    ax2.set_ybound(min(ocd.likelihood.prob),max(ocd.likelihood.prob)*1.7)
    tl = len(ocd.likelihood.calibAxis)
    ax2.set_xbound(ocd.likelihood.calibAxis[int(0.2*tl)],ocd.likelihood.calibAxis[int(0.90*tl)])
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

    mlab_low  = [ calib.bp[i]-calib.sigma[i] for i in range(len(calib.sigma)) ]
    mlab_high = [ calib.bp[i]+calib.sigma[i] for i in range(len(calib.sigma)) ]

    xs, ys = mlab.poly_between(calib.calibAxis,
                               mlab_low,
                               mlab_high)
    ax1.fill(xs, ys, 'b', alpha=0.3)

    # Confidence intervals


    ymin=[0.14, 0.10, 0.06]

    for j in range(2,-1,-1):
        for i in ocd.likelihood.range[j]:
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
    tl = len(ocd.likelihood.calibAxis)
    ax1.set_ybound(ocd.date - ocd.error * 8, ocd.date + ocd.error * 8)
    ax1.set_xbound(ocd.likelihood.calibAxis[int(0.*tl)],ocd.likelihood.calibAxis[int(1*tl)-1])

    #plt.savefig('image_%d±%d.pdf' %(f_m, sigma_m))
    plt.savefig(file_name)
    fig = plt.gcf()
    fig.clear()


def plot_single_prob(ocd,
                calib,
                file_name = "test.jpg"):
    fig = plt.figure(figsize=(10,2))
    ax1 = plt.subplot(111)
    plt.ylabel("Probability")
    plt.yticks([0.],("0"))

    plt.text(-0.12, -0.11,"Date (BC)",
         horizontalalignment='left',
         verticalalignment='bottom',
         transform = ax1.transAxes,
         size=11)

    plt.text(0.0, 0.96,"pyC14 v0.1; Xtof; Ard-team",
         horizontalalignment='left',
         verticalalignment='bottom',
         transform = ax1.transAxes,
         size=7,
         bbox=dict(facecolor='white', alpha=1, lw=0))


    # Confidence intervals

    ymin=[0.12, 0.09, 0.05]

    for j in range(2,-1,-1):
        for i in ocd.likelihood.range[j]:
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

    # imitate OxCal
    ax1.fill(
        ocd.likelihood.calibAxis,
        ocd.likelihood.prob,
        'k',
        alpha=0.3,
        label='Calendar Age'
        )
    ax1.plot(
        ocd.likelihood.calibAxis,
        ocd.likelihood.prob,
        'k',
        alpha=0.8
        )

    # FIXME the following values 10 and 5 are arbitrary and could be probably
    # drawn from the f_m value itself, while preserving their ratio
    tl = len(ocd.likelihood.calibAxis)
    ax1.set_xbound(ocd.likelihood.calibAxis[0],ocd.likelihood.calibAxis[tl-1])
    ax1.set_ybound(-0.2, 1.1)

    #plt.savefig('image_%d±%d.pdf' %(f_m, sigma_m))
    plt.savefig(file_name)
    fig = plt.gcf()
    fig.clear()