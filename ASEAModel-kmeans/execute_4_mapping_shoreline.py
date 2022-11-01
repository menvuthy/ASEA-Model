import os
import glob
import natsort
import folium
import geopandas as gpd
import matplotlib.pyplot as plt
import mapclassify
import rasterio
from rasterio.plot import show
import contextily as ctx
import warnings
warnings.filterwarnings("ignore")
from parameters import bins_tsc, bins_rpy


# File and folder paths
file_path = "output/shoreline/geojson"

# Make a search criteria to select the ndvi files
q = os.path.join(file_path, "shoreline_*.json")

shoreline_fp = natsort.natsorted(glob.glob(q)) # sorted files by name

# Read input image data
Image = rasterio.open('output/landsat-image/3m-images/image_snrgb_'+shoreline_fp[-1][-9:-5]+'.tif')
nir = Image.read(2)
transform = Image.transform

# Read shoreline data
Shoreline_change = gpd.read_file('output/shoreline/shoreline-change/shoreline_change.json')
shoreline_change = Shoreline_change.to_crs(epsg=3857)
Union_shoreline = gpd.read_file('output/shoreline/union-shoreline/union_shoreline.json')
union_shoreline = Union_shoreline.to_crs(epsg=3857)

# create a flat dictionary of the built-in providers:
providers = ctx.providers.flatten()


# ------------------------ Create Static Plot for Total Shoreline Changes ------------------#

########################## No Basemap ###############################
# Create one subplot. Control figure size in here.
fig, ax = plt.subplots(figsize=(15,10))

shoreline_change.plot(ax=ax,
          column="total change_m",
          markersize=10,
          cmap='RdBu',
          scheme='UserDefined', 
          classification_kwds={'bins': bins_tsc},
          legend=True,
          legend_kwds={'loc': 'best'}
          )

plt.xlabel('Longitude', fontsize=12)
plt.ylabel('Latitude', fontsize=12)
plt.title('Total shoreline change from '+shoreline_fp[0][-9:-5]+' to '+shoreline_fp[-1][-9:-5]+' (meter)', fontsize=12)
plt.tight_layout()
plt.savefig('output/shoreline/map/static/total_change/total_shoreline_change.png', dpi=300)

########################## NIR Basemap ###############################
# Create one subplot. Control figure size in here.
fig, ax = plt.subplots(figsize=(15,10))
show(nir, ax=ax, cmap='gray', transform=transform)
Shoreline_change.plot(ax=ax,
          column="total change_m",
          markersize=10,
          cmap='RdBu',
          scheme='UserDefined', 
          classification_kwds={'bins': bins_tsc},
          legend=True,
          legend_kwds={'loc': 'best'}
          )

plt.xlabel('Longitude', fontsize=12)
plt.ylabel('Latitude', fontsize=12)
plt.title('Total shoreline change from '+shoreline_fp[0][-9:-5]+' to '+shoreline_fp[-1][-9:-5]+' (meter)', fontsize=12)
plt.tight_layout()
plt.savefig('output/shoreline/map/static/total_change/total_shoreline_change_NIR.png', dpi=300)

########################## OpenStreetMap ###############################
# Create one subplot. Control figure size in here.
fig, ax = plt.subplots(figsize=(15,10))

shoreline_change.plot(ax=ax,
          column="total change_m",
          markersize=10,
          cmap='RdBu',
          scheme='UserDefined', 
          classification_kwds={'bins': bins_tsc},
          legend=True,
          legend_kwds={'loc': 'best'}
          )

# Add basemap
ctx.add_basemap(ax, source='https://a.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png')

plt.xlabel('Longitude', fontsize=12)
plt.ylabel('Latitude', fontsize=12)
plt.title('Total shoreline change from '+shoreline_fp[0][-9:-5]+' to '+shoreline_fp[-1][-9:-5]+' (meter)', fontsize=12)
plt.tight_layout()
plt.savefig('output/shoreline/map/static/total_change/total_shoreline_change_OSM.png', dpi=300)

########################## CartoDB.Positron ###############################
# Create one subplot. Control figure size in here.
fig, ax = plt.subplots(figsize=(15,10))

