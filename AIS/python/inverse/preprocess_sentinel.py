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
from bike_sentinel_prep import open_oceanmask, open_damage_data_500m, open_hogg_500m, save_nc, nctoamr

geom_data_dir = "/nfs/b0133/eetss/BISICLES/diagnostic_damage_study/data/AIS/inverse/steph_package/relax_thermodynamics/"
damage_data = "/nfs/b0133/eetss/BISICLES/diagnostic_damage_study/data/AIS/inverse/damage_data/d1ab_max_shear_50_10_01.tiff"
outdir = geom_data_dir

##Not certain about this, but let's have a look:
#from: /nfs/b0133/eetss/BISICLES/BISICLES/applications/bedmachine_antarctica/intermediate_data/preprocess_thk_bed_btrc.py
NX = 6144*2
NY = 6144*2
#sort of implies that the origin is 6144*500m from the centre... no fuckin idea.
#let's go for it though!

def make_damage_input_file():
    #aisgeo = Dataset(geom_data_dir + 'antarctica_bedmachine_geometry_500m.2d-002.hdf5','r')
    
    #print(aisgeo["thk"])
    
    #x = aisgeo.variables['x'][:]
    #y = aisgeo.variables['y'][:]
    
    #I the origin is in the bottom right, so we're going for:
    x = np.arange(0, 500*(NX), 500) - ((NX/2)*500)
    y = np.arange(0, 500*(NY), 500) - ((NY/2)*500)

    xx,yy = np.meshgrid(x,y)

#    thk = asegeo.variables['thk'][:,:]
#    topg = asegeo.variables['topg'][:,:]
   
#    xa,ya,uo,uc = open_hogg_500m(geom_data_dir + 'ASE_20210101-20211231_filt_speed.tif', x, y)

#    cropj = np.argmax(y > -720.0e+3)
#    uc[0:cropj,:] = 0.0
    
#    oceanmask = open_oceanmask(15, 12, x, y)

 #   uo = np.where(oceanmask > 0.5, 0, uo)
 #   uc = np.where(oceanmask > 0.5, 0, uc)
 #   thk = np.where(oceanmask > 0.5, 0, thk)
    
    xd, yd, damage_reg_weights = open_damage_data_500m(damage_data, x, y)

    ncf = outdir + 'ais_damage.nc'
    hdf = outdir + 'ais_damage.hdf5'

    x = x + ((NX/2)*500)
    y = y + ((NY/2)*500)
   
    save_nc(x, y, { 'damage_reg_weights': damage_reg_weights }, ncf)
    nctoamr(ncf, hdf, "damage_reg_weights")


make_damage_input_file()



