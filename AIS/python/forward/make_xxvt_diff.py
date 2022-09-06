from osgeo import gdal
import sys
sys.path.insert(1, "/nfs/b0133/eetss/my_python_modules")
from odd_geo_fcts import array_to_geotiff
import numpy as np

superdir = "/nfs/b0133/eetss/BISICLES/diagnostic_damage_study/data/AIS/forward/2km_no_dreg/outputs/"

t1 = gdal.Open(superdir + "xxvt_flaheal_shelves_clin_jfnk.tiff")
t1a = t1.ReadAsArray()
t2a = gdal.Open(superdir + "xxvt_flaheal_none_clin_jfnk.tiff").ReadAsArray()

#diff_p = ((t1a-t2a)/t2a)*100
diff = t1a-t2a
diff[t2a==0]=np.nan

array_to_geotiff(diff, t1, superdir+"damaged_shelves_xxvt_diff.tiff", compression="DEFLATE")


