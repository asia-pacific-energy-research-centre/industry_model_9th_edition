# Consolidated grab of steel and cement baseline production estimates

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
        temp_df['production'] = 'Steel production'
        temp_df['units'] = 'Thousand tonnes' #WSA source
        combined_df = pd.concat([combined_df, temp_df]).copy()

combined_df.to_csv('./data/ml_steel/ml_steel_all.csv', index = False)

# Choice of appropriate ML models for each of the economies
steel_model_dict = pd.read_csv('./data/config/ml_baseline_steel.csv', index_col = 0).squeeze().to_dict()

interim_steel_df = pd.DataFrame()

for economy in APEC_economies:
    temp_steel = combined_df[(combined_df['economy_code'] == economy) &
                             (combined_df['model'].isin(['Historic steel production', 
                                                         steel_model_dict[economy]]))]\
                                                            .copy().reset_index(drop = True)
    
    interim_steel_df = pd.concat([interim_steel_df, temp_steel]).copy().reset_index(drop = True)

# Save steel df with selected baseline model results for production 
interim_steel_df.to_csv('./data/ml_steel/ml_steel_selected.csv', index = False)

# Read in ML results: cement
combined_df = pd.DataFrame()

for economy in APEC_economies:
    filenames = glob.glob('./data/ml_cement/{}/ml_build/model_predictions*.csv'.format(economy))
    for i in filenames:
        temp_df = pd.read_csv(i)
        temp_df['economy_code'] = economy
        temp_df['production'] = 'Cement production'
        temp_df['units'] = 'Thousand tonnes' #USGS source
        combined_df = pd.concat([combined_df, temp_df]).copy()

combined_df.to_csv('./data/ml_cement/ml_cement_all.csv', index = False)

# Choice of appropriate ML models for each of the economies
cement_model_dict = pd.read_csv('./data/config/ml_baseline_cement.csv', index_col = 0).squeeze().to_dict()

interim_cement_df = pd.DataFrame()

for economy in APEC_economies:
    temp_cement = combined_df[(combined_df['economy_code'] == economy) &
                             (combined_df['model'].isin(['Historic cement production', 
                                                         cement_model_dict[economy]]))]\
                                                            .copy().reset_index(drop = True)
    
    interim_cement_df = pd.concat([interim_cement_df, temp_cement]).copy().reset_index(drop = True)

interim_cement_df.to_csv('./data/ml_cement/ml_cement_selected.csv', index = False)