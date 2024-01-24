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
from d2_projection_adjust import industry_adj, nonenergy_adj

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
industry_refine1 = pd.read_csv('./data/industry_production/4_industry_refine1/refined_industry_all.csv')
nonenergy_refine1 = pd.read_csv('./data/non_energy/2_nonenergy_refine1/refined_nonenergy_all.csv')

#################################################################################################

##################################################################
# Canada
# Mining
industry_adj(economy = '03_CDA',
             adjust = {2021: 0.95, 2022: 1.019},  
             sub1sectors = '14_01_mining_and_quarrying', 
             sub2sectors = 'x',
             data = industry_refine1)

# Construction
industry_adj(economy = '03_CDA',
             adjust = {2021: 0.951, 2022: 1.021},  
             sub1sectors = '14_02_construction', 
             sub2sectors = 'x',
             data = industry_refine1)

# Steel: no adjustment

# Chemicals
industry_adj(economy = '03_CDA',
             adjust = {2021: 0.951, 2022: 1.021},  
             sub1sectors = '14_03_manufacturing', 
             sub2sectors = '14_03_02_chemical_incl_petrochemical',
             data = industry_refine1)

# Non-ferrous metals: no adjustment

# Cement: no adjustment

# Transportation equip
industry_adj(economy = '03_CDA',
             adjust = {2021: 0.951, 2022: 1.021},  
             sub1sectors = '14_03_manufacturing', 
             sub2sectors = '14_03_05_transportation_equipment',
             data = industry_refine1)

# Machinery
industry_adj(economy = '03_CDA',
             adjust = {2021: 0.951, 2022: 1.021},  
             sub1sectors = '14_03_manufacturing', 
             sub2sectors = '14_03_06_machinery',
             data = industry_refine1)

# Food and beverages
industry_adj(economy = '03_CDA',
             adjust = {2021: 0.951, 2022: 1.021},  
             sub1sectors = '14_03_manufacturing', 
             sub2sectors = '14_03_07_food_beverages_and_tobacco',
             data = industry_refine1)

# Pulp paper
industry_adj(economy = '03_CDA',
             adjust = {2021: 0.951, 2022: 1.021},  
             sub1sectors = '14_03_manufacturing', 
             sub2sectors = '14_03_08_pulp_paper_and_printing',
             data = industry_refine1)

# Wood
industry_adj(economy = '03_CDA',
             adjust = {2021: 0.951, 2022: 1.021},  
             sub1sectors = '14_03_manufacturing', 
             sub2sectors = '14_03_09_wood_and_wood_products',
             data = industry_refine1)

# Textiles
industry_adj(economy = '03_CDA',
             adjust = {2021: 0.951, 2022: 1.021},  
             sub1sectors = '14_03_manufacturing', 
             sub2sectors = '14_03_10_textiles_and_leather',
             data = industry_refine1)

# Non-specified
industry_adj(economy = '03_CDA',
             adjust = {2021: 0.95, 2022: 1.02},  
             sub1sectors = '14_03_manufacturing', 
             sub2sectors = '14_03_11_nonspecified_industry',
             data = industry_refine1)

##################################################################
# China
# Construction
industry_adj(economy = '05_PRC',
             adjust = {2021: 0.88, 2022: 0.98, 2023: 0.99, 2024: 0.9925,
                       2025: 0.995, 2026: 0.9975, 2027: 0.999},  
             sub1sectors = '14_02_construction', 
             sub2sectors = 'x',
             data = industry_refine1)

# Chemicals
industry_adj(economy = '05_PRC',
             adjust = {2025: 0.99, 2026: 0.99, 2027: 0.99, 2028: 0.99, 2029: 0.98, 2030: 0.97},  
             sub1sectors = '14_03_manufacturing', 
             sub2sectors = '14_03_02_chemical_incl_petrochemical',
             data = industry_refine1)

# Wood
industry_adj(economy = '05_PRC',
             adjust = {2021: 0.93, 2022: 0.99},  
             sub1sectors = '14_03_manufacturing', 
             sub2sectors = '14_03_09_wood_and_wood_products',
             data = industry_refine1)

# Textiles
industry_adj(economy = '05_PRC',
             adjust = {2021: 0.9, 2022: 0.98, 2023: 0.99,
                       2024: 0.995, 2025: 0.9975},  
             sub1sectors = '14_03_manufacturing', 
             sub2sectors = '14_03_10_textiles_and_leather',
             data = industry_refine1)

nonenergy_adj(economy = '05_PRC',
              adjust = {2025: 0.99, 2026: 0.99, 2027: 0.99, 2028: 0.99, 2029: 0.98, 2030: 0.97},
              data = nonenergy_refine1)

##################################################################
# Japan
industry_adj(economy = '08_JPN',
             adjust = {2023: 0.93},  
             sub1sectors = '14_03_manufacturing', 
             sub2sectors = '14_03_01_iron_and_steel',
             data = industry_refine1)

##################################################################
# Chinese Taipei

