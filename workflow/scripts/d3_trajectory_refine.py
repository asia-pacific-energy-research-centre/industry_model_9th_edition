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
from d2_projection_adjust import industry_traj

# Define years list tp adjust later 
years = [i for i in range(1980, 2101, 1)]

# Grab APEC economies
APEC_economies = pd.read_csv('./data/config/APEC_economies.csv', index_col = 0).squeeze().to_dict()

# Energy industry subsectors
industry_sectors = pd.read_csv('./data/EGEDA/industry_egeda.csv', header = None)\
    .squeeze().to_dict()

ind1 = list(industry_sectors.values())[:3]
ind2 = list(industry_sectors.values())[3:]

# The interim modelled production estimates are located here (pre adjustment and refinement)
# Interim industry projections
industry_interim = pd.read_csv('./data/industry_production/3_industry_projections/interim_all_sectors.csv')

###################################################################################################
# Alter trajectory where necesary

#################################### Australia #################################################################
# Mining
industry_traj(economy = '01_AUS', sub1sectors = ind1[0], sub2sectors = 'x', proj_start_year = 2070,
              shape = 'decrease', magnitude = 1.3, apex_mag = 1.5, apex_loc = 20, data = industry_interim)

# Construction
industry_traj(economy = '01_AUS', sub1sectors = ind1[1], sub2sectors = 'x', proj_start_year = 2070,
              shape = 'decrease', magnitude = 1.3, apex_mag = 1.5, apex_loc = 20, data = industry_interim)

# Steel
industry_traj(economy = '01_AUS', sub1sectors = ind1[2], sub2sectors = ind2[0], proj_start_year = 2021,
              shape = 'decrease', magnitude = 1.3, apex_mag = 1.5, apex_loc = 20, data = industry_interim)

# Chemicals
industry_traj(economy = '01_AUS', sub1sectors = ind1[2], sub2sectors = ind2[1], proj_start_year = 2021,
              shape = 'increase', magnitude = 1.1, apex_mag = 1.5, apex_loc = 20, data = industry_interim)

# Non-ferrous metals
industry_traj(economy = '01_AUS', sub1sectors = ind1[2], sub2sectors = ind2[2], proj_start_year = 2021,
              shape = 'bottom', magnitude = 1.4, apex_mag = 0.9, apex_loc = 40, data = industry_interim)

# Non-metallic minerals
industry_traj(economy = '01_AUS', sub1sectors = ind1[2], sub2sectors = ind2[3], proj_start_year = 2021,
              shape = 'bottom', magnitude = 1.4, apex_mag = 0.9, apex_loc = 40, data = industry_interim)

# Transportation equipment
industry_traj(economy = '01_AUS', sub1sectors = ind1[2], sub2sectors = ind2[4], proj_start_year = 2021,
              shape = 'bottom', magnitude = 1.4, apex_mag = 0.9, apex_loc = 40, data = industry_interim)

# Machinery
industry_traj(economy = '01_AUS', sub1sectors = ind1[2], sub2sectors = ind2[5], proj_start_year = 2021,
              shape = 'bottom', magnitude = 1.4, apex_mag = 0.9, apex_loc = 40, data = industry_interim)

# Food and beverages
industry_traj(economy = '01_AUS', sub1sectors = ind1[2], sub2sectors = ind2[6], proj_start_year = 2021,
              shape = 'bottom', magnitude = 1.4, apex_mag = 0.9, apex_loc = 40, data = industry_interim)

# Pulp and paper
industry_traj(economy = '01_AUS', sub1sectors = ind1[2], sub2sectors = ind2[7], proj_start_year = 2021,
              shape = 'bottom', magnitude = 1.4, apex_mag = 0.9, apex_loc = 40, data = industry_interim)

# Wood and wood products
industry_traj(economy = '01_AUS', sub1sectors = ind1[2], sub2sectors = ind2[8], proj_start_year = 2021,
              shape = 'bottom', magnitude = 1.4, apex_mag = 0.9, apex_loc = 40, data = industry_interim)

# Textiles
industry_traj(economy = '01_AUS', sub1sectors = ind1[2], sub2sectors = ind2[9], proj_start_year = 2021,
              shape = 'bottom', magnitude = 1.4, apex_mag = 0.9, apex_loc = 40, data = industry_interim)

# Non-specified
industry_traj(economy = '01_AUS', sub1sectors = ind1[2], sub2sectors = ind2[10], proj_start_year = 2021,
              shape = 'bottom', magnitude = 1.4, apex_mag = 0.9, apex_loc = 40, data = industry_interim)


# Brunei
# Canada
# Chile
# China
# HKC
# Indonesia

#################################### Japan #################################################################
# Non-ferrous metals
industry_traj(economy = '08_JPN', sub1sectors = ind1[2], sub2sectors = ind2[2], proj_start_year = 2021,
              shape = 'constant', magnitude = 1.2, apex_mag = 0.9, apex_loc = 40, data = industry_interim)

# Non-metallic minerals
industry_traj(economy = '08_JPN', sub1sectors = ind1[2], sub2sectors = ind2[3], proj_start_year = 2021,
              shape = 'decrease', magnitude = 0.9, apex_mag = 0.9, apex_loc = 40, data = industry_interim)


# Korea
# Malaysia
# Mexico
# New Zealand
# PNG
# Peru
# Philippines
# Russia
# Singapore
# Chinese Taipei


