# -*- coding: utf-8 -*-

"""

    Part of the pyC14 scripts set, used to calibrate C14 data.

    @author Christophe Le Bourlot, MATEIS - INSA LYON - UMR CNRS 5510 
    @date 10/01/2014
    @version 0.1

    Copyright © 2014 INSA Lyon - MATEIS

    ..decription:
        a set of classes to store and describe radiocarbon data.
        It is based on the IOSACal package to try to be as
        compatible as possible, but some classes are redefined
        in order to be more general.


    :example:

    >>> print(RadiocarbonSample(4713, 54))
    RadiocarbonSample( 4713 ± 54 )



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




class RadiocarbonSample(object):
    '''A radiocarbon determination.

    Exactly the IOSACal definition.
    '''

    def __init__(self, date, sigma):
        self._date  = date
        self._sigma = sigma

    @property
    def date(self):
        doc = "Radiocarbon date (BP), before calibration."
        def fget(self):
            return self._date
    
    @property
    def sigma(self):
        doc = "Radiocarbon satndard deviation (years)."
        def fget(self):
            return self._sigma
        
    @property
    def string(self):
        doc = "string representation of the date: (age ± sigma)"
        def fget(self):
            return "( {date} ± {sigma} )".format(date=self._date, sigma=self._sigma)

    def __str__(self):
        return "RadiocarbonSample( {date} ± {sigma} )".format(date=self._date, sigma=self._sigma)



if __name__ == "__main__":
    print(RadiocarbonSample(4713, 54))

    import doctest
    doctest.testmod()