shoreline_change.plot(ax=ax,
          column="total change_m",
          markersize=10,
          cmap='RdBu',
          scheme='UserDefined', 
          classification_kwds={'bins': bins_tsc},
          legend=True,
          legend_kwds={'loc': 'best'}
          )

# Add basemap
ctx.add_basemap(ax, source=providers['CartoDB.Positron'])

plt.xlabel('Longitude', fontsize=12)
plt.ylabel('Latitude', fontsize=12)
plt.title('Total shoreline change from '+shoreline_fp[0][-9:-5]+' to '+shoreline_fp[-1][-9:-5]+' (meter)', fontsize=12)
plt.tight_layout()
plt.savefig('output/shoreline/map/static/total_change/total_shoreline_change_Positron.png', dpi=300)

########################## CartoDB.DarkMatter ###############################
# Create one subplot. Control figure size in here.
fig, ax = plt.subplots(figsize=(15,10))

shoreline_change.plot(ax=ax,
          column="total change_m",
          markersize=10,
          cmap='RdBu',
          scheme='UserDefined', 
          classification_kwds={'bins': bins_tsc},
          legend=True,
          legend_kwds={'loc': 'best'}
          )

# Add basemap
ctx.add_basemap(ax, source=providers['CartoDB.DarkMatter'])

plt.xlabel('Longitude', fontsize=12)
plt.ylabel('Latitude', fontsize=12)
plt.title('Total shoreline change from '+shoreline_fp[0][-9:-5]+' to '+shoreline_fp[-1][-9:-5]+' (meter)', fontsize=12)
plt.tight_layout()
plt.savefig('output/shoreline/map/static/total_change/total_shoreline_change_DarkMatter.png', dpi=300)

########################## Esri.WorldImagery ###############################
# Create one subplot. Control figure size in here.
fig, ax = plt.subplots(figsize=(15,10))

shoreline_change.plot(ax=ax,
          column="total change_m",
          markersize=10,
          cmap='RdBu',
          scheme='UserDefined', 
          classification_kwds={'bins': bins_tsc},
          legend=True,
          legend_kwds={'loc': 'best'}
          )

# Add basemap
ctx.add_basemap(ax, source=providers['Esri.WorldImagery'])

plt.xlabel('Longitude', fontsize=12)
plt.ylabel('Latitude', fontsize=12)
plt.title('Total shoreline change from '+shoreline_fp[0][-9:-5]+' to '+shoreline_fp[-1][-9:-5]+' (meter)', fontsize=12)
plt.tight_layout()
plt.savefig('output/shoreline/map/static/total_change/total_shoreline_change_Esri.png', dpi=300)

# ------------------------ Create Static Plot for Shoreline Changes Rate Per Year ------------------#

########################## No Basemap ###############################
# Create one subplot. Control figure size in here.
fig, ax = plt.subplots(figsize=(15,10))

shoreline_change.plot(ax=ax,
          column="rate per year_m",
          markersize=10,
          cmap='RdBu',
          scheme='UserDefined', 
          classification_kwds={'bins': bins_rpy},
          legend=True,
          legend_kwds={'loc': 'best'}
          )

plt.xlabel('Longitude', fontsize=12)
plt.ylabel('Latitude', fontsize=12)
plt.title('Shoreline change rate per year from '+shoreline_fp[0][-9:-5]+' to '+shoreline_fp[-1][-9:-5]+' (meter)', fontsize=12)
plt.tight_layout()
plt.savefig('output/shoreline/map/static/rate_per_year/shoreline_change_rate.png', dpi=300)

########################## NIR Basemap ###############################
# Create one subplot. Control figure size in here.
fig, ax = plt.subplots(figsize=(15,10))
show(nir, ax=ax, cmap='gray', transform=transform)
Shoreline_change.plot(ax=ax,
          column="rate per year_m",
          markersize=10,
          cmap='RdBu',
          scheme='UserDefined', 
          classification_kwds={'bins': bins_rpy},
          legend=True,
          legend_kwds={'loc': 'best'}
          )

