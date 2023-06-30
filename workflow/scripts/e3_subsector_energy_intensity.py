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
from e2_energy_use_function import energy_use

# Grab insudtrial production trajectories
indprod_df = pd.read_csv(latest_prod)

# Energy industry subsectors
industry_sectors = pd.read_csv('./data/EGEDA/industry_egeda.csv', header = None)\
    .squeeze().to_dict()

ind1 = list(industry_sectors.values())[:3]
ind2 = list(industry_sectors.values())[3:]

###############################################################################
# Thailand
# Mining
energy_use(economy = '19_THA', sub1sectors = ind1[0], sub2sectors = 'x',
           increment_ref = 0.01, increment_tgt = 0.015, end_year = 2100)

# Construction
energy_use(economy = '19_THA', sub1sectors = ind1[1], sub2sectors = 'x',
           increment_ref = 0.01, increment_tgt = 0.015, end_year = 2100)

# Steel
energy_use(economy = '19_THA', sub1sectors = ind1[2], sub2sectors = ind2[0],
           increment_ref = 0.005, increment_tgt = 0.01, end_year = 2100)

# Chemicals
energy_use(economy = '19_THA', sub1sectors = ind1[2], sub2sectors = ind2[1],
           increment_ref = 0.01, increment_tgt = 0.015, end_year = 2100)

# Non-metallic mineral products
energy_use(economy = '19_THA', sub1sectors = ind1[2], sub2sectors = ind2[3],
           increment_ref = 0.005, increment_tgt = 0.01, end_year = 2100)

# Transportation equipment
energy_use(economy = '19_THA', sub1sectors = ind1[2], sub2sectors = ind2[4],
           increment_ref = 0.01, increment_tgt = 0.015, end_year = 2100)

# Machinery
energy_use(economy = '19_THA', sub1sectors = ind1[2], sub2sectors = ind2[5],
           increment_ref = 0.01, increment_tgt = 0.015, end_year = 2100)

# Food and beverage
energy_use(economy = '19_THA', sub1sectors = ind1[2], sub2sectors = ind2[6],
           increment_ref = 0.01, increment_tgt = 0.015, end_year = 2100)

# Pulp and paper
energy_use(economy = '19_THA', sub1sectors = ind1[2], sub2sectors = ind2[7],
           increment_ref = 0.005, increment_tgt = 0.01, end_year = 2100)

# Wood and wood products
energy_use(economy = '19_THA', sub1sectors = ind1[2], sub2sectors = ind2[8],
           increment_ref = 0.01, increment_tgt = 0.015, end_year = 2100)

# Textiles
energy_use(economy = '19_THA', sub1sectors = ind1[2], sub2sectors = ind2[9],
           increment_ref = 0.01, increment_tgt = 0.015, end_year = 2100)

# Non-specified
energy_use(economy = '19_THA', sub1sectors = ind1[2], sub2sectors = ind2[10],
           increment_ref = 0.01, increment_tgt = 0.015, end_year = 2100)



