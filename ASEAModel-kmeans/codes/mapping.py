import ee
ee.Initialize()
import folium
from shapely.geometry import Polygon

# Add Layer to Folium map
def add_ee_layer(self, ee_image_object, vis_params, name):
    """Adds a method for displaying Earth Engine image tiles to folium map."""
    map_id_dict = ee.Image(ee_image_object).getMapId(vis_params)
    folium.raster_layers.TileLayer(
        tiles=map_id_dict['tile_fetcher'].url_format,
        attr='Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine</a>',
        name=name,
        overlay=True,
        control=True
    ).add_to(self)

# Add Earth Engine drawing method to folium.
folium.Map.add_ee_layer = add_ee_layer

# Calculate centroid for map zoom
def centroidObject(eeObject):
  # Retrieve the coordinate info
  center = eeObject.getInfo()
  # List of bounding box coordinate x, y
  geometry = []
  for i in center["coordinates"][0]:
    geometry.append(i)
  # Create polygon from bounding box x,y and calcualte the centroid x,y
  centroid = Polygon(geometry).centroid
  return centroid