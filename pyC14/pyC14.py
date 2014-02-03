# -*- coding: utf-8 -*-

from __future__ import print_function


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

from pyparsing import Word, alphanums, alphas, nums
from pyparsing import commaSeparatedList, ParseException

import numpy as np

from util import *


ocd_str_param = (u"ref", u"name", u"op", u"param", u"type")
ocd_int_param = (u"level", u"date", u"error", u"calib")

lh_int_param = (u"resolution")
lh_flt_param = (u"median", u"mean", u"sigma", u"probNorm", u"start", u"agreement")
lh_csv_param = (u"prob")

objectPath = alphanums + ".[]-"
divers = alphanums + ".,%()\"_- [];:"








class Likelihood(object):
    def __init__(self):
        self.comment = []
        self.range = []
        self.prob = np.zeros(0)
        self.calibAxis = np.zeros(0)
        self.used = False

    def __repr__(self):
        if(len(self.comment)>0):
            return self.comment[0]
        else:
            return ""

    def __str__(self):
        print(self.__dict__.keys())
        toto = ""
        for a in self.comment:
            toto = toto + a + "\n"
        for a in range(len(self.range)):
            tt = self.range[a]
            for b in range(len(tt)):
                toto = toto + "["+str(tt[b][0])+":"+str(tt[b][1])+"] "+str(tt[b][2])+"% "
            toto = toto + "\n"
        return toto

    def set_param(self,keywords,value):
        # define grammar
        pointPos = keywords[1].find("[")
        #print(keywords[1])
        if(pointPos<0):
            key = keywords[1]
            if(key in lh_flt_param):
                setattr(self,key,float(value))
            elif(key in lh_int_param):
                setattr(self,key,int(value))
            elif(key=="prob"):
                #print(value)
                self.prob = np.array([float(x) for x in commaSeparatedList.parseString(set_str(value))])
        elif(pointPos==7):
            self.comment.append(set_str(value))
            #print(keywords,value)
        else:
            #print(keywords[1])
            modele = "range[" + Word(nums) + "][" + Word(nums) + "]"
            try:
                rg = modele.parseString( keywords[1] )
            except ParseException as pe:
                pass
            else:
                #print(keywords[1],value)
                i = int(rg[1])
                if len(self.range)<i:
                    self.range.append([])
                self.range[i-1].append([float(x) for x in commaSeparatedList.parseString(set_str(value))])

    def get_meta(self,
                 arg="#",
                 all_meta=True):
        out = ""
        out = out + "{arg}\n".format(arg=arg)
        for a in self.comment:
            out = out + "{arg} {value}\n".format(arg=arg,value=a)
        if(all_meta):
            for a in range(len(self.range)):
                tt = self.range[a]
                out = out + "{arg} {id}\n".format(arg=arg,id=a)
                for b in range(len(tt)):
                    out = out + "{arg}  {value}\n".format(arg=arg,value="["+str(tt[b][0])+":"+str(tt[b][1])+"] "+str(tt[b][2])+"% ")
            out = out + "{arg}\n".format(arg=arg)
        return out

    def get_data(self,
                 arg="#"):
        out = ""
        for i in range(len(self.prob)):
            out = out + "{age}\t{prob}\n".format(age=(self.start+i*self.resolution),prob=self.prob[i])
        return out

    def set_axis(self):
        if(hasattr(self,"start") and hasattr(self,"resolution")):
            self.calibAxis = np.zeros(len(self.prob))
            for i in range(len(self.prob)):
                self.calibAxis[i] = self.start+i*self.resolution
            self.array = np.array([self.calibAxis,
                                  self.prob]
                                ).transpose()
            self.used = True

