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
from inverse_analysis_foe1 import save_raster, save_gradjphi_from_ctrl_file_mod

tiff_dir = "/nfs/b0133/eetss/BISICLES/diagnostic_damage_study/data/AIS/adjoint/2km_inv_chk/heal_none/j_total_gnd_usqrd/"
ctrl_fp = tiff_dir+"ctrl.ais_adj_500m_jgnd.02lev.000103000000.2d.hdf5"

if __name__ == '__main__':
    save_gradjphi_from_ctrl_file_mod(ctrl_fp, tiff_dir, mesh_level=2, overwrite=True)

