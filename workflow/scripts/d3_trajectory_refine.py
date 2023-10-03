# NB: Good idea to delete folder in data >> industry_production >> 4_industry_refine1 >> economy 
# Before running this for each economy's refined trajectory

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
from d2_projection_adjust import industry_traj, nonenergy_traj

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

# Interim nonenergy projections
nonenergy_production = pd.read_csv('./data/non_energy/1_nonenergy_projections/interim_all_sectors.csv')

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

#################################### Canada #################################################################
# Mining
industry_traj(economy = '03_CDA', sub1sectors = ind1[0], sub2sectors = 'x', proj_start_year = 2060,
              shape = 'decrease', magnitude = 1.3, data = industry_interim)

# Construction
industry_traj(economy = '03_CDA', sub1sectors = ind1[1], sub2sectors = 'x', proj_start_year = 2060,
              shape = 'decrease', magnitude = 1.2, data = industry_interim)

# Steel: no adjustment

# Chemicals: no adjustment

# Non-ferrous metals: no adjustment

# Non-metallic minerals
industry_traj(economy = '03_CDA', sub1sectors = ind1[2], sub2sectors = ind2[3], proj_start_year = 2023,
              shape = 'increase', magnitude = 1.4, data = industry_interim)

# Transportation equipment
industry_traj(economy = '03_CDA', sub1sectors = ind1[2], sub2sectors = ind2[4], proj_start_year = 2023,
              shape = 'bottom', magnitude = 1.4, apex_mag = 0.85, apex_loc = 40, data = industry_interim)

# Machinery
industry_traj(economy = '03_CDA', sub1sectors = ind1[2], sub2sectors = ind2[5], proj_start_year = 2023,
              shape = 'bottom', magnitude = 1.4, apex_mag = 0.85, apex_loc = 40, data = industry_interim)

# Food and beverages
industry_traj(economy = '03_CDA', sub1sectors = ind1[2], sub2sectors = ind2[6], proj_start_year = 2030,
              shape = 'bottom', magnitude = 1.35, apex_mag = 0.9, apex_loc = 40, data = industry_interim)

# Pulp and paper
industry_traj(economy = '03_CDA', sub1sectors = ind1[2], sub2sectors = ind2[7], proj_start_year = 2023,
              shape = 'decrease', magnitude = 1.2, apex_mag = 0.9, apex_loc = 40, data = industry_interim)

# Wood and wood products
industry_traj(economy = '03_CDA', sub1sectors = ind1[2], sub2sectors = ind2[8], proj_start_year = 2023,
              shape = 'bottom', magnitude = 1.35, apex_mag = 0.9, apex_loc = 40, data = industry_interim)

# Textiles
industry_traj(economy = '03_CDA', sub1sectors = ind1[2], sub2sectors = ind2[9], proj_start_year = 2023,
              shape = 'decrease', magnitude = 1.2, apex_mag = 0.9, apex_loc = 40, data = industry_interim)

# Non-specified
industry_traj(economy = '03_CDA', sub1sectors = ind1[2], sub2sectors = ind2[10], proj_start_year = 2023,
              shape = 'decrease', magnitude = 1.2, apex_mag = 0.9, apex_loc = 40, data = industry_interim)

# Non-energy: no adjustment


# Chile

#################################### China #################################################################
# Mining: no adjustment

# Construction
industry_traj(economy = '05_PRC', sub1sectors = ind1[1], sub2sectors = 'x', proj_start_year = 2021,
              shape = 'peak', magnitude = 0.2, apex_mag = 5.05, apex_loc = 1, data = industry_interim)

# Steel
industry_traj(economy = '05_PRC', sub1sectors = ind1[2], sub2sectors = ind2[0], proj_start_year = 2026,
              shape = 'decrease', magnitude = 0.4, data = industry_interim)

# Chemicals: no adjustment
industry_traj(economy = '05_PRC', sub1sectors = ind1[2], sub2sectors = ind2[1], proj_start_year = 2023,
              shape = 'peak', magnitude = 0.8, apex_mag = 1.5, apex_loc = 30, data = industry_interim)

# Non-ferrous metals
industry_traj(economy = '05_PRC', sub1sectors = ind1[2], sub2sectors = ind2[2], proj_start_year = 2021,
              shape = 'peak', magnitude = 0.8, apex_mag = 1.6, apex_loc = 40, data = industry_interim)

