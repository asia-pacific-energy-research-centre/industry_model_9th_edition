# Run the fuel switch model for economies import os
import re

wanted_wd = 'industry_model_9th_edition'
os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

# execute config file
config_file = './config/config_apr2023.py'
with open(config_file) as infile:
    exec(infile.read())

# Import function
from f2_fuel_switch_function import fuel_switch, hydrogen
from f3_non_energy_switch_function import fuel_switch_ne

# Energy industry subsectors
industry_sectors = pd.read_csv('./data/EGEDA/industry_egeda.csv', header = None)\
    .squeeze().to_dict()

ind1 = list(industry_sectors.values())[:3]
ind2 = list(industry_sectors.values())[3:]

# Only use 21 APEC economies (economy_list defined in config file)
economy_select = economy_list[:-7]

# Modelled years
proj_years = list(range(2022, 2101, 1))

# Historical energy data
hist_egeda = pd.read_csv(latest_EGEDA).loc[:, :'2021']

hist_egeda = hist_egeda.drop(columns = ['is_subtotal']).copy().reset_index(drop = True)

# PHL SGP edit
hist_egeda = hist_egeda.replace({'15_PHL': '15_RP',
                                 '17_SGP': '17_SIN'})

# Vectors for switching
# don't electrify
no_elec = ['11_geothermal', '12_solar', '17_electricity', '18_heat']
# biomass doesnt switch for the below fuels 
no_biomass = ['11_geothermal', '12_solar', '15_solid_biomass', '17_electricity', '18_heat']
# To gas (from coal); aka these fuels dont get switched from:
to_gas = ['06_crude_oil_and_ngl', '07_petroleum_products', '08_gas', '12_solar', '15_solid_biomass',
          '16_others', '17_electricity', '18_heat']

# CCS fuels
ccs_fuels = ['01_coal', '02_coal_products', '08_gas']

# Run the function for the different economies 

###########################################################################################################
# Australia
# Mining
fuel_switch(economy = '01_AUS', sector = ind1[0], elec_rate_tgt = 0.01, c2g_rate_ref = 0.0005, 
            c2g_rate_tgt = 0.0005)

# Construction
fuel_switch(economy = '01_AUS', sector = ind1[1], elec_rate_tgt = 0.011, c2g_rate_ref = 0.0005,
            c2g_rate_tgt = 0.0005, elec_start_ref = 2024, elec_start_tgt = 2024)

# Iron and steel
fuel_switch(economy = '01_AUS', sector = ind2[0], elec_rate_ref = 0.005, elec_rate_tgt = 0.04, 
            elec_start_tgt = 2025, hydrogen_ref = True, ccs_ref = False, hydrogen_tgt = True, ccs_tgt = False, 
            hyd_increment_tgt = 0.02, c2g_rate_ref = 0.001, hyd_fuel_mix = {'16_x_hydrogen': 0.6, '17_electricity': 0.4}, 
            hyd_only_tgt = True, hyd_only_year = 2030)

# # No green steel
# fuel_switch(economy = '01_AUS', sector = ind2[0], elec_rate_ref = 0.005, elec_rate_tgt = 0.0075, 
#             hydrogen_ref = True, ccs_ref = False, hydrogen_tgt = True, ccs_tgt = False, 
#             hyd_increment_tgt = 0.02, c2g_rate_ref = 0.001, c2g_rate_tgt = 0.01)

# Chemicals
fuel_switch(economy = '01_AUS', sector = ind2[1], elec_rate_ref = 0.002, elec_rate_tgt = 0.004,
            hydrogen_ref = False, hydrogen_tgt = True, ccs_ref = True, ccs_tgt = True,
            hyd_start_tgt = 2030, hyd_increment_tgt = 0.004, hyd_fuel_mix = {'16_x_hydrogen': 1.0, '17_electricity': 0.0},
            c2g_rate_tgt = 0.01)

# Non-ferrous metals
fuel_switch(economy = '01_AUS', sector = ind2[2], elec_rate_tgt = 0.01, c2g_rate_ref = 0.001, 
            c2g_rate_tgt = 0.0055)

# Non-metallic minerals
fuel_switch(economy = '01_AUS', sector = ind2[3], elec_rate_ref = 0.0015, elec_rate_tgt = 0.005, 
            ccs_ref = True, ccs_tgt = True, c2g_rate_tgt = 0.004, hydrogen_tgt = True,
            bio_start_ref = 2025, bio_start_tgt = 2025, bio_rate_ref = 0.002, bio_rate_tgt = 0.008,
            hyd_start_tgt = 2030, hyd_increment_tgt = 0.001, hyd_fuel_mix = {'16_x_hydrogen': 1.0, '17_electricity': 0.0})

# Transport
fuel_switch(economy = '01_AUS', sector = ind2[4], elec_rate_ref = 0.003, elec_rate_tgt = 0.006)

# Machinery
fuel_switch(economy = '01_AUS', sector = ind2[5], elec_rate_ref = 0.003, elec_rate_tgt = 0.01)

# Food and Beverages
fuel_switch(economy = '01_AUS', sector = ind2[6], elec_rate_tgt = 0.01, bio_rate_tgt = 0.005)

# Pulp and paper
fuel_switch(economy = '01_AUS', sector = ind2[7], elec_rate_ref = 0.0025, elec_rate_tgt = 0.011, 
            bio_rate_tgt = 0.015)

# Wood
fuel_switch(economy = '01_AUS', sector = ind2[8], bio_rate_tgt = 0.002)

# Textiles
fuel_switch(economy = '01_AUS', sector = ind2[9], elec_rate_ref = 0.003, elec_rate_tgt = 0.02)

# Non-specified
fuel_switch(economy = '01_AUS', sector = ind2[10], elec_rate_tgt = 0.021, bio_start_tgt = 2025,
            bio_rate_tgt = 0.021)

# Non-energy
fuel_switch_ne(economy = '01_AUS', hyd_increment_ref = 0.002, hyd_increment_tgt = 0.005, 
               gas_switch_ref = False, gas_switch_tgt = False)

##################################################################################################################
# Brunei
# Mining: no data

# Chemicals
fuel_switch(economy = '02_BD', sector = ind2[1], elec_rate_ref = 0.002, elec_rate_tgt = 0.004,
            hydrogen_ref = False, hydrogen_tgt = False, ccs_ref = False, ccs_tgt = False,
            hyd_start_tgt = 2030, hyd_increment_tgt = 0.004, hyd_fuel_mix = {'16_x_hydrogen': 1.0, '17_electricity': 0.0})

# Non-specified
fuel_switch(economy = '02_BD', sector = ind2[10], elec_rate_tgt = 0.01, c2g_rate_ref = 0.002, 
            c2g_rate_tgt = 0.008, c2g_start_ref = 2027, c2g_start_tgt = 2027)

# Non-energy
fuel_switch_ne(economy = '02_BD', hyd_increment_ref = 0.0, hyd_increment_tgt = 0.0, 
               gas_switch_ref = False, gas_switch_tgt = False)

###########################################################################################################
# Canada
# Mining
fuel_switch(economy = '03_CDA', sector = ind1[0], c2g_rate_ref = 0.001, c2g_rate_tgt = 0.002)

# Construction
fuel_switch(economy = '03_CDA', sector = ind1[1], c2g_rate_ref = 0.001, c2g_rate_tgt = 0.0025, 
            elec_start_ref = 2024, elec_start_tgt = 2024)

