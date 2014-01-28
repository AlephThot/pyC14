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

from os import system

from pyparsing import *
from pyparsing import Word, WordStart,WordEnd
from pyparsing import alphas, nums, alphanums, printables

from pyC14 import OxCalData, Calibration

OXCAL_TEMPDIR = "/tmp"
OXCAL_FILE_BASENAME = "calib"

def create_oxcal_file(ext,
                     basename = OXCAL_FILE_BASENAME,
                     tempdir = OXCAL_TEMPDIR):
    return "{tempdir}/{basename}.{ext}".format(
        tempdir = tempdir, 
        basename = basename, 
        ext = ext)

oxcal_input_calib = create_oxcal_file("c14")
oxcal_output_js = create_oxcal_file("js")
oxcal_output_log = create_oxcal_file("log")

OXCAL_BIN_LINUX = "/home/clebourlot/Documents/docs-archeo/oxcal-bin/OxCal/bin/OxCalLinux"



def calibrate_single(date,
                     error,
                     name = "",
                     verbose = True):
    in_f = open(oxcal_input_calib, "w")
    if(name != ""):
        in_f.write("R_Date(\"{name}\",{date},{error});".format(name=name,date=date, error=error))
    else:
        in_f.write("R_Date({date},{error});".format(date=date, error=error))
    in_f.close()
    
    system("{oxcal_bin} {input_calib}".format(oxcal_bin=OXCAL_BIN_LINUX, input_calib=oxcal_input_calib))
    
    out_f = open(oxcal_output_log, "r")
    out_st = ""
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
    fichier = open(oxcal_js_file, "r")

    for ligne in fichier:
    # ...
        modele = Word( alphas ) + "[" + Word(nums) + "]" + Word( printables )
        try:
            parsed_data = modele.parseString( ligne )
        except ParseException, pe:
            pass
        else:
            flg = parsed_data[0] 
            nb = int(parsed_data[2])
            if(flg=="ocd"):
                if(not myOCD.has_key(nb)):
                    myOCD[nb] = OxCalData(nb)
                myOCD[nb].set_param(ligne)
            elif(flg=="calib"):
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