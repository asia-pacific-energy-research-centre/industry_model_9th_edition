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

# Save location for stee; charts
steel_charts = './results/steel/'

if not os.path.isdir(steel_charts):
    os.makedirs(steel_charts)

# Production charts
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
                ylabel = 'Steel production (tonnes)')

    plt.tight_layout()
    fig.savefig(steel_charts + economy + '_steelprod.png')
    plt.close()