# Iron and steel
fuel_switch(economy = '03_CDA', sector = ind2[0], elec_rate_ref = 0.005, elec_rate_tgt = 0.0075, 
            hydrogen_ref = True, ccs_ref = False, hydrogen_tgt = True, ccs_tgt = False, 
            hyd_increment_tgt = 0.02, c2g_rate_ref = 0.001, c2g_rate_tgt = 0.01)

# Chemicals
fuel_switch(economy = '03_CDA', sector = ind2[1], elec_rate_ref = 0.002, elec_rate_tgt = 0.004,
            hydrogen_ref = False, hydrogen_tgt = True, ccs_ref = True, ccs_tgt = True,
            hyd_start_tgt = 2030, hyd_increment_tgt = 0.001, hyd_fuel_mix = {'16_x_hydrogen': 1.0, '17_electricity': 0.0})

# Non-ferrous metals
fuel_switch(economy = '03_CDA', sector = ind2[2], elec_rate_tgt = 0.006, c2g_rate_ref = 0.001, 
            c2g_rate_tgt = 0.001)

# Non-metallic minerals
fuel_switch(economy = '03_CDA', sector = ind2[3], elec_rate_ref = 0.0015, elec_rate_tgt = 0.003, 
            ccs_ref = True, ccs_tgt = True, c2g_rate_tgt = 0.004, hydrogen_tgt = True, 
            hyd_start_tgt = 2030, hyd_increment_tgt = 0.002, hyd_fuel_mix = {'16_x_hydrogen': 1.0, '17_electricity': 0.0})

# Transport
fuel_switch(economy = '03_CDA', sector = ind2[4], elec_rate_ref = 0.003, elec_rate_tgt = 0.006)

# Machinery
fuel_switch(economy = '03_CDA', sector = ind2[5], elec_rate_ref = 0.003, elec_rate_tgt = 0.005)

# Food and Beverages
fuel_switch(economy = '03_CDA', sector = ind2[6], elec_rate_tgt = 0.0075)

# Pulp and paper
fuel_switch(economy = '03_CDA', sector = ind2[7], elec_rate_ref = 0.0025, elec_rate_tgt = 0.008, 
            bio_rate_tgt = 0.006)

# Wood
fuel_switch(economy = '03_CDA', sector = ind2[8], bio_rate_tgt = 0.002)

# Textiles
fuel_switch(economy = '03_CDA', sector = ind2[9], elec_rate_ref = 0.003, elec_rate_tgt = 0.0075)

# Non-specified
fuel_switch(economy = '03_CDA', sector = ind2[10], elec_rate_tgt = 0.01)

# Non-energy
fuel_switch_ne(economy = '03_CDA', hyd_increment_ref = 0.002, hyd_increment_tgt = 0.005, 
               gas_switch_ref = False, gas_switch_tgt = False)

###########################################################################################################
# Chile
# Mining
fuel_switch(economy = '04_CHL', sector = ind1[0], elec_rate_tgt = 0.008, c2g_rate_ref = 0.0005, 
            c2g_rate_tgt = 0.0005)

# Construction
fuel_switch(economy = '04_CHL', sector = ind1[1], elec_rate_tgt = 0.01, c2g_rate_ref = 0.0005,
            c2g_rate_tgt = 0.004, elec_start_ref = 2024, elec_start_tgt = 2024)

# Iron and steel
fuel_switch(economy = '04_CHL', sector = ind2[0], elec_rate_ref = 0.005, elec_rate_tgt = 0.01, 
            hydrogen_ref = True, ccs_ref = False, hydrogen_tgt = True, ccs_tgt = False, 
            hyd_increment_tgt = 0.0175, c2g_rate_ref = 0.001, c2g_rate_tgt = 0.01)

# Chemicals
fuel_switch(economy = '04_CHL', sector = ind2[1], elec_rate_ref = 0.003, elec_rate_tgt = 0.006,
            hydrogen_ref = False, hydrogen_tgt = True, ccs_ref = False, ccs_tgt = False,
            ccs_increment_tgt = 0.01,
            hyd_start_tgt = 2030, hyd_increment_tgt = 0.003, hyd_fuel_mix = {'16_x_hydrogen': 1.0, '17_electricity': 0.0})

# Non-ferrous metals: no data

# Non-metallic minerals
fuel_switch(economy = '04_CHL', sector = ind2[3], elec_rate_ref = 0.0015, elec_rate_tgt = 0.0075, 
            ccs_ref = False, ccs_tgt = False, c2g_rate_tgt = 0.009, hydrogen_tgt = True,
            ccs_increment_tgt = 0.01, c2g_rate_ref = 0.002,
            hyd_start_tgt = 2030, hyd_increment_tgt = 0.002, hyd_fuel_mix = {'16_x_hydrogen': 1.0, '17_electricity': 0.0})

# Transport: no data

# Machinery: no data

# Food and Beverages
fuel_switch(economy = '04_CHL', sector = ind2[6], elec_rate_ref = 0.005, elec_rate_tgt = 0.01, c2g_rate_tgt = 0.005,
            bio_start_tgt = 2025, bio_rate_tgt = 0.004)

# Pulp and paper
fuel_switch(economy = '04_CHL', sector = ind2[7], elec_rate_ref = 0.0025, elec_rate_tgt = 0.008, 
            bio_rate_ref = 0.001, bio_rate_tgt = 0.003)

# Wood: no data

# Textiles: no data

# Non-specified
fuel_switch(economy = '04_CHL', sector = ind2[10], elec_rate_tgt = 0.011, bio_start_tgt = 2025, bio_rate_tgt = 0.005,
            c2g_rate_tgt = 0.004)

# Non-energy
fuel_switch_ne(economy = '04_CHL', hyd_increment_ref = 0.002, hyd_increment_tgt = 0.005, 
               gas_switch_ref = False, gas_switch_tgt = False)

###########################################################################################################
# China
# Mining
fuel_switch(economy = '05_PRC', sector = ind1[0], elec_rate_tgt = 0.011, c2g_rate_ref = 0.0005, c2g_rate_tgt = 0.0005)

# Construction
fuel_switch(economy = '05_PRC', sector = ind1[1], elec_rate_tgt = 0.008, c2g_rate_ref = 0.0005, 
            elec_start_ref = 2024, elec_start_tgt = 2024)

# Iron and steel
fuel_switch(economy = '05_PRC', sector = ind2[0], elec_rate_ref = 0.005, elec_rate_tgt = 0.01, 
            hydrogen_ref = True, ccs_ref = True, hydrogen_tgt = True, ccs_tgt = True, 
            hyd_increment_tgt = 0.0175, c2g_rate_ref = 0.001, c2g_rate_tgt = 0.01)

# Chemicals
fuel_switch(economy = '05_PRC', sector = ind2[1], elec_rate_ref = 0.003, elec_rate_tgt = 0.006,
            hydrogen_ref = False, hydrogen_tgt = True, ccs_ref = True, ccs_tgt = True,
            ccs_increment_tgt = 0.01,
            hyd_start_tgt = 2030, hyd_increment_tgt = 0.003, hyd_fuel_mix = {'16_x_hydrogen': 1.0, '17_electricity': 0.0})

# Non-ferrous metals
fuel_switch(economy = '05_PRC', sector = ind2[2], elec_rate_tgt = 0.0075, c2g_rate_ref = 0.001, 
            c2g_rate_tgt = 0.001)

# Non-metallic minerals
fuel_switch(economy = '05_PRC', sector = ind2[3], elec_rate_ref = 0.0015, elec_rate_tgt = 0.0075, 
            ccs_ref = True, ccs_tgt = True, c2g_rate_tgt = 0.009, hydrogen_tgt = True,
            bio_start_ref = 2025, bio_start_tgt = 2025, bio_rate_ref = 0.002, bio_rate_tgt = 0.006,
            ccs_increment_tgt = 0.01, c2g_rate_ref = 0.002,
            hyd_start_tgt = 2030, hyd_increment_tgt = 0.005, hyd_fuel_mix = {'16_x_hydrogen': 1.0, '17_electricity': 0.0})

