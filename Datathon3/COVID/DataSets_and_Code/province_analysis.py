#################################################################################################################################
# Note : This code is the one that was heavily refernced for making the inferences.
# This was purely self thought and at least personally makes great intuitive sense for the problem statement being explored.
#################################################################################################################################


import os
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# 'ProvincedAnalysis.csv' was created from the covid_19_data.csv through another script.
# Note, this assignment uses the entire dataset that was given in this csv while making inferences.
    
df = pd.read_csv('ProvinceAnalysis.csv', sep = '\t', index_col = 'SNo')
provinces_lst = list(df['Province'][:])
countries_lst = list(df['Country'][:])
confirmed_lst = list(df['Confirmed'][:])
deaths_lst = list(df['Deaths'][:])
recovered_lst = list(df['Recovered'][:])

# print(provinces_lst)

# print(len(latitude_indices))
countries_set = list(set(countries_lst))
# print(countries_set)
# latitude_indices_set.sort()

province_country_tuple_lst = []

province_death_dict = {}
province_recovered_dict = {}
province_confirmed_dict = {}

# output_file6 = open("nodes_provinces.txt", "w")  # For creating node list for Gephi
for i in range(len(provinces_lst)):
    # str6 = str(provinces_lst[i]) + "\n"
    # output_file6.write(str6)
    province_country_tuple = []
    province_country_tuple.append(provinces_lst[i])
    province_country_tuple.append(countries_lst[i])
    province_country_tuple_lst.append(province_country_tuple)

    province_death_dict.update({provinces_lst[i]: deaths_lst[i]})
    province_recovered_dict.update({provinces_lst[i]: recovered_lst[i]})
    province_confirmed_dict.update({provinces_lst[i]: confirmed_lst[i]})

# print(province_country_tuple_lst)
# print(province_death_dict)

# output_file1 = open("edges_deaths.csv", "w")
# output_file2 = open("edges_confirmed.txt", "w")

output_file3 = open("edges_recovered.csv", "w") # An intermediate csv that mirrors the exact data values as in the csv

# for i in range(len(province_country_tuple_lst)):
#     # print(province_country_tuple_lst[i][0])
#     str1 = ""
#     province_str = province_country_tuple_lst[i][0]
#     country_str = province_country_tuple_lst[i][1]
#     str1 += country_str + "    "
#     str1 += province_str + "    "
#     # print(str1)

grouped_provinces = []
for x in range(len(countries_set)):
    country = countries_set[x]
    country_lst = []
    for i in range(len(province_country_tuple_lst)):
        # print("Set country : ", country)
        # print("Province country : ", province_country_tuple_lst[i][1])
        if(province_country_tuple_lst[i][1] == country):
            country_lst.append(province_country_tuple_lst[i][0])
    grouped_provinces.append(country_lst)
    # output_file.write(str1)

# print(grouped_provinces)

output_file3.write("source,target,weight\n")
for group in range(len(grouped_provinces)):
    for i in range(len(grouped_provinces[group])-1):
        for j in range(i+1, len(grouped_provinces[group])):
            str1 = ""
            str2 = ""
            str3 = ""
            province = grouped_provinces[group][i]
            str1 += province + ","
            str2 += province + ","
            str3 += province + ","

            str1 += grouped_provinces[group][j] + ","
            str2 += grouped_provinces[group][j] + ","
            str3 += grouped_provinces[group][j] + ","

            death_weight = int((province_death_dict.get(grouped_provinces[group][i]) + province_death_dict.get(grouped_provinces[group][j]))/2)
            recovered_weight = int((province_recovered_dict.get(grouped_provinces[group][i]) + province_recovered_dict.get(grouped_provinces[group][j]))/2)
            confirmed_weight = int((province_confirmed_dict.get(grouped_provinces[group][i]) + province_confirmed_dict.get(grouped_provinces[group][j]))/2)
            
            str1 += str(death_weight) + "\n"
            str2 += str(confirmed_weight) + "\n"
            str3 += str(recovered_weight) + "\n"

            # print(str1)
            # output_file1.write(str1) # For calculating weights of the Deaths network
            # output_file2.write(str2) # For calculating weights of the Confirmed network
            output_file3.write(str3)   # For calculating weights of the Recovered network

# df1 = pd.read_csv('edges_deaths.csv', sep = ',')
# source_lst = list(df1['source'][:])
# target_lst = list(df1['target'][:])
# weight_lst = list(df1['weight'][:])

df2 = pd.read_csv('edges_recovered.csv', sep=',')
source_lst = list(df2['source'][:])
target_lst = list(df2['target'][:])
weight_lst = list(df2['weight'][:])


tuple_list = []
for i in range(len(source_lst)):
    temp = []
    temp.append(source_lst[i])
    temp.append(target_lst[i])
    temp.append(weight_lst[i])

    tuple_list.append(temp)

# print(len(tuple_list))

weight_lst.sort()

##########################
# For Death Data
##########################
n = 15
output_file4 = open("Edges_Deaths.csv", "w")  # This is the actual csv that is used as the weighted edge list in Gephi
for i in range(len(tuple_list)):
    str1 = ""
    str1 += tuple_list[i][0] + ","
    str1 += tuple_list[i][1] + ","

    for k in range((n-1)):
        if(tuple_list[i][2] >= weight_lst[k*int(len(weight_lst)/n)] and tuple_list[i][2] < weight_lst[(k+1)*int(len(weight_lst)/n)]):
            # print("earlier : ", tuple_list[i][2])
            # print("modified : ", k+1)
            str1 += str(k+1) + "\n"
            output_file4.write(str1)
            # tuple_list[i][2] = k+1
    
    if(tuple_list[i][2] >= weight_lst[(n-1)*int(len(weight_lst)/n)]):
        # print("earlier : ", tuple_list[i][2])
        # print("modified : ", n)
        str1 += str(n) + "\n"
        output_file4.write(str1)
        # tuple_list[i][2] = 20


####################
# For Recovery Data
####################

# output_file5 = open("Edges_Recovered.csv", "w")
# for i in range(len(tuple_list)):
#     str1 = ""
#     str1 += tuple_list[i][0] + ","
#     str1 += tuple_list[i][1] + ","

    
#     if(tuple_list[i][2] >= 100 and tuple_list[i][2] < 500):
#         # print("earlier : ", tuple_list[i][2])
#         # print("modified : ", k+1)
#         str1 += str(1) + "\n"
#         output_file5.write(str1)
#         # tuple_list[i][2] = k+1

#     elif(tuple_list[i][2] >= 500 and tuple_list[i][2] < 1500):
#         # print("earlier : ", tuple_list[i][2])
#         # print("modified : ", n)
#         str1 += str(2) + "\n"
#         output_file5.write(str1)
#         # tuple_list[i][2] = 20

#     elif(tuple_list[i][2] >= 1500):
#         # print("earlier : ", tuple_list[i][2])
#         # print("modified : ", n)
#         str1 += str(3) + "\n"
#         output_file5.write(str1)
#         # tuple_list[i][2] = 20
#     else:
#         str1 += str(0) + "\n"
#         output_file5.write(str1)
