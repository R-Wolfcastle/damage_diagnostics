#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 6 16:17:43 2022

@by: Trys
"""
from pathlib import Path
import numpy as np
from osgeo import gdal

import sys
sys.path.insert(1, "/nfs/b0133/eetss/my_python_modules/")

from inverse_analysis_foe1 import save_viscous_tesor_from_plot_file_mod, save_vel_from_plot_file_mod, save_thickness_from_plot_file_mod
from tensor_operations import flow_align
from odd_geo_fcts import array_to_geotiff

iodir = "/nfs/b0133/eetss/BISICLES/diagnostic_damage_study/data/AIS/forward/2km_no_dreg/outputs/"

paths = list(map(lambda p: str(p), Path(iodir).rglob("heal_none*/plot.*.hdf5")))

#xo = -1838500
#yo = -880500


def get_vt_fla(plot_fp, suffix):
    xxfp, xyfp, yxfp, yyfp = save_viscous_tesor_from_plot_file_mod(plot_fp, iodir, suffix=suffix, mesh_level=3)
    vxfp, vyfp, ufp = save_vel_from_plot_file_mod(plot_fp, iodir, suffix=suffix, mesh_level=3)
    thk_fp = save_thickness_from_plot_file_mod(plot_fp, iodir, suffix=suffix, mesh_level=3)

    thk = gdal.Open(thk_fp, gdal.GA_ReadOnly).ReadAsArray()

    xvel_tiff = gdal.Open(vxfp, gdal.GA_ReadOnly)
    xvel = xvel_tiff.ReadAsArray()
    yvel = gdal.Open(vyfp, gdal.GA_ReadOnly).ReadAsArray()
    xxvt = gdal.Open(xxfp, gdal.GA_ReadOnly).ReadAsArray()
    xyvt = gdal.Open(xyfp, gdal.GA_ReadOnly).ReadAsArray()
    yxvt = gdal.Open(yxfp, gdal.GA_ReadOnly).ReadAsArray()
    yyvt = gdal.Open(yyfp, gdal.GA_ReadOnly).ReadAsArray()
    
    vt = np.transpose(np.array([[np.transpose(xxvt), np.transpose(xyvt)], [np.transpose(yxvt), np.transpose(yyvt)]]))
    
    vtfla = flow_align(vt, xvel, yvel)
    
    xxvt_fla = vtfla[:,:,0,0]/thk
    yyvt_fla = vtfla[:,:,1,1]/thk
    xyvt_fla = vtfla[:,:,0,1]/thk
    yxvt_fla = vtfla[:,:,1,0]/thk
    
    array_to_geotiff(xxvt_fla, xvel_tiff, iodir+"xxvt_mean_fla{}.tiff".format(suffix), compression="DEFLATE")
    array_to_geotiff(yyvt_fla, xvel_tiff, iodir+"yyvt_mean_fla{}.tiff".format(suffix), compression="DEFLATE")
    array_to_geotiff(xyvt_fla, xvel_tiff, iodir+"xyvt_mean_fla{}.tiff".format(suffix), compression="DEFLATE")
    array_to_geotiff(yxvt_fla, xvel_tiff, iodir+"yxvt_mean_fla{}.tiff".format(suffix), compression="DEFLATE")


for path in paths:
    dir_ = "/".join(path.split("/")[:-1])
    suffix = dir_.split("/")[-1]
    get_vt_fla(path, suffix)






