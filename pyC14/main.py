# -*- coding: utf-8 -*-

ur"""

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




    :Example:

    >>> Radiocarbon().calibrate_single(4713, 54) # doctest: +NORMALIZE_WHITESPACE
    OxCal v4.2.3 Bronk Ramsey (2013); r:5
     IntCal13 atmospheric curve (Reimer et al 2013)
    R_Date(4713,54)
      68.2% probability
        3628BC (19.2%) 3584BC
        3531BC (15.0%) 3498BC
        3454BC (34.0%) 3378BC
      95.4% probability
        3634BC (53.1%) 3484BC
        3474BC (42.3%) 3371BC
    <BLANKLINE>
    ('/tmp/calib.log', '/tmp/calib.js')




"""

from __future__ import print_function

import os.path
from os import system
import json
import pkg_resources




class Radiocarbon(object):
    ur"""
    The main class of the pyC14 package. It holds an option
    manager, with th possibility to charge personnal and/or
    local set of options (totally or partially).
    """

    def __init__(self,
               param_file = "param_pyC14.json",
               verbose = False
               ):
        ur"""
            Initialise the paramter variables, load the parameter
            file and deals with it.

            :param param_file: the path to the parameters file
            :param verbose: if True, explicite the output
            :type params: string
            :type verbose: boolean
            :return: nothing
            :rtype: None
        """

        self.param_file = pkg_resources.resource_filename("pyC14", "param/%s" % param_file)
        self.param_oxcal = {}
        self.param_oxcal_data = {}
        self.param_load_fromFile(param_file, verbose = verbose)

        self.imput_oxcal_file = self._create_oxcal_file(self.param_oxcal["oxcal_ext_input"])
        self.output_oxcal_log = self._create_oxcal_file(self.param_oxcal["oxcal_ext_output_log"])
        self.output_oxcal_js = self._create_oxcal_file(self.param_oxcal["oxcal_ext_output_js"])

    def param_load_fromFile(self,
                            param_file,
                            verbose = False):
        ur"""
            Load the parameter file in the json format.

            :param param_file: the path to the parameters file
            :param verbose: if True, explicite the output
            :type params: string
            :type verbose: boolean
            :return: nothing
            :rtype: None
        """
        if(param_file == None):
            param_file = self.param_file

        if(os.path.exists(self.param_file)):
            f = open(self.param_file,"r")
            new_params = json.load(f)
            f.close()
            self.param_analyse(new_params, verbose = verbose)
        else:
            raise NameError("\n\tThe searched param file doesn't exist\n"
                "\tor the path is not valid.\n"
                "\t\t-> {}".format(self.param_file))

    def param_analyse(self,
                     params,
                     verbose = False
                     ):
        ur"""
            It analyses the dictionnary of parameters and makes them
            availlable for all the options.

            :param params: the set of dictionnay of parameters
            :param verbose: if True, explicite the output
            :type params: [dict]
            :type verbose: boolean
            :return: nothing
            :rtype: None
        """
        for param in params:
            if(not param.has_key("target")):
                print("\n\tThis param block does not contain the key 'target'\n"
                    "\tI can not analyse it. It will be omited\n"
                    "\t\t-> {}".format(param.keys()))
            else:
                if(param["target"]=="OxCal"):
                    #print("OxCal")
                    for (key, value) in param.items():
                        self.param_oxcal[key] = value
                    #print(self.param_oxcal)
                elif(param["target"]=="OxCaljs"):
                    #print("OxCaljs")
                    for (key, value) in param.items():
                        self.param_oxcal_data[key] = value
                    #print(self.param_oxcal_data)
        if(verbose):
            print("OxCal")
            for (key, value) in self.param_oxcal.items():
                print("\t{}: {}".format(key, value))
            print("OxCaljs")
            for (key, value) in self.param_oxcal_data.items():
                print("\t{}: {}".format(key, value))

    def calibrate_single(self,
                         date,
                         error,
                         name = "",
                         verbose = True):
        ur"""
            Use OxCal to calibrate a single radiocarbon date.

            :param date: the c14 date to calibrate
            :param error: the systemic error
            :type date: int
            :type error: int
            :return: a tuple of file names (oxcal.log, oxcal.js)
            :rtype: tuple(string, string)

        """
        imput_oxcal_file = self._create_oxcal_file(self.param_oxcal["oxcal_ext_input"])
        output_oxcal_log = self._create_oxcal_file(self.param_oxcal["oxcal_ext_output_log"])
        output_oxcal_js = self._create_oxcal_file(self.param_oxcal["oxcal_ext_output_js"])

        in_f = open(imput_oxcal_file, "w")
        if(name != ""):
            in_f.write("R_Date(\"{name}\",{date},{error});".format(name=name,date=date, error=error))
        else:
            in_f.write("R_Date({date},{error});".format(date=date, error=error))
        in_f.close()

        system("{oxcal_bin} {input_calib}".format(
            oxcal_bin = self.param_oxcal["OXCAL_BIN_LINUX"], 
            input_calib = imput_oxcal_file)
        )

        if(verbose):
            out_f = open(output_oxcal_log, "r")
            out_st = ""
            for line in out_f:
                out_st = out_st + line
            out_f.close()
            print(out_st)


        return (output_oxcal_log, output_oxcal_js)



    def calibrate_project(self,
                         project_file_path,
                         verbose = False):
        ur"""
            Use OxCal to calibrate a single radiocarbon date.

            :param project_file_path: path to the OxCal project file
            :type project_file_path: string
            :return: a tuple of file names (oxcal.log, oxcal.js)
            :rtype: tuple(string, string)

        """

        in_f = open(self.imput_oxcal_file, "w")
        oc_f = open(project_file_path, "r")
        for line in oc_f:
            in_f.write(line)
        in_f.close()
        oc_f.close()

        system("{oxcal_bin} {oxcal_opt} {input_calib}".format(
            oxcal_bin = self.param_oxcal["OXCAL_BIN_LINUX"], 
            oxcal_opt = "-i2",
            input_calib = self.imput_oxcal_file)
        )

        if(verbose):
            out_f = open(self.output_oxcal_log, "r")
            out_st = ""
            for line in out_f:
                out_st = out_st + line
            out_f.close()
            print(out_st)


        return (self.output_oxcal_log, self.output_oxcal_js)




    def _create_oxcal_file(self,
                          ext,
                          basename = None,
                          tempdir = None
                          ):
        ur"""
            Internal function to create a standard OxCal file-name

            :param ext: the expected file extension
            :param basename: base-name of the file
            :param tempdir: path of the temp directory
            :type ext: string
            :type basename: string
            :type tempdir: string
            :return: the full path of the expected file
            :rtype: string

        """

        if(basename == None and self.param_oxcal.has_key("OXCAL_FILE_BASENAME")):
            basename = self.param_oxcal["OXCAL_FILE_BASENAME"]
        if(tempdir == None and self.param_oxcal.has_key("OXCAL_TEMPDIR")):
            tempdir = self.param_oxcal["OXCAL_TEMPDIR"]

        return "{tempdir}/{basename}.{ext}".format(
            tempdir = tempdir, 
            basename = basename, 
            ext = ext)




if __name__ == "__main__":
    #Radiocarbon().calibrate_single(4713, 54)

    import doctest
    doctest.testmod()