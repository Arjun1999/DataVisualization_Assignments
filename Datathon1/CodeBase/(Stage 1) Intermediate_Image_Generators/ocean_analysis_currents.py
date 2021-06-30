import os
import pandas as pd
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from scipy.sparse import *
import math
from osgeo import ogr


#.....These functios generate the radius of impact based on the Haversine Formula.....
def createCircleAroundWithRadius(lat, lon, radiusMiles):
 ring = ogr.Geometry(ogr.wkbLinearRing)
 latArray = []
 lonArray = []

 for brng in range(0, 360):
   lat2, lon2 = getLocation(lat, lon, brng, radiusMiles)
   latArray.append(lat2)
   lonArray.append(lon2)


 return lonArray, latArray


def getLocation(lat1, lon1, brng, distanceMiles):
    lat1 = lat1 * math.pi / 180.0
    lon1 = lon1 * math.pi / 180.0
    # Earth's Radius
    # R = 6378.1 Km
    # R = 3954 Miles

    distanceMiles = distanceMiles/3954

    brng = (brng / 90) * math.pi / 2

    lat2 = math.asin(math.sin(lat1) * math.cos(distanceMiles)
                    + math.cos(lat1) * math.sin(distanceMiles) * math.cos(brng))

    lon2 = lon1 + math.atan2(math.sin(brng)*math.sin(distanceMiles)
                            * math.cos(lat1), math.cos(distanceMiles)-math.sin(lat1)*math.sin(lat2))

    lon2 = 180.0 * lon2 / math.pi
    lat2 = 180.0 * lat2 / math.pi


    return lat2, lon2

#....Ignore this path, this was specifically for the study of Tsunami.....
# data_source_dir1 = "/home/arjun/Desktop/Semester_7/DataVisualization/Datathon1/CD732-Datathon-1-20200828T160947Z-001/CD732-Datathon-1/TsunamiStudy/meridional-current/"
# data_source_dir2 = "/home/arjun/Desktop/Semester_7/DataVisualization/Datathon1/CD732-Datathon-1-20200828T160947Z-001/CD732-Datathon-1/TsunamiStudy/zonal-current/"

