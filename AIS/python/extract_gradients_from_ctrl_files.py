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

def save_var_tiffs_from_bike_file(fp, tif_dir, cycle, level=1, plot=True):
    with BisiclesData(fp, level=level, plot_file=plot) as bike_data:
        bike_data.get_gradjmu()
        save_path = tif_dir+'/grad_j_mu.{}.tiff'.format(cycle)
        save_raster(save_path, bike_data.x-(2000*bike_data.x.shape[0]/2), bike_data.y-(2000*bike_data.y.shape[0]/2), bike_data.gradjmu)

superdir = "/nfs/b0133/eetss/BISICLES/diagnostic_damage_study/data/AIS/inverse/steph_package/relax_thermodynamics/outputs/2km_run/"

paths = list(map(lambda p: str(p), Path(superdir).rglob("ctrl*.0001*.hdf5")))

for path in paths:
    dir_ = "/".join(path.split("/")[:-1])
    cycle = path.split(".")[-3]
    save_var_tiffs_from_bike_file(path, dir_, cycle, level=2, plot=False)

