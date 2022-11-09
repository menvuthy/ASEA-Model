import ee
ee.Initialize()


####################### Shoreline Analysis Parameters #################

# 1. Area of interest
# Note: always change from null to None, and false to False
aoi =  ee.Geometry.Polygon(
        [[[73.32074081281853, 0.2660138015438818],
          [73.32074081281853, 0.24713123949023472],
          [73.35503017286491, 0.24713123949023472],
          [73.35503017286491, 0.2660138015438818]]], None, False);
          
# 2. Start date and end date
date = ['2010-01-01', '2020-12-31']     

# 3. Scheme bins for total shoreline change
bins_tsc = [-100, -50, -25, -10, 0, 10, 25, 50, 100]  

# 4. Scheme bins for shoreline change rate per year
bins_rpy = [-10, -7.5, -5, -2.5, 0, 2.5, 5, 7.5, 10]    