# Transport
fuel_switch(economy = '05_PRC', sector = ind2[4], elec_rate_ref = 0.004, elec_rate_tgt = 0.007)

# Machinery
fuel_switch(economy = '05_PRC', sector = ind2[5], elec_rate_ref = 0.003, elec_rate_tgt = 0.005)

# Food and Beverages
fuel_switch(economy = '05_PRC', sector = ind2[6], elec_rate_ref = 0.005, elec_rate_tgt = 0.01, c2g_rate_tgt = 0.001)

# Pulp and paper
fuel_switch(economy = '05_PRC', sector = ind2[7], elec_rate_ref = 0.0025, elec_rate_tgt = 0.008, 
            bio_rate_ref = 0.001, bio_rate_tgt = 0.001)

# Wood
fuel_switch(economy = '05_PRC', sector = ind2[8], bio_rate_tgt = 0.001)

# Textiles
fuel_switch(economy = '05_PRC', sector = ind2[9], elec_rate_ref = 0.003, elec_rate_tgt = 0.0075)

# Non-specified
fuel_switch(economy = '05_PRC', sector = ind2[10], elec_rate_tgt = 0.01)

# Non-energy
fuel_switch_ne(economy = '05_PRC', hyd_increment_ref = 0.002, hyd_increment_tgt = 0.005, 
               gas_switch_ref = False, gas_switch_tgt = False)

###########################################################################################################
# Hong Kong
# Transport
fuel_switch(economy = '06_HKC', sector = ind2[4], elec_rate_ref = 0.005, elec_rate_tgt = 0.01)

# Non-specified
fuel_switch(economy = '06_HKC', sector = ind2[10], elec_rate_tgt = 0.01)

# Non-energy: no data

##################################################################################################################
# Indonesia
# Mining: no mining data
# fuel_switch(economy = '07_INA', sector = ind1[0], elec_rate_tgt = 0.011, c2g_rate_ref = 0.0005, 
#             c2g_rate_tgt = 0.0005)

# Construction: no construction data
# fuel_switch(economy = '07_INA', sector = ind1[1], elec_rate_tgt = 0.01, c2g_rate_ref = 0.0005,
#             c2g_rate_tgt = 0.0005, elec_start_ref = 2024, elec_start_tgt = 2024)

# Iron and steel
fuel_switch(economy = '07_INA', sector = ind2[0], elec_rate_ref = 0.005, elec_rate_tgt = 0.01, 
            hydrogen_ref = False, ccs_ref = False, hydrogen_tgt = True, ccs_tgt = True, ccs_start_tgt = 2035,
            hyd_start_ref = 2045, hyd_start_tgt = 2030, hyd_increment_ref = 0.005, hyd_increment_tgt = 0.01, 
            c2g_rate_ref = 0.0005, c2g_rate_tgt = 0.0075)

# Chemicals
fuel_switch(economy = '07_INA', sector = ind2[1], elec_rate_ref = 0.002, elec_rate_tgt = 0.004,
            hydrogen_ref = False, hydrogen_tgt = True, ccs_ref = False, ccs_tgt = True, ccs_start_tgt = 2035,
            hyd_start_tgt = 2030, hyd_increment_ref = 0.002, hyd_increment_tgt = 0.004, 
            hyd_fuel_mix = {'16_x_hydrogen': 1.0, '17_electricity': 0.0}, c2g_rate_tgt = 0.01)

# Non-ferrous metals: no non-ferrous metals data
# fuel_switch(economy = '07_INA', sector = ind2[2], elec_rate_tgt = 0.014, c2g_rate_ref = 0.001, 
#             c2g_rate_tgt = 0.0011)

# Non-metallic minerals
fuel_switch(economy = '07_INA', sector = ind2[3], elec_rate_ref = 0.001, elec_rate_tgt = 0.002, 
            ccs_ref = False, ccs_tgt = True, c2g_rate_tgt = 0.01, hydrogen_tgt = True, ccs_start_tgt = 2035,  
            bio_start_tgt = 2025, bio_rate_tgt = 0.01, hyd_start_tgt = 2030, hyd_increment_tgt = 0.001, 
            hyd_fuel_mix = {'16_x_hydrogen': 1.0, '17_electricity': 0.0})

# Transport: no data
# fuel_switch(economy = '07_INA', sector = ind2[4], elec_rate_ref = 0.003, elec_rate_tgt = 0.006)

# Machinery: no data
# fuel_switch(economy = '07_INA', sector = ind2[5], elec_rate_ref = 0.003, elec_rate_tgt = 0.01)

# Food and Beverages
fuel_switch(economy = '07_INA', sector = ind2[6], elec_rate_tgt = 0.01, elec_start_ref = 2030, elec_start_tgt = 2025)

# Pulp and paper
fuel_switch(economy = '07_INA', sector = ind2[7], elec_rate_ref = 0.0025, elec_rate_tgt = 0.011, 
            bio_rate_tgt = 0.015, c2g_start_tgt = 2030, c2g_rate_tgt = 0.005)

# Wood
fuel_switch(economy = '07_INA', sector = ind2[8], elec_start_ref = 2030, elec_start_tgt = 2025)

# Textiles
fuel_switch(economy = '07_INA', sector = ind2[9], elec_start_ref = 2030, elec_start_tgt = 2025, elec_rate_ref = 0.003, elec_rate_tgt = 0.01)

# Non-specified
fuel_switch(economy = '07_INA', sector = ind2[10], elec_rate_ref = 0.003, elec_rate_tgt = 0.006, bio_start_tgt = 2025, c2g_rate_tgt = 0.0005)

# Non-energy
fuel_switch_ne(economy = '07_INA', hyd_increment_ref = 0.001, hyd_increment_tgt = 0.005, 
               gas_switch_ref = False, gas_switch_tgt = False)

##################################################################################################################
# Japan
# Mining
fuel_switch(economy = '08_JPN', sector = ind1[0])

# Construction
fuel_switch(economy = '08_JPN', sector = ind1[1])

# Iron and steel
fuel_switch(economy = '08_JPN', sector = ind2[0], elec_rate_ref = 0.001, elec_rate_tgt = 0.005, 
            hydrogen_ref = True, ccs_ref = False, hydrogen_tgt = True, hyd_start_tgt = 2030, hyd_increment_tgt = 0.012,
            ccs_tgt = True, c2g_rate_tgt = 0.003, hyd_fuel_mix = {'16_x_hydrogen': 0.6, '17_electricity': 0.4}) 

# Chemicals
fuel_switch(economy = '08_JPN', sector = ind2[1], elec_rate_ref = 0.0025, elec_rate_tgt = 0.005,
            hydrogen_ref = False, hydrogen_tgt = True, ccs_ref = False, ccs_tgt = True, c2g_rate_tgt = 0.001, 
            hyd_start_tgt = 2030, hyd_increment_tgt = 0.002, hyd_fuel_mix = {'16_x_hydrogen': 1.0, '17_electricity': 0.0})

# Non-ferrous metals
fuel_switch(economy = '08_JPN', sector = ind2[2], c2g_rate_tgt = 0.001)