class OxCalData(object):
    """
    OxCalData defined to store ocd information
    """
    def __init__(self,
                 id):
        self.id = id
        self.likelihood = Likelihood()
        self.posterior = Likelihood()

    def __repr__(self):
        if(hasattr(self,"name")):
            if(hasattr(self,"date") and hasattr(self,"error")):
                return self.name + ": " + str(self.date) + "±" + str(self.error) + "BP"
            else:
                return self.name
        else:
            return "{}".format(self.id)

    def __str__(self):
        print(self.__dict__)
        print(self.likelihood)
        if(hasattr(self,"name")):
            if(hasattr(self,"date") and hasattr(self,"error")):
                return self.name + ": " + str(self.date) + "±" + str(self.error) + "BP"
            else:
                return self.name
        else:
            return "{}".format(self.id)

    def set_param(self,line):
        # define grammar
        a = line.find("]")
        b = line.find("=")
        if(a>0 and b>0 and (b-a)==1):
            return
        else:
            modele = Word( alphas ) + "[" + Word(nums) + "]" + Word(objectPath) + "=" + Word( divers )
            try:
                pd = modele.parseString( line )
            except ParseException as pe:
                pass
            else:
                obj = pd[0]
                key = pd[4]
                value = pd[6][:len(pd[6])-1]
                nb = int(pd[2])
                if(key[0]=="."):
                    key = key[1:]                           #expect ".keyword"
                    if(key.find(".")<0):                    #a single keyword
                        if(key in ocd_str_param):
                            setattr(self,key,set_str(value))
                            #print("->  ocd[{id}].{key}={value}".format(id=self.id,key=key,value=value))
                        elif(key in ocd_int_param):
                            setattr(self,key,int(value))
                            #print("->  ocd[{id}].{key}={value}".format(id=self.id,key=key,value=value))
                    else:
                        keywords = key.split(".")
                        if(keywords[0]=="likelihood"):
                            self.likelihood.set_param(keywords,value)
                        elif(keywords[0]=="posterior"):
                            self.posterior.set_param(keywords,value)

    def get_meta(self,
                 arg="#",
                 calib = None,
                 calibs = None):
        out = ""
        if("ref" in self.__dict__.keys()):
            out = out + "{arg} {value}\n".format(arg=arg,value=self.ref)
        if(calib != None):
            out = out + calib.get_meta(arg=arg)
        elif(calibs != None):
            out = out + calibs[self.calib].get_meta(arg=arg)
        if("name" in self.__dict__.keys()):
            out = out + "{arg} {value}\n".format(arg=arg,value=self.name + ": " + str(self.date) + "±" + str(self.error) + "BP")
        out = out + self.likelihood.get_meta(arg=arg)
        return out

    def set_axis(self):
        self.likelihood.set_axis()
        self.posterior.set_axis()

    def adjust_comparaison(self,
                           resolution = 2,
                           verbose = False):
        d0_l = self.likelihood.array[0,0]
        d0_p = self.posterior.array[0,0]
        dn_l = self.likelihood.array[-1,0]
        dn_p = self.posterior.array[-1,0]
        dbt = (d0_p - d0_l)/resolution
        fin = (dn_p - dn_l)/resolution
        #print(d0_l, dn_l, "-", d0_p, dn_p)
        #print(dbt, fin)

        a = len(self.likelihood.array[:,0])
        b = len(self.posterior.array[:,0])
        #print(a,b)
        tr_date_l = self.likelihood.array[max(0,dbt):a+min(0,fin),0]
        trunck_l = self.likelihood.array[max(0,dbt):a+min(0,fin),1]
        tr_date_p = self.posterior.array[-min(0,dbt):b-max(0,fin),0]
        trunck_p = self.posterior.array[-min(0,dbt):b-max(0,fin),1]

        #print(len(trunck_l), len(trunck_p))
        if(tr_date_l[0] != tr_date_p[0]):
            print("Warning!!! not same start date")
            print(tr_date_l[0], " vs ", tr_date_p[0])
        if(tr_date_l[-1] != tr_date_p[-1]):
            print("Warning!!! not same end date")
            print(tr_date_l[-1], " vs ", tr_date_p[-1])

        out = 0
        for i in range(len(trunck_l)):
            if(trunck_l[i]>0.1 and trunck_p[i]>0.1):
                out = max(out, (trunck_p[i]/trunck_l[i]))

        if(verbose):
            print("alpha = ", out)
        #print("agreement = ", self.posterior.agreement)
        return out



class Calibration(object):
    """
    Calibration structure, to store the calib curve
    """
    def __init__(self,
                 id):
        self.id = id
        self.bp = np.zeros(0)
        self.calibAxis = np.zeros(0)

    def __repr__(self):
        if("ref" in self.__dict__.keys()):
            return self.ref
        else:
            return "{}".format(self.id)

    def __str__(self):
        print(self.__dict__.keys())
        if("ref" in self.__dict__.keys()):
            return self.ref
        else:
            return "{}".format(self.id)

    def set_param(self,line):
        # define grammar
        a = line.find("]")
        b = line.find("=")
        if(a>0 and b>0 and (b-a)==1):
            return
        else:
            modele = Word( alphas ) + "[" + Word(nums) + "]" + Word(objectPath) + "=" + Word( divers )
            try:
                pd = modele.parseString( line )
            except ParseException as pe:
                pass
            else:
                obj = pd[0]
                key = pd[4]
                value = pd[6][:len(pd[6])-1]
                nb = int(pd[2])
                if(key[0]=="."):
                    key = key[1:]                           #expect ".keyword"
                    if(key.find(".")<0):                    #a single keyword
                        if(key in ("ref")):
                            setattr(self,key,set_str(value))
                            #print("->  ocd[{id}].{key}={value}".format(id=self.id,key=key,value=value))
                        elif(key in ("start","resolution")):
                            setattr(self,key,float(value))
                            #print("->  ocd[{id}].{key}={value}".format(id=self.id,key=key,value=value))
                        elif(key in ("bp","sigma")):
                            setattr(self,key,np.array([float(x) for x in commaSeparatedList.parseString(set_str(value))]))

    def set_axis(self):
        if(hasattr(self,"start") and hasattr(self,"resolution")):
            self.calibAxis = np.zeros(len(self.bp))
            for i in range(len(self.bp)):
                self.calibAxis[i] = self.start+i*self.resolution
            self.array = np.array([self.calibAxis,
                                  self.bp,
                                  self.sigma]
                                ).transpose()

    def get_meta(self,
                 arg="#"):
        out = ""
        if("ref" in self.__dict__.keys()):
            out = out + "{arg} {value}\n".format(arg=arg,value=self.ref)
        return out
