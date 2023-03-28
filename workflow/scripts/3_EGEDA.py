################### EGEDA data ####################

# Set working directory to the project folder
import os
import re

wanted_wd = 'industry_model_9th_edition'
os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

# Now run config file
execfile('./config/config_oct2022.py')

# Read EGEDA
EGEDA_location = './data/EGEDA/'
EGEDA_files = glob.glob(EGEDA_location + '*.csv')

# Which EGEDA dataset is most recent
file_dates = []

for file in EGEDA_files:
    date = datetime.strptime(file[-12:-4], '%d%m%Y')
    file_dates.append(date)

# Read in most recent data set
most_recent = file_dates.index(max(file_dates))

EGEDA_df = pd.read_csv(EGEDA_files[most_recent])

# item_code variables
items = EGEDA_df['item_code'].unique()

# industrial code variables
industry_prefix = '14'
industry_cat = pd.Series(items).str.startswith(industry_prefix)

# Industry categories
industry = items[industry_cat]

# product_code variables
product = EGEDA_df['product_code'].unique()
