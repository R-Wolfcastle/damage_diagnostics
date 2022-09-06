from osgeo import gdal
import sys
sys.path.insert(1, "/nfs/b0133/eetss/my_python_modules")
from odd_geo_fcts import array_to_geotiff, array_to_multiband_geotiff
import numpy as np

superdir = "/nfs/b0133/eetss/BISICLES/diagnostic_damage_study/data/AIS/forward/2km_no_dreg/outputs/"

def make_zone_map():
    xxvt_tiff = gdal.Open(superdir + "xxvt_flaheal_none_clin_jfnk.tiff")
    xxvt = xxvt_tiff.ReadAsArray()
    #xyvt = gdal.Open(superdir + "xyvt_flaheal_none_clin_jfnk.tiff").ReadAsArray()
    #yxvt = gdal.Open(superdir + "yxvt_flaheal_none_clin_jfnk.tiff").ReadAsArray()
    yyvt = gdal.Open(superdir + "yyvt_flaheal_none_clin_jfnk.tiff").ReadAsArray()
    
    #Assign +ve and -ve values of each to different primes
    #then products will be unique
    xxvt_primes = np.where(xxvt>0, 3, 2)
    yyvt_primes = np.where(yyvt>0, 7, 5)
    
    #zones are: 10: both negative, 14: -x and +y, 15: +x and -y, 21: both positive.
    zones = xxvt_primes*yyvt_primes
    
    array_to_geotiff(zones, xxvt_tiff, superdir+"vt_zones_flaheal_none_clin_jfnk.tiff", compression="DEFLATE")


def multiband_zone_map():
    xxvt_tiff = gdal.Open(superdir + "xxvt_mean_flaheal_none_clin_jfnk.tiff")
    xxvt = xxvt_tiff.ReadAsArray()
    #xyvt = gdal.Open(superdir + "xyvt_flaheal_none_clin_jfnk.tiff").ReadAsArray()
    #yxvt = gdal.Open(superdir + "yxvt_flaheal_none_clin_jfnk.tiff").ReadAsArray()
    yyvt = gdal.Open(superdir + "yyvt_mean_flaheal_none_clin_jfnk.tiff").ReadAsArray()

    vt_norms = np.sqrt(xxvt**2+yyvt**2)

    ting = vt_norms/(1e5)
    ting[ting>=1]=1


    array_to_geotiff(ting*100, xxvt_tiff, superdir+"vt_norm_transband_flaheal_none_clin_jfnk.tiff", compression="DEFLATE")

    raise

    #Assign +ve and -ve values of each to different primes
    #then products will be unique
    xxvt_primes = np.where(xxvt>0, 3, 2)
    yyvt_primes = np.where(yyvt>0, 7, 5)

    #zones are: 10: both negative, 14: -x and +y, 15: +x and -y, 21: both positive.
    zones = xxvt_primes*yyvt_primes
    
    mb_vt = np.zeros((4, xxvt.shape[0], xxvt.shape[1]))

    print(vt_norms.shape)
    print(vt_norms[zones==10])

    mb_vt[0,:,:] = np.where(zones==10, vt_norms, np.nan)
    mb_vt[1,:,:] = np.where(zones==14, vt_norms, np.nan)
    mb_vt[2,:,:] = np.where(zones==15, vt_norms, np.nan)
    mb_vt[3,:,:] = np.where(zones==21, vt_norms, np.nan)

    array_to_multiband_geotiff(mb_vt, xxvt_tiff, superdir+"vt_zones_multiband_flaheal_none_clin_jfnk.tiff", compression="DEFLATE")


def norm_map_per_zone():
    xxvt_tiff = gdal.Open(superdir + "xxvt_mean_flaheal_none_clin_jfnk.tiff")
    xxvt = xxvt_tiff.ReadAsArray()
    yyvt = gdal.Open(superdir + "yyvt_mean_flaheal_none_clin_jfnk.tiff").ReadAsArray()

    vt_norms = np.sqrt(xxvt**2+yyvt**2)

        #Assign +ve and -ve values of each to different primes
    #then products will be unique
    xxvt_primes = np.where(xxvt>0, 3, 2)
    yyvt_primes = np.where(yyvt>0, 7, 5)

    #zones are: 10: both negative, 14: -x and +y, 15: +x and -y, 21: both positive.
    zones = xxvt_primes*yyvt_primes

    nn = np.where(zones==10, vt_norms, np.nan)
    np_ = np.where(zones==14, vt_norms, np.nan)
    pn = np.where(zones==15, vt_norms, np.nan)
    pp = np.where(zones==21, vt_norms, np.nan)

    ids = ["nn", "np", "pn", "pp"]
    vars_ = [nn, np_, pn, pp]
    
    for id_, var_ in zip(ids, vars_):
        array_to_geotiff(var_, xxvt_tiff, superdir+"vt_{}_zone_multiband_flaheal_none_clin_jfnk.tiff".format(id_), compression="DEFLATE")


multiband_zone_map()