plt.xlabel('Longitude', fontsize=12)
plt.ylabel('Latitude', fontsize=12)
plt.title('Shoreline change rate per year from '+shoreline_fp[0][-9:-5]+' to '+shoreline_fp[-1][-9:-5]+' (meter)', fontsize=12)
plt.tight_layout()
plt.savefig('output/shoreline/map/static/rate_per_year/shoreline_change_rate_NIR.png', dpi=300)

########################## OpenStreetMap ###############################
# Create one subplot. Control figure size in here.
fig, ax = plt.subplots(figsize=(15,10))

shoreline_change.plot(ax=ax,
          column="rate per year_m",
          markersize=10,
          cmap='RdBu',
          scheme='UserDefined', 
          classification_kwds={'bins': bins_rpy},
          legend=True,
          legend_kwds={'loc': 'best'}
          )

# Add basemap
ctx.add_basemap(ax, source='https://a.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png')

plt.xlabel('Longitude', fontsize=12)
plt.ylabel('Latitude', fontsize=12)
plt.title('Shoreline change rate per year from '+shoreline_fp[0][-9:-5]+' to '+shoreline_fp[-1][-9:-5]+' (meter)', fontsize=12)
plt.tight_layout()
plt.savefig('output/shoreline/map/static/rate_per_year/shoreline_change_rate_OSM.png', dpi=300)

########################## CartoDB.Positron ###############################
# Create one subplot. Control figure size in here.
fig, ax = plt.subplots(figsize=(15,10))

shoreline_change.plot(ax=ax,
          column="rate per year_m",
          markersize=10,
          cmap='RdBu',
          scheme='UserDefined', 
          classification_kwds={'bins': bins_rpy},
          legend=True,
          legend_kwds={'loc': 'best'}
          )

# Add basemap
ctx.add_basemap(ax, source=providers['CartoDB.Positron'])

plt.xlabel('Longitude', fontsize=12)
plt.ylabel('Latitude', fontsize=12)
plt.title('Shoreline change rate per year from '+shoreline_fp[0][-9:-5]+' to '+shoreline_fp[-1][-9:-5]+' (meter)', fontsize=12)
plt.tight_layout()
plt.savefig('output/shoreline/map/static/rate_per_year/shoreline_change_rate_Positron.png', dpi=300)

########################## CartoDB.DarkMatter ###############################
# Create one subplot. Control figure size in here.
fig, ax = plt.subplots(figsize=(15,10))

shoreline_change.plot(ax=ax,
          column="rate per year_m",
          markersize=10,
          cmap='RdBu',
          scheme='UserDefined', 
          classification_kwds={'bins': bins_rpy},
          legend=True,
          legend_kwds={'loc': 'best'}
          )

# Add basemap
ctx.add_basemap(ax, source=providers['CartoDB.DarkMatter'])

plt.xlabel('Longitude', fontsize=12)
plt.ylabel('Latitude', fontsize=12)
plt.title('Shoreline change rate per year from '+shoreline_fp[0][-9:-5]+' to '+shoreline_fp[-1][-9:-5]+' (meter)', fontsize=12)
plt.tight_layout()
plt.savefig('output/shoreline/map/static/rate_per_year/shoreline_change_rate_DarkMatter.png', dpi=300)

########################## Esri.WorldImagery ###############################
# Create one subplot. Control figure size in here.
fig, ax = plt.subplots(figsize=(15,10))

shoreline_change.plot(ax=ax,
          column="rate per year_m",
          markersize=10,
          cmap='RdBu',
          scheme='UserDefined', 
          classification_kwds={'bins': bins_rpy},
          legend=True,
          legend_kwds={'loc': 'best'}
          )

# Add basemap
ctx.add_basemap(ax, source=providers['Esri.WorldImagery'])

plt.xlabel('Longitude', fontsize=12)
plt.ylabel('Latitude', fontsize=12)
plt.title('Shoreline change rate per year from '+shoreline_fp[0][-9:-5]+' to '+shoreline_fp[-1][-9:-5]+' (meter)', fontsize=12)
plt.tight_layout()
plt.savefig('output/shoreline/map/static/rate_per_year/shoreline_change_rate_Esri.png', dpi=300)

