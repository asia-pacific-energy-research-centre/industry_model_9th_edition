# These didn't work very well as the models are just not sophisticated enough to given 
# meanigful projections

#wdi_df['year'] = pd.to_datetime(wdi_df['year'], format = '%Y')

from sklearn.linear_model import LinearRegression

for economy in wdi_df['economy_code'].unique()[[0]]:
    chart_df = wdi_df[(wdi_df['economy_code'] == economy) & 
                      (wdi_df['series_code'] == 'NV.IND.MANF.ZS')]\
                        .dropna().copy().reset_index(drop = True)
    
    X = np.array(chart_df['year']).reshape((-1, 1))
    new_x = [[x, y] for x, y in zip(chart_df.year, chart_df.year ** 2)]                 
    y = np.array(chart_df['value'])

    model = LinearRegression()
    model.fit(new_x, y)

    x_start = chart_df['year'].max()
    x_years = range(x_start + 1, END_YEAR + 1, 1)
    x_pred = np.array(x_years).reshape((-1, 1))
    new_x_pred = [[x, y ** 2] for x, y in zip(pd.Series(x_years), pd.Series(x_years))] 

    y_pred = model.predict(new_x_pred)

    pred_df = pd.DataFrame(columns = chart_df.columns, 
                           data = {'economy_code': economy,
                                   'series': 'prediction',
                                   'year': x_years,
                                   'value': y_pred})
    
    chart_df = pd.concat([chart_df, pred_df]).reset_index(drop = True)

    #print(reg)
    
    fig, ax = plt.subplots()

    sns.set_theme(style = 'ticks')

    sns.scatterplot(data = chart_df, 
                    x = 'year',
                    y = 'value',
                    hue = 'series')
    
    ax.set(title = economy,
                  xlabel = 'year',
                  ylabel = 'Manufacturing %')
    
    plt.legend(title = '')
    
    plt.tight_layout()
    plt.show()
    plt.close()

####################################################################################

from sklearn import linear_model
from sklearn.linear_model import Ridge

for economy in wdi_df['economy_code'].unique():
    chart_df = wdi_df[(wdi_df['economy_code'] == economy) & 
                      (wdi_df['series_code'] == 'NV.IND.MANF.ZS')]\
                        .dropna().copy().reset_index(drop = True)
    
    X = np.array(chart_df['year']).reshape((-1, 1))
    new_x = [[x, y] for x, y in zip(chart_df.year, chart_df.year ** 2)]                 
    y = np.array(chart_df['value'])

    clf = Ridge(alpha = 0.01)
    clf.fit(new_x, y)

    x_start = chart_df['year'].max()
    x_years = range(x_start + 1, END_YEAR + 1, 1)
    x_pred = np.array(x_years).reshape((-1, 1))
    new_x_pred = [[x, y ** 2] for x, y in zip(pd.Series(x_years), pd.Series(x_years))] 

    y_pred = clf.predict(new_x_pred)

    pred_df = pd.DataFrame(columns = chart_df.columns, 
                           data = {'economy_code': economy,
                                   'series': 'prediction',
                                   'year': x_years,
                                   'value': y_pred})
    
    chart_df = pd.concat([chart_df, pred_df]).reset_index(drop = True)

    #print(reg)
    
    fig, ax = plt.subplots()

    sns.set_theme(style = 'ticks')

    sns.scatterplot(data = chart_df, 
                    x = 'year',
                    y = 'value',
                    hue = 'series')
    
    ax.set(title = economy,
                  xlabel = 'year',
                  ylabel = 'Manufacturing %')
    
    plt.legend(title = '')
    
    plt.tight_layout()
    plt.show()
    plt.close()


##################################################################################################

pop_gdp_df = pd.read_csv('./data/macro/APEC_GDP_population.csv')

