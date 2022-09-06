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
from inverse_analysis_foe1 import get_basal_stress_from_plot_file_mod
#from tensor_operations import flow_align, sorted_eigenvalues_2d, tensor_me_this
from odd_geo_fcts import array_to_geotiff

iodir = "/nfs/b0133/eetss/BISICLES/diagnostic_damage_study/data/AIS/inverse/steph_package/relax_thermodynamics/outputs/2km_run/"

plot_path = iodir+"plot.relax_thk.000000.2d.hdf5"


def calculate_magic_number(e2_fn, e1_fn, thk_fn):
    rho_i = 917
    rho_w = 1028
    g = 9.81

    thk_tif = gdal.Open(iodir+thk_fn, gdal.GA_ReadOnly)
    thk = thk_tif.ReadAsArray()
    e2 = gdal.Open(iodir+e2_fn, gdal.GA_ReadOnly).ReadAsArray()
    e1 = gdal.Open(iodir+e1_fn, gdal.GA_ReadOnly).ReadAsArray()

#    trace = e1+e2

    N = 0.5*rho_i*(1-rho_i/rho_w)*g*thk

    K = 1 - (e2)/N

    array_to_geotiff(K, thk_tif, iodir+"hilmar_magic_buttressing_number.tif", compression="DEFLATE")

calculate_magic_number("e1_mean.tiff", "e1_mean.tiff", "thickness.tiff")

raise

def get_basal_stress():
    get_basal_stress_from_plot_file_mod(plot_path, iodir, suffix=None, mesh_level=2, overwrite=True)


def compare_stresses(bstress_name, ev1_stress_name, ev2_stress_name, thk_name):
    bstress_tif = gdal.Open(iodir+bstress_name, gdal.GA_ReadOnly)
    bs = bstress_tif.ReadAsArray()
    e1_vs = gdal.Open(iodir+ev1_stress_name, gdal.GA_ReadOnly).ReadAsArray()
    e2_vs = gdal.Open(iodir+ev2_stress_name, gdal.GA_ReadOnly).ReadAsArray()
    thk = gdal.Open(iodir+thk_name, gdal.GA_ReadOnly).ReadAsArray()
    #vs_mag = np.sqrt(e1_vs**2+e2_vs**2)*thk #(they were "mean" e1/2 over the thickness, but I want vertically integrated vt!)
    vs_mag = np.sqrt(e1_vs**2+e2_vs**2)

    rat = vs_mag/bs

    array_to_geotiff(rat, bstress_tif, iodir+"mean_vs_bs_rat.tiff",compression="DEFLATE")

def scale_vt(vt_name, rat_name, limit):
    vt_tif = gdal.Open(iodir+vt_name, gdal.GA_ReadOnly)
    vt = vt_tif.ReadAsArray()
    rat = gdal.Open(iodir+rat_name, gdal.GA_ReadOnly).ReadAsArray()

    rat[rat>limit]=limit

    scaled_vt = vt*(1/limit)*rat

    array_to_geotiff(scaled_vt, vt_tif, iodir+"scaled_{}".format(vt_name), compression="DEFLATE")


#get_basal_stress()
#compare_stresses("bstress.tiff", "e1_mean.tiff", "e2_mean.tiff", "thickness.tiff")
scale_vt("yyvt_mean_fla.tiff", "mean_vs_bs_rat.tiff", 10)


raise

def get_vt_fla(plot_fp):
    xxfp, xyfp, yxfp, yyfp = save_viscous_tesor_from_plot_file_mod(plot_fp, iodir, suffix="", mesh_level=2, overwrite=True)
    vxfp, vyfp, ufp = save_vel_from_plot_file_mod(plot_fp, iodir, suffix="", mesh_level=2, overwrite=True)
    thk_fp = save_thickness_from_plot_file_mod(plot_fp, iodir, suffix="", mesh_level=2, overwrite=True)

    thk = gdal.Open(thk_fp, gdal.GA_ReadOnly).ReadAsArray()

    xvel_tiff = gdal.Open(vxfp, gdal.GA_ReadOnly)
    xvel = xvel_tiff.ReadAsArray()
    yvel = gdal.Open(vyfp, gdal.GA_ReadOnly).ReadAsArray()
    xxvt = gdal.Open(xxfp, gdal.GA_ReadOnly).ReadAsArray()
    xyvt = gdal.Open(xyfp, gdal.GA_ReadOnly).ReadAsArray()
    yxvt = gdal.Open(yxfp, gdal.GA_ReadOnly).ReadAsArray()
    yyvt = gdal.Open(yyfp, gdal.GA_ReadOnly).ReadAsArray()

