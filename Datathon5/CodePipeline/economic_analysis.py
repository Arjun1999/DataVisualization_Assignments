import numpy as np 
import pandas as pd
import networkx as nx
from matplotlib import pyplot, patches
from sklearn.preprocessing import StandardScaler
import seaborn as sns
from matplotlib import pyplot as plt
import plotly.express as px
from plotly.offline import iplot
# from chart_studio.plotly import iplot


# ---------For GDP Analysis----------------
# Reading Dataset
df = pd.read_csv('Datathon4.csv')

# Selecting Columns
X = df[['Country', 'Year', 'Total population', 'Population aged 64+, male', 'Population aged 64+, female',
        'Life expectancy at age 65, women', 'Life expectancy at age 65, men', 'GDP per capita at current prices and PPPs, US$',
        'Life expectancy at birth, women', 'Life expectancy at birth, men', 'Total fertility rate', 'Mean age of women at birth of first child',
        'Total employment, growth rate', 'Unemployment rate', 'Economic acivity rate, women 15-64', 'Economic activity rate, men 15-64',
        'Persons killed in road accidents', 'Total length of motorways (km)', 'Total length of railway lines (km)']]

# "GDP per capita at current prices and PPPs, US$"

# ---------Initial Exploration-------------
# print(df.describe())

# Number of non-null values 
# print(df.count())

# Number of null values
# print(df.isnull().sum())
# df.describe(include='all')

#----------Missing Values Replacement with Medians-----------------
# Medians are selected by grouping values across different years for each country together
# print(X.groupby('Country')[['Total population', 'Population aged 64+, male', 'Population aged 64+, female',
#                             'Life expectancy at age 65, women', 'Life expectancy at age 65, men', 'GDP per capita at current prices and PPPs, US$']].median())

# print(X.isnull().sum())
# X.describe(include='all')

for col in X.columns.values:
    # print(col)
    if X[col].isnull().sum() == 0:
        continue
    else:
        guess_values = X.groupby('Country')[col].median()
    for country in X['Country'].unique():
        X[col].loc[(X[col].isnull())&(X['Country'] == country)] = guess_values[country]

# print(X.isnull().sum())
# X.describe(include='all')

# print(X)

#---------Correlation Heatplot-----------------------
plt.figure(figsize=(16,12))
sns.heatmap(data=X.iloc[:, 2:].corr(), annot=True, fmt='.2f', xticklabels=1, yticklabels=1, cmap='coolwarm')
# plt.show()

#----------Parallel Coordinates Plot ----------------
# parallel_viz = X
# PViz2014 = X.query('Year == 2014')
parallel_viz = X[['GDP per capita at current prices and PPPs, US$',
                 'Economic acivity rate, women 15-64',
                 'Economic activity rate, men 15-64',
                 'Unemployment rate',
                 'Total employment, growth rate',
                 'Life expectancy at birth, women',
                 'Life expectancy at birth, men']]

fig = px.parallel_coordinates(parallel_viz, 
                              color='GDP per capita at current prices and PPPs, US$', 
                              labels={"GDP per capita at current prices and PPPs, US$": "GDP based on PPP",
                              "Economic acivity rate, women 15-64": "EcoActWomen", 
                              "Economic acivity rate, men 15-64": "EcoActMen",
                              "Unemployment rate": "UnemploymentRate", 
                              "Total employment, growth rate": "TotalEmpGrowth",
                              "Life expectancy at birth, women": "LifeExpWomen",
                              "Life expectancy at birth, men": "LifeExpMen" },
                              )
# fig.show()


#----------------Scatter Plot Matrices--------------------------------------
scatter_viz = X[['GDP per capita at current prices and PPPs, US$',
                  'Economic acivity rate, women 15-64',
                  'Economic activity rate, men 15-64',
                  'Unemployment rate',
                  'Total employment, growth rate',
                  'Life expectancy at birth, women',
                  'Life expectancy at birth, men']]

scatter_viz['DevelopmentStatus'] = 'Developed'
scatter_viz.loc[(scatter_viz['GDP per capita at current prices and PPPs, US$'] < 25000), 'DevelopmentStatus'] = 'Developing'
# print(scatter_viz['DevelopmentStatus'])

# print(scatter_viz)

fig = px.scatter_matrix(scatter_viz,
                        dimensions=["GDP per capita at current prices and PPPs, US$",
                                    "Economic acivity rate, women 15-64",
                                    "Economic activity rate, men 15-64",
                                    "Unemployment rate",
                                    "Total employment, growth rate",
                                    "Life expectancy at birth, women",
                                    "Life expectancy at birth, men"],
                        color="DevelopmentStatus", 
                        symbol="DevelopmentStatus",
                        title="Scatter matrix of Data Set",
                        labels={"GDP per capita at current prices and PPPs, US$": "GDP based on PPP",
                                "Economic acivity rate, women 15-64": "EcoActWomen",
                                "Economic activity rate, men 15-64": "EcoActMen",
                                "Unemployment rate": "UnemploymentRate",
                                "Total employment, growth rate": "TotalEmpGrowth",
                                "Life expectancy at birth, women": "LifeExpWomen",
                                "Life expectancy at birth, men": "LifeExpMen"})
