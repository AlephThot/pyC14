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
from pyC14.plot.singlePlot import expend, simple, probability, compare
from pyC14.OxCal import calibrate_single, parse_OxCal_data
from pyC14.main import Radiocarbon



example_data = [
 ("F.0206",4860,35),
 ("F.0603",4830,35)
]

#example_oxcal_project = "../../bellevue-c14/bellevue_parFosse.oxcal"
example_oxcal_project = "example.oxcal"

if __name__ == "__main__":

    OxCal = Radiocarbon()

    #for (name, date, error) in example_data:
        ##single calibration
        #(oxcal_output_log, oxcal_output_js) = OxCal.calibrate_single(date, error, name)
        ##the .js file is parsed
        #(myOCD, myCalib_ref) = parse_OxCal_data(oxcal_output_js)
        ##plot
        #fname = "output/gd/test_{name}_{date}-{error}_gd_s.png".format(name=name, date=date, error=error)
        #expend.plot(myOCD[2], myCalib_ref[0], fname)
        ##plot
        #fname = "output/ptt/test_{name}_{date}-{error}_ptt_s.png".format(name=name, date=date, error=error)
        #simple.plot(myOCD[2], myCalib_ref[0], fname)
        ##plot
        #fname = "output/prob/test_{name}_{date}-{error}_prob_s.png".format(name=name, date=date, error=error)
        #probability.plot(myOCD[2], myCalib_ref[0], fname)

    #single calibration
    (oxcal_output_log, oxcal_output_js) = OxCal.calibrate_project(example_oxcal_project, verbose=False)
    #the .js file is parsed
    (myOCD, myCalib) = parse_OxCal_data(oxcal_output_js)
    for i in range(len(myOCD)-1):
        if(myOCD[i+2].type=="date"):
            #plot
            oc = myOCD[i+2]

            fname = "output/gd/test_{name}_{date}-{error}_gd_p.png".format(name=oc.name, date=oc.date, error=oc.error)
            expend.plot(oc, myCalib[oc.calib], fname)
            print("plot gd done")
            #plot
            fname = "output/ptt/test_{name}_{date}-{error}_ptt_p.png".format(name=oc.name, date=oc.date, error=oc.error)
            simple.plot(oc, myCalib[oc.calib], fname)
            print("plot ptt done")
            #plot
            fname = "output/prob/test_{name}_{date}-{error}_prob_p.png".format(name=oc.name, date=oc.date, error=oc.error)
            probability.plot(oc, myCalib[oc.calib], fname)
            print("plot prob done")
            #plot
            fname = "output/comp/test_{name}_{date}-{error}_comp_p.png".format(name=oc.name, date=oc.date, error=oc.error)
            compare.plot(oc, myCalib[oc.calib], fname)
            print("plot comp done")
            
            #print(oc.likelihood.array)
            #print(oc.posterior.array)