# ------------------------ Create Static Plot for All Shorelines ------------------#

########################## No Basemap ###############################
# Create one subplot. Control figure size in here.
fig, ax = plt.subplots(figsize=(15,10))

union_shoreline.plot(ax=ax,
          column="year",
          categorical=True,
          linewidth=2,
          markersize=8,
          cmap='coolwarm',
          legend=True,
          legend_kwds={'loc': 'best'}
          )

plt.xlabel('Longitude', fontsize=12)
plt.ylabel('Latitude', fontsize=12)
plt.title('Shorelines from '+shoreline_fp[0][-9:-5]+' to '+shoreline_fp[-1][-9:-5], fontsize=12)
plt.tight_layout()
plt.savefig('output/shoreline/map/static/yearly_shoreline/shorelines.png', dpi=300)

########################## NIR Basemap ###############################
# Create one subplot. Control figure size in here.
fig, ax = plt.subplots(figsize=(15,10))
show(nir, ax=ax, cmap='gray', transform=Image.transform)
Union_shoreline.plot(ax=ax,
          column="year",
          categorical=True,
          linewidth=2,
          markersize=8,
          cmap='coolwarm',
          legend=True,
          legend_kwds={'loc': 'best'}
          )

plt.xlabel('Longitude', fontsize=12)
plt.ylabel('Latitude', fontsize=12)
plt.title('Shorelines from '+shoreline_fp[0][-9:-5]+' to '+shoreline_fp[-1][-9:-5], fontsize=12)
plt.tight_layout()
plt.savefig('output/shoreline/map/static/yearly_shoreline/shorelines_NIR.png', dpi=300)

########################## OpenStreetMap ###############################
# Create one subplot. Control figure size in here.
fig, ax = plt.subplots(figsize=(15,10))

union_shoreline.plot(ax=ax,
          column="year",
          categorical=True,
          linewidth=2,
          markersize=8,
          cmap='coolwarm',
          legend=True,
          legend_kwds={'loc': 'best'}
          )

# Add basemap
providers = ctx.providers.flatten()
ctx.add_basemap(ax, source='https://a.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png')

plt.xlabel('Longitude', fontsize=12)
plt.ylabel('Latitude', fontsize=12)
plt.title('Shorelines from '+shoreline_fp[0][-9:-5]+' to '+shoreline_fp[-1][-9:-5], fontsize=12)
plt.tight_layout()
plt.savefig('output/shoreline/map/static/yearly_shoreline/shorelines_OSM.png', dpi=300)

########################## CartoDB.Positron ###############################
# Create one subplot. Control figure size in here.
fig, ax = plt.subplots(figsize=(15,10))

union_shoreline.plot(ax=ax,
          column="year",
          categorical=True,
          linewidth=2,
          markersize=8,
          cmap='coolwarm',
          legend=True,
          legend_kwds={'loc': 'best'}
          )

# Add basemap
ctx.add_basemap(ax, source=providers['CartoDB.Positron'])

plt.xlabel('Longitude', fontsize=12)
plt.ylabel('Latitude', fontsize=12)
plt.title('Shorelines from '+shoreline_fp[0][-9:-5]+' to '+shoreline_fp[-1][-9:-5], fontsize=12)
plt.tight_layout()
plt.savefig('output/shoreline/map/static/yearly_shoreline/shorelines_Positron.png', dpi=300)


########################## CartoDB.DarkMatter ###############################
# Create one subplot. Control figure size in here.
fig, ax = plt.subplots(figsize=(15,10))

Union_shoreline.plot(ax=ax,
          column="year",
          categorical=True,
          linewidth=2,
          markersize=8,
          cmap='coolwarm',
          legend=True,
          legend_kwds={'loc': 'best'}
          )

# Add basemap
ctx.add_basemap(ax, source=providers['CartoDB.DarkMatter'])

