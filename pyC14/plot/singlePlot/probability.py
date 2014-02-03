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
                file_name = "test.jpg"):
    fig = plt.figure(figsize=(10,2))
    ax2 = plt.subplot(111)
    plt.ylabel("Probability")
    plt.yticks([0.],("0"))

    plt.text(-0.12, -0.11,"Date (BC)",
         horizontalalignment='left',
         verticalalignment='bottom',
         transform = ax2.transAxes,
         size=11)

    plt.text(0.0, 0.96,"pyC14 v0.1; Xtof; Ard-team",
         horizontalalignment='left',
         verticalalignment='bottom',
         transform = ax2.transAxes,
         size=7,
         bbox=dict(facecolor='white', alpha=1, lw=0))


    # Confidence intervals
    ymin=[0.12, 0.09, 0.05]

    if(ocd.posterior.used):
        calibrated = ocd.posterior
    else:
        calibrated = ocd.likelihood
    for j in range(2,-1,-1):
        for i in calibrated.range[j]:
            ax2.axvspan(
                i[0], i[1],
                ymin=ymin[j],
                ymax=ymin[j]+0.07,
                facecolor='none',
                alpha=0.8)
            ax2.axvspan(
                i[0], i[1],
                ymin=ymin[j]+0.03,
                ymax=ymin[j]+0.07,
                facecolor='w',
                edgecolor='w',
                lw=2)


    # imitate OxCal
    ax2.fill(
        ocd.likelihood.array[:,0],
        ocd.likelihood.array[:,1],
        'k',
        alpha=0.2,
        )
    ax2.plot(
        ocd.likelihood.array[:,0],
        ocd.likelihood.array[:,1],
        'k:',
        alpha=0.5
        )
    max_date = max(ocd.likelihood.array[:,0])
    min_date = min(ocd.likelihood.array[:,0])

    if(ocd.posterior.used):
        max_date = max(ocd.posterior.array[-1,0], max_date)
        min_date = min(ocd.posterior.array[0,0], min_date)

        beta = ocd.adjust_comparaison()
        # Calendar Age bis
        ax2b = plt.twinx()  
        ax2b.fill(
            ocd.posterior.array[:,0],
            ocd.posterior.array[:,1]/beta,
            'k',
            alpha=0.5,
            )
        ax2b.plot(
            ocd.posterior.array[:,0],
            ocd.posterior.array[:,1]/beta,
            'k',
            alpha=0.5
            )

        ax2b.set_axis_off()
        ax2b.set_ybound(-0.2, 1.1)

    ax2.set_xbound(min_date,max_date)
    ax2.set_ybound(-0.2, 1.1)

    plt.savefig(file_name)
    fig = plt.gcf()
    fig.clear()