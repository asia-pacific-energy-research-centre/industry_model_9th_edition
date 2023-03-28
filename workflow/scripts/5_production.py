# Set working directory to be the project folder
import os
import re

wanted_wd = 'industry_model_9th_edition'
os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

# Now run config file
execfile('./config/config_oct2022.py')

# APEC economies
APEC_econcode = pd.read_csv('./data/config/APEC_economies.csv', header = 0, index_col = 0)\
    .squeeze().to_dict()

# Industry sectprs
industry_sectors = pd.read_csv('./data/EGEDA/industry_egeda.csv', header = None)\
    .squeeze().to_dict()

# GDP and population data
macro_apec = pd.read_csv('./data/macro/combined_GDP_estimate.csv')