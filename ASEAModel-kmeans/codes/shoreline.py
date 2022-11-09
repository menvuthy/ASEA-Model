import math
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.enums import Resampling
from shapely.geometry import *
from shapely.affinity import rotate
from shapely.geometry import LineString, Point, MultiLineString
from shapely.ops import nearest_points, unary_union


# Function to normalize the grid values
def normalize(band):
  # We need to change that behaviour because we have a lot of 0 values in our data.
  np.seterr(divide='ignore', invalid='ignore')
  
  # Calculate min and max of band
  band_max, band_min = np.nanmax(band), np.nanmin(band)

  # Normalizes numpy arrays into scale 0.0 - 1.0
  normalized_band = ((band - band_min)/(band_max - band_min))
  
  return normalized_band

# Function to downscale or upscale image
def resampling(image, scale_factor):
  # Resample data to target shape
  rescaled_image = image.read(
    out_shape=(
          image.count,
          int(image.height * scale_factor),
          int(image.width * scale_factor)
    ),
    resampling=Resampling.bilinear
  )

  # scale image transform
  transform = image.transform * image.transform.scale(
          (image.width / rescaled_image.shape[-1]),
          (image.height / rescaled_image.shape[-2])
      )
  
  return rescaled_image, transform

# Function to create points along geometry at a specific distance
def Create_points(line_geo, distance):
    distances = np.arange(0, line_geo.length, distance)
    points = [line_geo.interpolate(dist) for dist in distances] + [line_geo.boundary]
    return points

# Function to extrapolate line forward
def ExtrapolateOut(p1,p2,distance):
    'Creates a line extrapoled in p1->p2 direction'
    EXTRAPOL_RATIO = distance
    a = p1
    b = (p1[0]+EXTRAPOL_RATIO*(p2[0]-p1[0]), p1[1]+EXTRAPOL_RATIO*(p2[1]-p1[1]) )
    return LineString([a,b])

# Function to extrapolate line backward
def ExtrapolateIn(p1,p2,distance):
    'Creates a line extrapoled in p1->p2 direction'
    EXTRAPOL_RATIO = -distance
    a = p1
    b = (p1[0]+EXTRAPOL_RATIO*(p2[0]-p1[0]), p1[1]+EXTRAPOL_RATIO*(p2[1]-p1[1]) )
    return LineString([a,b])

# Function to create union polygon from growth and retreat geometry
def create_union_polygon(geometry):
    polygons = []
    for i in range(len(geometry['geometry'])):

      if type(geometry['geometry'][i]) == Polygon:
        polygons.append(geometry['geometry'][i])

      if type(geometry['geometry'][i]) == MultiPolygon:
        for poly in geometry['geometry'][i].geoms:
          polygons.append(poly)

    geometry_poly = unary_union(polygons)
    return geometry_poly

# Function to create shoreline change in point distribution format
def create_shoreline_change_points(shoreline, change_polygon):
  '''
  This function is to calculate the shoreline growth or retreat distance from
  reference shoreline and convert the shoreline change from polygon to point distribution
  along the reference shoreline.

  Parameters:
  - shoreline : reference shoreline (usually use the most recent shoreline geometry)
  - change_polygon: shapely polygons of growth or retreat

  '''
  
  shoreline_change = []
  for k in range(len(shoreline['geometry'])):
    # Create points at every 10 m
    line = LineString(shoreline['geometry'][k].exterior.coords)
    points_line= Create_points(line, 10)

    # Create transect lines at every 10m point
    line_list, line_in, line_out = [], [], []
    for i in range(len(points_line)-2):
      LS = LineString([points_line[i].coords[0], points_line[i+1].coords[0]])
      rotate_line = rotate(LS, 90, origin=points_line[i].coords[0])
      Line_in = ExtrapolateIn(*rotate_line.coords, 50)
      Line_out = ExtrapolateOut(*rotate_line.coords, 50)
      Long_line = MultiLineString([Line_in, Line_out])
      line_list.append(Long_line)
      line_in.append(Line_in)
      line_out.append(Line_out)

    # Generate intersection points between transect line and growth polygon
    intersect = []
    for i in range(len(line_list)):
      cal_intersect = line_list[i].intersection(change_polygon.boundary)
      intersect.append(cal_intersect)

    # Calculate change distance 
    origin_list, destination_list = [], []
    for x in range(len(intersect)):
      if type(intersect[x]) == Point:
        origin_list.append([])
        destination_list.append([])

      if type(intersect[x]) == LineString:
        origin_list.append([])
        destination_list.append([])

      if type(intersect[x]) == MultiPoint:
        origin, destination = [], []
        for point in intersect[x].geoms:

          if points_line[x].buffer(0.00001).contains(point) == True:
            origin.append(point)

          if points_line[x].buffer(0.00001).contains(point) == False:
            destination.append(point)

        origin_list.append(origin)
        destination_list.append(destination)

    Length_list = []
    for i in range(len(origin_list)):
        
      if len(origin_list[i]) > 0 and len(destination_list[i]) > 0:
        Origin = origin_list[i][0]
        Destination = MultiPoint(destination_list[i])
        nearest_geoms = nearest_points(Origin, Destination)
        Length = LineString([nearest_geoms[0].coords[0], nearest_geoms[1].coords[0]]).length
        Length_list.append(Length)
      
      else:
        Length = 0
        Length_list.append(Length)

    points_along_geo = []
    for i in range(len(line_in)): 
      intersect_point = Point(line_in[i].coords[0])
      points_along_geo.append(intersect_point)

    # Save result to drive
    geo_shoreline = gpd.GeoDataFrame({'geometry':points_along_geo}, crs=shoreline.crs)
    geo_shoreline['id'] = geo_shoreline.index
    geo_shoreline['change_m'] = Length_list
    geo_shoreline['change_m'] = geo_shoreline['change_m'].round(2)

    shoreline_change.append(geo_shoreline)

  geo_dataframe = pd.concat(shoreline_change, ignore_index=True)
  geo_dataframe['id'] = geo_dataframe.index

  return geo_dataframe


# Function to merge shoreline growth and retreat
def merge_shoreline_change(growth_points, retreat_points):
  shoreline_change = []
  for i in range(len(growth_points)):

    if growth_points['change_m'][i] == 0.0:
      shoreline_change.append(-retreat_points['change_m'][i])

    else:
      shoreline_change.append(growth_points['change_m'][i])
  
  return shoreline_change