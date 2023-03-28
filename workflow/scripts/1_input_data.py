# First, set high level project space working directory 
import os
import re

wanted_wd = 'industry_model_9th_edition'

os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

# Run config file
execfile('./config/config_oct2022.py')

# CPB Netherlands Bureau for Economic Policy Analysis 
# CPB World Trade Monitor Excel workbook updated monthly

# October 2022 (data to August 2022) xlsx workbook location
# THIS URL CAN BE UPDATED EVERY MONTH TO REBUILD THE DATAFRAMES WITH MORE UP TO DATE DATA
CPB_WTM_URL = 'https://www.cpb.nl/sites/default/files/omnidownload/CPB-World-Trade-Monitor-December-2022.xlsx'

# Save the excel file
resp = requests.get(CPB_WTM_URL)
with open('./data/production_and_trade/source_download/CPB-World-Trade-Monitor-December-2022.xlsx', 'wb') as output:
    output.write(resp.content)

# Grab sheet names (trade_out and inpro_out)
sheet_names_cpb = pd.ExcelFile(CPB_WTM_URL).sheet_names

# Grab series' identifiers from the excel workbook to construct pandas dataframes
series_dict = {}

# squeeze turns a dataframe into a series; beginning at the second value removes 'nan'
for name in sheet_names_cpb:
    series_dict[name] = pd.read_excel(CPB_WTM_URL, 
                                      sheet_name = name,
                                      header = None,
                                      usecols = 'C').squeeze().unique()[1:]

# Merchandise world trade volumes, seasonally adjusted
wt_volumes = series_dict[sheet_names_cpb[0]][:29]
# Merchandise world trade prices / unit values in USD
wt_prices = series_dict[sheet_names_cpb[0]][29:]

# Import weighted industrial production volume, excluding construction, seasonally adjusted
ind_prod_mweighted = series_dict[sheet_names_cpb[1]][:14]
# Production weighted industrial production volume, excluding construction, seasonally adjusted
ind_prod_pweighted = series_dict[sheet_names_cpb[1]][14:]

# Grab dates
date_grab = pd.read_excel(CPB_WTM_URL, 
                          sheet_name = sheet_names_cpb[0],
                          header = None,
                          nrows = 4)

# Date of workbook update (create string)
update_date = datetime.strptime(date_grab.iloc[3,1], '%d %B %Y  %H:%M:%S').date()
month_year_cpb = update_date.strftime('%B_%Y')

# Dates (unparsed) as pandas series
wtm_dates = date_grab.iloc[3, 5:]

# Empty columns to not load
cols2skip = [0, 4]
cols = [i for i in range(len(wtm_dates) + 5) if i not in cols2skip]

cpb_dfs = {}

for name in sheet_names_cpb:
    cpb_dfs[name] = pd.read_excel(CPB_WTM_URL, 
                                  sheet_name = name, 
                                  header = 3,
                                  usecols = cols)

wt_df = cpb_dfs[sheet_names_cpb[0]].copy()
inpro_df = cpb_dfs[sheet_names_cpb[1]].copy()

# Change column headings of wt_df
wt_df.rename(columns = {'Unnamed: 2': 'series_code',
                        'Unnamed: 3': 'values_2010',
                        inpro_df.columns[0]: 'series'}, 
                        inplace = True)

# Change column headings of inpro_df            
inpro_df.rename(columns = {'Unnamed: 2': 'series_code',
                           'Unnamed: 3': 'weights_2010',
                           inpro_df.columns[0]: 'series'}, 
                           inplace = True)

# Parse date headers by making the first three non-date columns part of the index
wt_df = wt_df.set_index(['series', 'series_code', 'values_2010'])
inpro_df = inpro_df.set_index(['series', 'series_code', 'weights_2010'])

wt_df.columns = pd.to_datetime(wt_df.columns, format = '%Ym%m')
inpro_df.columns = pd.to_datetime(inpro_df.columns, format = '%Ym%m')

# World trade dataframe
wt_df = wt_df.copy().reset_index()

volumes = wt_df[wt_df['series_code'].isin(wt_volumes)].reset_index(drop = True)
volumes['type'] = 'volumes'
prices = wt_df[wt_df['series_code'].isin(wt_prices)].reset_index(drop = True)
prices['type'] = 'prices'

wt_df = pd.concat([volumes, prices]).reset_index(drop = True)

# Strip spaces
wt_df[['series']] = wt_df[['series']].apply(lambda x: x.str.strip())

# Rearrange columns
cols = wt_df.columns.to_list()
rearrange_cols = cols[:3] + cols[-1:] + cols[3:-1]
wt_df = wt_df[rearrange_cols].copy().reset_index(drop = True)

# Create industrial production dataframes (import weighted and production weighted)

inpro_df = inpro_df.reset_index()

mweight_df = inpro_df[inpro_df['series_code'].isin(ind_prod_mweighted)].reset_index(drop = True)
mweight_df.loc[mweight_df['series'] == 'World', 'weights_2010'] = 1
mweight_df['weight'] = 'imports'

pweight_df = inpro_df[inpro_df['series_code'].isin(ind_prod_pweighted)].reset_index(drop = True)
pweight_df.loc[pweight_df['series'] == 'World', 'weights_2010'] = 1
pweight_df['weight'] = 'production'

inpro_df = pd.concat([mweight_df, pweight_df]).reset_index(drop = True)

# Strip spaces
inpro_df[['series']] = inpro_df[['series']].apply(lambda x: x.str.strip())

# Rearrange columns
cols = inpro_df.columns.tolist()
rearrange_cols = cols[:3] + cols[-1:] + cols[3:-1]
inpro_df = inpro_df[rearrange_cols].copy().reset_index(drop = True)

# Add long dscription for series
long_series = pd.read_csv('./data/config/cpb_series.csv', header = None, index_col = 0).squeeze().to_dict()

wt_df['series_long'] = wt_df['series_code'].map(long_series)
inpro_df['series_long'] = inpro_df['series_code'].map(long_series)

# Long dataframes
wt_longdf = wt_df.melt(id_vars = ['series', 'series_code', 'series_long', 'values_2010', 'type'], 
                       var_name = 'date', 
                       value_name = 'index_value')

inpro_longdf = inpro_df.melt(id_vars = ['series', 'series_code', 'series_long', 'weights_2010', 'weight'], 
                             var_name = 'date', 
                             value_name = 'index_value')

# Save date frames
save_directory = './data/production_and_trade/'

if not os.path.isdir(save_directory):
    os.makedirs(save_directory)

# Save long dataframes
wt_longdf.to_csv(save_directory + 'cpb_world_trade_' + month_year_cpb + '_long.csv', index = False)
inpro_longdf.to_csv(save_directory + 'cpb_industrial_production_' + month_year_cpb + '_long.csv', index = False)
