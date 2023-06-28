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
from d2_projection_adjust import scenario_adj

# Define years list tp adjust later 
years = [i for i in range(1980, 2101, 1)]

# Grab APEC economies
APEC_economies = pd.read_csv('./data/config/APEC_economies.csv', index_col = 0).squeeze().to_dict()

# Energy industry subsectors
industry_sectors = pd.read_csv('./data/EGEDA/industry_egeda.csv', header = None)\
    .squeeze().to_dict()

ind1 = list(industry_sectors.values())[:3]
ind2 = list(industry_sectors.values())[3:]

# The interim modelled production estimates are located here (after adjustment and refinement)
# Interim industry projections
industry_refine2 = pd.read_csv('./data/industry_production/5_industry_refine2/refined_industry_all.csv')

# Australia


# Japan
# Mining
scenario_adj(economy = '08_JPN', sub1sectors = ind1[0], sub2sectors = 'x', 
             increment = 0.01, start_year = 2023, end_year = 2040, data = industry_refine2)

# Non-ferrous metals
scenario_adj(economy = '08_JPN', sub1sectors = ind1[2], sub2sectors = ind2[2], 
             increment = 0.01, start_year = 2023, end_year = 2040, data = industry_refine2)

# Consolidate new results
traj_overwrite_df = pd.DataFrame()

for economy in list(APEC_economies.keys())[:-7]:
    filenames = glob.glob('./data/industry_production/6_industry_scenarios/{}/*.csv'.format(economy))
    for i in filenames:
        temp_df = pd.read_csv(i)
        traj_overwrite_df = pd.concat([traj_overwrite_df, temp_df]).copy()

traj_overwrite_df.to_csv('./data/industry_production/6_industry_scenarios/industry_tgt_adj.csv', index = False)

# Now save an entire data frame with the selected results from above replacing the results from before

industry_ref = industry_refine2.copy()
industry_ref['scenario'] = 'reference'

industry_tgt = industry_refine2.copy().merge(traj_overwrite_df, how = 'left',
                                                on = ['economy', 'economy_code', 'series', 
                                                      'year', 'units', 'sub1sectors', 'sub2sectors'])

industry_tgt['value'] = (industry_tgt['value_x']).where(industry_tgt['value_y'].isna(), industry_tgt['value_y'])
industry_tgt['scenario'] = 'target'

industry_tgt = industry_tgt.copy().drop(columns = ['value_x', 'value_y'])

industry_scenarios = pd.concat([industry_ref, industry_tgt]).copy().reset_index(drop = True)

industry_scenarios.to_csv('./data/industry_production/6_industry_scenarios/industry_production_' + timestamp + '.csv', index = False) 


