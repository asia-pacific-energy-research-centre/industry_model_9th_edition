# Alter trajectory for chosen subsectors for each economy 
# This adjustment is only for subsectors where adjustment is deemed necessary (qualitative determination)

# Set working directory to be the project folder 
import os
import re

wanted_wd = 'industry_model_9th_edition'
os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

# execute config file
config_file = './config/config_apr2023.py'
with open(config_file) as infile:
    exec(infile.read())

# Grab functions from the previous script
from d2_projection_adjust import industry_adj

# Define years list tp adjust later 
years = [i for i in range(1980, 2101, 1)]

# Grab APEC economies
APEC_economies = pd.read_csv('./data/config/APEC_economies.csv', index_col = 0).squeeze().to_dict()

# The interim modelled production estimates are located here (pre adjustment and refinement)
# Interim industry projections
industry_interim = pd.read_csv('./data/industry_production/industry_projections/interim_all_sectors.csv')


industry_adj(economy = '10_MAS',
             adjust = {},  
             sub1sectors = '14_03_manufacturing', 
             sub2sectors = '14_03_01_iron_and_steel',
             data = industry_interim) 

industry_adj(economy = '10_MAS', adjust = {2025: 1.15, 2029: 1.25}, data = industry_interim)


# Consolidate new results
traj_overwrite_df = pd.DataFrame()

for economy in list(APEC_economies.keys())[:-7]:
    filenames = glob.glob('./data/industry_production/industry_refine1/{}/*.csv'.format(economy))
    for i in filenames:
        temp_df = pd.read_csv(i)
        traj_overwrite_df = pd.concat([traj_overwrite_df, temp_df]).copy()

traj_overwrite_df.to_csv('./data/industry_production/industry_refine1/industry_refine1_all.csv', index = False)

####################################################################


