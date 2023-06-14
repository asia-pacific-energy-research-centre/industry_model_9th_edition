# Choosing trajectories for all economies
# World Development Indicators industry data
import os
import re

wanted_wd = 'industry_model_9th_edition'

os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

# execute config file
config_file = './config/config_apr2023.py'
with open(config_file) as infile:
    exec(infile.read())

# Some required files for the below function runs
wdi_df = pd.read_csv('./data/wdi_industry.csv')
# Remove data series we don't need
wdi_df = wdi_df[wdi_df['series_code'] != 'NV.MNF.TECH.ZS.UN'].copy().reset_index(drop = True)

# Grab relevant function from previous script
from b1_wdi_input_data import ind_projection

# Run function for economies
##############################################################################################
# 01_AUS
# Industry (including construction) % GDP
ind_projection(economy = '01_AUS', series = 'NV.IND.TOTL.ZS', high_bound = 22, high_change = 0.9997)
# Manufacturing % GDP
ind_projection(economy = '01_AUS', series = 'NV.IND.MANF.ZS', low_bound = 5, high_bound = 6)

# Subsets of Manufacturing (% of Manufacturing)
# Chemicals
ind_projection(economy = '01_AUS', series = 'NV.MNF.CHEM.ZS.UN', high_bound = 4, high_change = 0.997)
# Food and beverage
ind_projection(economy = '01_AUS', series = 'NV.MNF.FBTO.ZS.UN', low_bound = 32, high_bound = 35, low_change = 1.0005)
# Machinery and Transport
ind_projection(economy = '01_AUS', series = 'NV.MNF.MTRN.ZS.UN', high_bound = 14)
# Other manufacturing
ind_projection(economy = '01_AUS', series = 'NV.MNF.OTHR.ZS.UN', low_bound = 40, high_bound = 60, low_change = 1.0005)
# Textiles
ind_projection(economy = '01_AUS', series = 'NV.MNF.TXTL.ZS.UN', low_bound = 0.3, high_bound = 0.5, high_change = 0.996) 

##############################################################################################
# 02_BD
# Industry (including construction) % GDP
ind_projection(economy = '02_BD', series = 'NV.IND.TOTL.ZS', high_change = 0.997)
# Manufacturing % GDP
ind_projection(economy = '02_BD', series = 'NV.IND.MANF.ZS', low_bound = 10, high_bound = 13, high_change = 0.9986)

###############################################################################################
# 03_CDA
# Industry (including construction) % GDP
ind_projection(economy = '03_CDA', series = 'NV.IND.TOTL.ZS', low_bound = 15, high_bound = 18)
# Manufacturing % GDP
ind_projection(economy = '03_CDA', series = 'NV.IND.MANF.ZS', low_bound = 6, high_bound = 7)

# Subsets of Manufacturing (% of Manufacturing)
# Chemicals
ind_projection(economy = '03_CDA', series = 'NV.MNF.CHEM.ZS.UN', low_bound = 7, high_bound = 7.5)
# Food and beverage
ind_projection(economy = '03_CDA', series = 'NV.MNF.FBTO.ZS.UN')
# Machinery and Transport
ind_projection(economy = '03_CDA', series = 'NV.MNF.MTRN.ZS.UN', low_bound = 20, high_bound = 30)
# Other manufacturing
ind_projection(economy = '03_CDA', series = 'NV.MNF.OTHR.ZS.UN', low_bound = 40, high_bound = 50)
# Textiles
ind_projection(economy = '03_CDA', series = 'NV.MNF.TXTL.ZS.UN', low_bound = 0.5, high_bound = 1)

###############################################################################################
# 04_CHL
# Industry (including construction) % GDP
ind_projection(economy = '04_CHL', series = 'NV.IND.TOTL.ZS')
# Manufacturing % GDP
ind_projection(economy = '04_CHL', series = 'NV.IND.MANF.ZS', low_bound = 5, high_bound = 6)