industry_adj(economy = '18_CT',
             adjust = {2022: 0.93, 2023: 1.05},  
             sub1sectors = '14_03_manufacturing', 
             sub2sectors = '14_03_01_iron_and_steel',
             data = industry_refine1)

industry_adj(economy = '18_CT',
             adjust = {2022: 0.88, 2023: 1.1},  
             sub1sectors = '14_03_manufacturing', 
             sub2sectors = '14_03_02_chemical_incl_petrochemical',
             data = industry_refine1)

industry_adj(economy = '18_CT',
             adjust = {2022: 0.88, 2023: 1.09},  
             sub1sectors = '14_03_manufacturing', 
             sub2sectors = '14_03_03_non_ferrous_metals',
             data = industry_refine1)

industry_adj(economy = '18_CT',
             adjust = {2022: 0.94, 2023: 1.04},  
             sub1sectors = '14_03_manufacturing', 
             sub2sectors = '14_03_04_nonmetallic_mineral_products',
             data = industry_refine1)

industry_adj(economy = '18_CT',
             adjust = {2022: 1.04, 2023: 0.98, 2024: 1.04, 2025: 1.04},  
             sub1sectors = '14_03_manufacturing', 
             sub2sectors = '14_03_06_machinery',
             data = industry_refine1)

industry_adj(economy = '18_CT',
             adjust = {2022: 0.97, 2023: 1.02},  
             sub1sectors = '14_03_manufacturing', 
             sub2sectors = '14_03_08_pulp_paper_and_printing',
             data = industry_refine1)

industry_adj(economy = '18_CT',
             adjust = {2022: 0.92, 2023: 1.06},  
             sub1sectors = '14_03_manufacturing', 
             sub2sectors = '14_03_09_wood_and_wood_products',
             data = industry_refine1)

industry_adj(economy = '18_CT',
             adjust = {2022: 0.93, 2023: 1.05},  
             sub1sectors = '14_03_manufacturing', 
             sub2sectors = '14_03_10_textiles_and_leather',
             data = industry_refine1)

##################################################################
# Thailand

industry_adj(economy = '19_THA',
             adjust = {2021: 0.968, 2022: 0.983},  
             sub1sectors = '14_01_mining_and_quarrying', 
             sub2sectors = 'x',
             data = industry_refine1)

industry_adj(economy = '19_THA',
             adjust = {2021: 0.968, 2022: 0.983},  
             sub1sectors = '14_03_manufacturing', 
             sub2sectors = '14_03_01_iron_and_steel',
             data = industry_refine1)

industry_adj(economy = '19_THA',
             adjust = {2021: 0.968, 2022: 0.983},  
             sub1sectors = '14_03_manufacturing', 
             sub2sectors = '14_03_02_chemical_incl_petrochemical',
             data = industry_refine1)

industry_adj(economy = '19_THA',
             adjust = {2021: 0.968, 2022: 0.983},  
             sub1sectors = '14_03_manufacturing', 
             sub2sectors = '14_03_03_non_ferrous_metals',
             data = industry_refine1)

industry_adj(economy = '19_THA',
             adjust = {2021: 0.968, 2022: 0.983},  
             sub1sectors = '14_03_manufacturing', 
             sub2sectors = '14_03_04_nonmetallic_mineral_products',
             data = industry_refine1)

industry_adj(economy = '19_THA',
             adjust = {2021: 0.968, 2022: 0.983},  
             sub1sectors = '14_03_manufacturing', 
             sub2sectors = '14_03_06_machinery',
             data = industry_refine1)

industry_adj(economy = '19_THA',
             adjust = {2021: 0.968, 2022: 0.983},  
             sub1sectors = '14_03_manufacturing', 
             sub2sectors = '14_03_07_food_beverages_and_tobacco',
             data = industry_refine1)

industry_adj(economy = '19_THA',
             adjust = {2021: 0.968, 2022: 0.983},  
             sub1sectors = '14_03_manufacturing', 
             sub2sectors = '14_03_08_pulp_paper_and_printing',
             data = industry_refine1)

industry_adj(economy = '19_THA',
             adjust = {2021: 0.968, 2022: 0.983},  
             sub1sectors = '14_03_manufacturing', 
             sub2sectors = '14_03_09_wood_and_wood_products',
             data = industry_refine1)

industry_adj(economy = '19_THA',
             adjust = {2021: 0.968, 2022: 0.983},  
             sub1sectors = '14_03_manufacturing', 
             sub2sectors = '14_03_10_textiles_and_leather',
             data = industry_refine1)

industry_adj(economy = '19_THA',
             adjust = {2021: 0.968, 2022: 0.983},  
             sub1sectors = '14_03_manufacturing', 
             sub2sectors = '14_03_11_nonspecified_industry',
             data = industry_refine1)

##################################################################
# United States
# Steel
industry_adj(economy = '20_USA',
             adjust = {2022: 0.924},  
             sub1sectors = '14_03_manufacturing', 
             sub2sectors = '14_03_01_iron_and_steel',
             data = industry_refine1)

