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
# Australia
# Mining
energy_use(economy = '01_AUS', sub1sectors = ind1[0], sub2sectors = 'x',
           increment_ref = 0.002, increment_tgt = 0.004, start_year = 2025, end_year = 2100)

# Construction
energy_use(economy = '01_AUS', sub1sectors = ind1[1], sub2sectors = 'x',
           increment_ref = 0.003, increment_tgt = 0.006, start_year = 2025, end_year = 2100)

# Steel
energy_use(economy = '01_AUS', sub1sectors = ind1[2], sub2sectors = ind2[0],
           increment_ref = 0.001, increment_tgt = 0.002, start_year = 2025, end_year = 2100)

# Chemicals
energy_use(economy = '01_AUS', sub1sectors = ind1[2], sub2sectors = ind2[1],
           increment_ref = 0.0025, increment_tgt = 0.005, start_year = 2025, end_year = 2100)

# Non-ferrous metals
energy_use(economy = '01_AUS', sub1sectors = ind1[2], sub2sectors = ind2[2],
           increment_ref = 0.003, increment_tgt = 0.006, start_year = 2025, end_year = 2100)

# Non-metallic mineral products
energy_use(economy = '01_AUS', sub1sectors = ind1[2], sub2sectors = ind2[3],
           increment_ref = 0.0025, increment_tgt = 0.005, start_year = 2025, end_year = 2100)

# Transportation equipment
energy_use(economy = '01_AUS', sub1sectors = ind1[2], sub2sectors = ind2[4],
           increment_ref = 0.005, increment_tgt = 0.0075, start_year = 2025, end_year = 2100)

# Machinery
energy_use(economy = '01_AUS', sub1sectors = ind1[2], sub2sectors = ind2[5],
           increment_ref = 0.005, increment_tgt = 0.0075, start_year = 2025, end_year = 2100)

# Food and beverage
energy_use(economy = '01_AUS', sub1sectors = ind1[2], sub2sectors = ind2[6],
           increment_ref = 0.004, increment_tgt = 0.008, start_year = 2025, end_year = 2100)

# Pulp and paper
energy_use(economy = '01_AUS', sub1sectors = ind1[2], sub2sectors = ind2[7],
           increment_ref = 0.003, increment_tgt = 0.006, start_year = 2025, end_year = 2100)

# Wood and wood products
energy_use(economy = '01_AUS', sub1sectors = ind1[2], sub2sectors = ind2[8],
           increment_ref = 0.003, increment_tgt = 0.006, start_year = 2025, end_year = 2100)

# Textiles
energy_use(economy = '01_AUS', sub1sectors = ind1[2], sub2sectors = ind2[9],
           increment_ref = 0.003, increment_tgt = 0.006, start_year = 2025, end_year = 2100)

# Non-specified
energy_use(economy = '01_AUS', sub1sectors = ind1[2], sub2sectors = ind2[10],
           increment_ref = 0.005, increment_tgt = 0.0075, start_year = 2025, end_year = 2100)

# Non-energy
nonenergy_use(economy = '01_AUS', increment_ref = 0.0025, increment_tgt = 0.005, 
              start_year = 2025, end_year = 2100)

##################################################################################
# Brunei D
# Mining
energy_use(economy = '02_BD', sub1sectors = ind1[0], sub2sectors = 'x',
           increment_ref = 0.002, increment_tgt = 0.004, start_year = 2025, end_year = 2100)

# Chemicals
energy_use(economy = '02_BD', sub1sectors = ind1[2], sub2sectors = ind2[1],
           increment_ref = 0.0025, increment_tgt = 0.005, start_year = 2028, end_year = 2100)

# Non-specified
energy_use(economy = '02_BD', sub1sectors = ind1[2], sub2sectors = ind2[10],
           increment_ref = 0.005, increment_tgt = 0.0075, start_year = 2025, end_year = 2100)

# Non-energy
nonenergy_use(economy = '02_BD', increment_ref = 0.0025, increment_tgt = 0.005, 
              start_year = 2028, end_year = 2100)

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

##################################################################################
# China
# Mining
energy_use(economy = '05_PRC', sub1sectors = ind1[0], sub2sectors = 'x',
           increment_ref = 0.002, increment_tgt = 0.004, end_year = 2100)

