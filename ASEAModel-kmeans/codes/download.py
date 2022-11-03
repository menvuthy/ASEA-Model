import ee
ee.Initialize()
import math
import folium
from shapely.geometry import Polygon


# Mask cloud function
def maskCloudSR(image):
  # Bits 3 and 5 are cloud shadow and cloud, respectively.
  cloudShadowBitMask = (1 << 3)
  cloudsBitMask = (1 << 5)
  # Get the pixel QA band
  qa = image.select('QA_PIXEL')
  # Both flags should be set to zero, indicating clear conditions
  mask = qa.bitwiseAnd(cloudShadowBitMask).eq(0).And(qa.bitwiseAnd(cloudsBitMask).eq(0))
  return image.updateMask(mask)

# ------ Landsat 8 & 9 ------ #
# Applies scaling factors.
def applyScaleFactorsL8(image):
  opticalBands = image.select('SR_B.').multiply(0.0000275).add(-0.2)
  thermalBands = image.select('ST_B.*').multiply(0.00341802).add(149.0)
  return image.addBands(opticalBands, None, True).addBands(thermalBands, None, True)

# ------ Landsat 5 & 7 ------ #
# Applies scaling factors.
def applyScaleFactorsL457(image):
  opticalBands = image.select('SR_B.').multiply(0.0000275).add(-0.2)
  thermalBands = image.select('ST_B6').multiply(0.00341802).add(149.0)
  return image.addBands(opticalBands, None, True).addBands(thermalBands, None, True)

# Create no-cloud image and clip area of interest
def image_no_clouds(aoi, start_date, end_date):
  # importing image collection and filtering
  # Rescale and mask cloud
  if int(start_date[:4]) > 2014:
    l8_collection = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
    l9_collection = ee.ImageCollection("LANDSAT/LC09/C02/T1_L2")
    img_col = ee.ImageCollection(l8_collection.merge(l9_collection)).filterDate(start_date, end_date)
    rescale_mkCloud = img_col.map(applyScaleFactorsL8).map(maskCloudSR).median()

  if int(start_date[:4]) <= 2014:
    l5_collection = ee.ImageCollection('LANDSAT/LT05/C02/T1_L2')
    l7_collection = ee.ImageCollection('LANDSAT/LE07/C02/T1_L2')
    img_col = ee.ImageCollection(l5_collection.merge(l7_collection)).filterDate(start_date, end_date)
    rescale_mkCloud = img_col.map(applyScaleFactorsL457).map(maskCloudSR).median()
  
  # Clip region
  dataset = rescale_mkCloud.clip(aoi)
  return dataset

# ------ Calculate EPSG ------ #
# Calculate the epsg code
def convert_wgs_to_utm(lon, lat):
    utm_band = str((math.floor((lon + 180) / 6 ) % 60) + 1)
    if len(utm_band) == 1:
        utm_band = '0'+utm_band
    if lat >= 0:
        epsg_code = '326' + utm_band
    else:
        epsg_code = '327' + utm_band
    return epsg_code






  