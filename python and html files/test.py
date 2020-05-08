import geopy
import gmplot

import numpy as np

with open("example.txt") as f:
    lines = f.readlines()
    
part_list = []
for line in lines:
    part = line.split(",")
    part[0] = float(part[0])
    part[1] = float(part[1][1:])
    part[2] = float(part[2][0:-1])
    part[3] = float(part[3])
    
    part_list.append(part)
    
data = np.asarray(part_list)

data_size = data.shape[0]
gps_data = data[:,1:3]
time_data = data[:,0]
numBT_data = data[:,-1]

mean_lat = np.mean(gps_data[:,0])
mean_long = np.mean(gps_data[:,1])

### Plot the map Journey ######### 
gmap3 = gmplot.GoogleMapPlotter(mean_lat, 
                                mean_long, 15) 
  
# scatter method of map object  
# scatter points on the google map 
gmap3.scatter( gps_data[:,0], gps_data[:,1], '# FF0000', 
                              size = 10, marker = False ) 
  
# Plot method Draw a line in 
# between given coordinates 
gmap3.plot(gps_data[:,0], gps_data[:,1],  
           'cornflowerblue', edge_width = 2.5) 
  
gmap3.draw( "map_path.html" ) 

#############################################################
### Plot heat map of the hotspots (threshold here is 2) #####

latitude_list = []
longitude_list = [] 
threshold = 2

for i in range(data_size):
    if(numBT_data[i]>=threshold):
        latitude_list.append(gps_data[i,0])
        longitude_list.append(gps_data[i,1])
  
gmap4 = gmplot.GoogleMapPlotter(mean_lat, 
                                mean_long, 15) 
  
# heatmap plot heating Type 
# points on the Google map 
gmap4.heatmap( latitude_list, longitude_list ) 
  
gmap4.draw( "hotspot_heatmap.html" ) 

############################################################

### Clustering of data points ##############################
data_points = []
 
for i in range(data_size):
    if(numBT_data[i]>0):
        data_points.append([gps_data[i,0],gps_data[i,1]])
        
data_points = np.asarray(data_points)
np.savetxt("gps.csv",data_points,delimiter=",")

import pandas as pd
from sklearn.cluster import DBSCAN
         
coords = data_points

cluster_radius = 0.01 #10 meters radius in km

kms_per_radian = 6371.0088
epsilon = cluster_radius / kms_per_radian
db = DBSCAN(eps=epsilon, min_samples=1, algorithm='ball_tree', metric='haversine').fit(np.radians(coords))
cluster_labels = db.labels_
num_clusters = len(set(cluster_labels))
clusters = pd.Series([coords[cluster_labels == n] for n in range(num_clusters)])
print('Number of Computed clusters: {}'.format(num_clusters))

clustered_list = clusters.to_list()
cluster_mean_list = []

num_dataPoints = data_points.shape[0]
num_clusters = len(clustered_list)

factor = int(num_dataPoints/num_clusters)

for x in clustered_list: 
    if(len(x) > factor ) :
        cluster_mean_list.append(np.mean(x,axis =0))
        
import reverse_geocoder as rg 
import pprint 
  
def reverseGeocode(coordinates): 
    result = rg.search(coordinates) 
      
    # result is a list containing ordered dictionary. 
    pprint.pprint(result)  
 
print("Substantial Cluster Means are")
for means in cluster_mean_list:
    print(means[0],means[1])
    reverseGeocode((means[0],means[1]))
    
# reverseGeocode is an offline library and so I have used it here
    

