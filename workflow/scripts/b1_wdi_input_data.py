# World Development Indicators industry data
import os
import re

wanted_wd = 'industry_model_9th_edition'

os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

# execute config file
config_file = './config/config_apr2023.py'
with open(config_file) as infile:
    exec(infile.read())

wdi_df1 = pd.read_excel('./data/production_rawgrab.xlsx', 
                       sheet_name = 'WDI_more', 
                       nrows = 140, 
                       na_values = ['..'])

wdi_df1 = wdi_df1.melt(id_vars = ['Country Name', 'Country Code', 'Series Name', 'Series Code'])\
    .rename(columns = {'Country Name': 'economy',
                       'Country Code': 'economy_code',
                       'Series Name': 'series',
                       'Series Code': 'series_code',
                       'variable': 'year'})

wdi_df1['year'] = wdi_df1['year'].str[:4]

wdi_df2 = pd.read_excel('./data/production_rawgrab.xlsx', 
                       sheet_name = 'Ind_VA',
                       skiprows = 4, 
                       na_values = ['..'])

wdi_df2 = wdi_df2.melt(id_vars = ['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code'])\
    .rename(columns = {'Country Name': 'economy',
                       'Country Code': 'economy_code',
                       'Indicator Name': 'series',
                       'Indicator Code': 'series_code',
                       'variable': 'year'})

wdi_df = pd.concat([wdi_df1, wdi_df2])

# Load the APEC codes (versus WDI)
APEC_economies = pd.read_csv('./data/config/APEC_WDI.csv', index_col = 0)\
    .squeeze().to_dict()

APEC_fullname = pd.read_csv('./data/config/APEC_economies.csv', index_col = 0)\
    .squeeze().to_dict()

wdi_df['economy_code'] = wdi_df['economy_code'].map(APEC_economies)
wdi_df = wdi_df.sort_values(['economy_code', 'series', 'year']).copy().dropna().reset_index(drop = True)

wdi_df.to_csv('./data/wdi_industry.csv', index = False)
wdi_df = pd.read_csv('./data/wdi_industry.csv')

# Remove data series we don't need
wdi_df = wdi_df[wdi_df['series_code'] != 'NV.MNF.TECH.ZS.UN'].copy().reset_index(drop = True)

# Now build a function that projects out to 2100
def ind_projection(input_data = wdi_df,
                   economy = '01_AUS',
                   series = 'NV.IND.MANF.ZS',
                   high_bound = 20,
                   low_bound = 10,
                   high_change = 0.999,
                   low_change = 1.001):
    
    ind_df1 = input_data[(input_data['economy_code'] == economy) &
                         (input_data['series_code'] == series)].copy()\
                         .reset_index(drop = True)
    
    if ind_df1.empty:
        pass
    
    else:
        hist_max = ind_df1['year'].max()
        proj_range = range(hist_max + 1, END_YEAR + 1, 1)

        proj_df = pd.DataFrame(columns = ind_df1.columns,
                            data = {'economy_code': economy,
                                    'series': 'Projection',
                                    'series_code': series,
                                    'year': proj_range})
        
        ind_df2 = pd.concat([ind_df1, proj_df]).set_index('year', drop = True)

        for year in proj_range:
            if ind_df2.loc[year - 1, 'value'] > high_bound:
                ind_df2.loc[year, 'value'] = ind_df2.loc[year - 1, 'value'] * high_change ** (np.cbrt(year - hist_max))

            elif ind_df2.loc[year - 1, 'value'] < low_bound:
                ind_df2.loc[year, 'value'] = ind_df2.loc[year - 1, 'value'] * low_change ** (np.cbrt(year - hist_max))

            else:
                ind_df2.loc[year, 'value'] = ind_df2.loc[year - 1, 'value']

        ind_df2 = ind_df2.copy().reset_index(drop = False)[['economy', 
                                                            'economy_code',
                                                            'series',
                                                            'series_code', 
                                                            'year',
                                                            'value']]
        
        ind_df2['economy'] = ind_df2['economy_code'].map(APEC_fullname)
        
        # Save location for data and charts
        save_data = './data/industry_production/industry_interim1/{}/'.format(economy)

        if not os.path.isdir(save_data):
            os.makedirs(save_data)

        ind_df2.to_csv(save_data + economy + '_' + series + '.csv', index = False)

        fig, ax = plt.subplots()

        sns.set_theme(style = 'ticks')

        sns.lineplot(data = ind_df2, 
                        x = 'year',
                        y = 'value',
                        hue = 'series')
        
        ax.set(title = economy + ' ' + series,
            xlabel = 'year',
            ylabel = 'Proportion %',
            ylim = (0, ind_df2['value'].max() * 1.1))
        
        plt.legend(title = '')
        
        plt.tight_layout()
        plt.savefig(save_data + economy + '_' + series + '.png')
        plt.show()
        plt.close()

# High level results for all economies with default values
# for economy in wdi_df['economy_code'].unique():
#     for series in wdi_df['series_code'].unique():
#         ind_projection(economy = economy,
#                        series = series)
