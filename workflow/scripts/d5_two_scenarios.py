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
from d2_projection_adjust import scenario_adj, scenario_adj_ne

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
nonenergy_refine2 = pd.read_csv('./data/non_energy/3_nonenergy_refine2/refined_nonenergy_all.csv')

##########################################################################################
# Australia

##########################################################################################
# Canada
# Mining
scenario_adj(economy = '03_CDA', sub1sectors = ind1[0], sub2sectors = 'x', 
             increment = 0.02, start_year = 2024, end_year = 2040, data = industry_refine2)

# Steel: Material efficiency
scenario_adj(economy = '03_CDA', sub1sectors = ind1[2], sub2sectors = ind2[0], 
             increment = -0.004, start_year = 2023, end_year = 2100, data = industry_refine2) 

# Chemicals: Material efficiency
scenario_adj(economy = '03_CDA', sub1sectors = ind1[2], sub2sectors = ind2[1], 
             increment = -0.003, start_year = 2023, end_year = 2100, data = industry_refine2)

# Non-ferrous metals
scenario_adj(economy = '03_CDA', sub1sectors = ind1[2], sub2sectors = ind2[2], 
             increment = 0.025, start_year = 2024, end_year = 2040, data = industry_refine2)

# Cement (non-metallic minerals): Material efficiency
scenario_adj(economy = '03_CDA', sub1sectors = ind1[2], sub2sectors = ind2[3], 
             increment = -0.004, start_year = 2023, end_year = 2100, data = industry_refine2)

# Non-energy
scenario_adj_ne(economy = '03_CDA', 
                increment = -0.003, start_year = 2023, end_year = 2100, data = nonenergy_refine2)

##############################################################################################
# Japan
# Mining
scenario_adj(economy = '08_JPN', sub1sectors = ind1[0], sub2sectors = 'x', 
             increment = 0.02, start_year = 2023, end_year = 2040, data = industry_refine2)

# Steel: Material efficiency
scenario_adj(economy = '08_JPN', sub1sectors = ind1[2], sub2sectors = ind2[0], 
             increment = -0.0025, start_year = 2023, end_year = 2100, data = industry_refine2)

# Chemicals: Material efficiency
scenario_adj(economy = '08_JPN', sub1sectors = ind1[2], sub2sectors = ind2[1], 
             increment = -0.004, start_year = 2023, end_year = 2100, data = industry_refine2)

# Non-ferrous metals
scenario_adj(economy = '08_JPN', sub1sectors = ind1[2], sub2sectors = ind2[2], 
             increment = 0.02, start_year = 2023, end_year = 2040, data = industry_refine2)

# Cement (non-metallic minerals): Material efficiency
scenario_adj(economy = '08_JPN', sub1sectors = ind1[2], sub2sectors = ind2[3], 
             increment = -0.0025, start_year = 2023, end_year = 2100, data = industry_refine2)

# Non-energy
scenario_adj_ne(economy = '08_JPN', 
                increment = -0.0025, start_year = 2023, end_year = 2100, data = nonenergy_refine2)

##########################################################################################
# Thailand
# Mining
scenario_adj(economy = '19_THA', sub1sectors = ind1[0], sub2sectors = 'x', 
             increment = 0.02, start_year = 2023, end_year = 2040, data = industry_refine2)

# Steel: Material efficiency
scenario_adj(economy = '19_THA', sub1sectors = ind1[2], sub2sectors = ind2[0], 
             increment = -0.0025, start_year = 2023, end_year = 2100, data = industry_refine2)

# Chemicals: Material efficiency
scenario_adj(economy = '19_THA', sub1sectors = ind1[2], sub2sectors = ind2[1], 
             increment = -0.0025, start_year = 2023, end_year = 2100, data = industry_refine2)

# Non-ferrous metals
scenario_adj(economy = '19_THA', sub1sectors = ind1[2], sub2sectors = ind2[2], 
             increment = 0.02, start_year = 2023, end_year = 2040, data = industry_refine2)

# Cement (non-metallic minerals): Material efficiency
scenario_adj(economy = '19_THA', sub1sectors = ind1[2], sub2sectors = ind2[3], 
             increment = -0.0025, start_year = 2023, end_year = 2100, data = industry_refine2)

# Non-energy
scenario_adj_ne(economy = '19_THA', 
                increment = -0.0025, start_year = 2023, end_year = 2100, data = nonenergy_refine2)


##########################################################################################
# United States
# Mining
scenario_adj(economy = '20_USA', sub1sectors = ind1[0], sub2sectors = 'x', 
             increment = 0.02, start_year = 2024, end_year = 2040, data = industry_refine2)

# Steel: Material efficiency
scenario_adj(economy = '20_USA', sub1sectors = ind1[2], sub2sectors = ind2[0], 
             increment = -0.004, start_year = 2023, end_year = 2100, data = industry_refine2) 

# Chemicals: Material efficiency
scenario_adj(economy = '20_USA', sub1sectors = ind1[2], sub2sectors = ind2[1], 
             increment = -0.003, start_year = 2023, end_year = 2100, data = industry_refine2)

# Non-ferrous metals
scenario_adj(economy = '20_USA', sub1sectors = ind1[2], sub2sectors = ind2[2], 
             increment = 0.025, start_year = 2024, end_year = 2040, data = industry_refine2)

# Cement (non-metallic minerals): Material efficiency
scenario_adj(economy = '20_USA', sub1sectors = ind1[2], sub2sectors = ind2[3], 
             increment = -0.004, start_year = 2023, end_year = 2100, data = industry_refine2)

# Non-energy
scenario_adj_ne(economy = '20_USA', 
                increment = -0.003, start_year = 2023, end_year = 2100, data = nonenergy_refine2)


##############################################################################################################

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

## NON-ENERGY
# Consolidate new results
traj_overwrite_df = pd.DataFrame()

for economy in list(APEC_economies.keys())[:-7]:
    filenames = glob.glob('./data/non_energy/4_nonenergy_scenarios/{}/*.csv'.format(economy))
    for i in filenames:
        temp_df = pd.read_csv(i)
        traj_overwrite_df = pd.concat([traj_overwrite_df, temp_df]).copy()

traj_overwrite_df.to_csv('./data/non_energy/4_nonenergy_scenarios/nonenergy_tgt_adj.csv', index = False)

# Now save an entire data frame with the selected results from above replacing the results from before

nonenergy_ref = nonenergy_refine2.copy()
nonenergy_ref['scenario'] = 'reference'

nonenergy_tgt = nonenergy_refine2.copy().merge(traj_overwrite_df, how = 'left',
                                                on = ['economy', 'economy_code', 'series', 
                                                      'year', 'units', 'sectors', 'sub1sectors'])

nonenergy_tgt['value'] = (nonenergy_tgt['value_x']).where(nonenergy_tgt['value_y'].isna(), nonenergy_tgt['value_y'])
nonenergy_tgt['scenario'] = 'target'

nonenergy_tgt = nonenergy_tgt.copy().drop(columns = ['value_x', 'value_y'])

nonenergy_scenarios = pd.concat([nonenergy_ref, nonenergy_tgt]).copy().reset_index(drop = True)

nonenergy_scenarios.to_csv('./data/non_energy/4_nonenergy_scenarios/nonenergy_production_' + timestamp + '.csv', index = False)