# Non-metallic minerals
fuel_switch(economy = '08_JPN', sector = ind2[3], elec_rate_ref = 0.0015, elec_rate_tgt = 0.003, 
            bio_rate_tgt = 0.001, ccs_tgt = True, c2g_rate_tgt = 0.002, hydrogen_tgt = True, hyd_start_tgt = 2030, 
            hyd_increment_tgt = 0.001, hyd_fuel_mix = {'16_x_hydrogen': 1.0, '17_electricity': 0.0})

# Transport
fuel_switch(economy = '08_JPN', sector = ind2[4], c2g_rate_tgt = 0.002)

# Machinery
fuel_switch(economy = '08_JPN', sector = ind2[5], c2g_rate_tgt = 0.001)

# Food and Beverages
fuel_switch(economy = '08_JPN', sector = ind2[6], elec_rate_tgt = 0.0065, c2g_rate_tgt = 0.002)

# Pulp and paper
fuel_switch(economy = '08_JPN', sector = ind2[7], elec_rate_ref = 0.0025, elec_rate_tgt = 0.008, 
            bio_rate_tgt = 0.008, c2g_rate_tgt = 0.002)

# Wood
fuel_switch(economy = '08_JPN', sector = ind2[8], c2g_rate_tgt = 0.001)

# Textiles
fuel_switch(economy = '08_JPN', sector = ind2[9], elec_rate_ref = 0.003, elec_rate_tgt = 0.01)

# Non-specified
fuel_switch(economy = '08_JPN', sector = ind2[10], elec_rate_tgt = 0.01)

# Non-energy
fuel_switch_ne(economy = '08_JPN', hyd_increment_ref = 0.002, hyd_increment_tgt = 0.005,
               gas_switch_ref = False, gas_switch_tgt = False)

###########################################################################################################
# Korea
# Mining
fuel_switch(economy = '09_ROK', sector = ind1[0], elec_start_ref = 2025, elec_start_tgt = 2025,  
            elec_rate_ref = 0.002, elec_rate_tgt = 0.004)

# Construction
fuel_switch(economy = '09_ROK', sector = ind1[1], elec_start_ref = 2025, 
            elec_start_tgt = 2025, elec_rate_ref = 0.002, elec_rate_tgt = 0.008)

# Iron and steel
fuel_switch(economy = '09_ROK', sector = ind2[0], elec_rate_ref = 0.005, elec_rate_tgt = 0.01, 
            hydrogen_ref = True, ccs_ref = False, hydrogen_tgt = True, ccs_tgt = True, 
            hyd_increment_tgt = 0.012, c2g_rate_ref = 0.001, c2g_rate_tgt = 0.0075)

# Chemicals
fuel_switch(economy = '09_ROK', sector = ind2[1], elec_rate_ref = 0.002, elec_rate_tgt = 0.007,
            hydrogen_ref = False, hydrogen_tgt = True, ccs_ref = False, ccs_tgt = True,
            c2g_rate_ref = 0.001, c2g_rate_tgt = 0.003, 
            hyd_start_tgt = 2030, hyd_increment_tgt = 0.002, hyd_fuel_mix = {'16_x_hydrogen': 1.0, '17_electricity': 0.0})

# Non-ferrous metals
fuel_switch(economy = '09_ROK', sector = ind2[2], elec_rate_tgt = 0.007, c2g_rate_ref = 0.001)

# Non-metallic minerals
fuel_switch(economy = '09_ROK', sector = ind2[3], elec_rate_ref = 0.0015, elec_rate_tgt = 0.003, 
            ccs_ref = False, ccs_tgt = True, c2g_rate_tgt = 0.005, hydrogen_tgt = True,
            bio_start_tgt = 2025, bio_rate_tgt = 0.005,
            hyd_start_tgt = 2030, hyd_increment_tgt = 0.002, hyd_fuel_mix = {'16_x_hydrogen': 1.0, '17_electricity': 0.0})

# Transport
fuel_switch(economy = '09_ROK', sector = ind2[4], elec_rate_ref = 0.003, elec_rate_tgt = 0.004)

# Machinery
fuel_switch(economy = '09_ROK', sector = ind2[5], elec_rate_ref = 0.002, elec_rate_tgt = 0.003)

# Food and Beverages
fuel_switch(economy = '09_ROK', sector = ind2[6], elec_rate_tgt = 0.0075)

# Pulp and paper
fuel_switch(economy = '09_ROK', sector = ind2[7], elec_rate_ref = 0.0025, elec_rate_tgt = 0.008, 
            bio_rate_tgt = 0.006)

# Wood
fuel_switch(economy = '09_ROK', sector = ind2[8], bio_rate_tgt = 0.001)

# Textiles
fuel_switch(economy = '09_ROK', sector = ind2[9], elec_rate_ref = 0.003, elec_rate_tgt = 0.008)

# Non-specified
fuel_switch(economy = '09_ROK', sector = ind2[10], elec_rate_tgt = 0.01, c2g_rate_tgt = 0.006)

# Non-energy
fuel_switch_ne(economy = '09_ROK', hyd_increment_ref = 0.002, hyd_increment_tgt = 0.005, 
               gas_switch_ref = False, gas_switch_tgt = False)

###########################################################################################################
# Malaysia
# Non-specified
fuel_switch(economy = '10_MAS', sector = ind2[10], elec_rate_ref = 0.003, elec_rate_tgt = 0.006,
            bio_rate_ref = 0.001, bio_rate_tgt = 0.002, bio_start_ref = 2025, bio_start_tgt = 2025)

# Non-energy
fuel_switch_ne(economy = '10_MAS', hyd_increment_ref = 0.002, hyd_increment_tgt = 0.005, 
               gas_switch_ref = False, gas_switch_tgt = False)

###########################################################################################################
# Mexico
# Mining
fuel_switch(economy = '11_MEX', sector = ind1[0], elec_rate_ref = 0.001, elec_rate_tgt = 0.003, c2g_rate_ref = 0.0005, 
            c2g_rate_tgt = 0.001)

# Construction
fuel_switch(economy = '11_MEX', sector = ind1[1], elec_rate_ref = 0.001, elec_rate_tgt = 0.004, 
            elec_start_ref = 2024, elec_start_tgt = 2024)

# Iron and steel
fuel_switch(economy = '11_MEX', sector = ind2[0], elec_rate_ref = 0.001, elec_rate_tgt = 0.002, 
            hydrogen_ref = False, ccs_ref = False, hydrogen_tgt = False, ccs_tgt = False, 
            hyd_increment_tgt = 0.011, c2g_rate_ref = 0.001, c2g_rate_tgt = 0.002)

# Chemicals
fuel_switch(economy = '11_MEX', sector = ind2[1], elec_rate_ref = 0.00, elec_rate_tgt = 0.001,
            hydrogen_ref = False, hydrogen_tgt = False, ccs_ref = False, ccs_tgt = False,
            ccs_increment_tgt = 0.01,
            hyd_start_tgt = 2030, hyd_increment_tgt = 0.003, hyd_fuel_mix = {'16_x_hydrogen': 1.0, '17_electricity': 0.0})

# Non-ferrous metals
fuel_switch(economy = '11_MEX', sector = ind2[2], elec_rate_tgt = 0.0075)

# Non-metallic minerals
fuel_switch(economy = '11_MEX', sector = ind2[3], elec_rate_ref = 0.001, elec_rate_tgt = 0.002, 
            ccs_ref = False, ccs_tgt = False, c2g_rate_tgt = 0.009, hydrogen_tgt = False,
            ccs_increment_tgt = 0.01, c2g_rate_ref = 0.002,
            hyd_start_tgt = 2030, hyd_increment_tgt = 0.002, hyd_fuel_mix = {'16_x_hydrogen': 1.0, '17_electricity': 0.0})