# Subsets of Manufacturing (% of Manufacturing)
# Chemicals
ind_projection(economy = '04_CHL', series = 'NV.MNF.CHEM.ZS.UN', low_bound = 6, high_bound = 7, high_change = 0.998)
# Food and beverage
ind_projection(economy = '04_CHL', series = 'NV.MNF.FBTO.ZS.UN', low_bound = 45, high_bound = 50, low_change = 1.0003)
# Machinery and Transport
ind_projection(economy = '04_CHL', series = 'NV.MNF.MTRN.ZS.UN')
# Other manufacturing
ind_projection(economy = '04_CHL', series = 'NV.MNF.OTHR.ZS.UN', low_bound = 30, high_bound = 60)
# Textiles
ind_projection(economy = '04_CHL', series = 'NV.MNF.TXTL.ZS.UN', low_bound = 1.5, high_bound = 2)

###############################################################################################
# 05_PRC
# Industry (including construction) % GDP
ind_projection(economy = '05_PRC', series = 'NV.IND.TOTL.ZS', low_bound = 20, high_bound = 22, high_change = 0.998)
# Manufacturing % GDP
ind_projection(economy = '05_PRC', series = 'NV.IND.MANF.ZS', low_bound = 10, high_bound = 13, high_change = 0.997)

# Subsets of Manufacturing (% of Manufacturing)
# Chemicals
ind_projection(economy = '05_PRC', series = 'NV.MNF.CHEM.ZS.UN')
# Food and beverage
ind_projection(economy = '05_PRC', series = 'NV.MNF.FBTO.ZS.UN')
# Machinery and Transport
ind_projection(economy = '05_PRC', series = 'NV.MNF.MTRN.ZS.UN', low_bound = 24, high_bound = 26)
# Other manufacturing
ind_projection(economy = '05_PRC', series = 'NV.MNF.OTHR.ZS.UN', low_bound = 40, high_bound = 50)
# Textiles
ind_projection(economy = '05_PRC', series = 'NV.MNF.TXTL.ZS.UN', low_bound = 5, high_bound = 7)

###############################################################################################
# 06_HKC
# Industry (including construction) % GDP
ind_projection(economy = '06_HKC', series = 'NV.IND.TOTL.ZS', low_bound = 4, high_bound = 5)
# Manufacturing % GDP
ind_projection(economy = '06_HKC', series = 'NV.IND.MANF.ZS', low_bound = 0.3, high_bound = 0.5)

# Subsets of Manufacturing (% of Manufacturing)
# Chemicals
ind_projection(economy = '06_HKC', series = 'NV.MNF.CHEM.ZS.UN', high_bound = 8)
# Food and beverage
ind_projection(economy = '06_HKC', series = 'NV.MNF.FBTO.ZS.UN', low_bound = 30, high_bound = 50)
# Machinery and Transport
ind_projection(economy = '06_HKC', series = 'NV.MNF.MTRN.ZS.UN', low_bound = 24, high_bound = 30)
# Other manufacturing
ind_projection(economy = '06_HKC', series = 'NV.MNF.OTHR.ZS.UN', low_bound = 24, high_bound = 30)
# Textiles
ind_projection(economy = '06_HKC', series = 'NV.MNF.TXTL.ZS.UN', low_bound = 3, high_bound = 4)

###############################################################################################
# 07_INA
# Industry (including construction) % GDP
ind_projection(economy = '07_INA', series = 'NV.IND.TOTL.ZS', low_bound = 25, high_bound = 35, high_change = 0.9995)
# Manufacturing % GDP
ind_projection(economy = '07_INA', series = 'NV.IND.MANF.ZS', low_bound = 10, high_bound = 14)

