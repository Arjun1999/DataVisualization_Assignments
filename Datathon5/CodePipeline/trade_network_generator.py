import os
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

df = pd.read_csv('Datathon4.csv')
X = df[['Year', 
        'Country', 
        'GDP per capita at current prices and PPPs, US$', 
        'External balance on goods and services, per cent of GDP']]

X['DevelopmentStatus'] = "Developed"
X.loc[(df['GDP per capita at current prices and PPPs, US$'] < 25000), 'DevelopmentStatus'] = 'Developing'
# print(X['DevelopmentStatus'])

#-----------------------Analyzing trade within European Union in 2014------------------
X2014 = X.query("Year == 2015")
X2014 = X2014.query(
    "Country == 'Austria' or Country == 'Belgium' or Country == 'Bulgaria' or Country == 'Croatia' or Country == 'Cyprus' or Country == 'Czechia' or Country == 'Denmark' or Country == 'Estonia' or Country == 'Finland' or Country == 'France' or Country == 'Germany' or Country == 'Greece' or Country == 'Hungary' or Country == 'Ireland' or Country == 'Italy' or Country == 'Latvia' or Country == 'Lithuania' or Country == 'Luxembourg' or Country == 'Malta' or Country == 'Netherlands' or Country == 'Poland' or Country == 'Portugal' or Country == 'Romania' or Country == 'Slovakia' or Country == 'Slovenia' or Country == 'Spain' or Country == 'Sweden'")

# print(X2014['Country'])

for col in X2014.columns.values:
    # print(col)
    if X2014[col].isnull().sum() == 0:
        continue
    else:
        guess_value = X2014[col].median()
    # for country in T['Country'].unique():
        X2014[col].loc[(X2014[col].isnull())] = guess_value


development_lst = list(X2014['DevelopmentStatus'][:])
countries_lst = list(X2014['Country'][:])
balance_lst = list(X2014['External balance on goods and services, per cent of GDP'][:])
gdp_lst = list(X2014['GDP per capita at current prices and PPPs, US$'][:])


gdp_country_tuple_lst = []

# output_file6 = open("nodes_provinces.txt", "w")  # For creating node list for Gephi
for i in range(len(countries_lst)):
    # str6 = str(provinces_lst[i]) + "\n"
    # output_file6.write(str6)
    balance_country_tuple = []
    balance_country_tuple.append(countries_lst[i])
    balance_country_tuple.append(gdp_lst[i])
    balance_country_tuple.append(balance_lst[i])
    balance_country_tuple.append(development_lst[i])
    gdp_country_tuple_lst.append(balance_country_tuple)

# print(gdp_country_tuple_lst)

developed_countries = []
developing_countries = []

developed_gdp = []
developing_gdp = []

for i in range(len(gdp_country_tuple_lst)):
    # print(gdp_country_tuple_lst[i])
    if(gdp_country_tuple_lst[i][3] == "Developed"):
        developed_countries.append(gdp_country_tuple_lst[i])
        developed_gdp.append(gdp_country_tuple_lst[i][1])
    else:
        developing_countries.append(gdp_country_tuple_lst[i])
        developing_gdp.append(gdp_country_tuple_lst[i][1])


print(len(developed_countries))
print(len(developing_countries))

developed_countries_selected_gdp = []
developing_countries_selected_gdp = []

sorted_development = sorted(developed_gdp)
sorted_developing = sorted(developing_gdp)

# print(sorted_developing)

developed_countries_selected_gdp.append(sorted_development[-3:])
developing_countries_selected_gdp.append(sorted_developing[:10])

# print(developing_countries_selected_gdp)
developed_countries_selected = []
developing_countries_selected = []

for i in range(len(gdp_country_tuple_lst)):
    for j in range(len(developed_countries_selected_gdp)):
        if(gdp_country_tuple_lst[i][1] in developed_countries_selected_gdp[j]):
            developed_countries_selected.append(gdp_country_tuple_lst[i])

    for j in range(len(developing_countries_selected_gdp)):
        if(gdp_country_tuple_lst[i][1] in developing_countries_selected_gdp[j]):
            developing_countries_selected.append(gdp_country_tuple_lst[i])

print(sorted(gdp_country_tuple_lst))
# print(developed_countries)

output_file1 = open("edges_economy.csv", "w")
output_file1.write("source,target,weight\n")

for developed_country in range(len(developed_countries_selected)):
    for developing_country in range(len(developing_countries_selected)):
            str1 = ""
            # print(developed_countries_selected[developed_country][0])
            str1 += developed_countries_selected[developed_country][0] + ","
            str1 += developing_countries_selected[developing_country][0] + ","
            
            balance_weight = int(((developed_countries_selected[developed_country][2]) + (developing_countries_selected[developing_country][2]))/2)

            str1 += str(balance_weight) + "\n"

            output_file1.write(str1)