# Non-metallic minerals
industry_traj(economy = '05_PRC', sub1sectors = ind1[2], sub2sectors = ind2[3], proj_start_year = 2022,
              shape = 'decrease', magnitude = 0.35, apex_mag = 7.4, apex_loc = 60, data = industry_interim)

# Transportation equipment: no adjustment
industry_traj(economy = '05_PRC', sub1sectors = ind1[2], sub2sectors = ind2[4], proj_start_year = 2023,
              shape = 'peak', magnitude = 0.45, apex_mag = 3.05, apex_loc = 30, data = industry_interim)

# Machinery: no adjustment
industry_traj(economy = '05_PRC', sub1sectors = ind1[2], sub2sectors = ind2[5], proj_start_year = 2023,
              shape = 'peak', magnitude = 0.45, apex_mag = 3.05, apex_loc = 30, data = industry_interim)

# Food and beverages: no adjustment
industry_traj(economy = '05_PRC', sub1sectors = ind1[2], sub2sectors = ind2[6], proj_start_year = 2023,
              shape = 'peak', magnitude = 0.45, apex_mag = 3.05, apex_loc = 30, data = industry_interim)

# Pulp and paper
industry_traj(economy = '05_PRC', sub1sectors = ind1[2], sub2sectors = ind2[7], proj_start_year = 2023,
              shape = 'peak', magnitude = 0.45, apex_mag = 2.9, apex_loc = 30, data = industry_interim)

# Wood and wood products
industry_traj(economy = '05_PRC', sub1sectors = ind1[2], sub2sectors = ind2[8], proj_start_year = 2023,
              shape = 'peak', magnitude = 0.5, apex_mag = 2.1, apex_loc = 30, data = industry_interim)

# Textiles
industry_traj(economy = '05_PRC', sub1sectors = ind1[2], sub2sectors = ind2[9], proj_start_year = 2023,
              shape = 'bottom', magnitude = 0.5, apex_mag = 2.2, apex_loc = 20, data = industry_interim)

# Non-specified: no adjustment
industry_traj(economy = '05_PRC', sub1sectors = ind1[2], sub2sectors = ind2[10], proj_start_year = 2023,
              shape = 'peak', magnitude = 0.6, apex_mag = 1.8, apex_loc = 30, data = industry_interim)

# Non-energy: no adjustment
nonenergy_traj(economy = '05_PRC', proj_start_year = 2023,
              shape = 'peak', magnitude = 0.8, apex_mag = 1.6, apex_loc = 30, data = nonenergy_production)

# HKC
# Indonesia

#################################### Japan #################################################################
# Construction
industry_traj(economy = '08_JPN', sub1sectors = ind1[1], sub2sectors = 'x', proj_start_year = 2023,
              shape = 'decrease', magnitude = 0.7, data = industry_interim)

# Steel
industry_traj(economy = '08_JPN', sub1sectors = ind1[2], sub2sectors = ind2[0], proj_start_year = 2023,
              shape = 'decrease', magnitude = 0.9, data = industry_interim)

# Non-ferrous metals
industry_traj(economy = '08_JPN', sub1sectors = ind1[2], sub2sectors = ind2[2], proj_start_year = 2023,
              shape = 'constant', magnitude = 1.2, apex_mag = 0.9, apex_loc = 40, data = industry_interim)

# Non-metallic minerals
industry_traj(economy = '08_JPN', sub1sectors = ind1[2], sub2sectors = ind2[3], proj_start_year = 2023,
              shape = 'decrease', magnitude = 0.9, apex_mag = 0.9, apex_loc = 40, data = industry_interim)

# Transportation equipment
industry_traj(economy = '08_JPN', sub1sectors = ind1[2], sub2sectors = ind2[4], proj_start_year = 2023,
              shape = 'decrease', magnitude = 1.1, data = industry_interim)

# Machinery
industry_traj(economy = '08_JPN', sub1sectors = ind1[2], sub2sectors = ind2[5], proj_start_year = 2023,
              shape = 'decrease', magnitude = 1.1, data = industry_interim)

# Food and beverages
industry_traj(economy = '08_JPN', sub1sectors = ind1[2], sub2sectors = ind2[6], proj_start_year = 2023,
              shape = 'decrease', magnitude = 1.3, data = industry_interim)

