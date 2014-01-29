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


from pyC14.pyC14 import OxCalData, Calibration
from pyC14.pyC14plot import plot_single_expend, plot_single_simple, plot_single_prob
from pyC14.OxCal import calibrate_single, parse_OxCal_data



example_data = [
 ("ex20140129",4305,35)
]


if __name__ == "__main__":
    for (name, date, error) in example_data:
        (oxcal_output_log, oxcal_output_js) = calibrate_single(date, error, name)
        (myOCD, myCalib) = parse_OxCal_data(oxcal_output_js)
        fname = "output/gd/test_{name}_{date}-{error}_gd.png".format(name=name, date=date, error=error)
        plot_single_expend(myOCD[2], myCalib[0], fname)
        fname = "output/ptt/test_{name}_{date}-{error}_ptt.png".format(name=name, date=date, error=error)
        plot_single_simple(myOCD[2], myCalib[0], fname)
        fname = "output/prob/test_{name}_{date}-{error}_prob.png".format(name=name, date=date, error=error)
        plot_single_prob(myOCD[2], myCalib[0], fname)
