# Energy intensity (efficiency) assumptions for all sectors

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
from e2_energy_use_function import energy_use, nonenergy_use

# Grab insudtrial production trajectories
indprod_df = pd.read_csv(latest_prod)

# Energy industry subsectors
industry_sectors = pd.read_csv('./data/EGEDA/industry_egeda.csv', header = None)\
    .squeeze().to_dict()

ind1 = list(industry_sectors.values())[:3]
ind2 = list(industry_sectors.values())[3:]

##################################################################################
# Canada
# Mining
energy_use(economy = '03_CDA', sub1sectors = ind1[0], sub2sectors = 'x',
           increment_ref = 0.002, increment_tgt = 0.004, end_year = 2100)

# Construction
energy_use(economy = '03_CDA', sub1sectors = ind1[1], sub2sectors = 'x',
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Steel
energy_use(economy = '03_CDA', sub1sectors = ind1[2], sub2sectors = ind2[0],
           increment_ref = 0.002, increment_tgt = 0.0025, end_year = 2100)

# Chemicals
energy_use(economy = '03_CDA', sub1sectors = ind1[2], sub2sectors = ind2[1],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Non-ferrous metals
energy_use(economy = '03_CDA', sub1sectors = ind1[2], sub2sectors = ind2[2],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Non-metallic mineral products
energy_use(economy = '03_CDA', sub1sectors = ind1[2], sub2sectors = ind2[3],
           increment_ref = 0.003, increment_tgt = 0.005, end_year = 2100)

# Transportation equipment
energy_use(economy = '03_CDA', sub1sectors = ind1[2], sub2sectors = ind2[4],
           increment_ref = 0.006, increment_tgt = 0.009, end_year = 2100)

# Machinery
energy_use(economy = '03_CDA', sub1sectors = ind1[2], sub2sectors = ind2[5],
           increment_ref = 0.006, increment_tgt = 0.009, end_year = 2100)

# Food and beverage
energy_use(economy = '03_CDA', sub1sectors = ind1[2], sub2sectors = ind2[6],
           increment_ref = 0.006, increment_tgt = 0.009, end_year = 2100)

# Pulp and paper
energy_use(economy = '03_CDA', sub1sectors = ind1[2], sub2sectors = ind2[7],
           increment_ref = 0.006, increment_tgt = 0.01, end_year = 2100)

# Wood and wood products
energy_use(economy = '03_CDA', sub1sectors = ind1[2], sub2sectors = ind2[8],
           increment_ref = 0.005, increment_tgt = 0.008, end_year = 2100)

# Textiles
energy_use(economy = '03_CDA', sub1sectors = ind1[2], sub2sectors = ind2[9],
           increment_ref = 0.005, increment_tgt = 0.008, end_year = 2100)

# Non-specified
energy_use(economy = '03_CDA', sub1sectors = ind1[2], sub2sectors = ind2[10],
           increment_ref = 0.004, increment_tgt = 0.008, end_year = 2100)

# Non-energy
nonenergy_use(economy = '03_CDA', increment_ref = 0.003, increment_tgt = 0.006, 
              end_year = 2100) 

###############################################################################
# Japan
# Mining
energy_use(economy = '08_JPN', sub1sectors = ind1[0], sub2sectors = 'x',
           increment_ref = 0.002, increment_tgt = 0.004, start_year = 2023, end_year = 2100)

# Construction
energy_use(economy = '08_JPN', sub1sectors = ind1[1], sub2sectors = 'x',
           increment_ref = 0.003, increment_tgt = 0.006, start_year = 2023, end_year = 2100)

# Steel
energy_use(economy = '08_JPN', sub1sectors = ind1[2], sub2sectors = ind2[0],
           increment_ref = 0.002, increment_tgt = 0.004, start_year = 2023, end_year = 2100)

# Chemicals
energy_use(economy = '08_JPN', sub1sectors = ind1[2], sub2sectors = ind2[1],
           increment_ref = 0.004, increment_tgt = 0.008, start_year = 2023, end_year = 2100)

# Non-ferrous metals
energy_use(economy = '08_JPN', sub1sectors = ind1[2], sub2sectors = ind2[2],
           increment_ref = 0.0025, increment_tgt = 0.005, start_year = 2023, end_year = 2100)

# Non-metallic mineral products
energy_use(economy = '08_JPN', sub1sectors = ind1[2], sub2sectors = ind2[3],
           increment_ref = 0.003, increment_tgt = 0.006, start_year = 2023, end_year = 2100)

# Transportation equipment
energy_use(economy = '08_JPN', sub1sectors = ind1[2], sub2sectors = ind2[4],
           increment_ref = 0.004, increment_tgt = 0.008, start_year = 2023, end_year = 2100)

# Machinery
energy_use(economy = '08_JPN', sub1sectors = ind1[2], sub2sectors = ind2[5],
           increment_ref = 0.004, increment_tgt = 0.008, start_year = 2023, end_year = 2100)

# Food and beverage
energy_use(economy = '08_JPN', sub1sectors = ind1[2], sub2sectors = ind2[6],
           increment_ref = 0.004, increment_tgt = 0.008, start_year = 2023, end_year = 2100)

# Pulp and paper
energy_use(economy = '08_JPN', sub1sectors = ind1[2], sub2sectors = ind2[7],
           increment_ref = 0.003, increment_tgt = 0.006, start_year = 2023, end_year = 2100)

# Wood and wood products
energy_use(economy = '08_JPN', sub1sectors = ind1[2], sub2sectors = ind2[8],
           increment_ref = 0.004, increment_tgt = 0.008, start_year = 2023, end_year = 2100)

# Textiles
energy_use(economy = '08_JPN', sub1sectors = ind1[2], sub2sectors = ind2[9],
           increment_ref = 0.004, increment_tgt = 0.008, start_year = 2023, end_year = 2100)

# Non-specified
energy_use(economy = '08_JPN', sub1sectors = ind1[2], sub2sectors = ind2[10],
           increment_ref = 0.004, increment_tgt = 0.008, start_year = 2023, end_year = 2100)

# Non-energy
nonenergy_use(economy = '08_JPN', increment_ref = 0.004, increment_tgt = 0.008, 
              start_year = 2023, end_year = 2100)

##################################################################################
# Thailand
# Mining
energy_use(economy = '19_THA', sub1sectors = ind1[0], sub2sectors = 'x',
           increment_ref = 0.002, increment_tgt = 0.004, end_year = 2100)

# Construction
energy_use(economy = '19_THA', sub1sectors = ind1[1], sub2sectors = 'x',
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Steel
energy_use(economy = '19_THA', sub1sectors = ind1[2], sub2sectors = ind2[0],
           increment_ref = 0.001, increment_tgt = 0.002, end_year = 2100)

# Chemicals
energy_use(economy = '19_THA', sub1sectors = ind1[2], sub2sectors = ind2[1],
           increment_ref = 0.0025, increment_tgt = 0.005, end_year = 2100)

# Non-ferrous metals
energy_use(economy = '19_THA', sub1sectors = ind1[2], sub2sectors = ind2[2],
           increment_ref = 0.0025, increment_tgt = 0.005, end_year = 2100)

# Non-metallic mineral products
energy_use(economy = '19_THA', sub1sectors = ind1[2], sub2sectors = ind2[3],
           increment_ref = 0.001, increment_tgt = 0.002, end_year = 2100)

# Transportation equipment
energy_use(economy = '19_THA', sub1sectors = ind1[2], sub2sectors = ind2[4],
           increment_ref = 0.005, increment_tgt = 0.0075, end_year = 2100)

# Machinery
energy_use(economy = '19_THA', sub1sectors = ind1[2], sub2sectors = ind2[5],
           increment_ref = 0.005, increment_tgt = 0.0075, end_year = 2100)

# Food and beverage
energy_use(economy = '19_THA', sub1sectors = ind1[2], sub2sectors = ind2[6],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Pulp and paper
energy_use(economy = '19_THA', sub1sectors = ind1[2], sub2sectors = ind2[7],
           increment_ref = 0.002, increment_tgt = 0.006, end_year = 2100)

# Wood and wood products
energy_use(economy = '19_THA', sub1sectors = ind1[2], sub2sectors = ind2[8],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Textiles
energy_use(economy = '19_THA', sub1sectors = ind1[2], sub2sectors = ind2[9],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Non-specified
energy_use(economy = '19_THA', sub1sectors = ind1[2], sub2sectors = ind2[10],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Non-energy
nonenergy_use(economy = '19_THA', increment_ref = 0.003, increment_tgt = 0.006, 
              end_year = 2100)

##################################################################################
# USA
# Mining
energy_use(economy = '20_USA', sub1sectors = ind1[0], sub2sectors = 'x',
           increment_ref = 0.002, increment_tgt = 0.004, end_year = 2100)

# Construction
energy_use(economy = '20_USA', sub1sectors = ind1[1], sub2sectors = 'x',
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Steel
energy_use(economy = '20_USA', sub1sectors = ind1[2], sub2sectors = ind2[0],
           increment_ref = 0.002, increment_tgt = 0.004, end_year = 2100)

# Chemicals
energy_use(economy = '20_USA', sub1sectors = ind1[2], sub2sectors = ind2[1],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Non-ferrous metals
energy_use(economy = '20_USA', sub1sectors = ind1[2], sub2sectors = ind2[2],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Non-metallic mineral products
energy_use(economy = '20_USA', sub1sectors = ind1[2], sub2sectors = ind2[3],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Transportation equipment
energy_use(economy = '20_USA', sub1sectors = ind1[2], sub2sectors = ind2[4],
           increment_ref = 0.005, increment_tgt = 0.0075, end_year = 2100)

# Machinery
energy_use(economy = '20_USA', sub1sectors = ind1[2], sub2sectors = ind2[5],
           increment_ref = 0.005, increment_tgt = 0.0075, end_year = 2100)

# Food and beverage
energy_use(economy = '20_USA', sub1sectors = ind1[2], sub2sectors = ind2[6],
           increment_ref = 0.005, increment_tgt = 0.0075, end_year = 2100)

# Pulp and paper
energy_use(economy = '20_USA', sub1sectors = ind1[2], sub2sectors = ind2[7],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Wood and wood products
energy_use(economy = '20_USA', sub1sectors = ind1[2], sub2sectors = ind2[8],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Textiles
energy_use(economy = '20_USA', sub1sectors = ind1[2], sub2sectors = ind2[9],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Non-specified
energy_use(economy = '20_USA', sub1sectors = ind1[2], sub2sectors = ind2[10],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Non-energy
nonenergy_use(economy = '20_USA', increment_ref = 0.003, increment_tgt = 0.006, 
              end_year = 2100) 

# Save all data in one csv
# Now package up all the results and save in one combined data frame
combined_df = pd.DataFrame()

for economy in economy_list[:-7]:
    filenames = glob.glob('./results/industry/1_total_energy_subsector/{}/*.csv'.format(economy))
    for i in filenames:
        temp_df = pd.read_csv(i)
        combined_df = pd.concat([combined_df, temp_df]).copy()

combined_df = combined_df.drop(['series', 'value'], axis = 1).rename(columns = {'energy': 'value'})
combined_df['units'] = 'Indexed energy use'

combined_df.to_csv('./results/industry/1_total_energy_subsector/industry_subsector_energy_trajectories_' + timestamp + '.csv', index = False)

# Do the same for non-energy
combined_df2 = pd.DataFrame()

for economy in economy_list[:-7]:
    filenames = glob.glob('./results/non_energy/1_total_nonenergy/{}/*.csv'.format(economy))
    for i in filenames:
        temp_df = pd.read_csv(i)
        combined_df2 = pd.concat([combined_df2, temp_df]).copy()

combined_df2 = combined_df2.drop(['series', 'value'], axis = 1).rename(columns = {'energy': 'value'})
combined_df2['units'] = 'Indexed energy use'

combined_df2.to_csv('./results/non_energy/1_total_nonenergy/non_energy_trajectories_' + timestamp + '.csv', index = False)