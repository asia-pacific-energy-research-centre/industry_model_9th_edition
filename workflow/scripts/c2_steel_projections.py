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
gdp_df = pd.read_csv('./data/macro/APEC_GDP_data.csv')

# Import some modelling dependencies
from sklearn import preprocessing
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_squared_error

from sklearn.linear_model import LinearRegression
from sklearn.svm import LinearSVC

from mlearn_functions import listGen, powerset

mse_results = pd.DataFrame(columns = ['Economy', 'Fold', 'MSE', 'Model', 'Model build'])

for economy in list(steel_df['economy_code'].unique())[:-1]:
    # Target variable: steel production
    target_df = steel_df[steel_df['economy_code'] == economy].copy().dropna().reset_index(drop = True)
    
    # Feature/explanatory variables
    gdp_pc = gdp_df[(gdp_df['economy_code'] == economy) &
                    (gdp_df['variable'] == 'GDP_per_capita')].copy().reset_index(drop = True)
    
    gdp = gdp_df[(gdp_df['economy_code'] == economy) &
                 (gdp_df['variable'] == 'real_GDP')].copy().reset_index(drop = True)
    
    pop = gdp_df[(gdp_df['economy_code'] == economy) &
                 (gdp_df['variable'] == 'population')].copy().reset_index(drop = True)
    
    # Target and features in one data frame that is historical
    full_df = pd.merge(left = target_df, right = gdp, on = 'year', how = 'outer').copy()

    full_df = full_df[['year', 'value_x', 'value_y']].rename(columns = {'value_x': 'steel',
                                                                        'value_y': 'real_GDP'}).copy()
    
    full_df = pd.merge(left = full_df, right = pop, on = 'year', how = 'outer')\
        .copy().rename(columns = {'value': 'population'})

    full_df = full_df[['year', 'steel', 'real_GDP', 'population']].copy()

    # Full data frame with steel (target only for historical) and real_GDP, population, and GDP per capita features to 2100
    full_df = pd.merge(left = full_df, right = gdp_pc, on = 'year', how = 'outer')\
        .copy().rename(columns = {'value': 'GDP_per_capita'})\
            [['steel', 'year', 'real_GDP', 'population', 'GDP_per_capita']]
    
    # Create historical dataframe for train and testing with known target 
    hist_df = full_df.copy().dropna().set_index('year')

    # Now need to feature engineer by generating even more features from the 3 that currently have
    # STEP 1: create lagged variables (features and target)

    lags = 1

    for year in hist_df.index:    
        for i in range(1, lags + 1):
            if (year - i > 1979) & (year - 1 in hist_df.index):
                hist_df.loc[year, 'steel_lag_{}'.format(i)] = hist_df.loc[year - i, 'steel']
                hist_df.loc[year, 'gdp_lag_{}'.format(i)] = hist_df.loc[year - i, 'real_GDP']
                hist_df.loc[year, 'pop_lag_{}'.format(i)] = hist_df.loc[year - i, 'population']
                hist_df.loc[year, 'gdp_pc_lag_{}'.format(i)] = hist_df.loc[year - i, 'GDP_per_capita']
            else:
                pass

    # Now only keep data that is notna
    hist_df = hist_df.dropna()

    # Define number of features in historical data: number of columns minus 1 which is the 
    # target (steel production in year i)
    x_n = hist_df.shape[1] - 1

    # Build numpy combinations of feature variables to use in models
    # Note: the first combination is an empyty set []
    X_arrays = {}
    for i, combo in enumerate(powerset(list(range(1, x_n + 1, 1))), 1):
        X_arrays[i] = hist_df.iloc[:, list(combo)].to_numpy()

    # Now remove the first empty X array
    del X_arrays[1]

    # Split out the target variable
    y = np.array(hist_df.iloc[:, 0])

    # Now split the data into training and test sets
    tscv = TimeSeriesSplit(n_splits = 5, test_size = None)

    for key, array in X_arrays.items():
        for fold, (train_index, test_index) in enumerate(tscv.split(array)):

            X_train, X_test = array[train_index], array[test_index]
            y_train, y_test = y[train_index], y[test_index]

            lm_1 = LinearRegression()
            lm_1.fit(X_train, y_train)

            y_pred = lm_1.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)

            mse_results.loc[len(mse_results.index)] = [economy, int(fold), mse, 'OLS', key]





    
    # Now standardise the size of x variables
     

    # Combination equation: n choose r

    
    

    # Time series cross validation
    tscv = TimeSeriesSplit(n_splits = int(hist_df.shape[0] / 3), test_size = 2)

    mse_results = pd.DataFrame(columns = ['Economy', 'Fold', 'MSE', 'Model'])

    for fold, (train_index, test_index) in enumerate(tscv.split(X1)):
        # print("Fold: {}".format(fold))
        # print('%s %s' % (train_index, test_index))
        X1_train, X1_test = X1[train_index], X1[test_index]
        y_train, y_test = y[train_index], y[test_index]

        X2_train, X2_test = X2[train_index], X2[test_index]
        X3_train, X3_test = X3[train_index], X3[test_index]
        X4_train, X4_test = X4[train_index], X4[test_index]
        X5_train, X5_test = X5[train_index], X5[test_index]
        X6_train, X6_test = X6[train_index], X6[test_index]
        X7_train, X7_test = X7[train_index], X7[test_index]

        lm_1 = LinearRegression()
        lm_1.fit(X1_train, y_train)

        y_pred = lm_1.predict(X1_test)
        mse = mean_squared_error(y_test, y_pred)

        mse_results.loc[len(mse_results.index)] = [economy, int(fold), mse, 'OLS_1']

        lm_2 = LinearRegression()
        lm_2.fit(X2_train, y_train)

        y_pred = lm_2.predict(X2_test)
        mse = mean_squared_error(y_test, y_pred)

        mse_results.loc[len(mse_results.index)] = [economy, int(fold), mse, 'OLS_2']

        lm_3 = LinearRegression()
        lm_3.fit(X3_train, y_train)

        y_pred = lm_3.predict(X3_test)
        mse = mean_squared_error(y_test, y_pred)

        mse_results.loc[len(mse_results.index)] = [economy, int(fold), mse, 'OLS_3']

        lm_4 = LinearRegression()
        lm_4.fit(X4_train, y_train)

        y_pred = lm_4.predict(X4_test)
        mse = mean_squared_error(y_test, y_pred)

        mse_results.loc[len(mse_results.index)] = [economy, int(fold), mse, 'OLS_4']

        lm_5 = LinearRegression()
        lm_5.fit(X5_train, y_train)

        y_pred = lm_5.predict(X5_test)
        mse = mean_squared_error(y_test, y_pred)

        mse_results.loc[len(mse_results.index)] = [economy, int(fold), mse, 'OLS_5']

        lm_6 = LinearRegression()
        lm_6.fit(X6_train, y_train)

        y_pred = lm_6.predict(X6_test)
        mse = mean_squared_error(y_test, y_pred)

        mse_results.loc[len(mse_results.index)] = [economy, int(fold), mse, 'OLS_6']

        lm_7 = LinearRegression()
        lm_7.fit(X7_train, y_train)

        y_pred = lm_7.predict(X7_test)
        mse = mean_squared_error(y_test, y_pred)

        mse_results.loc[len(mse_results.index)] = [economy, int(fold), mse, 'OLS_7']

        fig, ax = plt.subplots()

        sns.lineplot(data = mse_results,
                        x = 'Fold',
                        y = 'MSE',
                        hue = 'Model')

        ax.set(title = economy)

        
        





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