# Subsets of Manufacturing (% of Manufacturing)
# Chemicals
ind_projection(economy = '07_INA', series = 'NV.MNF.CHEM.ZS.UN', high_bound = 8)
# Food and beverage
ind_projection(economy = '07_INA', series = 'NV.MNF.FBTO.ZS.UN', high_bound = 18)
# Machinery and Transport
ind_projection(economy = '07_INA', series = 'NV.MNF.MTRN.ZS.UN')
# Other manufacturing
ind_projection(economy = '07_INA', series = 'NV.MNF.OTHR.ZS.UN')
# Textiles
ind_projection(economy = '07_INA', series = 'NV.MNF.TXTL.ZS.UN', high_bound = 10)

###############################################################################################
# 08_JPN
# Industry (including construction) % GDP
ind_projection(economy = '08_JPN', series = 'NV.IND.TOTL.ZS', low_bound = 20, high_bound = 22, high_change = 0.999)
# Manufacturing % GDP
ind_projection(economy = '08_JPN', series = 'NV.IND.MANF.ZS', low_bound = 25, high_bound = 16, high_change = 0.9993)

# Subsets of Manufacturing (% of Manufacturing)
# Chemicals
ind_projection(economy = '08_JPN', series = 'NV.MNF.CHEM.ZS.UN')
# Food and beverage
ind_projection(economy = '08_JPN', series = 'NV.MNF.FBTO.ZS.UN', low_bound = 15, low_change = 1.0006)
# Machinery and Transport
ind_projection(economy = '08_JPN', series = 'NV.MNF.MTRN.ZS.UN', low_bound = 50, high_bound = 60, low_change = 1.0003)
# Other manufacturing
ind_projection(economy = '08_JPN', series = 'NV.MNF.OTHR.ZS.UN')
# Textiles
ind_projection(economy = '08_JPN', series = 'NV.MNF.TXTL.ZS.UN', low_bound = 1, high_bound = 1.5)

###############################################################################################
# 09_ROK
# Industry (including construction) % GDP
ind_projection(economy = '09_ROK', series = 'NV.IND.TOTL.ZS')
# Manufacturing % GDP
ind_projection(economy = '09_ROK', series = 'NV.IND.MANF.ZS', high_bound = 15, high_change = 0.998)

# Subsets of Manufacturing (% of Manufacturing)
# Chemicals
ind_projection(economy = '09_ROK', series = 'NV.MNF.CHEM.ZS.UN', high_bound = 8)
# Food and beverage
ind_projection(economy = '09_ROK', series = 'NV.MNF.FBTO.ZS.UN', low_bound = 5)
# Machinery and Transport
ind_projection(economy = '09_ROK', series = 'NV.MNF.MTRN.ZS.UN', low_bound = 40, high_bound = 50)
# Other manufacturing
ind_projection(economy = '09_ROK', series = 'NV.MNF.OTHR.ZS.UN', low_bound = 30, high_bound = 35)
# Textiles
ind_projection(economy = '09_ROK', series = 'NV.MNF.TXTL.ZS.UN', low_bound = 2, high_bound = 3)

###############################################################################################
# 10_MAS
# Industry (including construction) % GDP
ind_projection(economy = '10_MAS', series = 'NV.IND.TOTL.ZS')
# Manufacturing % GDP
ind_projection(economy = '10_MAS', series = 'NV.IND.MANF.ZS', high_bound = 14, high_change = 0.998)

# Subsets of Manufacturing (% of Manufacturing)
# Chemicals
ind_projection(economy = '10_MAS', series = 'NV.MNF.CHEM.ZS.UN', low_bound = 5, high_bound = 10)
# Food and beverage
ind_projection(economy = '10_MAS', series = 'NV.MNF.FBTO.ZS.UN')
# Machinery and Transport
ind_projection(economy = '10_MAS', series = 'NV.MNF.MTRN.ZS.UN')
# Other manufacturing
ind_projection(economy = '10_MAS', series = 'NV.MNF.OTHR.ZS.UN', low_bound = 40, high_bound = 50)
# Textiles
ind_projection(economy = '10_MAS', series = 'NV.MNF.TXTL.ZS.UN', low_bound = 2, high_bound = 2.1)

