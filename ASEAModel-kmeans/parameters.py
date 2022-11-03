import ee
ee.Initialize()


####################### Shoreline Analysis Parameters #################

# 1. Area of interest
# Note: always change from null to None, and false to False
aoi =  ee.Geometry.Polygon(
        [[[73.4408700837089, 1.8290995750916517],
          [73.4408700837089, 1.8135291752263365],
          [73.46344355477824, 1.8135291752263365],
          [73.46344355477824, 1.8290995750916517]]], None, False);
          
# 2. Start date and end date
date = ['2015-01-01', '2020-12-31']     

# 3. Scheme bins for total shoreline change
bins_tsc = [-100, -50, -25, -10, 0, 10, 25, 50, 100]  

# 4. Scheme bins for shoreline change rate per year
bins_rpy = [-10, -7.5, -5, -2.5, 0, 2.5, 5, 7.5, 10]    