# Transport
fuel_switch(economy = '11_MEX', sector = ind2[4], elec_rate_ref = 0.001, elec_rate_tgt = 0.002)

# Machinery
fuel_switch(economy = '11_MEX', sector = ind2[5], elec_rate_ref = 0.00, elec_rate_tgt = 0.001)

# Food and Beverages
fuel_switch(economy = '11_MEX', sector = ind2[6], elec_rate_ref = 0.001, elec_rate_tgt = 0.003, c2g_rate_tgt = 0.001)

# Pulp and paper
fuel_switch(economy = '11_MEX', sector = ind2[7], elec_rate_ref = 0.002, elec_rate_tgt = 0.003)

# Wood: no data

# Textiles
fuel_switch(economy = '11_MEX', sector = ind2[9], elec_rate_ref = 0.00, elec_rate_tgt = 0.00)

# Non-specified
fuel_switch(economy = '11_MEX', sector = ind2[10], elec_rate_ref = 0.001, elec_rate_tgt = 0.002)

# Non-energy
fuel_switch_ne(economy = '11_MEX', hyd_increment_ref = 0.0, hyd_increment_tgt = 0.0, 
               gas_switch_ref = False, gas_switch_tgt = False)

###########################################################################################################
# New Zealand
# Mining
fuel_switch(economy = '12_NZ', sector = ind1[0], elec_rate_tgt = 0.014)

# Construction
fuel_switch(economy = '12_NZ', sector = ind1[1], elec_rate_tgt = 0.014, elec_start_ref = 2024, elec_start_tgt = 2024)

# Iron and steel
fuel_switch(economy = '12_NZ', sector = ind2[0], elec_rate_ref = 0.005, elec_rate_tgt = 0.02, 
            elec_start_tgt = 2024, hydrogen_ref = True, ccs_ref = False, hydrogen_tgt = True, ccs_tgt = False, 
            hyd_increment_tgt = 0.02, c2g_rate_ref = 0.001, hyd_fuel_mix = {'16_x_hydrogen': 0.2, '17_electricity': 0.9}, 
            hyd_only_tgt = True, hyd_only_year = 2032)

# Chemicals
fuel_switch(economy = '12_NZ', sector = ind2[1], elec_rate_ref = 0.002, elec_rate_tgt = 0.01,
            hydrogen_ref = False, hydrogen_tgt = True, ccs_ref = False, ccs_tgt = False,
            hyd_start_tgt = 2030, hyd_increment_tgt = 0.01, hyd_fuel_mix = {'16_x_hydrogen': 1.0, '17_electricity': 0.0})

# Non-ferrous metals
fuel_switch(economy = '12_NZ', sector = ind2[2], elec_rate_ref = 0.0001, elec_rate_tgt = 0.002)

# Non-metallic minerals
fuel_switch(economy = '12_NZ', sector = ind2[3], elec_rate_ref = 0.0015, elec_rate_tgt = 0.008, 
            ccs_ref = False, ccs_tgt = True, c2g_rate_tgt = 0.004, hydrogen_tgt = True,
            bio_start_ref = 2025, bio_start_tgt = 2025, bio_rate_ref = 0.002, bio_rate_tgt = 0.014,
            hyd_start_tgt = 2030, hyd_increment_tgt = 0.003, hyd_fuel_mix = {'16_x_hydrogen': 1.0, '17_electricity': 0.0})

# Transport
fuel_switch(economy = '12_NZ', sector = ind2[4], elec_rate_ref = 0.003, elec_rate_tgt = 0.015)

# Machinery
fuel_switch(economy = '12_NZ', sector = ind2[5], elec_rate_ref = 0.003, elec_rate_tgt = 0.01)

# Food and Beverages
fuel_switch(economy = '12_NZ', sector = ind2[6], elec_rate_tgt = 0.013, bio_rate_tgt = 0.012)

# Pulp and paper
fuel_switch(economy = '12_NZ', sector = ind2[7], elec_rate_ref = 0.005, elec_rate_tgt = 0.011, 
            bio_rate_ref = 0.005, bio_rate_tgt = 0.01)

# Wood
fuel_switch(economy = '12_NZ', sector = ind2[8])

# Textiles
fuel_switch(economy = '12_NZ', sector = ind2[9], elec_rate_ref = 0.004, elec_rate_tgt = 0.015)

# Non-specified
fuel_switch(economy = '12_NZ', sector = ind2[10], elec_rate_tgt = 0.01, bio_start_tgt = 2025, 
            bio_rate_tgt = 0.005)

# Non-energy
fuel_switch_ne(economy = '12_NZ', hyd_increment_ref = 0.002, hyd_increment_tgt = 0.005, 
               gas_switch_ref = False, gas_switch_tgt = False)

###########################################################################################################
# PNG
# Non-specified
fuel_switch(economy = '13_PNG', sector = ind2[10], elec_rate_ref = 0.0015, elec_rate_tgt = 0.003)

# Non-energy: no data

###########################################################################################################
# Peru
# Mining
fuel_switch(economy = '14_PE', sector = ind1[0], elec_rate_tgt = 0.005, c2g_rate_ref = 0.001)

# Non-specified
fuel_switch(economy = '14_PE', sector = ind2[10], elec_rate_tgt = 0.008, bio_rate_tgt = 0.002)

# Non-energy
fuel_switch_ne(economy = '14_PE', hyd_increment_ref = 0.002, hyd_increment_tgt = 0.005, 
               gas_switch_ref = False, gas_switch_tgt = False)

##################################################################################################################
# Philippines
# Mining
fuel_switch(economy = '15_RP', sector = ind1[0], elec_rate_ref = 0.001, elec_rate_tgt = 0.004)

# Construction
fuel_switch(economy = '15_RP', sector = ind1[1], elec_rate_ref = 0.001, elec_rate_tgt = 0.004, 
            elec_start_ref = 2024, elec_start_tgt = 2024)

# Iron and steel
fuel_switch(economy = '15_RP', sector = ind2[0], elec_rate_ref = 0.0002, elec_rate_tgt = 0.001, 
            elec_start_tgt = 2025, hydrogen_ref = False, ccs_ref = False, hydrogen_tgt = True, ccs_tgt = True, 
            hyd_start_tgt = 2035, hyd_increment_tgt = 0.003, c2g_rate_tgt = 0.002, 
            hyd_fuel_mix = {'16_x_hydrogen': 0.6, '17_electricity': 0.4})

# Chemicals
fuel_switch(economy = '15_RP', sector = ind2[1], elec_rate_ref = 0.0001, elec_rate_tgt = 0.001,
            hydrogen_ref = False, hydrogen_tgt = True, ccs_ref = False, ccs_tgt = True,
            hyd_start_tgt = 2032, hyd_increment_tgt = 0.001, hyd_fuel_mix = {'16_x_hydrogen': 1.0, '17_electricity': 0.0},
            c2g_rate_tgt = 0.002)

# Non-ferrous metals: no data

# Non-metallic minerals
fuel_switch(economy = '15_RP', sector = ind2[3], elec_rate_ref = 0.001, elec_rate_tgt = 0.002, 
            ccs_ref = False, ccs_tgt = True, c2g_rate_tgt = 0.001, hydrogen_ref = False, hydrogen_tgt = True, bio_start_tgt = 2025, 
            bio_rate_tgt = 0.001, hyd_start_tgt = 2030, hyd_increment_tgt = 0.0002, hyd_fuel_mix = {'16_x_hydrogen': 1.0, '17_electricity': 0.0})

# Transport
fuel_switch(economy = '15_RP', sector = ind2[4])

