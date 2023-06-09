# Cement projections using Machine Learning

# Set working directory to be the project folder
import os
import re

wanted_wd = 'industry_model_9th_edition'
os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

# execute config file
config_file = './config/config_apr2023.py'
with open(config_file) as infile:
    exec(infile.read())

# Import historical cement data and gdp
cement_df = pd.read_csv('./data/production_and_trade/production_cement/cement_usgs_cleaned.csv')
# Remove unneeded column
cement_df = cement_df.iloc[:, [0, 2, 3, 4, 5]] 
gdp_df = pd.read_csv('./data/macro/APEC_GDP_data.csv')

# Import some modelling dependencies
from sklearn import preprocessing
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV
from sklearn.metrics import mean_squared_error

from sklearn import linear_model
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.svm import LinearSVC

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.exceptions import ConvergenceWarning

from mlearn_functions import listGen, powerset

##############################################################################################
# For best model build after train/test
model_alpha = {'Ridge': GridSearchCV(estimator = Ridge(),
                                        param_grid = {'alpha': np.logspace(-3, 3, 7)},
                                        scoring = 'neg_root_mean_squared_error'),                       
                'Lasso': GridSearchCV(estimator = Lasso(tol = 0.1, max_iter = 10000),
                                        param_grid = {'alpha': np.logspace(-3, 3, 7)},
                                        scoring = 'neg_root_mean_squared_error')}

model_choice = {'OLS': LinearRegression,
                'Ridge': Ridge,
                'Lasso': Lasso}

##############################################################################################

economy_list = list(cement_df['economy_code'].unique())
# Remove Brunei
economy_list = [i for i in economy_list if i != '02_BD']

