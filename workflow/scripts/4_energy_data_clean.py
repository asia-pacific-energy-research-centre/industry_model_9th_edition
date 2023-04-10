################### EGEDA data ####################

# Set working directory to the project folder
import os
import re

wanted_wd = 'industry_model_9th_edition'
os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

# execute config file
config_file = './config/config_apr2023.py'
with open(config_file) as infile:
    exec(infile.read())

# Read EGEDA
EGEDA_location = './data/EGEDA/model_df/'
EGEDA_files = glob.glob(EGEDA_location + '*.csv')

# Identify file that is just the reference scenario
EGEDA_ref = [i for i, s in enumerate(EGEDA_files) if '_ref_' in s][0]

# Read in reference data frame
EGEDA_df = pd.read_csv(EGEDA_files[EGEDA_ref])

# item_code variables
sectors = EGEDA_df['sectors'].unique()

# industrial code variables
industry_prefix = '14'
industry_cat = pd.Series(sectors).str.startswith(industry_prefix)

# Industry categories
industry = sectors[industry_cat]

EGEDA_ind = EGEDA_df[EGEDA_df['sectors'].isin(industry)].copy().reset_index(drop = True)

EGEDA_ind.to_csv('./data/EGEDA/model_df_industry.csv', index = False)