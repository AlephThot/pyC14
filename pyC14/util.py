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
import numpy as np

try:
    from scipy.interpolate import interp1d
except ImportError:
    #: if SciPy is available, also interpolation will be
    HAS_SCIPY = False
else:
    HAS_SCIPY = True


def Property(func):
    return property(**func()) 

def set_str(mot):
    return mot[1:-1]


def interpolate(raw_data,
                step = 1):
    '''Interpolate calibration curve for more fine-grained results.'''
    if HAS_SCIPY is True:
        nd = len(raw_data[0])
        # XXX interp1d only accepts ascending values
        _data = raw_data.copy()
        #print("raw data", raw_data[:10])
        do_flip = (_data[0,0]>_data[-1,0])
        if(do_flip):
            _data = np.flipud(_data)
        #print("_data", _data[:10])
        _arange = np.arange(_data[0,0], _data[-1,0],step)
        #print("_arange", _data[0,0], _data[-1,0])
        #print("_arange", _arange)
        if(nd==2):
            _spline_0 = interp1d(_data[:,0], _data[:,1])
            _interpolated_0 = _spline_0(_arange)
            _data = np.array([_arange,
                            _interpolated_0]
                            ).transpose()
            if(do_flip):
                raw_data = np.flipud(_data) # see above XXX
        if(nd==3):
            _spline_0 = interp1d(_data[:,0], _data[:,1])
            _interpolated_0 = _spline_0(_arange)
            _spline_1 = interp1d(_data[:,0], _data[:,2])
            _interpolated_1 = _spline_1(_arange)
            _data = np.array([_arange,
                            _interpolated_0,
                            _interpolated_1]
                            ).transpose()
            if(do_flip):
                _data = np.flipud(_data) # see above XXX
    else:
        pass
    return _data