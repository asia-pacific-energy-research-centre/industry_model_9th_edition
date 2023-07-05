# Run the fuel switch model for economies import os
import re

wanted_wd = 'industry_model_9th_edition'
os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

# execute config file
config_file = './config/config_apr2023.py'
with open(config_file) as infile:
    exec(infile.read())

# Import function
from f2_fuel_switch_function import fuel_switch

# Energy industry subsectors
industry_sectors = pd.read_csv('./data/EGEDA/industry_egeda.csv', header = None)\
    .squeeze().to_dict()

ind1 = list(industry_sectors.values())[:3]
ind2 = list(industry_sectors.values())[3:]

# Only use 21 APEC economies (economy_list defined in config file)
economy_select = economy_list[:-7]

# Modelled years
proj_years = list(range(2021, 2101, 1))

# Vectors for switching
# don't electrify
no_elec = ['12_solar', '17_electricity', '18_heat']
# biomass doesnt switch for the below fuels 
no_biomass = ['12_solar', '15_solid_biomass', '17_electricity', '18_heat']
# To gas (from coal); aka these fuels dont get switched from:
to_gas = ['06_crude_oil_and_ngl', '07_petroleum_products', '08_gas', '12_solar', '15_solid_biomass',
          '16_others', '17_electricity', '18_heat']

# Run the function for the different economies
##################################################################################################################
# Thailand
# Mining
fuel_switch(economy = '19_THA', sector = ind1[0])

# Construction
fuel_switch(economy = '19_THA', sector = ind1[1])

# Iron and steel
fuel_switch(economy = '19_THA', sector = ind2[0])

# Chemicals
fuel_switch(economy = '19_THA', sector = ind2[1])

# Non-ferrous metals
fuel_switch(economy = '19_THA', sector = ind2[2])

# Non-metallic minerals
fuel_switch(economy = '19_THA', sector = ind2[3])

# Transport
fuel_switch(economy = '19_THA', sector = ind2[4])

# Machinery
fuel_switch(economy = '19_THA', sector = ind2[5])

# Food and Beverages
fuel_switch(economy = '19_THA', sector = ind2[6])

# Pulp and paper
fuel_switch(economy = '19_THA', sector = ind2[7])

# Wood
fuel_switch(economy = '19_THA', sector = ind2[8])

# Textiles
fuel_switch(economy = '19_THA', sector = ind2[9])

# Non-specified
fuel_switch(economy = '19_THA', sector = ind2[10])