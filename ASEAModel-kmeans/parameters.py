import ee
ee.Initialize()


#------ Parameter Setting ------#
# 1. Area of interest - format created from Google Earth Engine
# Set area of interest via Google Earth Engine Code Editor:
# https://code.earthengine.google.com
# ***Note: always change from null to None, and false to False
aoi =  ee.Geometry.Polygon(
        [[[103.49855114029242, 10.61440439559403],
          [103.49855114029242, 10.599471949016321],
          [103.52430034683539, 10.599471949016321],
          [103.52430034683539, 10.61440439559403]]], None, False);

# 2. Start date and end date
date = ['2022-01-01', '2022-12-31']
