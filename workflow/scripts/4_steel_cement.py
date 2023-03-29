# Set working directory to be the project folder
import os
import re

wanted_wd = 'industry_model_9th_edition'
os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

# Now run config file
execfile('./config/config_oct2022.py')

# Steel data for WSA
production_files = './data/production_and_trade/'

prod_files = glob.glob(production_files + '*.xlsx')
steel_index = [idx for idx, s in enumerate(prod_files) if 'steel_wsa' in s]
cement_index = [idx for idx, s in enumerate(prod_files) if 'cement' in s]

# Load steel data 
steel_to_2021 = pd.read_excel(prod_files[steel_index[0]], header = 2, nrows = 125, index_col = 'Country')
steel_to_2022 = pd.read_excel(prod_files[steel_index[1]], header = 2, nrows = 125, index_col = 'Country')

# Join the two steel data sets
steel_df = pd.concat([steel_to_2021[[2017]], steel_to_2022], axis = 1).copy().reset_index(drop = False)

# Load the APEC steel economies
steel_economies = pd.read_csv('./data/production_and_trade/wsa_countries.csv', header = None, index_col = 0)\
    .squeeze().to_dict()

# And subset the data so that only APEC steel economies remain
steel_df = steel_df[steel_df['Country'].isin(steel_economies.values())].copy().reset_index(drop = True)
steel_df['economy_code'] = steel_df['Country'].map({v: k for k, v in steel_economies.items()})
steel_df = steel_df[['economy_code', 2017, 2018, 2019, 2020, 2021, 2022]].sort_values('economy_code')

steel_df = steel_df.melt(id_vars = 'economy_code').rename(columns = {'variable': 'year'})

steel_df['production'] = 'Steel WSA'
steel_df['units'] = 'Thousand tonnes'

steel_df = steel_df[['economy_code', 'production', 'units', 'year', 'value']]

# Save steel dataframe
steel_df.to_csv(production_files + 'steel_wsa_cleaned.csv', index = False)

# Save location for stee; charts
steel_charts = './results/steel/'

if not os.path.isdir(steel_charts):
    os.makedirs(steel_charts)

# Steel production charts
for economy in steel_economies.keys():
    chart_df = steel_df[steel_df['economy_code'] == economy].reset_index(drop = True)

    fig, ax = plt.subplots()
    
    sns.set_theme(style = 'ticks')

    # Capital stock
    sns.lineplot(ax = ax,
                data = chart_df,
                x = 'year',
                y = 'value')
    
    ax.set(title = economy + ' steel production', 
                xlabel = 'Year', 
                ylabel = 'Steel production (thousand tonnes)')

    plt.tight_layout()
    fig.savefig(steel_charts + economy + '_steelprod.png')
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

cement_df.to_csv(production_files + 'cement_usgs_cleaned.csv', index = False)
cement_df = pd.read_csv(production_files + 'cement_usgs_cleaned.csv')

# Load the APEC cement economies
cement_economies = pd.read_csv('./data/production_and_trade/cement_economies.csv', header = None, index_col = 0)\
    .squeeze().to_dict()

cement_df['economy_code'] = cement_df['economy'].map({v: k for k, v in cement_economies.items()})
cement_df = cement_df[['economy_code', 'economy', '2016', '2017', '2018', '2019', '2020']].sort_values('economy_code')
cement_df = cement_df.melt(id_vars = ['economy_code', 'economy']).rename(columns = {'variable': 'year'})

cement_df['production'] = 'Cement USGS'
cement_df['units'] = 'Thousand tonnes'

cement_df = cement_df[['economy_code', 'economy', 'production', 'units', 'year', 'value']]

# Save cement dataframe
cement_df.to_csv(production_files + 'cement_usgs_cleaned.csv', index = False)

APEC_cement = list(cement_df['economy_code'].unique())

# Save location for cement charts
cement_charts = './results/cement/'

if not os.path.isdir(cement_charts):
    os.makedirs(cement_charts)

# Cement charts
for economy in APEC_cement:
    chart_df = cement_df[cement_df['economy_code'] == economy].reset_index(drop = True)

    fig, ax = plt.subplots()
    
    sns.set_theme(style = 'ticks')

    # Capital stock
    sns.lineplot(ax = ax,
                data = chart_df,
                x = 'year',
                y = 'value')
    
    ax.set(title = economy + ' cement production', 
                xlabel = 'Year', 
                ylabel = 'Cement production (thousand tonnes)')

    plt.tight_layout()
    fig.savefig(cement_charts + economy + '_cementprod.png')
    plt.close()