# Machinery
fuel_switch(economy = '15_RP', sector = ind2[5], elec_rate_ref = 0.0, elec_rate_tgt = 0.001)

# Food and Beverages
fuel_switch(economy = '15_RP', sector = ind2[6], elec_rate_tgt = 0.005, bio_rate_tgt = 0.0)

# Pulp and paper
fuel_switch(economy = '15_RP', sector = ind2[7], elec_rate_ref = 0.001, elec_rate_tgt = 0.004, 
            bio_rate_tgt = 0.002)

# Wood
fuel_switch(economy = '15_RP', sector = ind2[8], elec_rate_ref = 0.0, elec_rate_tgt = 0.002)

# Textiles
fuel_switch(economy = '15_RP', sector = ind2[9], elec_rate_ref = 0.001, elec_rate_tgt = 0.002)

# Non-specified
fuel_switch(economy = '15_RP', sector = ind2[10], elec_rate_ref = 0.002, elec_rate_tgt = 0.004, 
            bio_start_tgt = 2025, bio_rate_tgt = 0.001, c2g_rate_tgt = 0.001)

# Non-energy
fuel_switch_ne(economy = '15_RP', hyd_increment_ref = 0.001, hyd_increment_tgt = 0.003, 
               gas_switch_ref = False, gas_switch_tgt = False)

###########################################################################################################
# Russia
# Mining
fuel_switch(economy = '16_RUS', sector = ind1[0], elec_rate_ref = 0.0025, elec_rate_tgt = 0.005, 
            c2g_rate_ref = 0.0005, c2g_rate_tgt = 0.0005)

# Construction
fuel_switch(economy = '16_RUS', sector = ind1[1], elec_rate_tgt = 0.007, c2g_rate_ref = 0.0005,
            c2g_rate_tgt = 0.0005, elec_start_ref = 2024, elec_start_tgt = 2024)

# Iron and steel
fuel_switch(economy = '16_RUS', sector = ind2[0], elec_rate_ref = 0.002, elec_rate_tgt = 0.005, 
            elec_start_tgt = 2025, hydrogen_ref = True, ccs_ref = False, hydrogen_tgt = True, ccs_tgt = True, 
            hyd_increment_tgt = 0.0075, c2g_rate_ref = 0.004, c2g_rate_tgt = 0.01, hyd_fuel_mix = {'16_x_hydrogen': 0.6, '17_electricity': 0.4})

# Chemicals
fuel_switch(economy = '16_RUS', sector = ind2[1], elec_rate_ref = 0.002, elec_rate_tgt = 0.004,
            hydrogen_ref = False, hydrogen_tgt = True, ccs_ref = False, ccs_tgt = True,
            hyd_start_tgt = 2030, hyd_increment_tgt = 0.003, hyd_fuel_mix = {'16_x_hydrogen': 1.0, '17_electricity': 0.0},
            c2g_rate_tgt = 0.01)

# Non-ferrous metals
fuel_switch(economy = '16_RUS', sector = ind2[2])

# Non-metallic minerals
fuel_switch(economy = '16_RUS', sector = ind2[3], elec_rate_ref = 0.0015, elec_rate_tgt = 0.005, hydrogen_ref = False,
            ccs_ref = False, ccs_tgt = True, c2g_rate_tgt = 0.004, hydrogen_tgt = True,
            hyd_start_tgt = 2030, hyd_increment_tgt = 0.002, hyd_fuel_mix = {'16_x_hydrogen': 1.0, '17_electricity': 0.0})

# Transport
fuel_switch(economy = '16_RUS', sector = ind2[4], elec_rate_ref = 0.0025, elec_rate_tgt = 0.005)

# Machinery
fuel_switch(economy = '16_RUS', sector = ind2[5], elec_rate_ref = 0.003, elec_rate_tgt = 0.01)

# Food and Beverages
fuel_switch(economy = '16_RUS', sector = ind2[6], elec_rate_tgt = 0.0075)

# Pulp and paper
fuel_switch(economy = '16_RUS', sector = ind2[7], elec_rate_ref = 0.0025, elec_rate_tgt = 0.005)

# Wood
fuel_switch(economy = '16_RUS', sector = ind2[8], elec_rate_tgt = 0.01)

# Textiles
fuel_switch(economy = '16_RUS', sector = ind2[9], elec_rate_ref = 0.003, elec_rate_tgt = 0.0075)

# Non-specified
fuel_switch(economy = '16_RUS', sector = ind2[10], elec_rate_tgt = 0.01)

# Non-energy
fuel_switch_ne(economy = '16_RUS', hyd_increment_ref = 0.002, hyd_increment_tgt = 0.005, 
               gas_switch_ref = False, gas_switch_tgt = False)

##################################################################################################################
# Singapore
# Mining
#fuel_switch(economy = '17_SIN', sector = ind1[0])

# Construction
fuel_switch(economy = '17_SIN', sector = ind1[1])

# Chemicals
fuel_switch(economy = '17_SIN', sector = ind2[1], elec_rate_ref = 0.0025, elec_rate_tgt = 0.005,
            elec_start_ref = 2025, elec_start_tgt = 2025,
            hydrogen_ref = False, hydrogen_tgt = True, ccs_ref = False, ccs_tgt = False,
            c2g_rate_tgt = 0.002, hyd_start_tgt = 2030, hyd_increment_tgt = 0.001, 
            hyd_fuel_mix = {'16_x_hydrogen': 1.0, '17_electricity': 0.0})

# Non-specified
fuel_switch(economy = '17_SIN', sector = ind2[10], elec_rate_tgt = 0.0075)

# Non-energy
fuel_switch_ne(economy = '17_SIN', hyd_increment_ref = 0.002, hyd_increment_tgt = 0.005,
               gas_switch_ref = False, gas_switch_tgt = False)

##################################################################################################################
# Chinese Taipei
# Mining
fuel_switch(economy = '18_CT', sector = ind1[0], elec_rate_ref = 0.002, elec_rate_tgt = 0.004)

# Construction
fuel_switch(economy = '18_CT', sector = ind1[1], elec_rate_ref = 0.002, elec_rate_tgt = 0.003)

# Iron and steel
fuel_switch(economy = '18_CT', sector = ind2[0], elec_rate_ref = 0.003, elec_rate_tgt = 0.007, 
            hydrogen_ref = True, ccs_ref = False, hydrogen_tgt = True, hyd_start_tgt = 2030, 
            ccs_start_ref = 2040, ccs_tgt = True, c2g_rate_tgt = 0.009, hyd_increment_tgt = 0.015) 

# Chemicals
fuel_switch(economy = '18_CT', sector = ind2[1], elec_rate_ref = 0.0025, elec_rate_tgt = 0.005,
            hydrogen_ref = False, hydrogen_tgt = True, ccs_ref = False, ccs_tgt = True,
            c2g_rate_tgt = 0.0025, hyd_start_tgt = 2030, hyd_increment_tgt = 0.004, 
            hyd_fuel_mix = {'16_x_hydrogen': 1.0, '17_electricity': 0.0})

# Non-ferrous metals
fuel_switch(economy = '18_CT', sector = ind2[2], elec_rate_ref = 0.002, elec_rate_tgt = 0.004)

# Non-metallic minerals
fuel_switch(economy = '18_CT', sector = ind2[3], elec_rate_ref = 0.0015, elec_rate_tgt = 0.005, c2g_rate_tgt = 0.005,
            ccs_ref = False, ccs_tgt = True, bio_rate_tgt = 0.01, bio_start_tgt = 2025,
            hydrogen_tgt = False, hyd_start_tgt = 2030, hyd_increment_tgt = 0.001, hyd_fuel_mix = {'16_x_hydrogen': 1.0, '17_electricity': 0.0})

