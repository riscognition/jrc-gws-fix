# jrc-gws-fix

# datatype uint8 => just values from 0-255
# NaN and -1 not available
# set to 0

# next three lines are not needed!!
import os
os.environ['GDAL_DATA'] = r'C:\Users\Internet\anaconda3\envs\geo_env\Library\share\gdal'
os.environ['PROJ_LIB'] = r'C:\Users\Internet\anaconda3\envs\geo_env\Library\share\proj'

###########
#file = "seasonality_0E_10Nv1_4_2021.tif"
###########

# extract no data values
def nd_values(file):
    # read raster
    driver = gdal.GetDriverByName('GTiff')
    ras = gdal.Open(file)
    band = ras.GetRasterBand(1)
    ip_raster = band.ReadAsArray()

    # reclassify
    for row in range(0,ip_raster.shape[0]):
        ip_raster[row][np.where(ip_raster[row] != 255)] = 0
        ip_raster[row][np.where(ip_raster[row] == 255)] = 1

    # create new file
    nd_raster = driver.Create('nd_' + file, ras.RasterXSize , ras.RasterYSize , 1)
    nd_raster.GetRasterBand(1).WriteArray(ip_raster)
    
    # spatial ref system
    proj = ras.GetProjection()
    georef = ras.GetGeoTransform()
    nd_raster.SetProjection(proj)
    nd_raster.SetGeoTransform(georef)
    nd_raster.FlushCache()
    del nd_raster

#######
#file2 = "nd_seasonality_0E_10Nv1_4_2021.tif"
#######

def binary_dilation(file2):
    # read raster
    driver = gdal.GetDriverByName('GTiff')
    ras = gdal.Open(file2)
    band = ras.GetRasterBand(1)
    nd_raster = band.ReadAsArray()

    # binary dilation
    nd_raster = ndimage.binary_dilation(nd_raster, iterations = 50)

    # create new file
    bd_raster = driver.Create('bd_' + file, ras.RasterXSize , ras.RasterYSize , 1)
    bd_raster.GetRasterBand(1).WriteArray(nd_raster)

    # spatial ref system
    proj = ras.GetProjection()
    georef = ras.GetGeoTransform()
    bd_raster.SetProjection(proj)
    bd_raster.SetGeoTransform(georef)
    bd_raster.FlushCache()
    #del bd_raster

#####
#file3 = "bd_seasonality_0E_10Nv1_4_2021.tif"
#####

def bd_merge(file,file3):
    # read raster
    driver = gdal.GetDriverByName('GTiff')
    ras = gdal.Open(file)
    band = ras.GetRasterBand(1)
    original_raster = band.ReadAsArray()
    ras = gdal.Open(file3)
    band = ras.GetRasterBand(1)
    bd_raster = band.ReadAsArray()

    # new raster on condition
    bd_raster = np.where((bd_raster == 1), 100, original_raster)
    bd_raster = np.where((bd_raster > 10), 0, 1)

    # create new file
    wm_raster = driver.Create("wm_" + file, ras.RasterXSize , ras.RasterYSize , 1)
    wm_raster.GetRasterBand(1).WriteArray(bd_raster)
    # wm_raster.GetRasterBand(1).SetNoDataValue(0) 

    # spatial ref system
    proj = ras.GetProjection()
    georef = ras.GetGeoTransform()
    wm_raster.SetProjection(proj)
    wm_raster.SetGeoTransform(georef)
    wm_raster.FlushCache()
    del wm_raster, original_raster, bd_raster

def all_in_one(file):
    # read raster
    driver = gdal.GetDriverByName('GTiff')
    ras = gdal.Open(file)
    band = ras.GetRasterBand(1)
    original_raster = band.ReadAsArray()
    ip_raster = band.ReadAsArray()

    # reclassify
    for row in range(0,ip_raster.shape[0]):
        ip_raster[row][np.where(ip_raster[row] != 255)] = 0
        ip_raster[row][np.where(ip_raster[row] == 255)] = 1

    # binary dilation
    ip_raster = ndimage.binary_dilation(ip_raster, iterations = 50)

    # new raster on condition
    ip_raster = np.where((ip_raster == 1), 100, original_raster)
    ip_raster = np.where((ip_raster > 10), 0, 1)

    # create new file
    nd_raster = driver.Create(os.path.join('water_mask', file), ras.RasterXSize , ras.RasterYSize , 1)
    nd_raster.GetRasterBand(1).WriteArray(ip_raster)
    
    # spatial ref system
    proj = ras.GetProjection()
    georef = ras.GetGeoTransform()
    nd_raster.SetProjection(proj)
    nd_raster.SetGeoTransform(georef)
    nd_raster.FlushCache()
    del nd_raster, ip_raster

# saves only final result
if __name__ == "__main__":
    try:
        import gdal
    except ModuleNotFoundError:
        from osgeo import gdal
    import numpy as np
    from scipy import ndimage
    from datetime import datetime

    st = datetime.now()
    start_time = st.strftime("%d/%m/%Y %H:%M:%S")
    print("Start Time =", start_time, '\n')

    # new folder
    newpath = 'water_mask' 
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    file_counter = 1
    for file in os.listdir("D:\Riscognition\SAFERS\water_mask\seasonality_jrc"):
        print(file, '(file ', file_counter, 'of ', len(os.listdir("D:\Riscognition\SAFERS\water_mask\seasonality_jrc")), ')')
        all_in_one(file)

    et = datetime.now()
    current_time = et.strftime("%d/%m/%Y %H:%M:%S")
    duration = et - st
    print('Endtime Time =', current_time, '\n')
    print('Duration: ', duration, '\n')

# # stores intermediate results
# if __name__ == "__main__":
    # import os
    # try:
    #     import gdal
    # except ModuleNotFoundError:
    #     from osgeo import gdal
    # import numpy as np
    # from scipy import ndimage
    # from datetime import datetime

    # st = datetime.now()
    # start_time = st.strftime("%d/%m/%Y %H:%M:%S")
    # print("Start Time =", start_time, '\n')

    # nd_values(file)
    # binary_dilation(file2)
    # bd_merge(file, file3)

    # et = datetime.now()
    # current_time = et.strftime("%d/%m/%Y %H:%M:%S")
    # duration = et - st
    # print('Endtime Time =', current_time, '\n')
    # print('Duration: ', duration, '\n')