plt.xlabel('Longitude', fontsize=12)
plt.ylabel('Latitude', fontsize=12)
plt.title('Shorelines from '+shoreline_fp[0][-9:-5]+' to '+shoreline_fp[-1][-9:-5], fontsize=12)
plt.tight_layout()
plt.savefig('output/shoreline/map/static/yearly_shoreline/shorelines_DarkMatter.png', dpi=300)

########################## Esri.WorldImagery ###############################
# Create one subplot. Control figure size in here.
fig, ax = plt.subplots(figsize=(15,10))

union_shoreline.plot(ax=ax,
          column="year",
          categorical=True,
          linewidth=2,
          markersize=8,
          cmap='coolwarm',
          legend=True,
          legend_kwds={'loc': 'best'}
          )

# Add basemap
ctx.add_basemap(ax, source=providers['Esri.WorldImagery'])

plt.xlabel('Longitude', fontsize=12)
plt.ylabel('Latitude', fontsize=12)
plt.title('Shorelines from '+shoreline_fp[0][-9:-5]+' to '+shoreline_fp[-1][-9:-5], fontsize=12)
plt.tight_layout()
plt.savefig('output/shoreline/map/static/yearly_shoreline/shorelines_Esri.png', dpi=300)

# ------------------------ Create Interactive Map for All Shorelines ------------------#
map1 = union_shoreline.explore(
    column="year",
    popup=True,
    tooltip=True,
    cmap="coolwarm",
    categorical=True,
    name="Shoreline",
    tiles='CartoDB dark_matter',
    legend=True,
    highlight_kwds={'weight':5, 'color':'yellow'}
)

folium.TileLayer('CartoDB positron', name = 'CartoDB positron', control=True).add_to(map1) 
folium.TileLayer('OpenStreetMap', name = 'OpenStreetMap', control=True).add_to(map1)
folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'Google Satellite Hybrid',
        control = True
    ).add_to(map1)
    
folium.LayerControl(collapsed=True).add_to(map1)  # use folium to add layer control
map1.save("output/shoreline/map/interactive/shorelines.html")

# ------------------------ Create Interactive Map for Total Shoreline Change ------------------#

map2 = shoreline_change.explore(
          column="total change_m",
          name='Shoreline change',
          marker_type='circle',
          marker_kwds=dict(radius=2, fill=True),
          cmap='RdBu',
          scheme='UserDefined', 
          k=10,
          classification_kwds={'bins': bins_tsc},
          legend=True,
          legend_kwds={'colorbar':False},
          highlight_kwds={'weight':15, 'color':'yellow', 'fillColor':'red'}
          )

folium.TileLayer('CartoDB positron', name = 'cartoDB positron', control=True).add_to(map2) 
folium.TileLayer('CartoDB dark_matter', name = 'cartoDB dark_matter', control=True).add_to(map2) 
folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'google satellite hybrid',
        control = True
    ).add_to(map2)
    
folium.LayerControl(collapsed=True).add_to(map2)  # use folium to add layer control
map2.save("output/shoreline/map/interactive/total_shoreline_change.html")

# ------------------------ Create Interactive Map for Shoreline Change Rate ------------------#

map3 = shoreline_change.explore(
          column="rate per year_m",
          name='Shoreline change',
          marker_type='circle',
          marker_kwds=dict(radius=2, fill=True),
          cmap='RdBu',
          scheme='UserDefined', 
          k=10,
          classification_kwds={'bins': bins_rpy},
          legend=True,
          legend_kwds={'colorbar':False},
          highlight_kwds={'weight':15, 'color':'yellow', 'fillColor':'red'}
          )
folium.TileLayer('CartoDB positron', name = 'cartoDB positron', control=True).add_to(map3) 
folium.TileLayer('CartoDB dark_matter', name = 'cartoDB dark_matter', control=True).add_to(map3) 
folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'google satellite hybrid',
        control = True
    ).add_to(map3)
    
folium.LayerControl(collapsed=True).add_to(map3)  # use folium to add layer control
map3.save("output/shoreline/map/interactive/shoreline_change_rate.html")

#---------------------------------------------------------------------
if shoreline_fp == []:
  print('Error: There is no shoreline for creating map.')
else:
  print('Shoreline change map is created!')
