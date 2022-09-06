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

from inverse_analysis_foe1 import save_mucoef_from_ctrl_file_mod
from tensor_operations import flow_align
from odd_geo_fcts import array_to_geotiff

iodir = "/nfs/b0133/eetss/BISICLES/diagnostic_damage_study/data/AIS/inverse/steph_package/relax_thermodynamics/outputs/2km_dreg/1e6/"

#paths = list(map(lambda p: str(p), Path(iodir).rglob("heal_none*/plot.*.hdf5")))

#xo = -1838500
#yo = -880500


def get_mu_coef(ctrl_fp):
    mu_fp = save_mucoef_from_ctrl_file_mod(ctrl_fp, iodir, suffix=None, mesh_level=2)

    raise

    xxvt_fla = vtfla[:,:,0,0]/thk
    yyvt_fla = vtfla[:,:,1,1]/thk
    xyvt_fla = vtfla[:,:,0,1]/thk
    yxvt_fla = vtfla[:,:,1,0]/thk
    
    array_to_geotiff(xxvt_fla, xvel_tiff, iodir+"xxvt_mean_fla{}.tiff".format(suffix), compression="DEFLATE")
    array_to_geotiff(yyvt_fla, xvel_tiff, iodir+"yyvt_mean_fla{}.tiff".format(suffix), compression="DEFLATE")
    array_to_geotiff(xyvt_fla, xvel_tiff, iodir+"xyvt_mean_fla{}.tiff".format(suffix), compression="DEFLATE")
    array_to_geotiff(yxvt_fla, xvel_tiff, iodir+"yxvt_mean_fla{}.tiff".format(suffix), compression="DEFLATE")

get_mu_coef(iodir+"ctrl.ais_inv_1km_l1l2_dreg_1e6.02lev.000027000010.2d.hdf5")

raise

for path in paths:
    dir_ = "/".join(path.split("/")[:-1])
    suffix = dir_.split("/")[-1]
    get_vt_fla(path, suffix)