###############################################################################################
# 11_MEX
# Industry (including construction) % GDP
ind_projection(economy = '11_MEX', series = 'NV.IND.TOTL.ZS', low_bound = 25, high_bound = 26, high_change = 0.9995)
# Manufacturing % GDP
ind_projection(economy = '11_MEX', series = 'NV.IND.MANF.ZS', low_bound = 10, high_bound = 11, high_change = 0.998)

# Subsets of Manufacturing (% of Manufacturing)
# Chemicals
ind_projection(economy = '11_MEX', series = 'NV.MNF.CHEM.ZS.UN', low_bound = 5, high_bound = 10)
# Food and beverage
ind_projection(economy = '11_MEX', series = 'NV.MNF.FBTO.ZS.UN', low_bound = 20, high_bound = 35)
# Machinery and Transport
ind_projection(economy = '11_MEX', series = 'NV.MNF.MTRN.ZS.UN')
# Other manufacturing
ind_projection(economy = '11_MEX', series = 'NV.MNF.OTHR.ZS.UN', low_bound = 30, high_bound = 36)
# Textiles
ind_projection(economy = '11_MEX', series = 'NV.MNF.TXTL.ZS.UN', low_bound = 1, high_bound = 2.5, high_change = 0.9998)

###############################################################################################
# 12_NZ
# Industry (including construction) % GDP
ind_projection(economy = '12_NZ', series = 'NV.IND.TOTL.ZS', low_bound = 5, high_bound = 10, high_change = 0.999)
# Manufacturing % GDP
ind_projection(economy = '12_NZ', series = 'NV.IND.MANF.ZS', low_bound = 3, high_bound = 5, high_change = 0.998)

# Subsets of Manufacturing (% of Manufacturing)
# Chemicals
ind_projection(economy = '12_NZ', series = 'NV.MNF.CHEM.ZS.UN', low_bound = 0.5, high_bound = 0.7, high_change = 0.993)
# Food and beverage
ind_projection(economy = '12_NZ', series = 'NV.MNF.FBTO.ZS.UN', low_bound = 45, high_bound = 50, low_change = 1.0003)
# Machinery and Transport
ind_projection(economy = '12_NZ', series = 'NV.MNF.MTRN.ZS.UN')
# Other manufacturing
ind_projection(economy = '12_NZ', series = 'NV.MNF.OTHR.ZS.UN', low_bound = 40, high_bound = 50)
# Textiles
ind_projection(economy = '12_NZ', series = 'NV.MNF.TXTL.ZS.UN', low_bound = 1, high_bound = 2)

###############################################################################################
# 13_PNG
# Industry (including construction) % GDP
ind_projection(economy = '13_PNG', series = 'NV.IND.TOTL.ZS', low_bound = 20, high_bound = 25)
# Manufacturing % GDP
ind_projection(economy = '13_PNG', series = 'NV.IND.MANF.ZS', low_bound = 1, high_bound = 3)

# Subsets of Manufacturing (% of Manufacturing)
# Chemicals
ind_projection(economy = '13_PNG', series = 'NV.MNF.CHEM.ZS.UN', low_bound = 1, high_bound = 7)
# Food and beverage
ind_projection(economy = '13_PNG', series = 'NV.MNF.FBTO.ZS.UN', low_bound = 50, high_bound = 60)
# Machinery and Transport
ind_projection(economy = '13_PNG', series = 'NV.MNF.MTRN.ZS.UN', low_bound = 15)
# Other manufacturing
ind_projection(economy = '13_PNG', series = 'NV.MNF.OTHR.ZS.UN', low_bound = 30, high_bound = 40)
# Textiles
ind_projection(economy = '13_PNG', series = 'NV.MNF.TXTL.ZS.UN', low_bound = 1, high_bound = 2)

###############################################################################################
# 14_PE
# Industry (including construction) % GDP
ind_projection(economy = '14_PE', series = 'NV.IND.TOTL.ZS', low_bound =  20, high_bound = 22)
# Manufacturing % GDP
ind_projection(economy = '14_PE', series = 'NV.IND.MANF.ZS', high_bound = 10)

