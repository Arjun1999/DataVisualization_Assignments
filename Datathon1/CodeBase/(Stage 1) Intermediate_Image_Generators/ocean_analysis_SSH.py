import os
import pandas as pd
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from scipy.sparse import *

data_source_dir = "/home/arjun/Desktop/Semester_7/DataVisualization/Datathon1/CD732-Datathon-1-20200828T160947Z-001/CD732-Datathon-1/SSHA/"
for filename in os.listdir(data_source_dir):
    if(filename[-4:] == ".txt"):
        # if(filename[4:15] not in completed_lst):
        filepath = data_source_dir + filename
        temp_file = open(filepath, 'r')
        Lines = temp_file.readlines()

        ssh_list = []
        lat_list = []
        lon_list = []
        count = 1
        for line in Lines:
            if(count >= 11):
                num_comma = 0
                lon_str = ""
                lat_str = ""
                ssh_str = ""
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

                    if(num_comma == 4):
                        if(line[i] != '\n'):
                            if(line[i+1] != '\n'):
                                ssh_str += line[i+1]

                if(float(ssh_str) != -1e+34):
                    lon_list.append(float(lon_str))
                    lat_list.append(float(lat_str))
                    ssh_list.append(float(ssh_str))
            
            count += 1

        # print("LONS :", lon_list)
        # print("LATS :", lat_list)
        # print("sshS :", ssh_list)
        latitude_indices_set = list(set(lat_list))
        latitude_indices_set.sort()

        longitude_indices_set = list(set(lon_list))
        longitude_indices_set.sort()

        tuple_list = []
        grid = []
        min_val = min(ssh_list)
        max_val = max(ssh_list)

        # print(min_val)
        # print(max_val)
        # break

        min_lon = min(longitude_indices_set)
        max_lon = max(longitude_indices_set)

        min_lat = min(latitude_indices_set)
        max_lat = max(latitude_indices_set)

        for i in range(len(ssh_list)):
            tuple_list.append((lon_list[i], lat_list[i], ssh_list[i]))

        for i in range(len(latitude_indices_set)):
            grid.append([])
            for j in range(len(longitude_indices_set)):
                grid[i].append(np.nan)

        for i in range(len(tuple_list)):
            lon = tuple_list[i][0]
            lat = tuple_list[i][1]
            ssh = tuple_list[i][2]

            lon_ind = longitude_indices_set.index(lon)
            lat_ind = latitude_indices_set.index(lat)

            grid[lat_ind][lon_ind] = ((2 * (ssh - min_val))/(max_val - min_val)) - 1
            # grid[lat_ind][lon_ind] = ssh

        grid = np.array(grid)
        # print(grid)
        fig = plt.figure(figsize=(12, 8))

        m = Basemap(width=12000000, height=9000000, projection='cyl',
                    resolution=None, lat_0=0, lon_0=74, llcrnrlon=min_lon, urcrnrlon=max_lon, llcrnrlat=min_lat, urcrnrlat=max_lat)

        m.drawparallels(np.arange(-90.0, 90.0, 10.0), labels=[1, 0, 0, 0])
        m.drawmeridians(np.arange(-180.0, 180.0, 10.0), labels=[0, 0, 0, 1])

        #.....The geographical location of Sumatra.....
        Lon_Sumatra = 101.3431
        Lat_Sumatra = -0.5897
        x_Sumatra, y_Sumatra = m(Lon_Sumatra, Lat_Sumatra)
        m.plot(x_Sumatra, y_Sumatra, 'ro', markersize=5)
        plt.text(x_Sumatra - 3, y_Sumatra - 2, 'Sumatra')

        LON, LAT = np.meshgrid(longitude_indices_set, latitude_indices_set)
        x, y = m(LON, LAT)

        levels = np.linspace(min_val, max_val, 11)
        cmap_custom = plt.get_cmap('coolwarm')
        m.contourf(LON, LAT, grid, cmap =cmap_custom)

        cbar = m.colorbar(location='right')
        cbar.set_label('Magnitude' +'\n'+'(No units)')

        plt.title('Sea Surface Height Anamoly on ' + filename[4:15])
        # print(filename[4:15])
        plt.savefig(filename[4:15]+'.jpg')
        plt.clf()
        # plt.show()
        # break
