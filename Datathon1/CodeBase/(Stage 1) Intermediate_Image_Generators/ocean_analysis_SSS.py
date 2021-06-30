import os
import pandas as pd
import numpy as np
import matplotlib
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib import ticker
from scipy.sparse import *

# .....Ignore this piece of code.....
# completed_lst = []
# data_source_dir_temp = "/home/arjun/Desktop/Semester_7/DataVisualization/Datathon1/"
# for filename in os.listdir(data_source_dir_temp):
#     if(filename[-4:] == ".jpg"):
#          completed_lst.append(filename[:-4])

data_source_dir = "/home/arjun/Desktop/Semester_7/DataVisualization/Datathon1/CD732-Datathon-1-20200828T160947Z-001/CD732-Datathon-1/SSS/"
for filename in os.listdir(data_source_dir):

    # .....This was the initial file reading methodology based on csv that was being tested.....
    if(filename[-4:] == ".csv"):
        # if(filename[4:15] not in completed_lst):
            filepath = data_source_dir + filename
            df = pd.read_csv(filepath, usecols = [2,3,4])
            latitude_indices = df['LAT'][:]
            # print(len(latitude_indices))
            latitude_indices_set = list(set(latitude_indices))
            latitude_indices_set.sort()
            # print("Set :", latitude_indices_set)
            # print(len(latitude_indices_set))
            longitude_indices = df['LON'][:]
            # print(len(longitude_indices))
            longitude_indices_set = list(set(longitude_indices))
            longitude_indices_set.sort()
            # print("Set :", longitude_indices_set)
            # print(len(longitude_indices_set))
            sss_indices = df['SSS'][:]

            tuple_list = []
            new_sss_lst = []
            for i in range(len(sss_indices)):
                if(sss_indices[i] != -1.0000000000000001e+34):
                    tuple_list.append((longitude_indices[i], latitude_indices[i], sss_indices[i]))
                    new_sss_lst.append(sss_indices[i])
                
            min_val = min(new_sss_lst)
            max_val = max(new_sss_lst)

            min_lon = min(longitude_indices_set)
            max_lon = max(longitude_indices_set)

            min_lat = min(latitude_indices_set)
            max_lat = max(latitude_indices_set)
            grid = []
            for i in range(len(latitude_indices_set)):
                grid.append([])
                for j in range(len(longitude_indices_set)):
                    grid[i].append(np.nan)

            print_min = 100
            for i in range(len(tuple_list)):
                lon = tuple_list[i][0]
                lat = tuple_list[i][1]
                sss = tuple_list[i][2]

                lon_ind = longitude_indices_set.index(lon)
                lat_ind = latitude_indices_set.index(lat)

                grid[lat_ind][lon_ind] = (sss - min_val)/(max_val - min_val)
            grid = np.array(grid)
            # print(grid.shape)

            # print("Long : ", longitude_indices)
            # print("Lat :", latitude_indices)
            # print("SSS : ", sss_indices)


            fig = plt.figure(figsize=(12, 8))

            m = Basemap(width=12000000,height=9000000,projection='cyl', 
                        resolution=None,lat_0=0,lon_0=74, llcrnrlon = min_lon, urcrnrlon = max_lon, llcrnrlat = min_lat, urcrnrlat = max_lat)

            m.drawparallels(np.arange(-90.0, 90.0, 10.0), labels = [1, 0, 0 , 0])
            m.drawmeridians(np.arange(-180.0, 180.0, 10.0), labels = [0, 0, 0 , 1])
            LON, LAT = np.meshgrid(longitude_indices_set, latitude_indices_set)
            x, y = m(LON, LAT)

            cmap_custom = plt.get_cmap('viridis')
            m.pcolormesh(longitude_indices_set, latitude_indices_set, grid, norm=matplotlib.colors.LogNorm(vmin = 0.1, vmax = 1), shading='flat', cmap=cmap_custom)
            cbar = m.colorbar(location='right')
            cbar.set_label('Magnitude' + '\n'+'(Practical Salinity Unit (psu) - g/kg)')

            plt.title('Sea Surface Salinity on ' + filename[4:15])
            plt.savefig(filename[4:15]+'.jpg')
            plt.clf()

            # plt.show()
            # break
