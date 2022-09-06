from osgeo import gdal
import sys
sys.path.insert(1, "/nfs/b0133/eetss/my_python_modules")
from odd_geo_fcts import array_to_geotiff
import numpy as np

superdir = "/nfs/b0133/eetss/BISICLES/diagnostic_damage_study/data/AIS/forward/2km_no_dreg/outputs/"

t1 = gdal.Open(superdir + "modelled_speedheal_none_clin_jfnk.tiff")
t1a = t1.ReadAsArray()
t2a = gdal.Open(superdir + "heal_shelves_clin_jfnk_01_thres/modelled_speed.tiff").ReadAsArray()

#diff_p = ((t1a-t2a)/t2a)*100
diff = t1a-t2a
diff[t2a==0]=np.nan
diff_p = diff * 100/t1a

diff_p = np.where(t1a>50, diff_p, 0)

array_to_geotiff(diff_p, t1, superdir+"heal_shelves_clin_jfnk_01_thres/damaged_shelves_speed_diff_p_01_thres.tiff", compression="DEFLATE")



