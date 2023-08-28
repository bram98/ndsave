# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 13:04:49 2023

@author: bverr
"""
import numpy as np
from ast import literal_eval
import re

def savetxt(fname, X, fmt='%.18e',
              delimiter=' ', newline='\n', comments='#', 
              axisdata=None, axisnames=None,
              header='',
              footer=''):
    if not fname.endswith('.txt'):
        fnametxt = fname + '.txt'
    else: 
        fnametxt = fname
        
    with open(fnametxt, 'w') as f:
        shape = X.shape
        f.write(f'{comments}{shape}\n')
        
        if axisnames is None:
            axisnames = np.full( (len(shape), ), None )
        if axisdata is None:
                axisdata = np.full( (len(shape), ), None )            
                
        for axis in range(len(shape)):
            axisname = ''
            if axis >= len(axisnames) or axisnames[axis] is None:
                axisname = str(axis)
            else:
                axisname = axisnames[axis]
                
            f.write(f'{comments}axis {axis} ({axisname})\n')
        
            
            if axis >= len(axisdata) or axisdata[axis] is None:
                axisdata_ =  np.arange(shape[axis])
            else:
                if len(axisdata[axis]) != shape[axis]:
                    raise IndexError(f'Error at axis {axis}. Provided axisdata does not match shape of array. {len(axisdata[axis])} != {shape[axis]}')
                axisdata_ = axisdata[axis]
            axisdata_ = np.array(axisdata_)
            axisdata_ = np.array2string(axisdata_, separator=',')
            f.write(f'{comments}{axisdata_}\n')
            
        if header != '':
            f.write(f'{comments}{header}\n')
        
        prev_index = np.zeros(len(shape), dtype=np.int32)
        newline_multiplicity = np.flip(np.arange(len(shape)))
        for index, x in np.ndenumerate(X):
            index_ = np.array(index)
            
            newline_copies = int( 
                newline_multiplicity.dot( np.clip(index_ - prev_index, 0, np.inf) ) 
                )
            string = newline_copies*str(newline) + \
                fmt%x + \
                delimiter
            f.write(string)
            
            prev_index = index_
            
        if footer != '':
            f.write(f'\n{comments}{footer}')
            
def loadtxt(fname, comments='#', **kwargs):
    axisnames = []
    axisdata = []
    with open(fname, 'r') as f:
        shape = f.readline().replace(comments, '')
        shape = literal_eval(shape)
        for axis in range(len(shape)):
            axisname = f.readline()
        
            axisname = re.search(f'{comments} axis \d+ \((.+)\)', axisname)
            
            if axisname is None:
                axisname = ['',str(axis)]
            
            axisnames.append( axisname[1] )
            
            axisdata_ = f.readline().replace(comments, '')
            axisdata_ = literal_eval(axisdata_)
            axisdata.append(axisdata_)
            
    return ( np.loadtxt(fname, **kwargs).reshape(shape), axisdata, axisnames)

def genfromtxt(fname, comments='#', **kwargs):
    axisnames = []
    axisdata = []
    with open(fname, 'r') as f:
        shape = f.readline().replace(comments, '')
        shape = literal_eval(shape)
        for axis in shape:
            axisname = f.readline()
            axisname = re.search(f'{comments} axis \d+ \((.)\)', axisname)
            if axisname is None:
                axisname = ['',str(axis)]
            
            axisnames.append( axisname[1] )
            
            axisdata_ = f.readline().replace(comments, '')
            axisdata_ = literal_eval(axisdata_)
            axisdata.append(axisdata_)
        
    return ( np.genfromtxt(fname, **kwargs).reshape(shape), axisdata, axisnames)