fig.update_traces(diagonal_visible=False)
# fig.show()

# print(X.isnull().sum())
# X.describe(include='all')


T = X.query("Country == 'Norway'")
# T = X.query("Year == 2015")

# print(T)
# print(T.isnull().sum())
# T.describe(include='all')

for col in T.columns.values:
    # print(col)
    if T[col].isnull().sum() == 0:
        
        continue
    else:
        guess_value = T[col].median()
    # for country in T['Country'].unique():
        T[col].loc[(T[col].isnull())] = guess_value

# print(T.isnull().sum())
# T.describe(include='all')
# print(T)

#-----------TreeMap (Year -> Country)---------------------
treemap_viz = X
treemap_viz["Years"] = "Years"
fig = px.treemap(treemap_viz,
                 path=['Years', 'Year', 'Country'], 
                 values = 'GDP per capita at current prices and PPPs, US$',
                 color = 'GDP per capita at current prices and PPPs, US$'
                )
# fig.show()


#-----------Sunburst (Country -> Year)----------------------


sb2011 = X.query('Year == 2011')
sb2012 = X.query('Year == 2012')
sb2013 = X.query('Year == 2013')
sb2014 = X.query('Year == 2014')
sb2015 = X.query('Year == 2015')

frames = [sb2011, sb2012, sb2013, sb2014, sb2015]
sbviz = pd.concat(frames)

fig = px.sunburst(sbviz, 
                  path=['Country', 'Year'],
                  values='GDP per capita at current prices and PPPs, US$',
                  color='GDP per capita at current prices and PPPs, US$'
                 )
# fig.show()

#----------------GDP Vs. Life Expectancy------------------- (Choose Year)/(Choose Country)
# 2015 was chosen for across-country analysis from the sunburst visualization as a majority of the countries performed well
# Norway was chosen for in-country analysis

import plotly.graph_objs as go
max_GDP = T['GDP per capita at current prices and PPPs, US$'].max()
T['GDP per capita at current prices and PPPs, US$'] = T['GDP per capita at current prices and PPPs, US$']/max_GDP
data1=go.Scatter(x=T['Year'],
                 y=T['GDP per capita at current prices and PPPs, US$'],
             name="GDP per capita at current prices and PPPs, US$", mode="lines+markers")

# T['Economic activity rate, men 15-64'] = T['Economic activity rate, men 15-64'] * T['Total population']
max_ecom = T['Economic acivity rate, women 15-64'].max()
T['Economic acivity rate, women 15-64'] = T['Economic acivity rate, women 15-64']/max_ecom
data2=go.Scatter(x=T['Year'],
             y=T['Economic acivity rate, women 15-64'],
                 name='Economic acivity rate, women 15-64', mode="lines+markers")


max_lifeexp65w = T['Life expectancy at age 65, women'].max()
T['Life expectancy at age 65, women'] = T['Life expectancy at age 65, women']/max_lifeexp65w
data3 = go.Scatter(x=T['Year'],
                   y=T['Life expectancy at age 65, women'],
                   name='Life expectancy at age 65, women', mode="lines+markers")

max_lifeexpw = T['Life expectancy at birth, women'].max()
T['Life expectancy at birth, women'] = T['Life expectancy at birth, women']/max_lifeexpw
data4 = go.Scatter(x=T['Year'],
                   y=T['Life expectancy at birth, women'],
                   name='Life expectancy at birth, women', mode="lines+markers")

max_unempl = T['Unemployment rate'].max()
T['Unemployment rate'] = T['Unemployment rate']/max_unempl
data5 = go.Scatter(x=T['Year'],
                   y=T['Unemployment rate'],
                   name='Unemployment rate', mode="lines+markers")

max_pplkilled = T['Persons killed in road accidents'].max()
T['Persons killed in road accidents'] = T['Persons killed in road accidents']/max_pplkilled
data6 = go.Scatter(x=T['Year'],
                   y=T['Persons killed in road accidents'],
                   name='Persons killed in road accidents', mode="lines+markers")

max_roadbuild = T['Total length of motorways (km)'].max()
T['Total length of motorways (km)'] = T['Total length of motorways (km)']/max_roadbuild
data7 = go.Scatter(x=T['Year'],
                   y=T['Total length of motorways (km)'],
                   name='Total length of motorways (km)', mode="lines+markers")

mydata = [data1, data2, data3, data4, data5, data6, data7]
mylayout = go.Layout(
    title="GDP per capita combined relations")
fig = go.Figure(data=mydata, layout=mylayout)
# iplot(fig)

#----------------Bubble Plots for best visualization-------------------------
from bubbly.bubbly import bubbleplot
figure = bubbleplot(dataset=X, 
                    x_column= 'GDP per capita at current prices and PPPs, US$',
                    y_column='Life expectancy at birth, women',
                    bubble_column='Country', 
                    time_column='Year', 
                    size_column='Total population',
                    color_column='Country', 
                    x_title='GDP per Capita', 
                    y_title='Life Expectancy', 
                    title='GDP per Capita vs Life Expectancy',
                    x_logscale=True, 
                    scale_bubble=3, 
                    height=650)
# iplot(figure, config={'scrollzoom': True})