# Pulp and paper
industry_traj(economy = '08_JPN', sub1sectors = ind1[2], sub2sectors = ind2[7], proj_start_year = 2023,
              shape = 'decrease', magnitude = 0.8, data = industry_interim)

# Wood and wood products
industry_traj(economy = '08_JPN', sub1sectors = ind1[2], sub2sectors = ind2[8], proj_start_year = 2023,
              shape = 'decrease', magnitude = 0.8, data = industry_interim)

# Textiles
industry_traj(economy = '08_JPN', sub1sectors = ind1[2], sub2sectors = ind2[9], proj_start_year = 2023,
              shape = 'decrease', magnitude = 0.8, data = industry_interim)

# Non-specified
industry_traj(economy = '08_JPN', sub1sectors = ind1[2], sub2sectors = ind2[10], proj_start_year = 2023,
              shape = 'decrease', magnitude = 0.9, data = industry_interim)

# Non-energy
nonenergy_traj(economy = '08_JPN', proj_start_year = 2023,
              shape = 'decrease', magnitude = 1.2, data = nonenergy_production)

# Korea
# Malaysia

#################################### Mexico #################################################################
# Mining: no adjustment

# Construction: no adjustment

# Steel: no adjustment

# Chemicals: no adjustment

# Non-ferrous metals: no adjustment

# Non-metallic minerals: no adjustment

# Transportation equipment: no adjustment

# Machinery: no adjustment

# Food and beverages: no adjustment

# Pulp and paper: no adjustment

# Wood and wood products: no adjustment

# Textiles: no adjustment

# Non-specified: no adjustment


# New Zealand
# PNG
# Peru
# Philippines
# Russia
# Singapore

##################### Chinese Taipei ######################################################################
# Mining: no adjustment

# Construction: no adjustment
industry_traj(economy = '18_CT', sub1sectors = ind1[1], sub2sectors = 'x', proj_start_year = 2022,
              shape = 'decrease', magnitude = 0.95, data = industry_interim)

# Steel: no adjustment

# Chemicals
industry_traj(economy = '18_CT', sub1sectors = ind1[2], sub2sectors = ind2[1], proj_start_year = 2021,
              shape = 'decrease', magnitude = 1.1, apex_mag = 0.9, apex_loc = 40, data = industry_interim)

# Non-ferrous metals: no adjustment

# Non-metallic minerals: no adjustment

# Transportation equipment
industry_traj(economy = '18_CT', sub1sectors = ind1[2], sub2sectors = ind2[4], proj_start_year = 2021,
              shape = 'decrease', magnitude = 1.1, data = industry_interim)

# Machinery
industry_traj(economy = '18_CT', sub1sectors = ind1[2], sub2sectors = ind2[5], proj_start_year = 2021,
              shape = 'peak', magnitude = 1.1, apex_mag = 1.1, apex_loc = 30, data = industry_interim)

# Food and beverages
industry_traj(economy = '18_CT', sub1sectors = ind1[2], sub2sectors = ind2[6], proj_start_year = 2021,
              shape = 'decrease', magnitude = 1.1, data = industry_interim)

# Pulp and paper
industry_traj(economy = '18_CT', sub1sectors = ind1[2], sub2sectors = ind2[7], proj_start_year = 2021,
              shape = 'increase', magnitude = 0.9, data = industry_interim)

# Wood and wood products
industry_traj(economy = '18_CT', sub1sectors = ind1[2], sub2sectors = ind2[8], proj_start_year = 2021,
              shape = 'decrease', magnitude = 0.9, data = industry_interim)

# Textiles
industry_traj(economy = '18_CT', sub1sectors = ind1[2], sub2sectors = ind2[9], proj_start_year = 2021,
              shape = 'decrease', magnitude = 0.7, data = industry_interim)

# Non-specified
industry_traj(economy = '18_CT', sub1sectors = ind1[2], sub2sectors = ind2[10], proj_start_year = 2021,
              shape = 'decrease', magnitude = 1.1, data = industry_interim)

# Non-energy
nonenergy_traj(economy = '18_CT', proj_start_year = 2021,
              shape = 'decrease', magnitude = 1.1, data = nonenergy_production)


############################ Thailand ###########################################################
# Steel
industry_traj(economy = '19_THA', sub1sectors = ind1[2], sub2sectors = ind2[0], proj_start_year = 2021,
              shape = 'decrease', magnitude = 3.5, apex_mag = 1.5, apex_loc = 20, data = industry_interim)

