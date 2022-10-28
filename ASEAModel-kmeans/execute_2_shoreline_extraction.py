import os
import cv2
import folium
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon
import rasterio
from rasterio.plot import show
from rasterio.features import shapes
from rasterio.enums import Resampling
from rasterio.plot import show_hist
import matplotlib.pyplot as plt
from codes import shoreline, download, mapping
from parameters import aoi, date


# ------ Shoreline extraction ------ #
# Read input image data
Image = rasterio.open('output/landsat-image/30m-images/image_snrgb_'+date[0][:4]+'.tif')
if Image.read().any() == 0:
  print('Warning: The image is empty!!!')

# Resample data to target shape
rescale_image, transform = shoreline.resampling(image=Image, scale_factor=10)
normalized_rescale = shoreline.normalize(rescale_image)

# Set metadata
out_meta = Image.meta.copy()
out_meta.update({"driver": "GTiff",
                 "dtype": "float32",
                 "nodata": 0 and None,
                 "height": normalized_rescale.shape[1],
                 "width": normalized_rescale.shape[2],
                 "transform": transform,
                 "count": 5,
                 "crs": Image.crs
                 }
                )
# Write the clip raster
output = os.path.join('output/landsat-image/3m-images/image_snrgb_'+date[0][:4]+'.tif')
with rasterio.open(output, "w", **out_meta) as dest:
    dest.write(normalized_rescale.astype(np.float32))

# Read bands
swir = normalized_rescale[0]
nir = normalized_rescale[1]
red = normalized_rescale[2]
green = normalized_rescale[3]
blue = normalized_rescale[4]

# Create RGB natural color composite
RGB = np.dstack((red, green, blue))

# Separate water and non-water by K-Means
Input_DF = pd.DataFrame({'NIR': nir.reshape(-1)})

# Set X as input feature data
X_KMeans = Input_DF.dropna()

# Apply KMeans clustering
kmeans = KMeans(n_clusters=2, init='k-means++', max_iter=200, random_state=1)
Y_KMeans = kmeans.fit(X_KMeans)
# Assign label
X_group = X_KMeans.copy()
X_group['cluster_id'] = Y_KMeans.labels_

# Re-arrange cluster index
clust_kmean = pd.DataFrame()
clust_kmean['id'] = X_KMeans.index
clust_kmean['class'] = kmeans.labels_
indx = []
for i in range(len(Input_DF)):
    indx.append(i)
Index = pd.DataFrame()
Index['id'] = indx
df1 = Index.set_index('id')
df2 = clust_kmean.set_index('id')
df2 = clust_kmean.set_index(df2.index.astype('int64')).drop(columns=['id'])
mask = df2.index.isin(df1.index)
df1['cluster'] = df2.loc[mask, 'class']

# Reshape the cluster array
array = np.array(df1['cluster'])
n_array = array.reshape(nir.shape)

nir_max = np.where(nir == np.nanmax(nir)) 
if n_array[nir_max[0][0]][nir_max[1][0]] == 0:
  n_array2 = np.where(n_array==0, 255, n_array)
  mask = np.where(n_array2 == 1.0, np.nan, n_array2)
else:
  mask = np.where(n_array==1.0, 255, n_array)

# ------ Save result as GeoJSON file ------ #
# Export result
polygons = (
        {'properties': {'raster_val': v}, 'geometry': s}
        for i, (s, v) 
        in enumerate(
            shapes(mask.astype('uint8'), mask=None, transform=transform)))
geometry = list(polygons)

# Create new geodataframe
geom_dataframe  = gpd.GeoDataFrame.from_features(geometry)

# Set projection of dataframe
geom = geom_dataframe.set_crs(Image.crs)

# Remove no-data geometries
geom = geom[geom.raster_val != 0]

# Extract  boundaries
list_poly = []
for p in geom['geometry']:
  list_poly.append(Polygon(p.exterior))

smooth_poly = []
for i in range(len(list_poly)):
  poly_line = list_poly[i]
  outbuffer = poly_line.buffer(10, resolution=5, cap_style=1, join_style=1, mitre_limit=2, single_sided=True)
  inbuffer = outbuffer.buffer(-10.5, resolution=5, cap_style=1, join_style=1, mitre_limit=2, single_sided=True)
  simplified = inbuffer.simplify(1, preserve_topology=False) # False: Use Douglas-Peucker algorithm
  smooth_poly.append(simplified)

# Create new geodataframe for exterior boundaries
geo_shoreline = gpd.GeoDataFrame({'geometry':smooth_poly}, crs=Image.crs)
geo_shoreline['id'] = geo_shoreline.index

# Save to geojson file
outfp = 'output/shoreline/geojson/shoreline_'+date[0][:4]+'.json'
geo_shoreline.to_file(outfp, driver='GeoJSON')

# Create plot
fig, (axr, axg, axb) = plt.subplots(1,3, figsize=(20,7))
show(RGB.transpose(2, 0, 1), ax=axr, transform=transform, title='True color')
show(nir, ax=axg, cmap='gray', transform=transform, title='NIR channel')
show(mask, ax=axb, cmap='gray', transform=transform)
geo_shoreline.plot(ax=axb, facecolor='None', edgecolor='red', linewidth=1.5)
axb.set_title('Shoreline', fontweight='bold')
plt.tight_layout()
plt.savefig('output/shoreline/plot/plot_'+date[0][:4]+'.png', dpi=300)

#---------------------------------------------------------------------
if Image.read().any() == 0:
  print('Error: Shoreline cannot be extracted!!!')
else:
  print('Shoreline extraction is finished!')