for economy in economy_list:
    # Create empty data frame that saves k-fold fit information later
    mse_results = pd.DataFrame(columns = ['Economy', 'Fold', 'MSE', 'RMSE', 'Model', 'Model build', 'Features'])

    # Target variable: cement production
    target_df = cement_df[cement_df['economy_code'] == economy].copy().dropna().reset_index(drop = True)
    
    # Feature/explanatory variables
    gdp_pc = gdp_df[(gdp_df['economy_code'] == economy) &
                    (gdp_df['variable'] == 'GDP_per_capita')].copy().reset_index(drop = True)
    
    gdp = gdp_df[(gdp_df['economy_code'] == economy) &
                 (gdp_df['variable'] == 'real_GDP')].copy().reset_index(drop = True)
    
    pop = gdp_df[(gdp_df['economy_code'] == economy) &
                 (gdp_df['variable'] == 'population')].copy().reset_index(drop = True)
    
    # Target and features in one data frame that is historical
    full_df = pd.merge(left = target_df, right = gdp, on = 'year', how = 'outer').copy()

    full_df = full_df[['year', 'value_x', 'value_y']].rename(columns = {'value_x': 'cement',
                                                                        'value_y': 'real_GDP'}).copy()
    
    full_df = pd.merge(left = full_df, right = pop, on = 'year', how = 'outer')\
        .copy().rename(columns = {'value': 'population'})

    full_df = full_df[['year', 'cement', 'real_GDP', 'population']].copy()

    # Full data frame with cement (target only for historical) and real_GDP, population, and GDP per capita features to 2100
    full_df = pd.merge(left = full_df, right = gdp_pc, on = 'year', how = 'outer')\
        .copy().rename(columns = {'value': 'GDP_per_capita'})\
            [['cement', 'year', 'real_GDP', 'population', 'GDP_per_capita']]
    
    # Create historical dataframe for train and testing with known target 
    hist_df = full_df.copy().set_index('year')

    # Now need to feature engineer by generating even more features from the 3 that currently have
    # STEP 1: natural log transform independent variables and target variable (cement)

    hist_df['cement'] = np.log(hist_df['cement'])
    hist_df['real_GDP'] = np.log(hist_df['real_GDP'])
    hist_df['population'] = np.log(hist_df['population'])
    hist_df['GDP_per_capita'] = np.log(hist_df['GDP_per_capita'])
    
    # STEP 2: create polynomial transformations of GDP, population and GDP_per_capita
    for b in range(DEGREE, DEGREE + 1, 1):
        hist_df['gdp_{}'.format(b)] = hist_df['real_GDP'] ** b
        hist_df['pop_{}'.format(b)] = hist_df['population'] ** b

    # STEP 3: create lagged variables (features and target)

    for year in hist_df.index:    
        for i in range(1, LAGS + 1):
            if (year - i > 1979) & (year - i in hist_df.index):
                hist_df.loc[year, 'cement_lag_{}'.format(i)] = hist_df.loc[year - i, 'cement']
                hist_df.loc[year, 'gdp_lag_{}'.format(i)] = hist_df.loc[year - i, 'real_GDP']
                hist_df.loc[year, 'pop_lag_{}'.format(i)] = hist_df.loc[year - i, 'population']
                hist_df.loc[year, 'gdp_pc_lag_{}'.format(i)] = hist_df.loc[year - i, 'GDP_per_capita']
            else:
                pass

    # Keep all lagged data for updating arrays later
    all_hist_df = hist_df.copy()

    # But for now, only keep data that is notna
    hist_df = hist_df.dropna()

    # Define number of features in historical data: number of columns minus 1 which is the 
    # target (cement production in year i)
    x_n = hist_df.shape[1] - 1

    # Build numpy combinations of feature variables to use in models
    # Note: the first combination is an empyty set []
    X_arrays = {}
    X_cols = {}

    for i, combo in enumerate(powerset(list(range(1, x_n + 1, 1))), 1):
        X_arrays[i] = hist_df.iloc[:, list(combo)].to_numpy()
        X_cols[i] = list(combo)

    # Now remove the first empty X array 
    # (a relic of the powerset function which includes an empty set)
    del X_arrays[1]

    # Split out the target variable
    y = np.array(hist_df.iloc[:, 0])

    # Now split the data into training and test sets
    tscv = TimeSeriesSplit(n_splits = KFOLD_SPLIT, test_size = None)

    # For ridge regression and lasso, define a grid search to identify best alpha
    rr_alpha = GridSearchCV(estimator = Ridge(),
                            param_grid = {'alpha': np.logspace(-3, 3, 7)},
                            scoring = 'neg_root_mean_squared_error',
                            cv = tscv)
    
    lasso_alpha = GridSearchCV(estimator = Lasso(tol = 0.1, max_iter = 10000),
                               param_grid = {'alpha': np.logspace(-3, 3, 7)},
                               scoring = 'neg_root_mean_squared_error',
                               cv = tscv)
    
    # Define scalar to scale the features
    sc = StandardScaler()
    
    ##############################################################################################
    
    # Save location for data and charts
    save_data = './data/ml_cement/{}/'.format(economy)

    if not os.path.isdir(save_data):
        os.makedirs(save_data)

    for key, array in X_arrays.items():
        for fold, (train_index, test_index) in enumerate(tscv.split(array)):

            X_train, X_test = array[train_index], array[test_index]
            y_train, y_test = y[train_index], y[test_index]

            sc_X_train = sc.fit_transform(X_train)
            sc_X_test = sc.transform(X_test)

            lm_1 = LinearRegression()
            # For ridge regression and lasso, determine optimal alpha
            rr_alpha.fit(sc_X_train, y_train)
            alpha_rr = rr_alpha.best_params_['alpha']           

            rr_1 = Ridge(alpha = alpha_rr)

            lm_1.fit(sc_X_train, y_train)
            rr_1.fit(sc_X_train, y_train)

            # Linear
            y_pred_lm = lm_1.predict(sc_X_test)
            mse_lm = mean_squared_error(y_test, y_pred_lm)
            rmse_lm = mean_squared_error(y_test, y_pred_lm, squared = False)

            # Ridge regression
            y_pred_rr = rr_1.predict(sc_X_test)
            mse_rr = mean_squared_error(y_test, y_pred_rr)
            rmse_rr = mean_squared_error(y_test, y_pred_rr, squared = False)

            mse_results.loc[len(mse_results.index)] = [economy, int(fold), mse_lm, rmse_lm, 'OLS', key, list(hist_df.columns[X_cols[key]])]
            mse_results.loc[len(mse_results.index)] = [economy, int(fold), mse_rr, rmse_rr, 'Ridge', key, list(hist_df.columns[X_cols[key]])]

            # For Lasso, turn convergence warning into an error      
            try:
                # Use above built lasso to do a grid search for best alpha                
                lasso_alpha.fit(sc_X_train, y_train)
                alpha_lasso = lasso_alpha.best_params_['alpha']

                # Define lasso and fit it (with best alpha from above)
                lasso_1 = Lasso(alpha = alpha_lasso, tol = 0.1, max_iter = 10000)
                lasso_1.fit(sc_X_train, y_train)

                # Now predict using lasso and generate 
                y_pred_lasso = lasso_1.predict(sc_X_test)
                mse_lasso = mean_squared_error(y_test, y_pred_lasso)
                rmse_lasso = mean_squared_error(y_test, y_pred_lasso, squared = False)
                mse_results.loc[len(mse_results.index)] = [economy, int(fold), mse_lasso, rmse_lasso, 'Lasso', key, list(hist_df.columns[X_cols[key]])]
        
            except ConvergenceWarning:
                pass

            # # Charts
            # chart_df = hist_df[['cement']].copy() 
            # y_pred_lm_df = pd.DataFrame(y_pred_lm, index = hist_df.index[test_index], columns = ['cement_prediction_lm'])
            # y_pred_rr_df = pd.DataFrame(y_pred_rr, index = hist_df.index[test_index], columns = ['cement_prediction_rr'])
            # y_pred_lasso_df = pd.DataFrame(y_pred_lasso, index = hist_df.index[test_index], columns = ['cement_prediction_lasso'])
            
            # chart_df = pd.concat([chart_df, y_pred_lm_df, y_pred_rr_df, y_pred_lasso_df], axis = 1).reset_index().melt(id_vars = 'year')

            # fig, ax = plt.subplots()

            # sns.set_theme(style = 'ticks')

            # sns.lineplot(data = chart_df,
            #              x = 'year',
            #              y = 'value',
            #              hue = 'variable')
            
            # ax.set(title = economy + ' ' + str(list(hist_df.columns[X_cols[key]])) + ' ' + str(fold),
            #        xlabel = 'Year',
            #        ylabel = 'Cement production')
            
            # plt.legend(title = '')
        
            # plt.tight_layout()
            # plt.savefig(save_data + economy + '_' + str(key) + '_' + str(fold) + '.png')
            # plt.close()

    # Save results dataframe after looping through all models
    mse_results.to_csv(save_data + economy + '_' + 'mse_results.csv', index = False)

    # Best model will be in the 0 index, 2nd best in 1 index, etc.
    model_sort = pd.DataFrame(mse_results.groupby(['Model', 'Model build'])[['MSE', 'RMSE']]\
                              .sum()).reset_index().sort_values('RMSE')\
                                .reset_index(drop = True)
    
    model_sort['target_lag'] = np.nan
    model_sort['target_lag'] = model_sort['target_lag'].astype('boolean') 

    for q in range(model_sort.shape[0]):
        features = hist_df.columns[X_cols[model_sort.iloc[q, 1]]]
        if pd.Series(features).str.contains('cement_lag').any():
            model_sort.iloc[q, 4] = True
        else:
            model_sort.iloc[q, 4] = False

    # From the above, we now have a list of the best performing models for each economy in 'model_sort'
    # Save location for final model builds and charts
    build_save = save_data + 'ml_build/'

    if not os.path.isdir(build_save):
        os.makedirs(build_save)

    # Save model predictions

    saved_predictions = hist_df.copy().reset_index()[['year', 'cement']]
    saved_predictions['model'] = 'Historic cement production'

    target_lag_models = 0

    for i in range(TOP_MODELS):
        # Check whether any of the features are lagged versions of the target
        features = hist_df.columns[X_cols[model_sort.iloc[i, 1]]]
        if pd.Series(features).str.contains('cement_lag').any():
            target_lag_models += 1
            
            X_array = X_arrays[model_sort.iloc[i, 1]]
            X_col = X_cols[model_sort.iloc[i, 1]]

            temp_hist_df = all_hist_df.copy()

            # Scale the X array (y array is already defined above as 'y')
            sc_X = sc.fit_transform(X_array)

            # Optimise alpha if it is Ridge or Lasso (not needed for OLS)
            if model_sort.iloc[i, 0] in ['Ridge', 'Lasso']:
                alpha_sel = model_alpha[model_sort.iloc[i, 0]]
                alpha_sel.fit(sc_X, y)
                alpha_choice = alpha_sel.best_params_['alpha']
                
                model = model_choice[model_sort.iloc[i, 0]](alpha = alpha_choice)

            else:
                model = model_choice[model_sort.iloc[i, 0]]()

            model.fit(sc_X, y)

            for j in range(hist_df.index.max() + 1, temp_hist_df.index.max(), 1):
                # Create new line of X's to then predict cement
                new_X = temp_hist_df.loc[j, features]
                # Populate cement lagged cells
                for z in range(1, LAGS + 1, 1):
                    new_X['cement_lag_{}'.format(z)] = temp_hist_df.loc[j - z, 'cement']
                    temp_hist_df.loc[j, 'cement_lag_{}'.format(z)] = temp_hist_df.loc[j - z, 'cement']

                # Save this new array to predict y, and also append to X_array
                new_X_array = pd.DataFrame(new_X).to_numpy().T
                X_array = np.append(X_array, new_X_array, axis = 0)
                
                # Scale the x array
                new_X_sc = sc.transform(new_X_array)

                # Now predict and save that y in the temp_hist_df
                y_pred = model.predict(new_X_sc)

                temp_hist_df.loc[j, 'cement'] = y_pred

            predicted = temp_hist_df.reset_index()[['year', 'cement']]
            predicted = predicted[predicted['year'] > hist_df.index.max()].copy().reset_index(drop = True)
            predicted['model'] = 'model_' + str(i + 1) + '_' + str(model_sort.iloc[i, 0]) + str(model_sort.iloc[i, 1])

            saved_predictions = pd.concat([saved_predictions, predicted]).copy()

            temp_hist_df.to_csv(build_save + 'model_' + str(i + 1) + '_' + str(model_sort.iloc[i, 0]) + str(model_sort.iloc[i, 1]) + '.csv')

        else:    
            # This is for where there are no lagged feature variables
            X_array = X_arrays[model_sort.iloc[i, 1]]
            X_col = X_cols[model_sort.iloc[i, 1]]

            temp_hist_df = all_hist_df.copy()

            # Scale the X array (y array is already defined above as 'y')
            sc_X = sc.fit_transform(X_array)

            # Optimise alpha if it is Ridge or Lasso
            if model_sort.iloc[i, 0] in ['Ridge', 'Lasso']:
                alpha_sel = model_alpha[model_sort.iloc[i, 0]]
                alpha_sel.fit(sc_X, y)
                alpha_choice = alpha_sel.best_params_['alpha']
                
                model = model_choice[model_sort.iloc[i, 0]](alpha = alpha_choice)

            else:
                model = model_choice[model_sort.iloc[i, 0]]()

            model.fit(sc_X, y)
        
            # Create new line of X's to then predict cement
            new_X = temp_hist_df.loc[(hist_df.index.max() + 1):(temp_hist_df.index.max() - 1), features]

            # Save this new array to predict y, and also append to X_array
            new_X_array = pd.DataFrame(new_X).to_numpy()
            X_array = np.append(X_array, new_X_array, axis = 0)
            
            # Scale the x array
            new_X_sc = sc.transform(new_X_array)

            # Now predict and save that y in the temp_hist_df
            y_pred = model.predict(new_X_sc)

            predicted = pd.DataFrame(y_pred, index = range(hist_df.index.max() + 1, temp_hist_df.index.max()))
            predicted = predicted.reset_index()
            predicted.columns = ['year', 'cement']
            predicted['model'] = 'model_' + str(i + 1) + '_' + str(model_sort.iloc[i, 0]) + str(model_sort.iloc[i, 1]) + '_no_tlag'

            saved_predictions = pd.concat([saved_predictions, predicted]).copy().reset_index(drop = True)

    # Now ensure some non-lagged target variable models are included
    model_sort_nolag = model_sort[model_sort['target_lag'] == False].copy().reset_index(drop = True)

    for p in range(target_lag_models, 0, -1):
        # This is for where there are no lagged feature variables
        nolag_index = TOP_MODELS - p
        features = hist_df.columns[X_cols[model_sort_nolag.iloc[nolag_index, 1]]]

        X_array = X_arrays[model_sort_nolag.iloc[nolag_index, 1]]
        X_col = X_cols[model_sort_nolag.iloc[nolag_index, 1]]

        temp_hist_df = all_hist_df.copy()

        # Scale the X array (y array is already defined above as 'y')
        sc_X = sc.fit_transform(X_array)

        # Optimise alpha if it is Ridge or Lasso
        if model_sort_nolag.iloc[nolag_index, 0] in ['Ridge', 'Lasso']:
            alpha_sel = model_alpha[model_sort_nolag.iloc[nolag_index, 0]]
            alpha_sel.fit(sc_X, y)
            alpha_choice = alpha_sel.best_params_['alpha']
            
            model = model_choice[model_sort_nolag.iloc[nolag_index, 0]](alpha = alpha_choice)

        else:
            model = model_choice[model_sort_nolag.iloc[nolag_index, 0]]()

        model.fit(sc_X, y)
    
        # Create new line of X's to then predict cement
        new_X = temp_hist_df.loc[(hist_df.index.max() + 1):(temp_hist_df.index.max() - 1), features]

        # Save this new array to predict y, and also append to X_array
        new_X_array = pd.DataFrame(new_X).to_numpy()
        X_array = np.append(X_array, new_X_array, axis = 0)
        
        # Scale the x array
        new_X_sc = sc.transform(new_X_array)

        # Now predict and save that y in the temp_hist_df
        y_pred = model.predict(new_X_sc)

        predicted = pd.DataFrame(y_pred, index = range(hist_df.index.max() + 1, temp_hist_df.index.max()))
        predicted = predicted.reset_index()
        predicted.columns = ['year', 'cement']
        predicted['model'] = 'model_' + str(target_lag_models + nolag_index + 1) + '_' + str(model_sort_nolag.iloc[nolag_index, 0]) + str(model_sort_nolag.iloc[nolag_index, 1]) + '_no_tlag'

        saved_predictions = pd.concat([saved_predictions, predicted]).copy().reset_index(drop = True)

    # Revert cement to original unit (reverse log transformation)
    saved_predictions['cement'] = np.exp(saved_predictions['cement']) 

    saved_predictions.to_csv(build_save + 'model_predictions_' + economy + '.csv', index = False)

    # Build some charts
    chart_df = pd.read_csv(build_save + 'model_predictions_' + economy + '.csv')

    fig, ax = plt.subplots()

    sns.set_theme(style = 'ticks')

    sns.lineplot(data = chart_df,
                    x = 'year',
                    y = 'cement',
                    hue = 'model')
    
    ax.set(title = economy + ' best performing models',
            xlabel = 'Year',
            ylabel = 'Cement production')
    
    plt.legend(title = '')

    plt.tight_layout()
    plt.savefig(build_save + economy + '_model_prediction_all.png')
    plt.close()

    # Second chart and third charts

    best = chart_df[~(chart_df['model'].str.contains('tlag'))]
    
    fig, ax = plt.subplots()

    sns.set_theme(style = 'ticks')

    sns.lineplot(data = best,
                    x = 'year',
                    y = 'cement',
                    hue = 'model')
    
    ax.set(title = economy + ' best performing models w target lag',
            xlabel = 'Year',
            ylabel = 'Cement production')
    
    plt.legend(title = '')

    plt.tight_layout()
    plt.savefig(build_save + economy + '_model_prediction_tlag.png')
    plt.close()

    # Third chart
    no_tlag = chart_df[(chart_df['model'].str.contains('tlag')) |
                       (chart_df['model'].str.contains('Historic'))] 
    
    fig, ax = plt.subplots()

    sns.set_theme(style = 'ticks')

    sns.lineplot(data = no_tlag,
                    x = 'year',
                    y = 'cement',
                    hue = 'model')
    
    ax.set(title = economy + ' best performing models no target lag variables',
            xlabel = 'Year',
            ylabel = 'Cement production')
    
    plt.legend(title = '')

    plt.tight_layout()
    plt.savefig(build_save + economy + '_model_prediction_no_tlag.png')
    plt.close()