# Non-metallic minerals
industry_traj(economy = '19_THA', sub1sectors = ind1[2], sub2sectors = ind2[3], proj_start_year = 2021,
              shape = 'decrease', magnitude = 1.9, apex_mag = 0.9, apex_loc = 40, data = industry_interim)

# Textiles
industry_traj(economy = '19_THA', sub1sectors = ind1[2], sub2sectors = ind2[9], proj_start_year = 2021,
              shape = 'decrease', magnitude = 2.8, apex_mag = 0.8, apex_loc = 50, data = industry_interim)

# Non-specified
industry_traj(economy = '19_THA', sub1sectors = ind1[2], sub2sectors = ind2[10], proj_start_year = 2021,
              shape = 'decrease', magnitude = 3, apex_mag = 1.1, apex_loc = 70, data = industry_interim)

# Non-energy
nonenergy_traj(economy = '19_THA', proj_start_year = 2021,
              shape = 'decrease', magnitude = 2.2, apex_mag = 1.5, apex_loc = 80, data = nonenergy_production)


############################ USA ##############################################################
# Mining: no adjustment

# Construction
industry_traj(economy = '20_USA', sub1sectors = ind1[1], sub2sectors = 'x', proj_start_year = 2021,
              shape = 'decrease', magnitude = 1.7, apex_mag = 1.5, apex_loc = 20, data = industry_interim)

# Steel
industry_traj(economy = '20_USA', sub1sectors = ind1[2], sub2sectors = ind2[0], proj_start_year = 2021,
              shape = 'decrease', magnitude = 1.5, apex_mag = 1.5, apex_loc = 20, data = industry_interim)

# Chemicals: no adjustment

# Non-ferrous metals
industry_traj(economy = '20_USA', sub1sectors = ind1[2], sub2sectors = ind2[2], proj_start_year = 2021,
              shape = 'peak', magnitude = 2.2, apex_mag = 0.9, apex_loc = 60, data = industry_interim)

# Transportation equipment: no adjustment

# Machinery
industry_traj(economy = '20_USA', sub1sectors = ind1[2], sub2sectors = ind2[5], proj_start_year = 2030,
              shape = 'decrease', magnitude = 1.7, apex_mag = 0.9, apex_loc = 40, data = industry_interim)

# Food and beverages: no adjustment

# Pulp and paper
industry_traj(economy = '20_USA', sub1sectors = ind1[2], sub2sectors = ind2[7], proj_start_year = 2021,
              shape = 'decrease', magnitude = 1.3, apex_mag = 1.1, apex_loc = 40, data = industry_interim)

# Wood and wood products
industry_traj(economy = '20_USA', sub1sectors = ind1[2], sub2sectors = ind2[8], proj_start_year = 2021,
              shape = 'decrease', magnitude = 1.3, apex_mag = 0.9, apex_loc = 40, data = industry_interim)

# Textiles
industry_traj(economy = '20_USA', sub1sectors = ind1[2], sub2sectors = ind2[9], proj_start_year = 2021,
              shape = 'decrease', magnitude = 0.9, apex_mag = 0.9, apex_loc = 40, data = industry_interim)

# Non-specified: no adjustment

# Non-energy: no adjustment


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

#################################################################################################################

# Consolidate refined trajectories
traj_overwrite_df = pd.DataFrame()

for economy in list(APEC_economies.keys())[:-7]:
    filenames = glob.glob('./data/non_energy/2_nonenergy_refine1/{}/*.csv'.format(economy))
    for i in filenames:
        temp_df = pd.read_csv(i)
        traj_overwrite_df = pd.concat([traj_overwrite_df, temp_df]).copy()

traj_overwrite_df.to_csv('./data/non_energy/2_nonenergy_refine1/nonenergy_refine1.csv', index = False)

####################################################################

nonenergy_refine = nonenergy_production.merge(traj_overwrite_df, how = 'left',
                              on = ['economy', 'economy_code', 'series', 
                                    'year', 'units', 'sectors', 'sub1sectors'])

nonenergy_refine['value'] = (nonenergy_refine['value_x']).where(nonenergy_refine['value_y'].isna(), nonenergy_refine['value_y'])

nonenergy_refine = nonenergy_refine.copy().drop(columns = ['value_x', 'value_y'])
nonenergy_refine.to_csv('./data/non_energy/2_nonenergy_refine1/refined_nonenergy_all.csv', index = False)