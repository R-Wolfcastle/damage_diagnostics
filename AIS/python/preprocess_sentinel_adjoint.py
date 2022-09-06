#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mayb 04 14:33:30 2022

@author: Trys
"""

from netCDF4 import Dataset
import numpy as np
import sys
sys.path.insert(1, "/nfs/b0133/eetss/my_python_modules")
from bike_sentinel_prep import open_hogg_500m, save_nc, nctoamr

geom_data_dir = "/nfs/b0133/eetss/BISICLES/damage_in_the_ASE/inputs/bike_input_data/"
io_dir = "/nfs/b0133/eetss/BISICLES/damage_in_the_ASE/inputs/damage_representation_inv/all_21_much_damage/"

def make_input_files():
    asegeo = Dataset(geom_data_dir + 'ase_bedmachine_500m.nc','r')
    x = asegeo.variables['x'][:]
    y = asegeo.variables['y'][:]
    
    xx,yy = np.meshgrid(x,y)

    thk = asegeo.variables['thk'][:,:]
    topg = asegeo.variables['topg'][:,:]
   
    xa,ya,uo,uc = open_hogg_500m(geom_data_dir + 'ASE_20210101-20211231_filt_speed.tif', x, y)

    cropj = np.argmax(y > -720.0e+3)
    uc[0:cropj,:] = 0.0
    
    ncf = io_dir + 'ase_init_2021.nc'
    hdf = io_dir + 'ase_init_2021.hdf5'
   
    save_nc(x, y, { 'uo' : uo , 'uc' : uc }, ncf)
    nctoamr(ncf, hdf, "uo uc")


make_input_files()
