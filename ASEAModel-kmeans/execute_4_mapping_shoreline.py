import os
import glob
import natsort
import folium
import geopandas as gpd
import matplotlib.pyplot as plt
import mapclassify
import contextily as ctx
import warnings
warnings.filterwarnings("ignore")

# File and folder paths
file_path = "output/shoreline/geojson"

# Make a search criteria to select the ndvi files
q = os.path.join(file_path, "shoreline_*.json")

shoreline_fp = natsort.natsorted(glob.glob(q)) # sorted files by name

# Read shoreline data
shoreline_change = gpd.read_file('output/shoreline/shoreline-change/shoreline_change.json').to_crs(epsg=3857)
union_shoreline = gpd.read_file('output/shoreline/union-shoreline/union_shoreline.json').to_crs(epsg=3857)

# create a flat dictionary of the built-in providers:
providers = ctx.providers.flatten()


# ------------------------ Create Static Plot for Total Shoreline Changes ------------------#

# Create custom bins for schemes
bins = [-100, -50, -25, -10, 0, 10, 25, 50, 100]

########################## OpenStreetMap ###############################
# Create one subplot. Control figure size in here.
fig, ax = plt.subplots(figsize=(15,10))

shoreline_change.plot(ax=ax,
          column="total change_m",
          markersize=10,
          cmap='RdBu',
          scheme='UserDefined', 
          classification_kwds={'bins': bins},
          legend=True,
          legend_kwds={'loc': 'best'}
          )

# Add basemap
ctx.add_basemap(ax, source='https://a.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png')

plt.xlabel('Longitude', fontsize=15)
plt.ylabel('Latitude', fontsize=15)
plt.title('Total shoreline change from '+shoreline_fp[0][-9:-5]+' to '+shoreline_fp[-1][-9:-5]+' (meter)', fontsize=18)
plt.tight_layout()
plt.savefig('output/shoreline/map/static/total_shoreline_change_OSM.png', dpi=300)

########################## CartoDB.Positron ###############################
# Create one subplot. Control figure size in here.
fig, ax = plt.subplots(figsize=(15,10))

shoreline_change.plot(ax=ax,
          column="total change_m",
          markersize=10,
          cmap='RdBu',
          scheme='UserDefined', 
          classification_kwds={'bins': bins},
          legend=True,
          legend_kwds={'loc': 'best'}
          )

# Add basemap
ctx.add_basemap(ax, source=providers['CartoDB.Positron'])

plt.xlabel('Longitude', fontsize=15)
plt.ylabel('Latitude', fontsize=15)
plt.title('Total shoreline change from '+shoreline_fp[0][-9:-5]+' to '+shoreline_fp[-1][-9:-5]+' (meter)', fontsize=18)
plt.tight_layout()
plt.savefig('output/shoreline/map/static/total_shoreline_change_Positron.png', dpi=300)

########################## CartoDB.DarkMatter ###############################
# Create one subplot. Control figure size in here.
fig, ax = plt.subplots(figsize=(15,10))

shoreline_change.plot(ax=ax,
          column="total change_m",
          markersize=10,
          cmap='RdBu',
          scheme='UserDefined', 
          classification_kwds={'bins': bins},
          legend=True,
          legend_kwds={'loc': 'best'}
          )

# Add basemap
ctx.add_basemap(ax, source=providers['CartoDB.DarkMatter'])

plt.xlabel('Longitude', fontsize=15)
plt.ylabel('Latitude', fontsize=15)
plt.title('Total shoreline change from '+shoreline_fp[0][-9:-5]+' to '+shoreline_fp[-1][-9:-5]+' (meter)', fontsize=18)
plt.tight_layout()
plt.savefig('output/shoreline/map/static/total_shoreline_change_DarkMatter.png', dpi=300)

########################## Esri.WorldImagery ###############################
# Create one subplot. Control figure size in here.
fig, ax = plt.subplots(figsize=(15,10))

shoreline_change.plot(ax=ax,
          column="total change_m",
          markersize=10,
          cmap='RdBu',
          scheme='UserDefined', 
          classification_kwds={'bins': bins},
          legend=True,
          legend_kwds={'loc': 'best'}
          )

# Add basemap
ctx.add_basemap(ax, source=providers['Esri.WorldImagery'])

plt.xlabel('Longitude', fontsize=15)
plt.ylabel('Latitude', fontsize=15)
plt.title('Total shoreline change from '+shoreline_fp[0][-9:-5]+' to '+shoreline_fp[-1][-9:-5]+' (meter)', fontsize=18)
plt.tight_layout()
plt.savefig('output/shoreline/map/static/total_shoreline_change_Esri.png', dpi=300)

# ------------------------ Create Static Plot for Shoreline Changes Rate Per Year ------------------#

# Create custom bins for schemes
bins = [-50, -25, -10, -5, 0, 5, 10, 25, 50]