data_source_dir1 = "/home/arjun/Desktop/Semester_7/DataVisualization/Datathon1/CD732-Datathon-1-20200828T160947Z-001/CD732-Datathon-1/meridional-current/"
data_source_dir2 = "/home/arjun/Desktop/Semester_7/DataVisualization/Datathon1/CD732-Datathon-1-20200828T160947Z-001/CD732-Datathon-1/zonal-current/"
for filename in os.listdir(data_source_dir1):
    if(filename[-4:] == ".txt"):
        # if(filename[4:15] not in completed_lst):
        filepath1 = data_source_dir1 + filename
        filepath2 = data_source_dir2 + filename
        
        temp_file1 = open(filepath1, 'r')
        temp_file2 = open(filepath2, 'r')
        
        Lines1 = temp_file1.readlines()
        Lines2 = temp_file2.readlines()

        meridional_list = []
        lat_list = []
        lon_list = []
        count = 1
        
        for line in Lines1:
            if(count >= 12):
                num_comma = 0
                lon_str = ""
                lat_str = ""
                meridional_str = ""
                i = 0
                for i in range(len(line)):

                    if(line[i] == ","):
                        num_comma += 1

                    if(num_comma == 2):
                        if(line[i+1] != ","):
                            lon_str += line[i+1]

                    if(num_comma == 3):
                        if(line[i+1] != ","):
                            lat_str += line[i+1]

                    if(num_comma == 5):
                        if(line[i] != '\n'):
                            if(line[i+1] != '\n'):
                                meridional_str += line[i+1]

                # print(lon_str)
                # print(lat_str)
                # print(meridional_str)
                if(float(meridional_str) != -1e+34):
                    lon_list.append(float(lon_str))
                    lat_list.append(float(lat_str))
                    if(float(meridional_str) > 1):
                        meridional_list.append(float(1))
                    elif(float(meridional_str) < -1):
                        meridional_list.append(float(-1))
                    else:
                        meridional_list.append(float(meridional_str))
              
            count += 1


        zonal_list = []
        lat_list = []
        lon_list = []
        
        count = 1

        for line in Lines2:
            if(count >= 12):
                num_comma = 0
                lon_str = ""
                lat_str = ""
                zonal_str = ""
                i = 0
                for i in range(len(line)):

                    if(line[i] == ","):
                        num_comma += 1

                    if(num_comma == 2):
                        if(line[i+1] != ","):
                            lon_str += line[i+1]

                    if(num_comma == 3):
                        if(line[i+1] != ","):
                            lat_str += line[i+1]

                    if(num_comma == 5):
                        if(line[i] != '\n'):
                            if(line[i+1] != '\n'):
                                zonal_str += line[i+1]

                # print(lon_str)
                # print(lat_str)
                # print(zonal_str)
                if(float(zonal_str) != -1e+34):
                    lon_list.append(float(lon_str))
                    lat_list.append(float(lat_str))
                    if(float(zonal_str) > 1):
                        zonal_list.append(float(1))
                    elif(float(zonal_str) < -1):
                        zonal_list.append(float(-1))
                    else:
                        zonal_list.append(float(zonal_str))
            count += 1

        # print("LONS :", lon_list)
        # print("LATS :", lat_list)
        # print("SSTS :", sst_list)
        
        # print(len(lon_list), len(lat_list), len(meridional_list), len(zonal_list))
        # break
        latitude_indices_set = list(set(lat_list))
        latitude_indices_set.sort()

        longitude_indices_set = list(set(lon_list))
        longitude_indices_set.sort()

        # print(len(latitude_indices_set), len(longitude_indices_set))
        # break
        tuple_list = []
        grid = []
        
        min_val_zonal = min(zonal_list)
        max_val_zonal = max(zonal_list)

        min_val_meridional = min(meridional_list)
        max_val_meridional = max(meridional_list)

        min_lon = min(longitude_indices_set)
        max_lon = max(longitude_indices_set)

        min_lat = min(latitude_indices_set)
        max_lat = max(latitude_indices_set)

        for i in range(len(meridional_list)):
            tuple_list.append((lon_list[i], lat_list[i], zonal_list[i], meridional_list[i]))

        magnitude_list = []
        for i in range(len(meridional_list)):
            magnitude_list.append(math.sqrt((zonal_list[i]*zonal_list[i]) + (meridional_list[i]*meridional_list[i])))
        
        min_mag = min(magnitude_list)
        max_mag = max(magnitude_list)

        new_magnitude_list = []
        for i in range(len(magnitude_list)):
            new_magnitude_list.append((magnitude_list[i] - min_mag) / (max_mag - min_mag))
        
        fig = plt.figure(figsize=(12, 8))

        m = Basemap(width=12000000, height=9000000, projection='cyl',
                    resolution=None, lat_0=0, lon_0=74, llcrnrlon=min_lon, urcrnrlon=max_lon, llcrnrlat=min_lat, urcrnrlat=max_lat)

        m.drawparallels(np.arange(-90.0, 90.0, 10.0), labels=[1, 0, 0, 0])
        m.drawmeridians(np.arange(-180.0, 180.0, 10.0), labels=[0, 0, 0, 1])

        LON, LAT = np.meshgrid(longitude_indices_set, latitude_indices_set)
        x, y = m(LON, LAT)

        cmap_custom = plt.get_cmap('coolwarm')
        m.quiver(lon_list, lat_list, meridional_list, zonal_list, new_magnitude_list, cmap=cmap_custom)

        # .....The location of Sumatra..... 
        # Lon_Sumatra = 101.3431
        # Lat_Sumatra = -0.5897

        # .....The location of the exact epicentre of the Tsunami..... 
        Lon_Sumatra = 95.51
        Lat_Sumatra = 3.25

        x_Sumatra, y_Sumatra = m(Lon_Sumatra, Lat_Sumatra)
        m.plot(x_Sumatra, y_Sumatra, 'ko', markersize=5)
        plt.text(x_Sumatra - 3, y_Sumatra - 2, 'Epicentre')

        # .....Outermost radius of impact.....
        distanceInMiles1 = 1860
        X, Y = createCircleAroundWithRadius(Lat_Sumatra, Lon_Sumatra, distanceInMiles1)

        X, Y = m(X, Y)
        m.plot(X, Y, marker=None, color='black', linewidth=2)

        # .....Middle radius of impact.....
        distanceInMiles2 = 930
        X2, Y2 = createCircleAroundWithRadius(Lat_Sumatra, Lon_Sumatra, distanceInMiles2)

        X2, Y2 = m(X2, Y2)
        m.plot(X2, Y2, marker=None, color='black', linewidth=1.5)

        # .....Innermost radius of impact.....
        distanceInMiles3 = 465
        X3, Y3 = createCircleAroundWithRadius(Lat_Sumatra, Lon_Sumatra, distanceInMiles3)

        X3, Y3 = m(X3, Y3)
        m.plot(X3, Y3, marker=None, color='black', linewidth=1)

        # .....Reading the shapefiles for each of the affected countries by the Tsunami.....
        m.readshapefile(
            '/home/arjun/Desktop/Semester_7/DataVisualization/Datathon1/MyAttempt/gadm36_IND_shp/gadm36_IND_0', 'India', color = 'orange')
        m.readshapefile(
            '/home/arjun/Desktop/Semester_7/DataVisualization/Datathon1/MyAttempt/gadm36_MDG_shp/gadm36_MDG_0', 'Madagascar', color = 'orange')
        m.readshapefile(
            '/home/arjun/Desktop/Semester_7/DataVisualization/Datathon1/MyAttempt/gadm36_BGD_shp/gadm36_BGD_0', 'Bangladesh', color = 'orange')
        m.readshapefile(
            '/home/arjun/Desktop/Semester_7/DataVisualization/Datathon1/MyAttempt/gadm36_IDN_shp/gadm36_IDN_1', 'Indonesia', color = 'orange')
        m.readshapefile(
            '/home/arjun/Desktop/Semester_7/DataVisualization/Datathon1/MyAttempt/gadm36_KEN_shp/gadm36_KEN_0', 'Kenya', color = 'orange')
        m.readshapefile(
            '/home/arjun/Desktop/Semester_7/DataVisualization/Datathon1/MyAttempt/gadm36_MMR_shp/gadm36_MMR_0', 'Myanmar', color = 'orange')
        m.readshapefile(
            '/home/arjun/Desktop/Semester_7/DataVisualization/Datathon1/MyAttempt/gadm36_MYS_shp/gadm36_MYS_0', 'Malaysia', color = 'orange')
        m.readshapefile(
            '/home/arjun/Desktop/Semester_7/DataVisualization/Datathon1/MyAttempt/gadm36_SOM_shp/gadm36_SOM_0', 'Somalia', color = 'orange')
        m.readshapefile(
            '/home/arjun/Desktop/Semester_7/DataVisualization/Datathon1/MyAttempt/gadm36_THA_shp/gadm36_THA_0', 'Thailand', color = 'orange')
        m.readshapefile(
            '/home/arjun/Desktop/Semester_7/DataVisualization/Datathon1/MyAttempt/gadm36_ZAF_shp/gadm36_ZAF_0', 'South Africa', color = 'orange')
        m.readshapefile(
            '/home/arjun/Desktop/Semester_7/DataVisualization/Datathon1/MyAttempt/gadm36_TZA_shp/gadm36_TZA_0', 'Tanzania', color = 'orange')
        
        # m.rotate_vector(lon_list, lat_list, meridional_list, zonal_list, returnxy = True)
        cbar = m.colorbar(location='right')
        cbar.set_label('Magnitude' + '\n'+'(m/sec)')

        plt.title('Ocean Currents on ' + filename[4:15])
        # print(filename[4:15])
        plt.savefig(filename[4:15]+'.jpg')
        # plt.savefig('TsunamiStudy'+filename[4:15]+'.jpg')
        plt.clf()
        # plt.show()
        # break