for economy in wdi_df['economy_code'].unique():
    chart_df = wdi_df[(wdi_df['economy_code'] == economy) & 
                      (wdi_df['series_code'] == 'NV.IND.MANF.ZS')]\
                        .dropna().copy().reset_index(drop = True)
    
    gdp_pc = pop_gdp_df[(pop_gdp_df['economy_code'] == economy) & 
                        (pop_gdp_df['variable'] == 'GDP_per_capita')].copy().reset_index(drop = True)
    
    new_df = pd.merge(left = chart_df, right = gdp_pc, left_on = 'year', right_on = 'year').copy().dropna()
    
    X = np.array(chart_df['year']).reshape((-1, 1))
    new_x = [[x, y, z] for x, y, z in zip(new_df.year, new_df.year ** 2, new_df.value_y)]
    y = np.array(new_df['value_x'])

    model = LinearRegression()
    model.fit(new_x, y)

    x_start = new_df['year'].max()
    x_years = range(x_start + 1, END_YEAR + 1, 1)
    x_pred = np.array(x_years).reshape((-1, 1))
    new_x_pred = [[x, y ** 2, z] for x, y, z in zip(pd.Series(x_years), 
                                                    pd.Series(x_years), 
                                                    pd.Series(gdp_pc[(gdp_pc['year'] >= x_start + 1) & 
                                                                     (gdp_pc['year'] <= END_YEAR)].reset_index(drop = True)['value']))] 

    y_pred = model.predict(new_x_pred)

    pred_df = pd.DataFrame(columns = chart_df.columns, 
                           data = {'economy_code': economy,
                                   'series': 'prediction',
                                   'year': x_years,
                                   'value': y_pred})
    
    chart_df = pd.concat([chart_df, pred_df]).reset_index(drop = True)

    #print(reg)
    
    fig, ax = plt.subplots()

    sns.set_theme(style = 'ticks')

    sns.scatterplot(data = chart_df, 
                    x = 'year',
                    y = 'value',
                    hue = 'series')
    
    ax.set(title = economy,
                  xlabel = 'year',
                  ylabel = 'Manufacturing %')
    
    plt.legend(title = '')
    
    plt.tight_layout()
    plt.show()
    plt.close()


#################################################################################

for economy in wdi_df['economy_code'].unique():
    chart_df = wdi_df[(wdi_df['economy_code'] == economy) & 
                      (wdi_df['series_code'] == 'NV.IND.MANF.ZS')]\
                        .dropna().copy().reset_index(drop = True)
    
    gdp_pc = pop_gdp_df[(pop_gdp_df['economy_code'] == economy) & 
                        (pop_gdp_df['variable'] == 'GDP_per_capita')].copy().reset_index(drop = True)
    
    new_df = pd.merge(left = chart_df, right = gdp_pc, left_on = 'year', right_on = 'year').copy().dropna()
    
    X = np.array(chart_df['year']).reshape((-1, 1))
    new_x = [[x, y] for x, y in zip(new_df.year, new_df.value_y)]
    y = np.array(new_df['value_x'])

    model = LinearRegression()
    model.fit(new_x, y)

    x_start = new_df['year'].max()
    x_years = range(x_start + 1, END_YEAR + 1, 1)
    x_pred = np.array(x_years).reshape((-1, 1))
    new_x_pred = [[x, y] for x, y in zip(pd.Series(x_years), 
                                         pd.Series(gdp_pc[(gdp_pc['year'] >= x_start + 1) & 
                                                          (gdp_pc['year'] <= END_YEAR)].reset_index(drop = True)['value']))] 

    y_pred = model.predict(new_x_pred)

    pred_df = pd.DataFrame(columns = chart_df.columns, 
                           data = {'economy_code': economy,
                                   'series': 'prediction',
                                   'year': x_years,
                                   'value': y_pred})
    
    chart_df = pd.concat([chart_df, pred_df]).reset_index(drop = True)

    #print(reg)
    
    fig, ax = plt.subplots()

    sns.set_theme(style = 'ticks')

    sns.scatterplot(data = chart_df, 
                    x = 'year',
                    y = 'value',
                    hue = 'series')
    
    ax.set(title = economy,
                  xlabel = 'year',
                  ylabel = 'Manufacturing %')
    
    plt.legend(title = '')
    
    plt.tight_layout()
    plt.show()
    plt.close()