# Chemicals
industry_adj(economy = '20_USA',
             adjust = {2021: 0.978, 2022: 0.992},  
             sub1sectors = '14_03_manufacturing', 
             sub2sectors = '14_03_02_chemical_incl_petrochemical',
             data = industry_refine1)

# Non-ferrous metals
industry_adj(economy = '20_USA',
             adjust = {2021: 1.056, 2022: 0.974},  
             sub1sectors = '14_03_manufacturing', 
             sub2sectors = '14_03_03_non_ferrous_metals',
             data = industry_refine1)

# Cement
industry_adj(economy = '20_USA',
             adjust = {2021: 0.967},  
             sub1sectors = '14_03_manufacturing', 
             sub2sectors = '14_03_04_nonmetallic_mineral_products',
             data = industry_refine1)

# Transportation equip
industry_adj(economy = '20_USA',
             adjust = {2021: 0.978, 2022: 0.992},  
             sub1sectors = '14_03_manufacturing', 
             sub2sectors = '14_03_05_transportation_equipment',
             data = industry_refine1)

# Machinery
industry_adj(economy = '20_USA',
             adjust = {2021: 0.978, 2022: 0.992},  
             sub1sectors = '14_03_manufacturing', 
             sub2sectors = '14_03_06_machinery',
             data = industry_refine1)

# Food and beverages
industry_adj(economy = '20_USA',
             adjust = {2021: 0.978, 2022: 0.992},  
             sub1sectors = '14_03_manufacturing', 
             sub2sectors = '14_03_07_food_beverages_and_tobacco',
             data = industry_refine1)

# Pulp paper
industry_adj(economy = '20_USA',
             adjust = {2021: 0.979},  
             sub1sectors = '14_03_manufacturing', 
             sub2sectors = '14_03_08_pulp_paper_and_printing',
             data = industry_refine1)

# Wood
industry_adj(economy = '20_USA',
             adjust = {2021: 0.98},  
             sub1sectors = '14_03_manufacturing', 
             sub2sectors = '14_03_09_wood_and_wood_products',
             data = industry_refine1)

# Textiles
industry_adj(economy = '20_USA',
             adjust = {2021: 0.981},  
             sub1sectors = '14_03_manufacturing', 
             sub2sectors = '14_03_10_textiles_and_leather',
             data = industry_refine1)

# Non-specified
industry_adj(economy = '20_USA',
             adjust = {2021: 0.978, 2022: 0.993},  
             sub1sectors = '14_03_manufacturing', 
             sub2sectors = '14_03_11_nonspecified_industry',
             data = industry_refine1)


# Consolidate new results
traj_overwrite_df = pd.DataFrame()

for economy in list(APEC_economies.keys())[:-7]:
    filenames = glob.glob('./data/industry_production/5_industry_refine2/{}/*.csv'.format(economy))
    for i in filenames:
        temp_df = pd.read_csv(i)
        traj_overwrite_df = pd.concat([traj_overwrite_df, temp_df]).copy()

traj_overwrite_df.to_csv('./data/industry_production/5_industry_refine2/industry_refine2.csv', index = False)

####################################################################

# Now save an entire data frame with the selected results from above replacing the results from before

industry_refine = industry_refine1.merge(traj_overwrite_df, how = 'left',
                              on = ['economy', 'economy_code', 'series', 
                                    'year', 'units', 'sub1sectors', 'sub2sectors'])

industry_refine['value'] = (industry_refine['value_x']).where(industry_refine['value_y'].isna(), industry_refine['value_y'])

industry_refine = industry_refine.copy().drop(columns = ['value_x', 'value_y'])
industry_refine.to_csv('./data/industry_production/5_industry_refine2/refined_industry_all.csv', index = False) 

#########################################################################################################

# Consolidate new results
traj_overwrite_df = pd.DataFrame()

for economy in list(APEC_economies.keys())[:-7]:
    filenames = glob.glob('./data/non_energy/3_nonenergy_refine2/{}/*.csv'.format(economy))
    for i in filenames:
        temp_df = pd.read_csv(i)
        traj_overwrite_df = pd.concat([traj_overwrite_df, temp_df]).copy()

traj_overwrite_df.to_csv('./data/non_energy/3_nonenergy_refine2/nonenergy_refine2.csv', index = False)

####################################################################

# Now save an entire data frame with the selected results from above replacing the results from before

if traj_overwrite_df.empty:
    nonenergy_refine = nonenergy_refine1.copy()

else:
    nonenergy_refine = nonenergy_refine1.merge(traj_overwrite_df, how = 'left',
                                on = ['economy', 'economy_code', 'series', 
                                        'year', 'units', 'sectors', 'sub1sectors'])

    nonenergy_refine['value'] = (nonenergy_refine['value_x']).where(nonenergy_refine['value_y'].isna(), nonenergy_refine['value_y'])

    nonenergy_refine = nonenergy_refine.copy().drop(columns = ['value_x', 'value_y'])

nonenergy_refine.to_csv('./data/non_energy/3_nonenergy_refine2/refined_nonenergy_all.csv', index = False)