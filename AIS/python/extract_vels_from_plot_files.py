#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 6 16:20:32 2022

@by: Trys
"""

from pathlib import Path

import sys
sys.path.insert(1, '/nfs/b0133/eetss/BISICLES/BISICLES/applications/bedmachine_antarctica/python/')
from bisiclesIO import BisiclesData
sys.path.insert(1, "/nfs/b0133/eetss/my_python_modules")
from inverse_analysis_foe1 import save_raster

#xo = -3128078
xo = -3333250
#yo = 2517033
yo = -3333250
#Just the ol BedMachine ones...

def save_var_tiffs_from_bike_file(fp, xo, yo, tif_dir, level=1, plot=True):
    with BisiclesData(fp, level=level, plot_file=plot) as bike_data:
        u = bike_data.speed
        u_path = tif_dir+'/modelled_speed.tiff'
        save_raster(u_path, bike_data.x-(1000*bike_data.x.shape[0]/2), bike_data.y-(1000*bike_data.y.shape[0]/2), u)

superdir = "/nfs/b0133/eetss/BISICLES/diagnostic_damage_study/data/AIS/forward/2km_no_dreg/outputs/"

#paths = list(map(lambda p: str(p), Path(superdir).rglob("heal_shelves_clin_jfnk_01_thres*/plot*.hdf5")))

#for path in paths:
#    dir_ = "/".join(path.split("/")[:-1])
#    save_var_tiffs_from_bike_file(path, xo, yo, dir_, level=3, plot=True)

path = superdir+"heal_shelves_clin_jfnk_01_thres/plot.ais_thermo_2km_heal_shelves.000000.2d.hdf5"
dir_ = superdir+"heal_shelves_clin_jfnk_01_thres/"
save_var_tiffs_from_bike_file(path, xo, yo, dir_, level=3, plot=True)