# Subsets of Manufacturing (% of Manufacturing)
# Chemicals
ind_projection(economy = '14_PE', series = 'NV.MNF.CHEM.ZS.UN', low_bound = 5, high_bound = 8)
# Food and beverage
ind_projection(economy = '14_PE', series = 'NV.MNF.FBTO.ZS.UN', low_bound = 24, high_bound = 30)
# Machinery and Transport
ind_projection(economy = '14_PE', series = 'NV.MNF.MTRN.ZS.UN')
# Other manufacturing
ind_projection(economy = '14_PE', series = 'NV.MNF.OTHR.ZS.UN', low_bound = 50, high_bound = 60)
# Textiles
ind_projection(economy = '14_PE', series = 'NV.MNF.TXTL.ZS.UN', low_bound = 7)

###############################################################################################
# 15_RP
# Industry (including construction) % GDP
ind_projection(economy = '15_RP', series = 'NV.IND.TOTL.ZS')
# Manufacturing % GDP
ind_projection(economy = '15_RP', series = 'NV.IND.MANF.ZS', low_bound = 7, high_bound = 8, high_change = 0.998)

# Subsets of Manufacturing (% of Manufacturing)
# Chemicals
ind_projection(economy = '15_RP', series = 'NV.MNF.CHEM.ZS.UN', low_bound = 3, high_bound = 4)
# Food and beverage
ind_projection(economy = '15_RP', series = 'NV.MNF.FBTO.ZS.UN')
# Machinery and Transport
ind_projection(economy = '15_RP', series = 'NV.MNF.MTRN.ZS.UN')
# Other manufacturing
ind_projection(economy = '15_RP', series = 'NV.MNF.OTHR.ZS.UN')
# Textiles
ind_projection(economy = '15_RP', series = 'NV.MNF.TXTL.ZS.UN', low_bound = 2, high_bound = 3)

###############################################################################################
# 16_RUS
# Industry (including construction) % GDP
ind_projection(economy = '16_RUS', series = 'NV.IND.TOTL.ZS', low_bound = 22, high_bound = 25)
# Manufacturing % GDP
ind_projection(economy = '16_RUS', series = 'NV.IND.MANF.ZS', high_bound = 12, high_change = 0.9995)

# Subsets of Manufacturing (% of Manufacturing)
# Chemicals
ind_projection(economy = '16_RUS', series = 'NV.MNF.CHEM.ZS.UN', low_bound = 13)
# Food and beverage
ind_projection(economy = '16_RUS', series = 'NV.MNF.FBTO.ZS.UN')
# Machinery and Transport
ind_projection(economy = '16_RUS', series = 'NV.MNF.MTRN.ZS.UN')
# Other manufacturing
ind_projection(economy = '16_RUS', series = 'NV.MNF.OTHR.ZS.UN', low_bound = 50, high_bound = 70)
# Textiles
ind_projection(economy = '16_RUS', series = 'NV.MNF.TXTL.ZS.UN', low_bound = 1, high_bound = 2)

###############################################################################################
# 17_SIN
# Industry (including construction) % GDP
ind_projection(economy = '17_SIN', series = 'NV.IND.TOTL.ZS', high_bound = 15)
# Manufacturing % GDP
ind_projection(economy = '17_SIN', series = 'NV.IND.MANF.ZS', high_bound = 10, high_change = 0.997)

# Subsets of Manufacturing (% of Manufacturing)
# Chemicals
ind_projection(economy = '17_SIN', series = 'NV.MNF.CHEM.ZS.UN', high_bound = 14)
# Food and beverage
ind_projection(economy = '17_SIN', series = 'NV.MNF.FBTO.ZS.UN')
# Machinery and Transport
ind_projection(economy = '17_SIN', series = 'NV.MNF.MTRN.ZS.UN')
# Other manufacturing
ind_projection(economy = '17_SIN', series = 'NV.MNF.OTHR.ZS.UN')
# Textiles
ind_projection(economy = '17_SIN', series = 'NV.MNF.TXTL.ZS.UN')

