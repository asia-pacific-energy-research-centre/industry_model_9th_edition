# Manual refinement

# Set working directory to be the project folder
import os
import re

wanted_wd = 'industry_model_9th_edition'
os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

# execute config file
config_file = './config/config_apr2023.py'
with open(config_file) as infile:
    exec(infile.read())

# Grab APEC economies
APEC_economies = pd.read_csv('./data/config/APEC_economies.csv', index_col = 0).squeeze().to_dict()

# Read in industry projections data

wdi_subsectors = pd.read_csv('./data/industry_production/industry_subsectors.csv')
steel_df = pd.read_csv('./data/ml_steel/interim_steel/ml_steel_indexed.csv')
cement_df = pd.read_csv('./data/ml_cement/interim_cement/ml_cement_indexed.csv')
alum_df = pd.read_csv('./data/ml_alum/interim_alum/ml_alum_indexed.csv')

# Energy industry subsectors
ind1 = ['14_01_mining_and_quarrying', '14_02_construction', '14_03_manufacturing']

ind2 = ['14_03_01_iron_and_steel', '14_03_02_chemical_incl_petrochemical', '14_03_03_non_ferrous_metals',
        '14_03_04_nonmetallic_mineral_products', '14_03_05_transportation_equipment', '14_03_06_machinery',
        '14_03_07_food_beverages_and_tobacco', '14_03_08_pulp_paper_and_printing', '14_03_09_wood_and_wood_products',
        '14_03_10_textiles_and_leather', '14_03_11_nonspecified_industry']

# Need to build production series for all industry subsectors that are defined in EGEDA energy data

steel_df['sub2sectors'] = '14_03_01_iron_and_steel'
cement_df['sub2sectors'] = '14_03_04_nonmetallic_mineral_products'
alum_df['sub2sectors'] = '14_03_03_non_ferrous_metals'

# Other sectors

chem_df = wdi_subsectors[wdi_subsectors['series'] == 'NV.MNF.CHEM.ZS.UN'].copy().reset_index(drop = True)
chem_df['sub2sectors'] = '14_03_02_chemical_incl_petrochemical'

trans_df = wdi_subsectors[wdi_subsectors['series'] == 'NV.MNF.MTRN.ZS.UN'].copy().reset_index(drop = True)
trans_df['sub2sectors'] = '14_03_05_transportation_equipment'

mach_df = wdi_subsectors[wdi_subsectors['series'] == 'NV.MNF.MTRN.ZS.UN'].copy().reset_index(drop = True)
mach_df['sub2sectors'] = '14_03_06_machinery'

fb_df = wdi_subsectors[wdi_subsectors['series'] == 'NV.MNF.FBTO.ZS.UN'].copy().reset_index(drop = True)
fb_df['sub2sectors'] = '14_03_07_food_beverages_and_tobacco'

pp_df = wdi_subsectors[wdi_subsectors['series'] == 'NV.MNF.OTHR.ZS.UN'].copy().reset_index(drop = True)
pp_df['sub2sectors'] = '14_03_08_pulp_paper_and_printing'

ww_df = wdi_subsectors[wdi_subsectors['series'] == 'NV.MNF.OTHR.ZS.UN'].copy().reset_index(drop = True)
ww_df['sub2sectors'] = '14_03_09_wood_and_wood_products'

txt_df = wdi_subsectors[wdi_subsectors['series'] == 'NV.MNF.TXTL.ZS.UN'].copy().reset_index(drop = True)
txt_df['sub2sectors'] = '14_03_10_textiles_and_leather'

ns_df = wdi_subsectors[wdi_subsectors['series'] == 'NV.IND.TOTL.ZS'].copy().reset_index(drop = True)
ns_df['sub2sectors'] = '14_03_11_nonspecified_industry'