# Steel projections

# Set working directory to be the project folder
import os
import re

wanted_wd = 'industry_model_9th_edition'
os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

# execute config file
config_file = './config/config_apr2023.py'
with open(config_file) as infile:
    exec(infile.read())

# Import historical steel data and gdp

steel_df = pd.read_csv('./data/production_and_trade/production_steel/steel_wsa_cleaned.csv') 
steel_ex = pd.read_csv('./data/production_and_trade/wsa_steelexport.csv', index_col = 'year')

for i in range(2022, 2101):
    steel_ex.loc[i, 'export_share'] = steel_ex.loc[i - 1, 'export_share']

steel_ex = steel_ex.copy().reset_index(drop = False)[['year', 'export_share']]

pop_gdp_df = pd.read_csv('./data/macro/APEC_GDP_population.csv')

from sklearn.linear_model import LinearRegression

for economy in list(steel_df['economy_code'].unique())[0:1]:
    hist_df = steel_df[steel_df['economy_code'] == economy].copy().dropna().reset_index(drop = True)
    gdp_pc = pop_gdp_df[(pop_gdp_df['economy_code'] == economy) &
                        (pop_gdp_df['variable'] == 'GDP_per_capita')].copy().reset_index(drop = True)
    
    gdp = pop_gdp_df[(pop_gdp_df['economy_code'] == economy) &
                        (pop_gdp_df['variable'] == 'real_GDP')].copy().reset_index(drop = True)
    
    pop = pop_gdp_df[(pop_gdp_df['economy_code'] == economy) &
                        (pop_gdp_df['variable'] == 'population')].copy().reset_index(drop = True)
    
    new_df = pd.merge(left = hist_df, right = gdp, left_on = 'year', right_on = 'year').copy().dropna()

    new_df = new_df[['year', 'value_x', 'value_y']].rename(columns = {'value_x': 'steel',
                                                                      'value_y': 'real_GDP'}).copy()
    
    new_df = pd.merge(left = new_df, right = pop, left_on = 'year', right_on = 'year')\
        .copy().dropna().rename(columns = {'value': 'population'})

    new_df = new_df[['year', 'steel', 'real_GDP', 'population']].copy()

    new_df = pd.merge(left = new_df, right = steel_ex, on = 'year').copy().dropna()
    
    X = [[x, y] for x, y in zip(new_df['real_GDP'], new_df['population'])]
    y = np.array(new_df.steel)

    model = LinearRegression()
    model.fit(X, y)

    x_start = new_df['year'].max() + 1
    x_years = range(x_start, END_YEAR + 1, 1)
    
    x_gdp = pd.Series(gdp[(gdp['year'] >= x_start) & 
                          (gdp['year'] <= END_YEAR)].reset_index(drop = True)['value'])
    
    x_pop = pd.Series(pop[(pop['year'] >= x_start) &
                          (pop['year'] <= END_YEAR)].reset_index(drop = True)['value'])
    
    x_ex = pd.Series(steel_ex[(steel_ex['year'] >= x_start) & 
                              (steel_ex['year'] <= END_YEAR)].reset_index(drop = True)['export_share'])
    
    x_years = pd.Series(x_years)
    
    x_pred = [[x, y] for x, y in zip(x_gdp, x_pop)]
    
    y_pred = model.predict(x_pred)

    pred_df = pd.DataFrame(columns = hist_df.columns, 
                           data = {'economy_code': economy,
                                   'production': 'Steel estimate',
                                   'year': x_years,
                                   'value': y_pred})
    
    steel_pred_df = pd.concat([hist_df, pred_df]).reset_index(drop = True)

    fig, ax = plt.subplots()

    sns.set_theme(style = 'ticks')

    sns.lineplot(data = steel_pred_df, 
                    x = 'year',
                    y = 'value',
                    hue = 'production')
    
    ax.set(title = economy,
           xlabel = 'Year',
           ylabel = 'Steel production',
           ylim = (0, steel_pred_df['value'].max() * 1.1))
    
    plt.legend(title = '')
    
    plt.tight_layout()
    plt.show()
    plt.close()


##################################

from sklearn.svm import LinearSVC
from sklearn.datasets import load_iris
from sklearn.feature_selection import SelectFromModel

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif

from sklearn import preprocessing

X = np.array(new_df.iloc[:, 2:])
y = np.array(new_df.iloc[:, 1])
X.shape
y.shape
X_normalised = preprocessing.normalize(X, 'l2')

X_normalised

X_new = SelectKBest(f_classif, k = 'all').fit_transform(X, y)
X_new

lsvc = LinearSVC(C=0.01, penalty="l1", dual=False).fit(X, y)
model = SelectFromModel(lsvc, prefit=True)
X_new = model.transform(X)
X_new.shape

X

import featuretools as ft