import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
pd.options.display.max_columns = 30
import os
import re
from colorama import Fore, Back, Style
import seaborn as sns
import plotly.express as px
import matplotlib
from matplotlib.patches import Patch
from matplotlib import pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})
plt.style.use('fivethirtyeight')
cmap_data = plt.cm.Paired
cmap_cv = plt.cm.coolwarm
import warnings
warnings.filterwarnings('ignore')



def plot_cv_indices(cv, n_splits, X, y, date_col = None):
    """Create a sample plot for indices of a cross-validation object."""
    
    fig, ax = plt.subplots()
    
    # Generate the training/testing visualizations for each CV split
    for ii, (tr, tt) in enumerate(cv.split(X=X, y=y)):
        # Fill in indices with the training/test groups
        indices = np.array([np.nan] * len(X))
        indices[tt] = 1
        indices[tr] = 0

        # Visualize the results
        ax.scatter(range(len(indices)), [ii + .5] * len(indices),
                   c=indices, marker='_', lw=10, cmap = cmap_cv,
                   vmin=-.2, vmax=1.2)


    # Formatting
    yticklabels = list(range(n_splits))
    
    if date_col is not None:
        tick_locations  = ax.get_xticks()
        tick_dates = [" "] + date_col.iloc[list(tick_locations[1:-1])].astype(str).tolist() + [" "]

        tick_locations_str = [str(int(i)) for i in tick_locations]
        new_labels = ['\n\n'.join(x) for x in zip(list(tick_locations_str), tick_dates) ]
        ax.set_xticks(tick_locations)
        ax.set_xticklabels(new_labels)
    
    ax.set()
    ax.legend()



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





# Global steel exports as a percentange of production
steel_ex = pd.read_csv('./data/production_and_trade/wsa_steelexport.csv', index_col = 'year')

# Project it to 2100 so that it stays constant
for i in range(2022, 2101):
    steel_ex.loc[i, 'export_share'] = steel_ex.loc[i - 1, 'export_share']

steel_ex = steel_ex.copy().reset_index(drop = False)[['year', 'export_share']]

# Normalise: possibly incorporate this later
    # X = np.array(hist_df.iloc[:, 1:])
    # y = np.array(hist_df.iloc[:, 0])

    # X_normalised = preprocessing.normalize(X, norm = 'l2', axis = 0)