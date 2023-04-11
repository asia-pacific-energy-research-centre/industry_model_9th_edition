# Set working directory to be the project folder
import os
import re

wanted_wd = 'industry_model_9th_edition'
os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

# execute config file
config_file = './config/config_apr2023.py'
with open(config_file) as infile:
    exec(infile.read())

# Steel data for WSA
production_files = './data/production_and_trade/'

prod_files = glob.glob(production_files + '*.xlsx')
steel_index = [idx for idx, s in enumerate(prod_files) if 'steel_wsa' in s]
cement_index = [idx for idx, s in enumerate(prod_files) if 'cement_usgs' in s]

# Load steel data 
steel_to_2021 = pd.read_excel(prod_files[steel_index[0]], header = 2, nrows = 125, index_col = 'Country')
steel_to_2022 = pd.read_excel(prod_files[steel_index[1]], header = 2, nrows = 125, index_col = 'Country')

# Join the two steel data sets
steel_df = pd.concat([steel_to_2021[[2017]], steel_to_2022], axis = 1).copy().reset_index(drop = False)

# Load the APEC steel economies
steel_economies = pd.read_csv('./data/config/wsa_countries.csv', header = None, index_col = 0)\
    .squeeze().to_dict()

# And subset the data so that only APEC steel economies remain
steel_df = steel_df[steel_df['Country'].isin(steel_economies.values())].copy().reset_index(drop = True)
steel_df['economy_code'] = steel_df['Country'].map({v: k for k, v in steel_economies.items()})
steel_df = steel_df[['economy_code', 2017, 2018, 2019, 2020, 2021, 2022]].sort_values('economy_code')

steel_df = steel_df.melt(id_vars = 'economy_code').rename(columns = {'variable': 'year'})

steel_df['production'] = 'Steel WSA'
steel_df['units'] = 'Thousand tonnes'

steel_df = steel_df[['economy_code', 'production', 'units', 'year', 'value']]

# Read in older steel production from 8th Outlook
steel8th = pd.read_excel('./data/production_and_trade/cement_steel_8th_production.xlsx', sheet_name = 'steel')
steel8th = steel8th.melt(id_vars = ['economy', 'item', 'unit']).rename(columns = {'variable': 'year',
                                                                                  'unit': 'units',
                                                                                  'economy': 'economy_code',
                                                                                  'item': 'production'}).dropna()

steel8th['production'] = 'Steel WSA'
steel8th['units'] = 'Thousand tonnes'

steel8th = steel8th[steel8th['year'] < 2017].copy().reset_index(drop = True)

steel_df = pd.concat([steel_df, steel8th]).sort_values(['economy_code', 'year']).copy().reset_index(drop = True)

# Save location for steel charts
steel_charts = './data/production_and_trade/production_steel/'

if not os.path.isdir(steel_charts):
    os.makedirs(steel_charts)

# Save steel dataframe
steel_df.to_csv(steel_charts + 'steel_wsa_cleaned.csv', index = False)

for economy in steel_df['economy_code'].unique():
    chart_df = steel_df[steel_df['economy_code'] == economy].copy()

    # Construct some plots
    fig, ax = plt.subplots()

    sns.set_theme(style = 'ticks')

    sns.lineplot(data = chart_df, 
                    x = 'year',
                    y = 'value',
                    hue = 'production')

    ax.set(title = economy,
           xlabel = 'Year',
           ylabel = 'Thousand tonnes',
           ylim = (0, chart_df['value'].max() * 1.1))

    plt.legend(title = '')

    plt.tight_layout()
    plt.savefig(steel_charts + economy + '_steel_prod.png')
    #plt.show()
    plt.close()

# Load cement data
cement_df = pd.read_excel(prod_files[cement_index[0]], header = 5, nrows = 160)\
    .rename(columns = {'Country or locality': 'economy'})
cement_df = cement_df[['economy', '2016', 2017, '2018', '2019', '2020']]

APEC_cement = ['Australiae', 'Canada', 'Chile', 'China', 'Hong Kong', 'Indonesia', 'Japan', 
               'Korea, Republic of', 'Malaysia', 'Mexico', 'New Zealande', 'Papua New Guineae', 
               'Peru', 'Philippines', 'Russia', 'Taiwan', 'Thailand', 'United States7', 'Vietnam']

cement_df = cement_df[cement_df['economy'].isin(APEC_cement)].copy()\
    .replace({'Australiae': 'Australia',
              'Hong Kong': 'Hong Kong, China',
              'Korea, Republic of': 'Korea',
              'New Zealande': 'New Zealand',
              'Papua New Guineae': 'Papua New Guinea',
              'Taiwan': 'Chinese Taipei',
              'United States7': 'United States',
              'Vietnam': 'Viet Nam'}).reset_index(drop = True)

cement_df.to_csv(production_files + 'cement_usgs_interim.csv', index = False)
cement_df = pd.read_csv(production_files + 'cement_usgs_interim.csv')

# Load the APEC cement economies
cement_economies = pd.read_csv('./data/config/cement_economies.csv', header = None, index_col = 0)\
    .squeeze().to_dict()

cement_df['economy_code'] = cement_df['economy'].map({v: k for k, v in cement_economies.items()})
cement_df = cement_df[['economy_code', 'economy', '2016', '2017', '2018', '2019', '2020']].sort_values('economy_code')
cement_df = cement_df.melt(id_vars = ['economy_code', 'economy']).rename(columns = {'variable': 'year'})

cement_df['production'] = 'Cement USGS'
cement_df['units'] = 'Thousand tonnes'

cement_df = cement_df[['economy_code', 'economy', 'production', 'units', 'year', 'value']]

# Read in older cement production from 8th Outlook
cement8th = pd.read_excel('./data/production_and_trade/cement_steel_8th_production.xlsx', sheet_name = 'cement')
cement8th = cement8th.melt(id_vars = ['economy', 'item', 'unit']).rename(columns = {'variable': 'year',
                                                                                  'unit': 'units',
                                                                                  'economy': 'economy_code',
                                                                                  'item': 'production'}).dropna()

cement8th['production'] = 'Cement USGS'
cement8th['units'] = 'Thousand tonnes'

cement8th = cement8th[cement8th['year'] < 2016].copy().reset_index(drop = True)

cement_df = pd.concat([cement_df, cement8th]).sort_values(['economy_code', 'year']).copy().reset_index(drop = True)

# Save location for steel charts
cement_charts = './data/production_and_trade/production_cement/'

if not os.path.isdir(cement_charts):
    os.makedirs(cement_charts)

# Save cement dataframe
cement_df.to_csv(cement_charts + 'cement_usgs_cleaned.csv', index = False)

for economy in cement_df['economy_code'].unique():
    chart_df = cement_df[cement_df['economy_code'] == economy].copy()

    # Construct some plots
    fig, ax = plt.subplots()

    sns.set_theme(style = 'ticks')

    sns.lineplot(data = chart_df, 
                    x = 'year',
                    y = 'value',
                    hue = 'production')

    ax.set(title = economy,
           xlabel = 'Year',
           ylabel = 'Thousand tonnes',
           ylim = (0, chart_df['value'].max() * 1.1))

    plt.legend(title = '')

    plt.tight_layout()
    plt.savefig(cement_charts + economy + '_cement_prod.png')
    #plt.show()
    plt.close()

