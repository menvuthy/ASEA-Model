import os
import io
import ee
import glob
import shutil
import requests
import geemap
import numpy as np
import folium
from codes import download
from parameters import aoi, date
import rasterio
from rasterio.merge import merge
from rasterio.mask import mask
from natsort import natsorted
from pyproj import CRS

# Create temporary folder
if not os.path.exists('output/landsat-image/30m-images'):
  os.makedirs('output/landsat-image/30m-images')

# ------ Main Code Execution ------ #
Start_date, End_date = [], []
for i in range(int(date[0][:4]), int(date[1][:4])+1):
  Start_date.append(str(i)+date[0][4:])
  End_date.append(str(i)+date[1][4:])

# Loop download satellite image
for m in range(len(Start_date)):
  start_date = Start_date[m]
  end_date = End_date[m]
  
  # ------ Calculate EPSG ------ #
  # epsg_code = '4326' # WGS 84
  lon = aoi.geometries().getInfo()[0]['coordinates'][0][0][0]
  lat = aoi.geometries().getInfo()[0]['coordinates'][0][0][1]
  epsg_code = download.convert_wgs_to_utm(lon, lat)

  # Split the geometry to small grid 
  grid = geemap.fishnet(aoi, h_interval=0.1, v_interval=0.1, delta=1)
  gridList = grid.toList(grid.size())
  grid_num = grid.toList(grid.size()).length()

  # Create list of each grid feature
  ls_feature = []
  for i in range(grid_num.getInfo()):
    feature = ee.Feature(gridList.get(i)).geometry().bounds()
    ls_feature.append(feature)

  # Create temporary folder
  if not os.path.exists('/content/temp/grid'):
      os.makedirs('/content/temp/grid')

  # Download image by grid
  for i in range(grid_num.getInfo()):
    print('Downloading grid image:', i+1)

    # Extract image from GEE and apply pre-process function
    image = download.image_no_clouds(ls_feature[i], start_date, end_date)

    # Set band IDs based on landsat collection
    if int(start_date[:4]) > 2014:
      BandIDs = ['SR_B6', 'SR_B5', 'SR_B4', 'SR_B3', 'SR_B2']
    else:
      BandIDs = ['SR_B5', 'SR_B4', 'SR_B3', 'SR_B2', 'SR_B1']

    # Download pre-processed image
    download_id = ee.data.getDownloadId({
        'image': image,
        'bands': BandIDs,
        'region': ls_feature[i],
        'scale': 30,
        'format': 'GEO_TIFF',
        'crs' : 'EPSG:'+str(epsg_code),
    })
    response = requests.get(ee.data.makeDownloadUrl(download_id))
    with open('/content/temp/grid/image_grid_'+str(i)+'.tif', 'wb') as fd:
      fd.write(response.content)

  # ------ Merge all grid image to one image ------ #
  # Make a search criteria to select the ndvi files
  q = os.path.join("/content/temp/grid/image*.tif") 

  # sorted files by name
  fp = natsorted(glob.glob(q)) 

  # List for storing the raster image
  src_files = []

  # Open each raster files by iterating and then append to our list
  for raster in fp:
      # open raster file
      files = rasterio.open(raster)

      # add each file to our list
      src_files.append(files)

  # Merge function returns a single mosaic array and the transformation info
  mosaic, out_trans = merge(src_files)

  # Set metadata
  out_meta = src_files[0].meta.copy()
  out_meta.update({"driver": "GTiff",
                  "dtype": "float32",
                  "nodata": None,
                  "height": mosaic.shape[1],
                  "width": mosaic.shape[2],
                  "transform": out_trans,
                  "count": 5,
                  "crs": CRS.from_epsg(int(epsg_code))
                  }
                  )
  # Write the mosaic raster
  # Create temporary folder
  if not os.path.exists('/content/temp/main'):
      os.makedirs('/content/temp/main')
  output = os.path.join('/content/temp/main/image_snrgb_'+start_date[:4]+'.tif')
  with rasterio.open(output, "w", **out_meta) as dest:
      dest.write(mosaic.astype(np.float32))

  # Clip image to aoi geometry
  img_grid = rasterio.open('/content/temp/main/image_snrgb_'+start_date[:4]+'.tif')

  aoi_epsg = aoi.transform(ee.Projection('EPSG:'+str(epsg_code)), 1)

  # Mask raster
  clip, clip_transform = mask(img_grid, aoi_epsg.geometries().getInfo(), crop=True)
  # Set metadata
  out_meta = img_grid.meta.copy()
  out_meta.update({"driver": "GTiff",
                  "dtype": "float32",
                  "nodata": 0 and None,
                  "height": clip.shape[1],
                  "width": clip.shape[2],
                  "transform": clip_transform,
                  "count": 5,
                  "crs": img_grid.crs
                  }
                  )
                  
  # Write the clip raster
  output = os.path.join('output/landsat-image/30m-images/image_snrgb_'+start_date[:4]+'.tif')
  with rasterio.open(output, "w", **out_meta) as dest:
      dest.write(clip.astype(np.float32))

# Shut down temporary directory
shutil.rmtree('/content/temp')

#---------------------------------------------------------------------
if img_grid.read().any() == 0:
  print('Error: Images are not available for this area within the given date.')
else:
  print('Download is finished!')