# -*- coding: utf-8 -*-
 
"""

    Part of the pyC14 scripts set, used to calibrate C14 data.

    @author Christophe Le Bourlot, MATEIS - INSA LYON - UMR CNRS 5510 
    @date 10/01/2014
    @version 0.1

    Copyright © 2014 INSA Lyon - MATEIS

    This file is part of pyC14.

"""


from __future__ import print_function


from pyC14.pyC14 import OxCalData, Calibration
from pyC14.pyC14plot import plot_single_expend, plot_single_simple, plot_single_prob
from pyC14.OxCal import calibrate_single, parse_OxCal_data





#print(myOCD[2])
#print(myOCD[2].__dict__.keys())

#print(myOCD[2].get_meta(calibs=myCalib))

bellevue = [
 ("F.0206",4860,35),
 ("F.0603",4830,35),
 ("F.0207",4810,35),
 ("F.0404",4807,53),
 ("St.11201b",4795,35),
 ("F0301",4786,53),
 ("F.0205",4765,35),
 ("F.020607",4750,40),
 ("St.1602",4735,35),
 ("F.0102",4715,35),
 ("F.0305",4713,54),
 ("F.0504",4690,30),
 ("F.0101b",4675,35),
 ("F.0101a",4650,35),
 ("St3",4635,35),
 ("St47",4630,30),
 ("St3.vase",4575,30),
 ("St16",4550,35),
 ("St18",4305,35)
]


for (name, date, error) in bellevue:
    (oxcal_output_log, oxcal_output_js) = calibrate_single(date,error,name)
    (myOCD, myCalib) = parse_OxCal_data(oxcal_output_js)
    #fname = "blv/gd/blv_{name}_{date}-{error}_gd.png".format(name=name, date=date, error=error)
    #plot_single_expend(myOCD[2], myCalib[0], fname)
    #fname = "blv/ptt/blv_{name}_{date}-{error}_ptt.png".format(name=name, date=date, error=error)
    #plot_single_simple(myOCD[2], myCalib[0], fname)
    fname = "blv/prob/blv_{name}_{date}-{error}_prob.png".format(name=name, date=date, error=error)
    plot_single_prob(myOCD[2], myCalib[0], fname)


 