# Construction
energy_use(economy = '05_PRC', sub1sectors = ind1[1], sub2sectors = 'x',
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Steel
energy_use(economy = '05_PRC', sub1sectors = ind1[2], sub2sectors = ind2[0],
           increment_ref = 0.0015, increment_tgt = 0.0025, end_year = 2100)

# Chemicals
energy_use(economy = '05_PRC', sub1sectors = ind1[2], sub2sectors = ind2[1],
           increment_ref = 0.0025, increment_tgt = 0.005, end_year = 2100)

# Non-ferrous metals
energy_use(economy = '05_PRC', sub1sectors = ind1[2], sub2sectors = ind2[2],
           increment_ref = 0.0025, increment_tgt = 0.005, end_year = 2100)

# Non-metallic mineral products
energy_use(economy = '05_PRC', sub1sectors = ind1[2], sub2sectors = ind2[3],
           increment_ref = 0.0015, increment_tgt = 0.0025, end_year = 2100)

# Transportation equipment
energy_use(economy = '05_PRC', sub1sectors = ind1[2], sub2sectors = ind2[4],
           increment_ref = 0.005, increment_tgt = 0.0075, end_year = 2100)

# Machinery
energy_use(economy = '05_PRC', sub1sectors = ind1[2], sub2sectors = ind2[5],
           increment_ref = 0.005, increment_tgt = 0.0075, end_year = 2100)

# Food and beverage
energy_use(economy = '05_PRC', sub1sectors = ind1[2], sub2sectors = ind2[6],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Pulp and paper
energy_use(economy = '05_PRC', sub1sectors = ind1[2], sub2sectors = ind2[7],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Wood and wood products
energy_use(economy = '05_PRC', sub1sectors = ind1[2], sub2sectors = ind2[8],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Textiles
energy_use(economy = '05_PRC', sub1sectors = ind1[2], sub2sectors = ind2[9],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Non-specified
energy_use(economy = '05_PRC', sub1sectors = ind1[2], sub2sectors = ind2[10],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Non-energy
nonenergy_use(economy = '05_PRC', increment_ref = 0.003, increment_tgt = 0.006, 
              end_year = 2100)

##################################################################################
# Chile
# Mining
energy_use(economy = '04_CHL', sub1sectors = ind1[0], sub2sectors = 'x',
           increment_ref = 0.002, increment_tgt = 0.004, end_year = 2100)

# Construction
energy_use(economy = '04_CHL', sub1sectors = ind1[1], sub2sectors = 'x',
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Steel
energy_use(economy = '04_CHL', sub1sectors = ind1[2], sub2sectors = ind2[0],
           increment_ref = 0.0015, increment_tgt = 0.0025, end_year = 2100)

# Chemicals
energy_use(economy = '04_CHL', sub1sectors = ind1[2], sub2sectors = ind2[1],
           increment_ref = 0.0025, increment_tgt = 0.005, end_year = 2100)

# Non-ferrous metals: no data

# Non-metallic mineral products
energy_use(economy = '04_CHL', sub1sectors = ind1[2], sub2sectors = ind2[3],
           increment_ref = 0.0015, increment_tgt = 0.0025, end_year = 2100)

# Transportation equipment
energy_use(economy = '04_CHL', sub1sectors = ind1[2], sub2sectors = ind2[4],
           increment_ref = 0.005, increment_tgt = 0.0075, end_year = 2100)

# Machinery
energy_use(economy = '04_CHL', sub1sectors = ind1[2], sub2sectors = ind2[5],
           increment_ref = 0.005, increment_tgt = 0.0075, end_year = 2100)

# Food and beverage
energy_use(economy = '04_CHL', sub1sectors = ind1[2], sub2sectors = ind2[6],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Pulp and paper
energy_use(economy = '04_CHL', sub1sectors = ind1[2], sub2sectors = ind2[7],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Wood and wood products
energy_use(economy = '04_CHL', sub1sectors = ind1[2], sub2sectors = ind2[8],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Textiles
energy_use(economy = '04_CHL', sub1sectors = ind1[2], sub2sectors = ind2[9],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Non-specified
energy_use(economy = '04_CHL', sub1sectors = ind1[2], sub2sectors = ind2[10],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Non-energy
nonenergy_use(economy = '04_CHL', increment_ref = 0.003, increment_tgt = 0.006, 
              end_year = 2100)

##################################################################################
# Hong Kong
# Mining
energy_use(economy = '06_HKC', sub1sectors = ind1[0], sub2sectors = 'x',
           increment_ref = 0.002, increment_tgt = 0.004, start_year = 2025, end_year = 2100)

# Construction
energy_use(economy = '06_HKC', sub1sectors = ind1[1], sub2sectors = 'x',
           increment_ref = 0.003, increment_tgt = 0.006, start_year = 2025, end_year = 2100)

# Chemicals
energy_use(economy = '06_HKC', sub1sectors = ind1[2], sub2sectors = ind2[1],
           increment_ref = 0.0025, increment_tgt = 0.005, start_year = 2025, end_year = 2100)

# Non-metallic mineral products
energy_use(economy = '06_HKC', sub1sectors = ind1[2], sub2sectors = ind2[3],
           increment_ref = 0.0025, increment_tgt = 0.005, start_year = 2025, end_year = 2100)

# Transportation equipment
energy_use(economy = '06_HKC', sub1sectors = ind1[2], sub2sectors = ind2[4],
           increment_ref = 0.005, increment_tgt = 0.0075, start_year = 2025, end_year = 2100)

# Machinery
energy_use(economy = '06_HKC', sub1sectors = ind1[2], sub2sectors = ind2[5],
           increment_ref = 0.005, increment_tgt = 0.0075, start_year = 2025, end_year = 2100)

# Food and beverage
energy_use(economy = '06_HKC', sub1sectors = ind1[2], sub2sectors = ind2[6],
           increment_ref = 0.004, increment_tgt = 0.008, start_year = 2025, end_year = 2100)

# Pulp and paper
energy_use(economy = '06_HKC', sub1sectors = ind1[2], sub2sectors = ind2[7],
           increment_ref = 0.003, increment_tgt = 0.006, start_year = 2025, end_year = 2100)

# Wood and wood products
energy_use(economy = '06_HKC', sub1sectors = ind1[2], sub2sectors = ind2[8],
           increment_ref = 0.003, increment_tgt = 0.006, start_year = 2025, end_year = 2100)

# Textiles
energy_use(economy = '06_HKC', sub1sectors = ind1[2], sub2sectors = ind2[9],
           increment_ref = 0.003, increment_tgt = 0.006, start_year = 2025, end_year = 2100)

# Non-specified
energy_use(economy = '06_HKC', sub1sectors = ind1[2], sub2sectors = ind2[10],
           increment_ref = 0.005, increment_tgt = 0.0075, start_year = 2025, end_year = 2100)

# Non-energy
nonenergy_use(economy = '06_HKC', increment_ref = 0.0025, increment_tgt = 0.005, 
              start_year = 2025, end_year = 2100)


##################################################################################
# Indonesia
# Mining
energy_use(economy = '07_INA', sub1sectors = ind1[0], sub2sectors = 'x',
           increment_ref = 0.002, increment_tgt = 0.004, start_year = 2025, end_year = 2100)

# Construction
energy_use(economy = '07_INA', sub1sectors = ind1[1], sub2sectors = 'x',
           increment_ref = 0.003, increment_tgt = 0.006, start_year = 2025, end_year = 2100)

# Steel
energy_use(economy = '07_INA', sub1sectors = ind1[2], sub2sectors = ind2[0],
           increment_ref = 0.001, increment_tgt = 0.002, start_year = 2025, end_year = 2100)

# Chemicals
energy_use(economy = '07_INA', sub1sectors = ind1[2], sub2sectors = ind2[1],
           increment_ref = 0.0025, increment_tgt = 0.005, start_year = 2025, end_year = 2100)

# Non-ferrous metals
energy_use(economy = '07_INA', sub1sectors = ind1[2], sub2sectors = ind2[2],
           increment_ref = 0.003, increment_tgt = 0.006, start_year = 2025, end_year = 2100)

# Non-metallic mineral products
energy_use(economy = '07_INA', sub1sectors = ind1[2], sub2sectors = ind2[3],
           increment_ref = 0.0025, increment_tgt = 0.005, start_year = 2025, end_year = 2100)

# Transportation equipment
energy_use(economy = '07_INA', sub1sectors = ind1[2], sub2sectors = ind2[4],
           increment_ref = 0.005, increment_tgt = 0.0075, start_year = 2025, end_year = 2100)

# Machinery
energy_use(economy = '07_INA', sub1sectors = ind1[2], sub2sectors = ind2[5],
           increment_ref = 0.005, increment_tgt = 0.0075, start_year = 2025, end_year = 2100)

# Food and beverage
energy_use(economy = '07_INA', sub1sectors = ind1[2], sub2sectors = ind2[6],
           increment_ref = 0.004, increment_tgt = 0.008, start_year = 2025, end_year = 2100)

# Pulp and paper
energy_use(economy = '07_INA', sub1sectors = ind1[2], sub2sectors = ind2[7],
           increment_ref = 0.003, increment_tgt = 0.006, start_year = 2025, end_year = 2100)

# Wood and wood products
energy_use(economy = '07_INA', sub1sectors = ind1[2], sub2sectors = ind2[8],
           increment_ref = 0.003, increment_tgt = 0.006, start_year = 2025, end_year = 2100)

# Textiles
energy_use(economy = '07_INA', sub1sectors = ind1[2], sub2sectors = ind2[9],
           increment_ref = 0.003, increment_tgt = 0.006, start_year = 2025, end_year = 2100)

# Non-specified
energy_use(economy = '07_INA', sub1sectors = ind1[2], sub2sectors = ind2[10],
           increment_ref = 0.0025, increment_tgt = 0.005, start_year = 2025, end_year = 2100)

# Non-energy
nonenergy_use(economy = '07_INA', increment_ref = 0.0025, increment_tgt = 0.005, 
              start_year = 2025, end_year = 2100)

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
# Korea
# Mining
energy_use(economy = '09_ROK', sub1sectors = ind1[0], sub2sectors = 'x',
           increment_ref = 0.002, increment_tgt = 0.004, end_year = 2100)

# Construction
energy_use(economy = '09_ROK', sub1sectors = ind1[1], sub2sectors = 'x',
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Steel
energy_use(economy = '09_ROK', sub1sectors = ind1[2], sub2sectors = ind2[0],
           increment_ref = 0.002, increment_tgt = 0.003, end_year = 2100)

# Chemicals
energy_use(economy = '09_ROK', sub1sectors = ind1[2], sub2sectors = ind2[1],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Non-ferrous metals
energy_use(economy = '09_ROK', sub1sectors = ind1[2], sub2sectors = ind2[2],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Non-metallic mineral products
energy_use(economy = '09_ROK', sub1sectors = ind1[2], sub2sectors = ind2[3],
           increment_ref = 0.003, increment_tgt = 0.005, end_year = 2100)

# Transportation equipment
energy_use(economy = '09_ROK', sub1sectors = ind1[2], sub2sectors = ind2[4],
           increment_ref = 0.006, increment_tgt = 0.009, end_year = 2100)

# Machinery
energy_use(economy = '09_ROK', sub1sectors = ind1[2], sub2sectors = ind2[5],
           increment_ref = 0.006, increment_tgt = 0.009, end_year = 2100)

# Food and beverage
energy_use(economy = '09_ROK', sub1sectors = ind1[2], sub2sectors = ind2[6],
           increment_ref = 0.006, increment_tgt = 0.009, end_year = 2100)

# Pulp and paper
energy_use(economy = '09_ROK', sub1sectors = ind1[2], sub2sectors = ind2[7],
           increment_ref = 0.006, increment_tgt = 0.01, end_year = 2100)

# Wood and wood products
energy_use(economy = '09_ROK', sub1sectors = ind1[2], sub2sectors = ind2[8],
           increment_ref = 0.005, increment_tgt = 0.008, end_year = 2100)

# Textiles
energy_use(economy = '09_ROK', sub1sectors = ind1[2], sub2sectors = ind2[9],
           increment_ref = 0.005, increment_tgt = 0.008, end_year = 2100)

# Non-specified
energy_use(economy = '09_ROK', sub1sectors = ind1[2], sub2sectors = ind2[10],
           increment_ref = 0.004, increment_tgt = 0.008, end_year = 2100)

# Non-energy
nonenergy_use(economy = '09_ROK', increment_ref = 0.003, increment_tgt = 0.006, 
              end_year = 2100)

##################################################################################
# Malaysia
# Non-specified
energy_use(economy = '10_MAS', sub1sectors = ind1[2], sub2sectors = ind2[10],
           increment_ref = 0.005, increment_tgt = 0.0075, start_year = 2025, end_year = 2100)

# Non-energy
nonenergy_use(economy = '10_MAS', increment_ref = 0.0025, increment_tgt = 0.005, 
              start_year = 2025, end_year = 2100)

##################################################################################
# Mexico
# Mining
energy_use(economy = '11_MEX', sub1sectors = ind1[0], sub2sectors = 'x',
           increment_ref = 0.002, increment_tgt = 0.004, end_year = 2100)

# Construction
energy_use(economy = '11_MEX', sub1sectors = ind1[1], sub2sectors = 'x',
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Steel
energy_use(economy = '11_MEX', sub1sectors = ind1[2], sub2sectors = ind2[0],
           increment_ref = 0.0015, increment_tgt = 0.0025, end_year = 2100)

# Chemicals
energy_use(economy = '11_MEX', sub1sectors = ind1[2], sub2sectors = ind2[1],
           increment_ref = 0.0025, increment_tgt = 0.005, end_year = 2100)

# Non-ferrous metals
energy_use(economy = '11_MEX', sub1sectors = ind1[2], sub2sectors = ind2[2],
           increment_ref = 0.0025, increment_tgt = 0.005, end_year = 2100)

# Non-metallic mineral products
energy_use(economy = '11_MEX', sub1sectors = ind1[2], sub2sectors = ind2[3],
           increment_ref = 0.0015, increment_tgt = 0.0025, end_year = 2100)

# Transportation equipment
energy_use(economy = '11_MEX', sub1sectors = ind1[2], sub2sectors = ind2[4],
           increment_ref = 0.005, increment_tgt = 0.0075, end_year = 2100)

# Machinery
energy_use(economy = '11_MEX', sub1sectors = ind1[2], sub2sectors = ind2[5],
           increment_ref = 0.005, increment_tgt = 0.0075, end_year = 2100)

# Food and beverage
energy_use(economy = '11_MEX', sub1sectors = ind1[2], sub2sectors = ind2[6],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Pulp and paper
energy_use(economy = '11_MEX', sub1sectors = ind1[2], sub2sectors = ind2[7],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Wood and wood products
energy_use(economy = '11_MEX', sub1sectors = ind1[2], sub2sectors = ind2[8],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Textiles
energy_use(economy = '11_MEX', sub1sectors = ind1[2], sub2sectors = ind2[9],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Non-specified
energy_use(economy = '11_MEX', sub1sectors = ind1[2], sub2sectors = ind2[10],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Non-energy
nonenergy_use(economy = '11_MEX', increment_ref = 0.003, increment_tgt = 0.006, 
              end_year = 2100)

##################################################################################
# New Zealand
# Mining
energy_use(economy = '12_NZ', sub1sectors = ind1[0], sub2sectors = 'x',
           increment_ref = 0.002, increment_tgt = 0.004, start_year = 2025, end_year = 2100)

# Construction
energy_use(economy = '12_NZ', sub1sectors = ind1[1], sub2sectors = 'x',
           increment_ref = 0.003, increment_tgt = 0.006, start_year = 2025, end_year = 2100)

# Steel
energy_use(economy = '12_NZ', sub1sectors = ind1[2], sub2sectors = ind2[0],
           increment_ref = 0.001, increment_tgt = 0.002, start_year = 2025, end_year = 2100)

# Chemicals
energy_use(economy = '12_NZ', sub1sectors = ind1[2], sub2sectors = ind2[1],
           increment_ref = 0.0025, increment_tgt = 0.005, start_year = 2025, end_year = 2100)

# Non-ferrous metals
energy_use(economy = '12_NZ', sub1sectors = ind1[2], sub2sectors = ind2[2],
           increment_ref = 0.003, increment_tgt = 0.003, start_year = 2025, end_year = 2100)

# Non-metallic mineral products
energy_use(economy = '12_NZ', sub1sectors = ind1[2], sub2sectors = ind2[3],
           increment_ref = 0.0025, increment_tgt = 0.005, start_year = 2025, end_year = 2100)

# Transportation equipment
energy_use(economy = '12_NZ', sub1sectors = ind1[2], sub2sectors = ind2[4],
           increment_ref = 0.005, increment_tgt = 0.0075, start_year = 2025, end_year = 2100)

# Machinery
energy_use(economy = '12_NZ', sub1sectors = ind1[2], sub2sectors = ind2[5],
           increment_ref = 0.005, increment_tgt = 0.0075, start_year = 2025, end_year = 2100)

# Food and beverage
energy_use(economy = '12_NZ', sub1sectors = ind1[2], sub2sectors = ind2[6],
           increment_ref = 0.004, increment_tgt = 0.008, start_year = 2025, end_year = 2100)

# Pulp and paper
energy_use(economy = '12_NZ', sub1sectors = ind1[2], sub2sectors = ind2[7],
           increment_ref = 0.003, increment_tgt = 0.006, start_year = 2025, end_year = 2100)

# Wood and wood products
energy_use(economy = '12_NZ', sub1sectors = ind1[2], sub2sectors = ind2[8],
           increment_ref = 0.003, increment_tgt = 0.006, start_year = 2025, end_year = 2100)

# Textiles
energy_use(economy = '12_NZ', sub1sectors = ind1[2], sub2sectors = ind2[9],
           increment_ref = 0.003, increment_tgt = 0.006, start_year = 2025, end_year = 2100)

# Non-specified
energy_use(economy = '12_NZ', sub1sectors = ind1[2], sub2sectors = ind2[10],
           increment_ref = 0.005, increment_tgt = 0.0075, start_year = 2025, end_year = 2100)

# Non-energy
nonenergy_use(economy = '12_NZ', increment_ref = 0.0025, increment_tgt = 0.005, 
              start_year = 2025, end_year = 2100)

##################################################################################
# PNG
# Mining
energy_use(economy = '13_PNG', sub1sectors = ind1[0], sub2sectors = 'x',
           increment_ref = 0.002, increment_tgt = 0.004, end_year = 2100)

# Construction
energy_use(economy = '13_PNG', sub1sectors = ind1[1], sub2sectors = 'x',
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Steel: no data

# Chemicals
energy_use(economy = '13_PNG', sub1sectors = ind1[2], sub2sectors = ind2[1],
           increment_ref = 0.0025, increment_tgt = 0.005, end_year = 2100)

# Non-ferrous metals: no data

# Non-metallic mineral products
energy_use(economy = '13_PNG', sub1sectors = ind1[2], sub2sectors = ind2[3],
           increment_ref = 0.0015, increment_tgt = 0.0025, end_year = 2100)

# Transportation equipment
energy_use(economy = '13_PNG', sub1sectors = ind1[2], sub2sectors = ind2[4],
           increment_ref = 0.005, increment_tgt = 0.0075, end_year = 2100)

# Machinery
energy_use(economy = '13_PNG', sub1sectors = ind1[2], sub2sectors = ind2[5],
           increment_ref = 0.005, increment_tgt = 0.0075, end_year = 2100)

# Food and beverage
energy_use(economy = '13_PNG', sub1sectors = ind1[2], sub2sectors = ind2[6],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Pulp and paper
energy_use(economy = '13_PNG', sub1sectors = ind1[2], sub2sectors = ind2[7],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Wood and wood products
energy_use(economy = '13_PNG', sub1sectors = ind1[2], sub2sectors = ind2[8],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Textiles
energy_use(economy = '13_PNG', sub1sectors = ind1[2], sub2sectors = ind2[9],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Non-specified
energy_use(economy = '13_PNG', sub1sectors = ind1[2], sub2sectors = ind2[10],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Non-energy
nonenergy_use(economy = '13_PNG', increment_ref = 0.003, increment_tgt = 0.006, 
              end_year = 2100)

##################################################################################
# Peru
# Mining
energy_use(economy = '14_PE', sub1sectors = ind1[0], sub2sectors = 'x',
           increment_ref = 0.002, increment_tgt = 0.004, end_year = 2100)

# Construction
energy_use(economy = '14_PE', sub1sectors = ind1[1], sub2sectors = 'x',
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Steel
energy_use(economy = '14_PE', sub1sectors = ind1[2], sub2sectors = ind2[0],
           increment_ref = 0.0015, increment_tgt = 0.0025, end_year = 2100)

# Chemicals
energy_use(economy = '14_PE', sub1sectors = ind1[2], sub2sectors = ind2[1],
           increment_ref = 0.0025, increment_tgt = 0.005, end_year = 2100)

# Non-ferrous metals: no data

# Non-metallic mineral products
energy_use(economy = '14_PE', sub1sectors = ind1[2], sub2sectors = ind2[3],
           increment_ref = 0.0015, increment_tgt = 0.0025, end_year = 2100)

# Transportation equipment
energy_use(economy = '14_PE', sub1sectors = ind1[2], sub2sectors = ind2[4],
           increment_ref = 0.005, increment_tgt = 0.0075, end_year = 2100)

# Machinery
energy_use(economy = '14_PE', sub1sectors = ind1[2], sub2sectors = ind2[5],
           increment_ref = 0.005, increment_tgt = 0.0075, end_year = 2100)

# Food and beverage
energy_use(economy = '14_PE', sub1sectors = ind1[2], sub2sectors = ind2[6],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Pulp and paper
energy_use(economy = '14_PE', sub1sectors = ind1[2], sub2sectors = ind2[7],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Wood and wood products
energy_use(economy = '14_PE', sub1sectors = ind1[2], sub2sectors = ind2[8],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Textiles
energy_use(economy = '14_PE', sub1sectors = ind1[2], sub2sectors = ind2[9],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Non-specified
energy_use(economy = '14_PE', sub1sectors = ind1[2], sub2sectors = ind2[10],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Non-energy
nonenergy_use(economy = '14_PE', increment_ref = 0.003, increment_tgt = 0.006, 
              end_year = 2100)

##################################################################################
# Philippines
# Mining
energy_use(economy = '15_RP', sub1sectors = ind1[0], sub2sectors = 'x',
           increment_ref = 0.002, increment_tgt = 0.004, start_year = 2025, end_year = 2100)

# Construction
energy_use(economy = '15_RP', sub1sectors = ind1[1], sub2sectors = 'x',
           increment_ref = 0.003, increment_tgt = 0.006, start_year = 2025, end_year = 2100)

# Steel
energy_use(economy = '15_RP', sub1sectors = ind1[2], sub2sectors = ind2[0],
           increment_ref = 0.0015, increment_tgt = 0.0025, start_year = 2025, end_year = 2100)

# Chemicals
energy_use(economy = '15_RP', sub1sectors = ind1[2], sub2sectors = ind2[1],
           increment_ref = 0.0025, increment_tgt = 0.005, start_year = 2025, end_year = 2100)

# Non-ferrous metals: no data
# energy_use(economy = '15_RP', sub1sectors = ind1[2], sub2sectors = ind2[2],
#            increment_ref = 0.003, increment_tgt = 0.006, start_year = 2025, end_year = 2100)

# Non-metallic mineral products
energy_use(economy = '15_RP', sub1sectors = ind1[2], sub2sectors = ind2[3],
           increment_ref = 0.0025, increment_tgt = 0.005, start_year = 2025, end_year = 2100)

# Transportation equipment
energy_use(economy = '15_RP', sub1sectors = ind1[2], sub2sectors = ind2[4],
           increment_ref = 0.005, increment_tgt = 0.0075, start_year = 2025, end_year = 2100)

# Machinery
energy_use(economy = '15_RP', sub1sectors = ind1[2], sub2sectors = ind2[5],
           increment_ref = 0.005, increment_tgt = 0.0075, start_year = 2025, end_year = 2100)

# Food and beverage
energy_use(economy = '15_RP', sub1sectors = ind1[2], sub2sectors = ind2[6],
           increment_ref = 0.004, increment_tgt = 0.008, start_year = 2025, end_year = 2100)

# Pulp and paper
energy_use(economy = '15_RP', sub1sectors = ind1[2], sub2sectors = ind2[7],
           increment_ref = 0.003, increment_tgt = 0.006, start_year = 2025, end_year = 2100)

# Wood and wood products
energy_use(economy = '15_RP', sub1sectors = ind1[2], sub2sectors = ind2[8],
           increment_ref = 0.003, increment_tgt = 0.006, start_year = 2025, end_year = 2100)

# Textiles
energy_use(economy = '15_RP', sub1sectors = ind1[2], sub2sectors = ind2[9],
           increment_ref = 0.003, increment_tgt = 0.006, start_year = 2025, end_year = 2100)

# Non-specified
energy_use(economy = '15_RP', sub1sectors = ind1[2], sub2sectors = ind2[10],
           increment_ref = 0.005, increment_tgt = 0.0075, start_year = 2025, end_year = 2100)

# Non-energy
nonenergy_use(economy = '15_RP', increment_ref = 0.0025, increment_tgt = 0.005, 
              start_year = 2025, end_year = 2100)

##################################################################################
# Russia
# Mining
energy_use(economy = '16_RUS', sub1sectors = ind1[0], sub2sectors = 'x',
           increment_ref = 0.002, increment_tgt = 0.004, start_year = 2025, end_year = 2100)

# Construction
energy_use(economy = '16_RUS', sub1sectors = ind1[1], sub2sectors = 'x',
           increment_ref = 0.003, increment_tgt = 0.006, start_year = 2025, end_year = 2100)

# Steel
energy_use(economy = '16_RUS', sub1sectors = ind1[2], sub2sectors = ind2[0],
           increment_ref = 0.0015, increment_tgt = 0.0025, start_year = 2025, end_year = 2100)

# Chemicals
energy_use(economy = '16_RUS', sub1sectors = ind1[2], sub2sectors = ind2[1],
           increment_ref = 0.0025, increment_tgt = 0.005, start_year = 2025, end_year = 2100)

# Non-ferrous metals
energy_use(economy = '16_RUS', sub1sectors = ind1[2], sub2sectors = ind2[2],
           increment_ref = 0.003, increment_tgt = 0.006, start_year = 2025, end_year = 2100)

# Non-metallic mineral products
energy_use(economy = '16_RUS', sub1sectors = ind1[2], sub2sectors = ind2[3],
           increment_ref = 0.0025, increment_tgt = 0.005, start_year = 2025, end_year = 2100)

# Transportation equipment
energy_use(economy = '16_RUS', sub1sectors = ind1[2], sub2sectors = ind2[4],
           increment_ref = 0.005, increment_tgt = 0.0075, start_year = 2025, end_year = 2100)

# Machinery
energy_use(economy = '16_RUS', sub1sectors = ind1[2], sub2sectors = ind2[5],
           increment_ref = 0.005, increment_tgt = 0.0075, start_year = 2025, end_year = 2100)

# Food and beverage
energy_use(economy = '16_RUS', sub1sectors = ind1[2], sub2sectors = ind2[6],
           increment_ref = 0.004, increment_tgt = 0.008, start_year = 2025, end_year = 2100)

# Pulp and paper
energy_use(economy = '16_RUS', sub1sectors = ind1[2], sub2sectors = ind2[7],
           increment_ref = 0.003, increment_tgt = 0.006, start_year = 2025, end_year = 2100)

# Wood and wood products
energy_use(economy = '16_RUS', sub1sectors = ind1[2], sub2sectors = ind2[8],
           increment_ref = 0.003, increment_tgt = 0.006, start_year = 2025, end_year = 2100)

# Textiles
energy_use(economy = '16_RUS', sub1sectors = ind1[2], sub2sectors = ind2[9],
           increment_ref = 0.003, increment_tgt = 0.006, start_year = 2025, end_year = 2100)

# Non-specified
energy_use(economy = '16_RUS', sub1sectors = ind1[2], sub2sectors = ind2[10],
           increment_ref = 0.005, increment_tgt = 0.0075, start_year = 2025, end_year = 2100)

# Non-energy
nonenergy_use(economy = '16_RUS', increment_ref = 0.0025, increment_tgt = 0.005, 
              start_year = 2025, end_year = 2100)

##################################################################################
# Singapore
# Mining
energy_use(economy = '17_SIN', sub1sectors = ind1[0], sub2sectors = 'x',
           increment_ref = 0.002, increment_tgt = 0.004, end_year = 2100)

# Construction
energy_use(economy = '17_SIN', sub1sectors = ind1[1], sub2sectors = 'x',
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Steel
energy_use(economy = '17_SIN', sub1sectors = ind1[2], sub2sectors = ind2[0],
           increment_ref = 0.001, increment_tgt = 0.002, end_year = 2100)

# Chemicals
energy_use(economy = '17_SIN', sub1sectors = ind1[2], sub2sectors = ind2[1],
           increment_ref = 0.0025, increment_tgt = 0.005, end_year = 2100)

# Non-ferrous metals
energy_use(economy = '17_SIN', sub1sectors = ind1[2], sub2sectors = ind2[2],
           increment_ref = 0.0025, increment_tgt = 0.005, end_year = 2100)

# Non-metallic mineral products
energy_use(economy = '17_SIN', sub1sectors = ind1[2], sub2sectors = ind2[3],
           increment_ref = 0.001, increment_tgt = 0.002, end_year = 2100)

# Transportation equipment
energy_use(economy = '17_SIN', sub1sectors = ind1[2], sub2sectors = ind2[4],
           increment_ref = 0.005, increment_tgt = 0.0075, end_year = 2100)

# Machinery
energy_use(economy = '17_SIN', sub1sectors = ind1[2], sub2sectors = ind2[5],
           increment_ref = 0.005, increment_tgt = 0.0075, end_year = 2100)

# Food and beverage
energy_use(economy = '17_SIN', sub1sectors = ind1[2], sub2sectors = ind2[6],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Pulp and paper
energy_use(economy = '17_SIN', sub1sectors = ind1[2], sub2sectors = ind2[7],
           increment_ref = 0.002, increment_tgt = 0.006, end_year = 2100)

# Wood and wood products
energy_use(economy = '17_SIN', sub1sectors = ind1[2], sub2sectors = ind2[8],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Textiles
energy_use(economy = '17_SIN', sub1sectors = ind1[2], sub2sectors = ind2[9],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Non-specified
energy_use(economy = '17_SIN', sub1sectors = ind1[2], sub2sectors = ind2[10],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Non-energy
nonenergy_use(economy = '17_SIN', increment_ref = 0.003, increment_tgt = 0.006, 
              end_year = 2100)

##################################################################################
# Chinese Taipei
# Mining
energy_use(economy = '18_CT', sub1sectors = ind1[0], sub2sectors = 'x',
           increment_ref = 0.002, increment_tgt = 0.004,  end_year = 2100)

# Construction
energy_use(economy = '18_CT', sub1sectors = ind1[1], sub2sectors = 'x',
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Steel
energy_use(economy = '18_CT', sub1sectors = ind1[2], sub2sectors = ind2[0],
           increment_ref = 0.001, increment_tgt = 0.002, end_year = 2100)

# Chemicals
energy_use(economy = '18_CT', sub1sectors = ind1[2], sub2sectors = ind2[1],
           increment_ref = 0.002, increment_tgt = 0.004, end_year = 2100)

# Non-ferrous metals
energy_use(economy = '18_CT', sub1sectors = ind1[2], sub2sectors = ind2[2],
           increment_ref = 0.0025, increment_tgt = 0.005, end_year = 2100)

# Non-metallic mineral products
energy_use(economy = '18_CT', sub1sectors = ind1[2], sub2sectors = ind2[3],
           increment_ref = 0.001, increment_tgt = 0.002, end_year = 2100)

# Transportation equipment
energy_use(economy = '18_CT', sub1sectors = ind1[2], sub2sectors = ind2[4],
           increment_ref = 0.004, increment_tgt = 0.007, end_year = 2100)

# Machinery
energy_use(economy = '18_CT', sub1sectors = ind1[2], sub2sectors = ind2[5],
           increment_ref = 0.004, increment_tgt = 0.007, end_year = 2100)

# Food and beverage
energy_use(economy = '18_CT', sub1sectors = ind1[2], sub2sectors = ind2[6],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Pulp and paper
energy_use(economy = '18_CT', sub1sectors = ind1[2], sub2sectors = ind2[7],
           increment_ref = 0.0025, increment_tgt = 0.005, end_year = 2100)

# Wood and wood products
energy_use(economy = '18_CT', sub1sectors = ind1[2], sub2sectors = ind2[8],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Textiles
energy_use(economy = '18_CT', sub1sectors = ind1[2], sub2sectors = ind2[9],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Non-specified
energy_use(economy = '18_CT', sub1sectors = ind1[2], sub2sectors = ind2[10],
           increment_ref = 0.003, increment_tgt = 0.006, end_year = 2100)

# Non-energy
nonenergy_use(economy = '18_CT', increment_ref = 0.0025, increment_tgt = 0.005, 
              end_year = 2100)

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

##################################################################################
# Viet Nam
# Mining
energy_use(economy = '21_VN', sub1sectors = ind1[0], sub2sectors = 'x',
           increment_ref = 0.002, increment_tgt = 0.004, start_year = 2025, end_year = 2100)

# Construction
energy_use(economy = '21_VN', sub1sectors = ind1[1], sub2sectors = 'x',
           increment_ref = 0.003, increment_tgt = 0.006, start_year = 2025, end_year = 2100)

# Steel
energy_use(economy = '21_VN', sub1sectors = ind1[2], sub2sectors = ind2[0],
           increment_ref = 0.0015, increment_tgt = 0.0025, start_year = 2025, end_year = 2100)

# Chemicals
energy_use(economy = '21_VN', sub1sectors = ind1[2], sub2sectors = ind2[1],
           increment_ref = 0.0025, increment_tgt = 0.005, start_year = 2025, end_year = 2100)

# Non-ferrous metals: no data
# energy_use(economy = '21_VN', sub1sectors = ind1[2], sub2sectors = ind2[2],
#            increment_ref = 0.003, increment_tgt = 0.006, start_year = 2025, end_year = 2100)

# Non-metallic mineral products
energy_use(economy = '21_VN', sub1sectors = ind1[2], sub2sectors = ind2[3],
           increment_ref = 0.0025, increment_tgt = 0.005, start_year = 2025, end_year = 2100)

# Transportation equipment
energy_use(economy = '21_VN', sub1sectors = ind1[2], sub2sectors = ind2[4],
           increment_ref = 0.005, increment_tgt = 0.0075, start_year = 2025, end_year = 2100)

# Machinery
energy_use(economy = '21_VN', sub1sectors = ind1[2], sub2sectors = ind2[5],
           increment_ref = 0.005, increment_tgt = 0.0075, start_year = 2025, end_year = 2100)

# Food and beverage
energy_use(economy = '21_VN', sub1sectors = ind1[2], sub2sectors = ind2[6],
           increment_ref = 0.004, increment_tgt = 0.008, start_year = 2025, end_year = 2100)

# Pulp and paper
energy_use(economy = '21_VN', sub1sectors = ind1[2], sub2sectors = ind2[7],
           increment_ref = 0.003, increment_tgt = 0.006, start_year = 2025, end_year = 2100)

# Wood and wood products
energy_use(economy = '21_VN', sub1sectors = ind1[2], sub2sectors = ind2[8],
           increment_ref = 0.003, increment_tgt = 0.006, start_year = 2025, end_year = 2100)

# Textiles
energy_use(economy = '21_VN', sub1sectors = ind1[2], sub2sectors = ind2[9],
           increment_ref = 0.003, increment_tgt = 0.006, start_year = 2025, end_year = 2100)

# Non-specified
energy_use(economy = '21_VN', sub1sectors = ind1[2], sub2sectors = ind2[10],
           increment_ref = 0.005, increment_tgt = 0.0075, start_year = 2025, end_year = 2100)

# Non-energy
nonenergy_use(economy = '21_VN', increment_ref = 0.0025, increment_tgt = 0.005, 
              start_year = 2025, end_year = 2100)

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