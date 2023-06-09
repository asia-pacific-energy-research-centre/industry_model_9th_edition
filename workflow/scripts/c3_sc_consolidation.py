# Cement projections using Machine Learning

# Set working directory to be the project folder
import os
import re

wanted_wd = 'industry_model_9th_edition'
os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

# execute config file
config_file = './config/config_apr2023.py'
with open(config_file) as infile:
    exec(infile.read())

# Grab APEC economies
gdp_df = pd.read_csv('./data/macro/APEC_GDP_data.csv')
APEC_economies = gdp_df['economy_code'].unique()

# Read in ML results: steel
combined_df = pd.DataFrame()

for economy in APEC_economies:
    filenames = glob.glob('./data/ml_steel/{}/ml_build/model_predictions*.csv'.format(economy))
    for i in filenames:
        temp_df = pd.read_csv(i)
        temp_df['economy_code'] = economy
        combined_df = pd.concat([combined_df, temp_df]).copy()

combined_df.to_csv('./data/ml_steel/ml_steel_all.csv', index = False)