# Transport
fuel_switch(economy = '18_CT', sector = ind2[4], elec_rate_ref = 0.002, elec_rate_tgt = 0.004)

# Machinery
fuel_switch(economy = '18_CT', sector = ind2[5], elec_rate_ref = 0.001, elec_rate_tgt = 0.002)

# Food and Beverages
fuel_switch(economy = '18_CT', sector = ind2[6], elec_rate_tgt = 0.006)

# Pulp and paper
fuel_switch(economy = '18_CT', sector = ind2[7], elec_rate_ref = 0.0025, elec_rate_tgt = 0.006, 
            bio_rate_ref = 0.001, bio_rate_tgt = 0.01, c2g_rate_tgt = 0.004)

# Wood
fuel_switch(economy = '18_CT', sector = ind2[8], elec_rate_ref = 0.001, elec_rate_tgt = 0.002)

# Textiles
fuel_switch(economy = '18_CT', sector = ind2[9], elec_rate_ref = 0.005, elec_rate_tgt = 0.009, 
            c2g_rate_ref = 0.0015, c2g_rate_tgt= 0.004)

# Non-specified
fuel_switch(economy = '18_CT', sector = ind2[10], elec_rate_tgt = 0.0075)

# Non-energy
fuel_switch_ne(economy = '18_CT', hyd_increment_ref = 0.002, hyd_increment_tgt = 0.005,
               gas_switch_ref = False, gas_switch_tgt = False)

#################################################################################################################
# Thailand
# Mining
fuel_switch(economy = '19_THA', sector = ind1[0])

# Construction
fuel_switch(economy = '19_THA', sector = ind1[1])

# Iron and steel
fuel_switch(economy = '19_THA', sector = ind2[0], elec_rate_ref = 0.001, elec_rate_tgt = 0.002, 
            hydrogen_ref = True, ccs_ref = False, hydrogen_tgt = True, ccs_tgt = True, c2g_rate_tgt = 0.001)

# Chemicals
fuel_switch(economy = '19_THA', sector = ind2[1], elec_rate_ref = 0.002, elec_rate_tgt = 0.004,
            hydrogen_ref = False, hydrogen_tgt = True, ccs_ref = False, ccs_tgt = True,
            hyd_start_tgt = 2035, hyd_increment_tgt = 0.001, hyd_fuel_mix = {'16_x_hydrogen': 1.0, '17_electricity': 0.0})

# Non-ferrous metals
fuel_switch(economy = '19_THA', sector = ind2[2])

# Non-metallic minerals
fuel_switch(economy = '19_THA', sector = ind2[3], elec_rate_ref = 0.0015, elec_rate_tgt = 0.003, 
            bio_rate_tgt = 0.001, ccs_tgt = True, c2g_rate_tgt = 0.001, hydrogen_tgt = True,
            hyd_start_tgt = 2035, hyd_increment_tgt = 0.001, hyd_fuel_mix = {'16_x_hydrogen': 1.0, '17_electricity': 0.0})

# Transport
fuel_switch(economy = '19_THA', sector = ind2[4])

# Machinery
fuel_switch(economy = '19_THA', sector = ind2[5])

# Food and Beverages
fuel_switch(economy = '19_THA', sector = ind2[6], elec_rate_tgt = 0.007)

# Pulp and paper
fuel_switch(economy = '19_THA', sector = ind2[7], elec_rate_ref = 0.0025, elec_rate_tgt = 0.008, 
            bio_rate_tgt = 0.006)

# Wood
fuel_switch(economy = '19_THA', sector = ind2[8])

# Textiles
fuel_switch(economy = '19_THA', sector = ind2[9], elec_rate_ref = 0.003, elec_rate_tgt = 0.006, 
            bio_rate_tgt = 0.002, c2g_rate_tgt = 0.001)

# Non-specified
fuel_switch(economy = '19_THA', sector = ind2[10], elec_rate_tgt = 0.01, c2g_rate_tgt = 0.001)

# Non-energy
fuel_switch_ne(economy = '19_THA', hyd_increment_ref = 0.002, hyd_increment_tgt = 0.005,
               gas_switch_ref = False, gas_switch_tgt = False)

###########################################################################################################
# USA
# Mining
fuel_switch(economy = '20_USA', sector = ind1[0])

# Construction
fuel_switch(economy = '20_USA', sector = ind1[1])

# Iron and steel
fuel_switch(economy = '20_USA', sector = ind2[0], elec_rate_ref = 0.0025, elec_rate_tgt = 0.005, 
            hydrogen_ref = True, ccs_ref = True, hydrogen_tgt = True, ccs_tgt = True, c2g_rate_tgt = 0.001)

# Chemicals
fuel_switch(economy = '20_USA', sector = ind2[1], elec_rate_ref = 0.002, elec_rate_tgt = 0.004,
            hydrogen_ref = False, hydrogen_tgt = True, ccs_ref = True, ccs_tgt = True, ccs_increment_tgt = 0.008,
            hyd_start_tgt = 2030, hyd_increment_tgt = 0.001, hyd_fuel_mix = {'16_x_hydrogen': 1.0, '17_electricity': 0.0})

# Non-ferrous metals
fuel_switch(economy = '20_USA', sector = ind2[2], elec_rate_tgt = 0.006)

# Non-metallic minerals
fuel_switch(economy = '20_USA', sector = ind2[3], elec_rate_ref = 0.0015, elec_rate_tgt = 0.003, 
            bio_rate_tgt = 0.001, ccs_ref = True, ccs_tgt = True, ccs_increment_tgt = 0.008, hydrogen_tgt = True,
            hyd_start_tgt = 2030, hyd_increment_tgt = 0.001, hyd_fuel_mix = {'16_x_hydrogen': 1.0, '17_electricity': 0.0})

# Transport
fuel_switch(economy = '20_USA', sector = ind2[4], elec_rate_ref = 0.003, elec_rate_tgt = 0.0075)

# Machinery
fuel_switch(economy = '20_USA', sector = ind2[5], elec_rate_ref = 0.003, elec_rate_tgt = 0.0075)

# Food and Beverages
fuel_switch(economy = '20_USA', sector = ind2[6], elec_rate_tgt = 0.0075)

# Pulp and paper
fuel_switch(economy = '20_USA', sector = ind2[7], elec_rate_ref = 0.0025, elec_rate_tgt = 0.008, 
            bio_rate_tgt = 0.006, c2g_rate_tgt = 0.002)

# Wood
fuel_switch(economy = '20_USA', sector = ind2[8])

# Textiles
fuel_switch(economy = '20_USA', sector = ind2[9], elec_rate_ref = 0.003, elec_rate_tgt = 0.006)

# Non-specified
fuel_switch(economy = '20_USA', sector = ind2[10], elec_rate_tgt = 0.01)

# Non-energy
fuel_switch_ne(economy = '20_USA', hyd_increment_ref = 0.002, hyd_increment_tgt = 0.005, 
               gas_switch_ref = False, gas_switch_tgt = False)

###########################################################################################################
# Viet Nam
# Mining
fuel_switch(economy = '21_VN', sector = ind1[0], elec_rate_ref = 0.002, elec_rate_tgt = 0.0075)

# Construction
fuel_switch(economy = '21_VN', sector = ind1[1], elec_rate_ref = 0.002, elec_rate_tgt = 0.004, elec_start_ref = 2024, 
            elec_start_tgt = 2024)

