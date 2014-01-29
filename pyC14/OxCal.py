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

from os import system

from pyparsing import *
from pyparsing import Word, WordStart,WordEnd
from pyparsing import alphas, nums, alphanums, printables

from pyC14 import OxCalData, Calibration

OXCAL_TEMPDIR = u"/tmp"
OXCAL_FILE_BASENAME = u"calib"

def create_oxcal_file(ext,
                     basename = OXCAL_FILE_BASENAME,
                     tempdir = OXCAL_TEMPDIR):
    return u"{tempdir}/{basename}.{ext}".format(
        tempdir = tempdir, 
        basename = basename, 
        ext = ext)

oxcal_input_calib = create_oxcal_file(u"c14")
oxcal_output_js = create_oxcal_file(u"js")
oxcal_output_log = create_oxcal_file(u"log")

OXCAL_BIN_LINUX = u"/home/clebourlot/Documents/docs-archeo/oxcal-bin/OxCal/bin/OxCalLinux"



def calibrate_single(date,
                     error,
                     name = "",
                     verbose = True):
    in_f = open(oxcal_input_calib, "w")
    if(name != ""):
        in_f.write(u"R_Date(\"{name}\",{date},{error});".format(name=name,date=date, error=error))
    else:
        in_f.write(u"R_Date({date},{error});".format(date=date, error=error))
    in_f.close()

    system(u"{oxcal_bin} {input_calib}".format(oxcal_bin=OXCAL_BIN_LINUX, input_calib=oxcal_input_calib))

    out_f = open(oxcal_output_log, 'r')
    out_st = u""
    for line in out_f:
        out_st = out_st + line
    out_f.close()

    if(verbose):
        print(out_st)


    return (oxcal_output_log, oxcal_output_js)

def parse_OxCal_data(oxcal_js_file):
    myOCD = {}
    myCalib = {}

    # Ouverture d'un fichier en *lecture*:
    fichier = open(oxcal_js_file, 'r')

    for ligne in fichier:
        modele = Word( alphas ) + '[' + Word(nums) + ']' + Word( printables )
        try:
            parsed_data = modele.parseString( ligne )
        except ParseException, pe:
            pass
        else:
            flg = parsed_data[0] 
            nb = int(parsed_data[2])
            if(flg==u"ocd"):
                if(not myOCD.has_key(nb)):
                    myOCD[nb] = OxCalData(nb)
                myOCD[nb].set_param(ligne)
            elif(flg==u"calib"):
                if(not myCalib.has_key(nb)):
                    myCalib[nb] = Calibration(nb)
                myCalib[nb].set_param(ligne)

    # Fermeture du fichier
    fichier.close()

    for ocd in myOCD:
        myOCD[ocd].set_axis()
    for c in myCalib:
        myCalib[c].set_axis()

    return (myOCD, myCalib)