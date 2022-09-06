import sys
sys.path.insert(1, "/nfs/b0133/eetss/my_python_modules")
from odd_geo_fcts import clip_tiff_w_shp

#shp = "/nfs/b0133/eetss/MEaSUREs Antarctic Boundaries/Coastline_Antarctica_v2.shp"
#in_fp = "/nfs/b0133/eetss/BISICLES/diagnostic_damage_study/data/AIS/forward/2km_no_dreg/outputs/damaged_shelves_speed_diff_p.tiff"
#out_fp = "/nfs/b0133/eetss/BISICLES/diagnostic_damage_study/data/AIS/forward/2km_no_dreg/outputs/damaged_shelves_speed_diff_p_measures_clipped.tiff"

shp = "/nfs/b0133/eetss/MEaSUREs Antarctic Boundaries/GroundingLine_Antarctica_v2.shp"
in_fp = "/nfs/b0133/eetss/BISICLES/diagnostic_damage_study/data/AIS/adjoint/2km_inv_chk/heal_none/j_total_gnd_usqrd/grad_j_phi.tiff"
out_fp = "/nfs/b0133/eetss/BISICLES/diagnostic_damage_study/data/AIS/adjoint/2km_inv_chk/heal_none/j_total_gnd_usqrd/grad_j_phi_shelves.tiff"

clip_tiff_w_shp(in_fp, shp, out_fp, invert=True)