# Iron and steel
fuel_switch(economy = '21_VN', sector = ind2[0], elec_rate_ref = 0.0015, elec_rate_tgt = 0.003, 
            elec_start_tgt = 2025, hydrogen_ref = False, ccs_ref = False, hydrogen_tgt = True, ccs_tgt = True, 
            hyd_increment_ref = 0.0025, hyd_increment_tgt = 0.0075, c2g_rate_ref = 0.001, c2g_rate_tgt = 0.01, 
            hyd_fuel_mix = {'16_x_hydrogen': 0.6, '17_electricity': 0.4})

# Chemicals
fuel_switch(economy = '21_VN', sector = ind2[1], elec_rate_ref = 0.002, elec_rate_tgt = 0.004,
            hydrogen_ref = False, hydrogen_tgt = True, ccs_ref = False, ccs_tgt = True,
            hyd_start_tgt = 2030, hyd_increment_tgt = 0.003, hyd_fuel_mix = {'16_x_hydrogen': 1.0, '17_electricity': 0.0},
            c2g_rate_tgt = 0.008)

# Non-ferrous metals: no data

# Non-metallic minerals
fuel_switch(economy = '21_VN', sector = ind2[3], elec_rate_ref = 0.0015, elec_rate_tgt = 0.004, 
            ccs_ref = False, ccs_tgt = True, c2g_rate_tgt = 0.004, hydrogen_ref = False, hydrogen_tgt = True,
            bio_start_ref = 2025, bio_start_tgt = 2025, bio_rate_ref = 0.002, bio_rate_tgt = 0.012,
            hyd_start_tgt = 2030, hyd_increment_tgt = 0.001, hyd_fuel_mix = {'16_x_hydrogen': 1.0, '17_electricity': 0.0})

# Transport
fuel_switch(economy = '21_VN', sector = ind2[4], elec_rate_ref = 0.002, elec_rate_tgt = 0.0075, c2g_rate_tgt = 0.002)

# Machinery
fuel_switch(economy = '21_VN', sector = ind2[5])

# Food and Beverages
fuel_switch(economy = '21_VN', sector = ind2[6], elec_rate_tgt = 0.01, bio_rate_tgt = 0.005)

# Pulp and paper
fuel_switch(economy = '21_VN', sector = ind2[7], elec_rate_ref = 0.0025, elec_rate_tgt = 0.012, 
            bio_rate_tgt = 0.014)

# Wood
fuel_switch(economy = '21_VN', sector = ind2[8], bio_rate_tgt = 0.002)

# Textiles
fuel_switch(economy = '21_VN', sector = ind2[9], elec_rate_ref = 0.003, elec_rate_tgt = 0.008, bio_rate_tgt = 0.011)

# Non-specified
fuel_switch(economy = '21_VN', sector = ind2[10], elec_rate_tgt = 0.01, bio_start_tgt = 2025,
            bio_rate_tgt = 0.005)

# Non-energy
fuel_switch_ne(economy = '21_VN', hyd_increment_ref = 0.0015, hyd_increment_tgt = 0.004, 
               gas_switch_ref = False, gas_switch_tgt = False) 


#################################################################################################

# Now read in all data for each economy
for economy in list(economy_select):
    data_location = './results/industry/3_fuel_switch/{}/'.format(economy)

    if not os.path.isdir(data_location):
        os.makedirs(data_location)

    all_sector_save = './results/industry/3_fuel_switch/{}/all_sectors/'.format(economy)

    if not os.path.isdir(all_sector_save):
        os.makedirs(all_sector_save)

    economy_df = pd.DataFrame()

    economy_files = glob.glob(data_location + '*.csv')

    if len(economy_files) < 2:
        pass

    else:
        for i in economy_files:
            temp_df = pd.read_csv(i)
            economy_df = pd.concat([economy_df, temp_df]).copy().reset_index(drop = True)

        economy_df.to_csv(all_sector_save + '{}_all_subsectors.csv'.format(economy), index = False)
        
        # Create some charts
        # Pivot the DataFrame
        chart_df_ref = economy_df[(economy_df['energy'] != 0) &
                                (economy_df['energy'].isna() == False) &
                                (economy_df['scenarios'] == 'reference') &
                                (economy_df['year'] <= 2070)].copy().reset_index(drop = True)
        
        # Custom chart column
        chart_df_ref['fuel'] = np.where(chart_df_ref['subfuels'] == 'x', chart_df_ref['fuels'], chart_df_ref['subfuels'])
        
        chart_df_ref = chart_df_ref.groupby(['fuel', 'year'])['energy'].sum().reset_index()
        
        chart_pivot_ref = chart_df_ref.pivot(index = 'year', columns = 'fuel', values = 'energy')
        
        chart_df_tgt = economy_df[(economy_df['energy'] != 0) &
                                (economy_df['energy'].isna() == False) & 
                                (economy_df['scenarios'] == 'target') &
                                (economy_df['year'] <= 2070)].copy().reset_index(drop = True)
        
        # Custom chart column
        chart_df_tgt['fuel'] = np.where(chart_df_tgt['subfuels'] == 'x', chart_df_tgt['fuels'], chart_df_tgt['subfuels'])
        
        chart_df_tgt = chart_df_tgt.groupby(['fuel', 'year'])['energy'].sum().reset_index()

        chart_pivot_tgt = chart_df_tgt.pivot(index = 'year', columns = 'fuel', values = 'energy')

        max_y = 1.1 * max(chart_df_ref.groupby('year')['energy'].sum().max(), chart_df_tgt.groupby('year')['energy'].sum().max())
        proj_location = 0.925 * max_y

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize = (8, 8))

        sns.set_theme(style = 'ticks')

        chart_pivot_ref.plot.area(ax = ax1,
                                    stacked = True,
                                    #alpha = 0.8,
                                    color = fuel_palette1, 
                                    linewidth = 0)
        
        chart_pivot_tgt.plot.area(ax = ax2,
                                    stacked = True,
                                    #alpha = 0.8,
                                    color = fuel_palette1,
                                    linewidth = 0)
        
        ax1.set(title = economy + ' all industry REF',
                xlabel = 'Year',
                ylabel = 'Energy (PJ)',
                xlim = (2000, 2070),
                ylim = (0, max_y))
        
        ax2.set(title = economy + ' all industry TGT',
                xlabel = 'Year',
                ylabel = 'Energy (PJ)',
                xlim = (2000, 2070),
                ylim = (0, max_y))
        
        # Projection demarcation
        ax1.axvline(x = 2021, linewidth = 1, linestyle = '--', color = 'black')
        ax2.axvline(x = 2021, linewidth = 1, linestyle = '--', color = 'black')

        # Projection text
        ax1.annotate('Projection', 
                    xy = (2031, proj_location),
                    xytext = (2025, proj_location),
                    va = 'center',
                    ha = 'center',
                    fontsize = 9,
                    arrowprops = {'arrowstyle': '-|>',
                                'lw': 0.5,
                                'ls': '-',
                                'color': 'black'})
        
        ax2.annotate('Projection', 
                    xy = (2031, proj_location),
                    xytext = (2025, proj_location),
                    va = 'center',
                    ha = 'center',
                    fontsize = 9,
                    arrowprops = {'arrowstyle': '-|>',
                                'lw': 0.5,
                                'ls': '-',
                                'color': 'black'})
        
        ax1.legend(title = '', fontsize = 7)
        ax2.legend(title = '', fontsize = 7)

        #ax2.set_ylim(ax1.get_ylim())
                
        plt.tight_layout()
        plt.savefig(all_sector_save + economy + '_industry.png')
        plt.show()
        plt.close()