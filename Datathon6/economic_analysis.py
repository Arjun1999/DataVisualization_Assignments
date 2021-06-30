import numpy as np
import pandas as pd
from matplotlib import pyplot, patches
from sklearn.preprocessing import StandardScaler
import seaborn as sns
from matplotlib import pyplot as plt
import plotly.express as px
from plotly.offline import iplot
import geopandas as gpd
from matplotlib.lines import Line2D
# from chart_studio.plotly import iplot


# ---------For GDP Analysis----------------
# Reading Dataset
df = pd.read_csv('Datathon4.csv')

# Selecting Columns
X = df[['Country', 'Year', 'Total population', 'Population aged 64+, male', 'Population aged 64+, female',
        'Life expectancy at age 65, women', 'Life expectancy at age 65, men', 'GDP per capita at current prices and PPPs, US$', 'Export of goods and services, per cent of GDP', 'Import of goods and services, per cent of GDP',
        'Life expectancy at birth, women', 'Life expectancy at birth, men', 'Total fertility rate', 'Mean age of women at birth of first child',
        'Total employment, growth rate', 'Unemployment rate', 'Economic acivity rate, women 15-64', 'Economic activity rate, men 15-64',
        'Persons killed in road accidents', 'Total length of motorways (km)', 'Total length of railway lines (km)']]


for col in X.columns.values:
    # print(col)
    if X[col].isnull().sum() == 0:
        continue
    else:
        guess_values = X.groupby('Country')[col].median()
    for country in X['Country'].unique():
        X[col].loc[(X[col].isnull())&(X['Country'] == country)] = guess_values[country]

shapefile = 'MapData/ne_110m_admin_0_countries.shp'#Read shapefile using Geopandas
gdf = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]#Rename columns.
gdf.columns = ['country', 'country_code', 'geometry']
# gdf.head()

# print(gdf[gdf['country'] == 'Antarctica'])#Drop row corresponding to 'Antarctica'
gdf = gdf.drop(gdf.index[159])
# df = X.query("Year==2014")

X['Country'] = X['Country'].replace(['United States','The former Yugoslav Republic of Macedonia','Russian Federation'],['United States of America','Macedonia', 'Russia'])

for i in range(2000, 2016):
    df_year = X[X['Year'] == i]#Perform left merge to preserve every row in gdf.
    merged = gdf.merge(df_year, left_on = 'country', right_on = 'Country', how = 'left')#Replace NaN values to string 'No data'.

    # max_GDP = merged['GDP per capita at current prices and PPPs, US$'].max()
    # merged['GDP per capita at current prices and PPPs, US$'] = merged['GDP per capita at current prices and PPPs, US$']/max_GDP

    # max_export = merged['Export of goods and services, per cent of GDP'].max()
    # merged['Export of goods and services, per cent of GDP'] = merged['Export of goods and services, per cent of GDP']/max_export

    max_import = merged['Import of goods and services, per cent of GDP'].max()
    merged['Import of goods and services, per cent of GDP'] = merged['Import of goods and services, per cent of GDP']/max_import

    # developed_point = 25000/max_GDP
    merged.fillna(np.nan, inplace = True)
    # merged

    title_name = "Import of goods percent of GDP of the countries in dataset for the year " + str(i)
    fig = px.choropleth(
        merged,
        locations="country_code",
        color="Import of goods and services, per cent of GDP",
        # range_color = [0, 50000],
        title=title_name,
        # color_continuous_midpoint=developed_point,
        hover_name="Country",  # column to add to hover information
        color_continuous_scale=px.colors.sequential.Plasma)
    # fig.show()
    # fig.write_image("choropleth_Import_" + str(i) + ".jpeg")



for i in range(2000, 2016):
    df_year = X[X['Year'] == i]#Perform left merge to preserve every row in gdf.
    merged = gdf.merge(df_year, left_on = 'country', right_on = 'Country', how = 'left')#Replace NaN values to string 'No data'.

    cat_dict = {
        0: {
            'color': 'black',
            'legend': r'$POP < \mu_{POP}, GDP < dev_{GDP}$'
        },
        1: {
            'color': 'green',
            'legend': r'$POP < \mu_{POP}, GDP \geq dev_{GDP}$'
        },
        2: {
            'color': 'red',
            'legend': r'$POP \geq \mu_{POP}, GDP < dev_{GDP}$'
        },
        3: {
            'color': 'blue',
            'legend': r'$POP \geq \mu_{POP}, GDP \geq dev_{GDP}$'
        }
    }

    merged['Color'] = 'grey'

    merged.loc[(merged['Total population'] < merged['Total population'].mean()) & (merged['GDP per capita at current prices and PPPs, US$'] < 25000), 'Color'] = cat_dict[0]['color']
    merged.loc[(merged['Total population'] < merged['Total population'].mean()) & (merged['GDP per capita at current prices and PPPs, US$'] >= 25000), 'Color'] = cat_dict[1]['color']
    merged.loc[(merged['Total population'] >= merged['Total population'].mean()) & (merged['GDP per capita at current prices and PPPs, US$'] < 25000), 'Color'] = cat_dict[2]['color']
    merged.loc[(merged['Total population'] >= merged['Total population'].mean()) & (merged['GDP per capita at current prices and PPPs, US$'] >= 25000), 'Color'] = cat_dict[3]['color']

    fig, ax = plt.subplots(dpi=350)
    title_str = "GDP per capita and population analysis for the year " + str(i)
    plt.title(title_str)
    # fig.show()
    # merged.plot(ax=ax, color=merged['Color'])
    
    # merged.plot()
    markers = []
    labels = []

    for cat in cat_dict.keys():
        markers.append(Line2D([0], [0], marker='o', color='w', markerfacecolor=cat_dict[cat]['color'], markersize=8))
        labels.append(cat_dict[cat]['legend'])

    ax.legend(markers, labels, fontsize=8, loc='upper right', bbox_to_anchor=(0.65, -0.2))

    savestr = "Combined_" + str(i) + ".jpeg"
    merged.plot(ax=ax, color = merged['Color']).get_figure().savefig(savestr)