########################## OpenStreetMap ###############################
# Create one subplot. Control figure size in here.
fig, ax = plt.subplots(figsize=(15,10))

shoreline_change.plot(ax=ax,
          column="rate per year_m",
          markersize=10,
          cmap='RdBu',
          scheme='UserDefined', 
          classification_kwds={'bins': bins},
          legend=True,
          legend_kwds={'loc': 'best'}
          )

# Add basemap
ctx.add_basemap(ax, source='https://a.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png')

plt.xlabel('Longitude', fontsize=15)
plt.ylabel('Latitude', fontsize=15)
plt.title('Shoreline change rate per year from '+shoreline_fp[0][-9:-5]+' to '+shoreline_fp[-1][-9:-5]+' (meter)', fontsize=18)
plt.tight_layout()
plt.savefig('output/shoreline/map/static/shoreline_change_rate_OSM.png', dpi=300)

########################## CartoDB.Positron ###############################
# Create one subplot. Control figure size in here.
fig, ax = plt.subplots(figsize=(15,10))

shoreline_change.plot(ax=ax,
          column="rate per year_m",
          markersize=10,
          cmap='RdBu',
          scheme='UserDefined', 
          classification_kwds={'bins': bins},
          legend=True,
          legend_kwds={'loc': 'best'}
          )

# Add basemap
ctx.add_basemap(ax, source=providers['CartoDB.Positron'])

plt.xlabel('Longitude', fontsize=15)
plt.ylabel('Latitude', fontsize=15)
plt.title('Shoreline change rate per year from '+shoreline_fp[0][-9:-5]+' to '+shoreline_fp[-1][-9:-5]+' (meter)', fontsize=18)
plt.tight_layout()
plt.savefig('output/shoreline/map/static/shoreline_change_rate_Positron.png', dpi=300)

########################## CartoDB.DarkMatter ###############################
# Create one subplot. Control figure size in here.
fig, ax = plt.subplots(figsize=(15,10))

shoreline_change.plot(ax=ax,
          column="rate per year_m",
          markersize=10,
          cmap='RdBu',
          scheme='UserDefined', 
          classification_kwds={'bins': bins},
          legend=True,
          legend_kwds={'loc': 'best'}
          )

# Add basemap
ctx.add_basemap(ax, source=providers['CartoDB.DarkMatter'])

plt.xlabel('Longitude', fontsize=15)
plt.ylabel('Latitude', fontsize=15)
plt.title('Shoreline change rate per year from '+shoreline_fp[0][-9:-5]+' to '+shoreline_fp[-1][-9:-5]+' (meter)', fontsize=18)
plt.tight_layout()
plt.savefig('output/shoreline/map/static/shoreline_change_rate_DarkMatter.png', dpi=300)

########################## Esri.WorldImagery ###############################
# Create one subplot. Control figure size in here.
fig, ax = plt.subplots(figsize=(15,10))

shoreline_change.plot(ax=ax,
          column="rate per year_m",
          markersize=10,
          cmap='RdBu',
          scheme='UserDefined', 
          classification_kwds={'bins': bins},
          legend=True,
          legend_kwds={'loc': 'best'}
          )

# Add basemap
ctx.add_basemap(ax, source=providers['Esri.WorldImagery'])

plt.xlabel('Longitude', fontsize=15)
plt.ylabel('Latitude', fontsize=15)
plt.title('Shoreline change rate per year from '+shoreline_fp[0][-9:-5]+' to '+shoreline_fp[-1][-9:-5]+' (meter)', fontsize=18)
plt.tight_layout()
plt.savefig('output/shoreline/map/static/shoreline_change_rate_Esri.png', dpi=300)

# ------------------------ Create Static Plot for All Shorelines ------------------#
########################## OpenStreetMap ###############################
# Create one subplot. Control figure size in here.
fig, ax = plt.subplots(figsize=(15,10))

union_shoreline.plot(ax=ax,
          column="year",
          categorical=True,
          linewidth=2,
          markersize=8,
          cmap='magma_r',
          legend=True,
          legend_kwds={'loc': 'best'}
          )

# Add basemap
providers = ctx.providers.flatten()
ctx.add_basemap(ax, source='https://a.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png')

plt.xlabel('Longitude', fontsize=15)
plt.ylabel('Latitude', fontsize=15)
plt.title('Shorelines from '+shoreline_fp[0][-9:-5]+' to '+shoreline_fp[-1][-9:-5], fontsize=18)
plt.tight_layout()
plt.savefig('output/shoreline/map/static/shorelines_OSM.png', dpi=300)

########################## CartoDB.Positron ###############################
# Create one subplot. Control figure size in here.
fig, ax = plt.subplots(figsize=(15,10))

union_shoreline.plot(ax=ax,
          column="year",
          categorical=True,
          linewidth=2,
          markersize=8,
          cmap='magma_r',
          legend=True,
          legend_kwds={'loc': 'best'}
          )