############################ Thailand ###########################################################
# Steel
industry_traj(economy = '19_THA', sub1sectors = ind1[2], sub2sectors = ind2[0], proj_start_year = 2021,
              shape = 'decrease', magnitude = 3, apex_mag = 1.5, apex_loc = 20, data = industry_interim)

# Non-metallic minerals
industry_traj(economy = '19_THA', sub1sectors = ind1[2], sub2sectors = ind2[3], proj_start_year = 2021,
              shape = 'bottom', magnitude = 1.4, apex_mag = 0.9, apex_loc = 40, data = industry_interim)

# Textiles
industry_traj(economy = '19_THA', sub1sectors = ind1[2], sub2sectors = ind2[9], proj_start_year = 2021,
              shape = 'decrease', magnitude = 2.3, apex_mag = 0.8, apex_loc = 50, data = industry_interim)

# Non-specified
industry_traj(economy = '19_THA', sub1sectors = ind1[2], sub2sectors = ind2[10], proj_start_year = 2021,
              shape = 'decrease', magnitude = 2.5, apex_mag = 0.9, apex_loc = 40, data = industry_interim)


############################ USA ##############################################################
# Mining
industry_traj(economy = '20_USA', sub1sectors = ind1[0], sub2sectors = 'x', proj_start_year = 2021,
              shape = 'increase', magnitude = 3.1, apex_mag = 0.8, apex_loc = 20, data = industry_interim)

# Construction
industry_traj(economy = '20_USA', sub1sectors = ind1[1], sub2sectors = 'x', proj_start_year = 2021,
              shape = 'decrease', magnitude = 1.7, apex_mag = 1.5, apex_loc = 20, data = industry_interim)

# Steel
industry_traj(economy = '20_USA', sub1sectors = ind1[2], sub2sectors = ind2[0], proj_start_year = 2021,
              shape = 'decrease', magnitude = 1.5, apex_mag = 1.5, apex_loc = 20, data = industry_interim)

# Non-ferrous metals
industry_traj(economy = '20_USA', sub1sectors = ind1[2], sub2sectors = ind2[2], proj_start_year = 2021,
              shape = 'peak', magnitude = 2.2, apex_mag = 0.9, apex_loc = 60, data = industry_interim)

# Transportation equipment
industry_traj(economy = '20_USA', sub1sectors = ind1[2], sub2sectors = ind2[4], proj_start_year = 2030,
              shape = 'decrease', magnitude = 1.7, apex_mag = 0.9, apex_loc = 40, data = industry_interim)

# Machinery
industry_traj(economy = '20_USA', sub1sectors = ind1[2], sub2sectors = ind2[5], proj_start_year = 2030,
              shape = 'decrease', magnitude = 1.7, apex_mag = 0.9, apex_loc = 40, data = industry_interim)

# Food and beverages
industry_traj(economy = '20_USA', sub1sectors = ind1[2], sub2sectors = ind2[6], proj_start_year = 2021,
              shape = 'bottom', magnitude = 1.4, apex_mag = 0.9, apex_loc = 40, data = industry_interim)

# Pulp and paper
industry_traj(economy = '20_USA', sub1sectors = ind1[2], sub2sectors = ind2[7], proj_start_year = 2021,
              shape = 'decrease', magnitude = 1.7, apex_mag = 1.1, apex_loc = 40, data = industry_interim)

# Wood and wood products
industry_traj(economy = '20_USA', sub1sectors = ind1[2], sub2sectors = ind2[8], proj_start_year = 2021,
              shape = 'decrease', magnitude = 1.7, apex_mag = 0.9, apex_loc = 40, data = industry_interim)

# Textiles
industry_traj(economy = '20_USA', sub1sectors = ind1[2], sub2sectors = ind2[9], proj_start_year = 2021,
              shape = 'bottom', magnitude = 1.4, apex_mag = 0.9, apex_loc = 40, data = industry_interim)

# Non-specified
industry_traj(economy = '20_USA', sub1sectors = ind1[2], sub2sectors = ind2[10], proj_start_year = 2021,
              shape = 'decrease', magnitude = 1.9, apex_mag = 0.9, apex_loc = 40, data = industry_interim) 


# VN





# Consolidate refined trajectories
traj_overwrite_df = pd.DataFrame()

for economy in list(APEC_economies.keys())[:-7]:
    filenames = glob.glob('./data/industry_production/4_industry_refine1/{}/*.csv'.format(economy))
    for i in filenames:
        temp_df = pd.read_csv(i)
        traj_overwrite_df = pd.concat([traj_overwrite_df, temp_df]).copy()

traj_overwrite_df.to_csv('./data/industry_production/4_industry_refine1/industry_refine1.csv', index = False)

####################################################################

industry_refine = industry_interim.merge(traj_overwrite_df, how = 'left',
                              on = ['economy', 'economy_code', 'series', 
                                    'year', 'units', 'sub1sectors', 'sub2sectors'])

industry_refine['value'] = (industry_refine['value_x']).where(industry_refine['value_y'].isna(), industry_refine['value_y'])

industry_refine = industry_refine.copy().drop(columns = ['value_x', 'value_y'])
industry_refine.to_csv('./data/industry_production/4_industry_refine1/refined_industry_all.csv', index = False) 