#    vt = np.transpose(np.array([[np.transpose(xxvt), np.transpose(xyvt)], [np.transpose(yxvt), np.transpose(yyvt)]]))
    
    vt = tensor_me_this(xxvt, xyvt, yxvt, yyvt)    
    
    evals = sorted_eigenvalues_2d(vt)

    array_to_geotiff(evals[:,:,0], xvel_tiff, iodir+"e1_mean.tiff", compression="DEFLATE")
    array_to_geotiff(evals[:,:,1], xvel_tiff, iodir+"e2_mean.tiff", compression="DEFLATE")
    

    vtfla = flow_align(vt, xvel, yvel)
    xxvt_fla = vtfla[:,:,0,0]/thk
    yyvt_fla = vtfla[:,:,1,1]/thk
    xyvt_fla = vtfla[:,:,0,1]/thk
    yxvt_fla = vtfla[:,:,1,0]/thk
    

    array_to_geotiff(xxvt_fla, xvel_tiff, iodir+"xxvt_mean_fla.tiff", compression="DEFLATE")
    array_to_geotiff(yyvt_fla, xvel_tiff, iodir+"yyvt_mean_fla.tiff", compression="DEFLATE")
    array_to_geotiff(xyvt_fla, xvel_tiff, iodir+"xyvt_mean_fla.tiff", compression="DEFLATE")
    array_to_geotiff(yxvt_fla, xvel_tiff, iodir+"yxvt_mean_fla.tiff", compression="DEFLATE")


#get_vt_fla(plot_path)

#raise

def principal_visc_stresses(xxfp, xyfp, yxfp, yyfp):
    xxvt_tiff = gdal.Open(xxfp, gdal.GA_ReadOnly)
    xxvt = xxvt_tiff.ReadAsArray()
    xyvt = gdal.Open(xyfp, gdal.GA_ReadOnly).ReadAsArray()
    yxvt = gdal.Open(yxfp, gdal.GA_ReadOnly).ReadAsArray()
    yyvt = gdal.Open(yyfp, gdal.GA_ReadOnly).ReadAsArray()

#    vt = np.transpose(np.array([[np.transpose(xxvt), np.transpose(xyvt)], [np.transpose(yxvt), np.transpose(yyvt)]]))

    vt = tensor_me_this(xxvt, xyvt, yxvt, yyvt)
   
    vt_mod = np.nan_to_num(vt)

    print(np.count_nonzero(~np.isnan(vt_mod)))

    evals = sorted_eigenvalues_2d(vt_mod)
    array_to_geotiff(evals[:,:,0], xxvt_tiff, iodir+"e1_mean.tiff", compression="DEFLATE")
    array_to_geotiff(evals[:,:,1], xxvt_tiff, iodir+"e2_mean.tiff", compression="DEFLATE") 



def vt_mag(e1_fp, e2_fp, mucoef_fp):
    e1_tiff = gdal.Open(e1_fp, gdal.GA_ReadOnly)
    e1 = e1_tiff.ReadAsArray()
    e2 = gdal.Open(e2_fp, gdal.GA_ReadOnly).ReadAsArray()
    mucoef = gdal.Open(mucoef_fp, gdal.GA_ReadOnly).ReadAsArray()

    mag = np.sqrt(e1**2+e2**2)
    mag_dc = mag/mucoef

    array_to_geotiff(mag, e1_tiff, iodir+"e_mag.tiff", compression="DEFLATE")
    array_to_geotiff(mag_dc, e1_tiff, iodir+"e_mag_dc.tiff", compression="DEFLATE")


e1_fp = iodir+"e1_mean.tiff"
e2_fp = iodir+"e2_mean.tiff"
mucoef_fp = iodir+"modelled_mucoef.tiff"

vt_mag(e1_fp, e2_fp, mucoef_fp)