# Add basemap
ctx.add_basemap(ax, source=providers['CartoDB.Positron'])

plt.xlabel('Longitude', fontsize=15)
plt.ylabel('Latitude', fontsize=15)
plt.title('Shorelines from '+shoreline_fp[0][-9:-5]+' to '+shoreline_fp[-1][-9:-5], fontsize=18)
plt.tight_layout()
plt.savefig('output/shoreline/map/static/shorelines_Positron.png', dpi=300)


########################## CartoDB.DarkMatter ###############################
# Create one subplot. Control figure size in here.
fig, ax = plt.subplots(figsize=(15,10))

union_shoreline.plot(ax=ax,
          column="year",
          categorical=True,
          linewidth=2,
          markersize=8,
          cmap='magma',
          legend=True,
          legend_kwds={'loc': 'best'}
          )

# Add basemap
ctx.add_basemap(ax, source=providers['CartoDB.DarkMatter'])

plt.xlabel('Longitude', fontsize=15)
plt.ylabel('Latitude', fontsize=15)
plt.title('Shorelines from '+shoreline_fp[0][-9:-5]+' to '+shoreline_fp[-1][-9:-5], fontsize=18)
plt.tight_layout()
plt.savefig('output/shoreline/map/static/shorelines_DarkMatter.png', dpi=300)

########################## Esri.WorldImagery ###############################
# Create one subplot. Control figure size in here.
fig, ax = plt.subplots(figsize=(15,10))

union_shoreline.plot(ax=ax,
          column="year",
          categorical=True,
          linewidth=2,
          markersize=8,
          cmap='magma',
          legend=True,
          legend_kwds={'loc': 'best'}
          )

# Add basemap
ctx.add_basemap(ax, source=providers['Esri.WorldImagery'])

plt.xlabel('Longitude', fontsize=15)
plt.ylabel('Latitude', fontsize=15)
plt.title('Shorelines from '+shoreline_fp[0][-9:-5]+' to '+shoreline_fp[-1][-9:-5], fontsize=18)
plt.tight_layout()
plt.savefig('output/shoreline/map/static/shorelines_Esri.png', dpi=300)


# ------------------------ Create Interactive Map for Shoreline Changes ------------------#

# ------------------------ Create Interactive Map for All Shorelines ------------------#
map1 = union_shoreline.explore(
    column="year",
    popup=True,
    tooltip=True,
    cmap="magma",
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
# Create custom bins for schemes
bins = [-100, -50, -25, -10, 0, 10, 25, 50, 100]
map2 = shoreline_change.explore(
          column="total change_m",
          name='Shoreline change',
          marker_type='circle',
          marker_kwds=dict(radius=2, fill=True),
          cmap='RdBu',
          scheme='UserDefined', 
          k=10,
          classification_kwds={'bins': bins},
          legend=True,
          legend_kwds={'colorbar':False},
          tiles='CartoDB dark_matter',
          highlight_kwds={'weight':15, 'color':'yellow', 'fillColor':'red'}
          )

folium.TileLayer('CartoDB positron', name = 'CartoDB positron', control=True).add_to(map2) 
folium.TileLayer('OpenStreetMap', name = 'Open Street Map', control=True).add_to(map2)
folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'Google Satellite Hybrid',
        control = True
    ).add_to(map2)
    
folium.LayerControl(collapsed=True).add_to(map2)  # use folium to add layer control
map2.save("output/shoreline/map/interactive/total_shoreline_change.html")

# ------------------------ Create Interactive Map for Shoreline Change Rate ------------------#
# Create custom bins for schemes
bins = [-50, -25, -10, -5, 0, 5, 10, 25, 50]
map3 = shoreline_change.explore(
          column="rate per year_m",
          name='Shoreline change',
          marker_type='circle',
          marker_kwds=dict(radius=2, fill=True),
          cmap='RdBu',
          scheme='UserDefined', 
          k=10,
          classification_kwds={'bins': bins},
          legend=True,
          legend_kwds={'colorbar':False},
          tiles='CartoDB dark_matter',
          highlight_kwds={'weight':15, 'color':'yellow', 'fillColor':'red'}
          )

folium.TileLayer('CartoDB positron', name = 'CartoDB positron', control=True).add_to(map3) 
folium.TileLayer('OpenStreetMap', name = 'Open Street Map', control=True).add_to(map3)
folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'Google Satellite Hybrid',
        control = True
    ).add_to(map3)
    
folium.LayerControl(collapsed=True).add_to(map3)  # use folium to add layer control
map3.save("output/shoreline/map/interactive/shoreline_change_rate.html")

#---------------------------------------------------------------------
if shoreline_fp == []:
  print('Error: There is no shoreline for creating map.')
else:
  print('Shoreline change map is created!')
