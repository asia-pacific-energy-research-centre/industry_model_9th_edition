# Set working directory to be the project folder
import os
import re

wanted_wd = 'industry_model_9th_edition'
os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

# Now run config file
execfile('./config/config_oct2022.py')

# Read in CPB data
input_data_folder = './data/production_and_trade/'

production_files = glob.glob(input_data_folder + '*.csv')

# Determine index of industrial_production file
prod_index = [idx for idx, s in enumerate(production_files) if 'industrial_production' in s][0]
wt_index = [idx for idx, s in enumerate(production_files) if 'world_trade' in s][0]

cpb_prod_df = pd.read_csv(production_files[prod_index], parse_dates = ['date'], infer_datetime_format = True)
cpb_wt_df = pd.read_csv(production_files[wt_index], parse_dates = ['date'], infer_datetime_format = True)

# Read in series dictionary
long_series = pd.read_csv('./data/config/cpb_series.csv', header = None, index_col = 0)\
    .squeeze().to_dict()

# Production and world trade series
cpb_prod_series = cpb_prod_df['series_code'].unique()
cpb_wt_series = cpb_wt_df['series_code'].unique()

# Save location for production and trade charts
production_charts = './results/production/'
trade_charts = './results/trade/'

if not os.path.isdir(production_charts):
    os.makedirs(production_charts)

if not os.path.isdir(trade_charts):
    os.makedirs(trade_charts)

years = mdates.YearLocator()
date_format = mdates.DateFormatter('%Y')

# Production charts
for series in cpb_prod_series:
    chart_df = cpb_prod_df[cpb_prod_df['series_code'] == series].reset_index(drop = True)

    fig, ax = plt.subplots()
    x = chart_df['date']
    y = chart_df['index_value']

    ax.plot(x, y)

    ax.set_ylim([0, max(y) * 1.1])

    ax.xaxis.set_major_formatter(date_format)
    title = ax.set_title('\n'.join(wrap(long_series[series], 60)))

    fig.tight_layout()

    plt.savefig(production_charts + series + '.png')
    plt.close()

# Trade charts
for series in cpb_wt_series:
    chart_df = cpb_wt_df[cpb_wt_df['series_code'] == series].reset_index(drop = True)

    fig, ax = plt.subplots()
    x = chart_df['date']
    y = chart_df['index_value']

    ax.plot(x, y)

    ax.set_ylim([0, max(y) * 1.1])

    ax.xaxis.set_major_formatter(date_format)
    title = ax.set_title('\n'.join(wrap(long_series[series], 60)))

    fig.tight_layout()

    plt.savefig(trade_charts + series + '.png')
    plt.close()