###############################################################################################
# 19_THA
# Industry (including construction) % GDP
ind_projection(economy = '19_THA', series = 'NV.IND.TOTL.ZS', high_bound = 27, high_change = 0.999)
# Manufacturing % GDP
ind_projection(economy = '19_THA', series = 'NV.IND.MANF.ZS', high_bound = 15, high_change = 0.9985)

# Subsets of Manufacturing (% of Manufacturing)
# Chemicals
ind_projection(economy = '19_THA', series = 'NV.MNF.CHEM.ZS.UN', low_bound = 5, high_bound = 15)
# Food and beverage
ind_projection(economy = '19_THA', series = 'NV.MNF.FBTO.ZS.UN')
# Machinery and Transport
ind_projection(economy = '19_THA', series = 'NV.MNF.MTRN.ZS.UN')
# Other manufacturing
ind_projection(economy = '19_THA', series = 'NV.MNF.OTHR.ZS.UN', low_bound = 30, high_bound = 40)
# Textiles
ind_projection(economy = '19_THA', series = 'NV.MNF.TXTL.ZS.UN', high_bound = 6)

###############################################################################################
# 20_USA
# Industry (including construction) % GDP
ind_projection(economy = '20_USA', series = 'NV.IND.TOTL.ZS', high_bound = 16, high_change = 0.9997)
# Manufacturing % GDP
ind_projection(economy = '20_USA', series = 'NV.IND.MANF.ZS', low_bound = 5, high_bound = 8, high_change = 0.9993)

# Subsets of Manufacturing (% of Manufacturing)
# Chemicals
ind_projection(economy = '20_USA', series = 'NV.MNF.CHEM.ZS.UN', high_bound = 13, high_change = 0.9993)
# Food and beverage
ind_projection(economy = '20_USA', series = 'NV.MNF.FBTO.ZS.UN')
# Machinery and Transport
ind_projection(economy = '20_USA', series = 'NV.MNF.MTRN.ZS.UN', low_bound = 25, high_bound = 30)
# Other manufacturing
ind_projection(economy = '20_USA', series = 'NV.MNF.OTHR.ZS.UN', low_bound = 35, high_bound = 40)
# Textiles
ind_projection(economy = '20_USA', series = 'NV.MNF.TXTL.ZS.UN', low_bound = 1, high_bound = 1.5)

###############################################################################################
# 21_VN
# Industry (including construction) % GDP
ind_projection(economy = '21_VN', series = 'NV.IND.TOTL.ZS')
# Manufacturing % GDP
ind_projection(economy = '21_VN', series = 'NV.IND.MANF.ZS', low_bound = 15, high_bound = 17, high_change = 0.9992)

# Subsets of Manufacturing (% of Manufacturing)
# Chemicals
ind_projection(economy = '21_VN', series = 'NV.MNF.CHEM.ZS.UN', low_bound = 2, high_bound = 3)
# Food and beverage
ind_projection(economy = '21_VN', series = 'NV.MNF.FBTO.ZS.UN')
# Machinery and Transport
ind_projection(economy = '21_VN', series = 'NV.MNF.MTRN.ZS.UN', low_bound = 25, high_bound = 30)
# Other manufacturing
ind_projection(economy = '21_VN', series = 'NV.MNF.OTHR.ZS.UN', low_bound = 35, high_bound = 40)
# Textiles
ind_projection(economy = '21_VN', series = 'NV.MNF.TXTL.ZS.UN')

#################################################################################################

# Now package up all the results and save in one combined data frame

combined_df = pd.DataFrame()

for economy in wdi_df['economy_code'].unique():
    filenames = glob.glob('./data/industry_interim1/{}/*.csv'.format(economy))
    for i in filenames:
        temp_df = pd.read_csv(i)
        combined_df = pd.concat([combined_df, temp_df]).copy()

combined_df.to_csv('./data/industry_interim1/wdi_projections.csv', index = False)