for economy in wdi_df['economy_code'].unique()[[6]]:
    chart_df = wdi_df[(wdi_df['economy_code'] == economy) & 
                      (wdi_df['series_code'] == 'NV.MNF.OTHR.ZS.UN')]\
                        .dropna().copy().reset_index(drop = True)
    
    # X = np.array(chart_df['year']).reshape((-1, 1))
    # new_x = [[x, y] for x, y in zip(chart_df.year, chart_df.year ** 2)]                 
    # y = np.array(chart_df['value'])

    # model = LinearRegression()
    # model.fit(new_x, y)

    # x_start = chart_df['year'].max()
    # x_years = range(x_start + 1, END_YEAR + 1, 1)
    # x_pred = np.array(x_years).reshape((-1, 1))
    # new_x_pred = [[x, y ** 2] for x, y in zip(pd.Series(x_years), pd.Series(x_years))] 

    # y_pred = model.predict(new_x_pred)

    # pred_df = pd.DataFrame(columns = chart_df.columns, 
    #                        data = {'economy_code': economy,
    #                                'series': 'prediction',
    #                                'year': x_years,
    #                                'value': y_pred})
    
    # chart_df = pd.concat([chart_df, pred_df]).reset_index(drop = True)

    #print(reg)
    
    fig, ax = plt.subplots()

    sns.set_theme(style = 'ticks')

    sns.scatterplot(data = chart_df, 
                    x = 'year',
                    y = 'value',
                    hue = 'series')
    
    ax.set(title = economy,
                  xlabel = 'year',
                  ylabel = 'Proportion')
    
    plt.legend(title = '')
    
    plt.tight_layout()
    plt.show()
    plt.close()



    # Inspect the data series

for economy in wdi_df['economy_code'].unique():
    for series in wdi_df['series_code'].unique():
        chart_df = wdi_df[(wdi_df['economy_code'] == economy) & 
                          (wdi_df['series_code'] == series)]\
                                .dropna().copy().reset_index(drop = True)

        fig, ax = plt.subplots()

        sns.set_theme(style = 'ticks')

        sns.scatterplot(data = chart_df, 
                        x = 'year', 
                        y = 'value',
                        hue = 'series')

        ax.set(title = economy,
               xlabel = 'year',
               ylabel = 'Proportion')

        plt.legend(title = '')
        
        # Save location for charts
        charts = './results/production/industry/{}/'.format(economy)

        if not os.path.isdir(charts):
            os.makedirs(charts)

        plt.tight_layout()
        plt.savefig(charts + economy + '_' + series + '.png')
        plt.close()


#####################################################################################################

input_data = pd.DataFrame([
    [1, 5, 12, 4],
    [1, 5, 16, 5],
    [1, 5, 20, 6],
    [1, 5, 8, 3],
    [1, 5, 10, 3.5],
    [1, 5, 22, 6.5],
    [2, 8, 12, 44],
    [2, 8, 10, 33],
    [2, 8, 14, 50],
    [2, 8, 8, 15],
    [2, 8, 0, 0],
    [2, 8, 3, -5]
], columns = ['id', 'constant_feature', 'time_dependent_feature', 'target_variable'])

input_data = input_data.set_index('id')

unique_ids = input_data.index.unique()

X = []
Y = []

for identifier in unique_ids:
    single_process_data = input_data.loc[identifier] #1
    
    data = pd.DataFrame(single_process_data[['target_variable', 'time_dependent_feature']].copy()) #2
    data.columns = ['y', 'time_dependent_feature'] #2

    # last 5 values of the target variable as "lag" variables (the most recent one is the dependent feature (y))
    for i in range(1, 6): #3
        data['target_lag_{}'.format(i)] = data.y.shift(i)
        
    # last 6 values of the target variable as "time_dependent_feature" variables
    for i in range(0, 6): #4
        data['time_dependent_feature_lag_{}'.format(i)] = data.time_dependent_feature.shift(i)
    
    #rewrite constants
    data['constant_feature'] = single_process_data['constant_feature'] #5

    #the shift operations in the loops create many partial results. They are useless, and we don't want them
    data = data.dropna()
    y = data.y #6
    x = data.drop(['y', 'time_dependent_feature'], axis=1) #6
    
    X.append(np.array(x).flatten()) #7
    Y.append(y) #7