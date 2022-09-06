#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 9 14:35:00 2022

@by: Trys
"""

from pathlib import Path

import sys
sys.path.insert(1, '/nfs/b0133/eetss/BISICLES/BISICLES/applications/bedmachine_antarctica/python/')
from bisiclesIO import BisiclesData
sys.path.insert(1, "/nfs/b0133/eetss/my_python_modules")
from bike_sentinel_prep import save_nc, nctoamr
import numpy as np
import cv2


##ASE:
#xo = -1838500
#yo = -880500

##AIS:
xo = 0
yo = 0


def reg_coulomb_from_linear_coef(c_lin, u_base, uf=300, m=3):
    #HACK, but I don't want infinite values of C_rc, so:
    u_base[u_base==0]=1
    #hopefully, given that it's just isolated spots, this shouldn't balls things up too much...

    return c_lin * (0.5 + u_base) * ((1/uf+1/u_base)**(1/m))


def increase_res(data, factor):
    if data.ndim == 2:
        dsize1 = data.shape[1] * factor
        dsize2 = data.shape[0] * factor
        dsize = (dsize1, dsize2)
        newdata = cv2.resize(data, dsize, interpolation = cv2.INTER_LINEAR)
    elif data.ndim == 1:
        #we just have a linear line of coords:
        current_res = data[1]-data[0]
        new_res = current_res/factor
        min_ = data[0]-(current_res/2)
        max_ = data[-1]+(current_res/2)
        newdata = np.arange(min_+(new_res/2), max_+(new_res/2), new_res)
    return newdata

def prep(bike_file, out_ncf, out_hdf, level=3, plot=False, mucoef_region_type=1, up_factor=1, sliding_law=2, j_region="all"):
    with BisiclesData(bike_file, level=level, plot_file=plot) as bike_data:
        assert (up_factor & (up_factor-1) == 0) and up_factor != 0, "up_factor must be a power of 2"
        assert j_region in ["all", "gnd", "flt"], "j_region should be one of `all`, `gnd` (grounded ice) or `flt` (floating ice)"

        u = bike_data.speed
        mucoef = bike_data.mucoef
        btrac = bike_data.beta
        ocean = (bike_data.surf==0)

        if sliding_law==2:
            basal_friction_param_name = "c_third_jreg_300"
#        btrac[ocean]=0
            print("regularised coulomb friction law")
            c_rc = reg_coulomb_from_linear_coef(btrac, u)
#        c_rc[ocean]=0
        elif sliding_law==1:
            basal_friction_param_name = "c_one"
            print("linear friction law")
            c_rc = btrac
       
        mucoef = {
            '1': lambda mucoef: mucoef,
            '2': lambda mucoef: np.ones_like(mucoef),
            '3': lambda mucoef: np.where(btrac==0, 1, mucoef),
            '4': lambda mucoef: np.where(btrac==0, mucoef, 1)
        }.get(str(mucoef_region_type),
                lambda mucoef: print("1: use mucoef everywhere,\
                                      2: set mucoef to 1 everywhere\
                                      3: set mucoef to 1 on floating ice,\
                                      4: set mucoef to 1 on grounded ice"))(mucoef)

        if up_factor==1:
            x = bike_data.x + xo
            y = bike_data.y + yo
        else:
            x = increase_res(bike_data.x + xo, 4)
            y = increase_res(bike_data.y + yo, 4)
            c_rc = increase_res(c_rc, 4)
            mucoef = increase_res(mucoef, 4)

        uo = np.zeros_like(u)
        uc = np.ones_like(uo)
        uc[ocean]=0

        if j_region=="gnd":
            uc[btrac==0]=0
        elif j_region=="flt":
            uc[btrac!=0]=0

        save_nc(x, y, {'uo': uo, 'uc': uc, basal_friction_param_name: c_rc,  'mucoef': mucoef}, out_ncf)
        nctoamr(out_ncf, out_hdf, 'uo uc {} mucoef'.format(basal_friction_param_name))

data_dir = "/nfs/b0133/eetss/BISICLES/diagnostic_damage_study/data/AIS/adjoint/inv_2km_no_dreg/"

ctrls_dir = "/nfs/b0133/eetss/BISICLES/diagnostic_damage_study/data/AIS/inverse/steph_package/relax_thermodynamics/outputs/2km_run/"
ctrl_file = ctrls_dir + "ctrl.relax_thk.02lev.000103000005.2d.hdf5"

prep(ctrl_file, data_dir+"AIS_thermo_c_reg_clm_heal_none_jgnd.nc", 
				data_dir+"AIS_thermo_c_reg_clm_heal_none_jgnd.hdf5",
				level=2, plot=False, mucoef_region_type=1,
				up_factor=1, sliding_law=1, j_region="gnd")







