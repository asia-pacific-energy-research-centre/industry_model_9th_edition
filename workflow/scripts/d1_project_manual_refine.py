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
wdi_subsectors = pd.read_csv('./data/industry_interim2/industry_subsectors.csv')
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

# Steel
steel_df['sub2sectors'] = '14_03_01_iron_and_steel'
steel_df = steel_df.rename(columns = {'production': 'series'})

# Cement
cement_df['sub2sectors'] = '14_03_04_nonmetallic_mineral_products'
cement_df = cement_df.rename(columns = {'production': 'series'})

# Alum
alum_df['sub2sectors'] = '14_03_03_non_ferrous_metals'
alum_df = alum_df.rename(columns = {'production': 'series'})

################################# Other (WDI based) manufacturing sectors ############################
# Chemicals 
chem_df = wdi_subsectors[wdi_subsectors['series'] == 'NV.MNF.CHEM.ZS.UN'].copy().reset_index(drop = True)
chem_df['sub2sectors'] = '14_03_02_chemical_incl_petrochemical'

# Transportation equipment
trans_df = wdi_subsectors[wdi_subsectors['series'] == 'NV.MNF.MTRN.ZS.UN'].copy().reset_index(drop = True)
trans_df['sub2sectors'] = '14_03_05_transportation_equipment'

# Machinery
mach_df = wdi_subsectors[wdi_subsectors['series'] == 'NV.MNF.MTRN.ZS.UN'].copy().reset_index(drop = True)
mach_df['sub2sectors'] = '14_03_06_machinery'

# Food and beverages
fb_df = wdi_subsectors[wdi_subsectors['series'] == 'NV.MNF.FBTO.ZS.UN'].copy().reset_index(drop = True)
fb_df['sub2sectors'] = '14_03_07_food_beverages_and_tobacco'

# Pulp, paper and printing
pp_df = wdi_subsectors[wdi_subsectors['series'] == 'NV.MNF.OTHR.ZS.UN'].copy().reset_index(drop = True)
pp_df['sub2sectors'] = '14_03_08_pulp_paper_and_printing'

# Wood and wood products
ww_df = wdi_subsectors[wdi_subsectors['series'] == 'NV.MNF.OTHR.ZS.UN'].copy().reset_index(drop = True)
ww_df['sub2sectors'] = '14_03_09_wood_and_wood_products'

# Textiles
txt_df = wdi_subsectors[wdi_subsectors['series'] == 'NV.MNF.TXTL.ZS.UN'].copy().reset_index(drop = True)
txt_df['sub2sectors'] = '14_03_10_textiles_and_leather'

# Non-specified
ns_df = wdi_subsectors[wdi_subsectors['series'] == 'NV.IND.TOTL.ZS'].copy().reset_index(drop = True)
# No IND.TOTL for Viet Nam, so different grab:
vn_ns_df = wdi_subsectors[(wdi_subsectors['series'] == 'NV.IND.MANF.ZS') &
                          (wdi_subsectors['economy_code'] == '21_VN')].copy().reset_index(drop = True)

ns_df = pd.concat([ns_df, vn_ns_df]).copy().reset_index(drop = True)
ns_df['sub2sectors'] = '14_03_11_nonspecified_industry'

################################## All manufacturing #############################################
all_manf = pd.concat([steel_df, chem_df, alum_df, cement_df, trans_df, mach_df, fb_df, pp_df, ww_df, txt_df, ns_df]).copy().reset_index(drop = True)
all_manf['sub1sectors'] = '14_03_manufacturing'

################################# Level 1 industry: construction and mining ######################
# Construction
cons_df = wdi_subsectors[wdi_subsectors['series'] == 'NV.MNF.OTHR.ZS.UN'].copy().reset_index(drop = True)
cons_df['sub1sectors'] = '14_02_construction'
cons_df['sub2sectors'] = 'x'

# Mining
min_df = wdi_subsectors[wdi_subsectors['series'] == 'NV.IND.TOTL.ZS'].copy().reset_index(drop = True)
# No IND.TOTL for Viet Nam, so different grab:
vn_min_df = wdi_subsectors[(wdi_subsectors['series'] == 'NV.IND.MANF.ZS') &
                           (wdi_subsectors['economy_code'] == '21_VN')].copy().reset_index(drop = True)

min_df = pd.concat([min_df, vn_min_df]).copy().reset_index(drop = True)
min_df['sub1sectors'] = '14_01_mining_and_quarrying'
min_df['sub2sectors'] = 'x'

####################################################################################################
# Industry subsector production
ind_prod_df = pd.concat([min_df, cons_df, all_manf]).copy().reset_index(drop = True)
ind_prod_df = ind_prod_df[ind_prod_df['year'] < 2101].copy()
ind_prod_df = ind_prod_df[['economy', 'economy_code', 'series', 'year', 'units', 'sub1sectors', 'sub2sectors', 'value']]\
    .sort_values(by = ['economy_code', 'sub1sectors', 'sub2sectors']).copy().reset_index(drop = True)

economy_list = list(APEC_economies.keys())[:-7]
# Remove CT
economy_list = [i for i in economy_list if i != '18_CT']

for economy in economy_list:
    # Save data
    save_data = './data/industry_projections/{}/'.format(economy)

    if not os.path.isdir(save_data):
        os.makedirs(save_data)

    for sector in ind1[:-1]:
        chart_df1 = ind_prod_df[(ind_prod_df['economy_code'] == economy) & 
                                (ind_prod_df['sub1sectors'] == sector) &
                                (ind_prod_df['year'] <= 2070)].copy().reset_index(drop = True)
        if chart_df1.empty:
            pass

        else:
            fig, ax = plt.subplots()

            sns.set_theme(style = 'ticks')

            sns.lineplot(data = chart_df1,
                        x = 'year',
                        y = 'value',
                        hue = 'sub1sectors')

            ax.set(title = economy + ' ' + sector,
                xlabel = 'Year',
                ylabel = 'Production (2017 = 100)',
                ylim = (0, chart_df1['value'].max() * 1.1))
            
            plt.legend(title = '')
                    
            plt.tight_layout()
            plt.savefig(save_data + economy + '_' + sector + '.png')
            plt.show()
            plt.close()

    for sector in ind2:
        chart_df2 = ind_prod_df[(ind_prod_df['economy_code'] == economy) & 
                                (ind_prod_df['sub2sectors'] == sector) &
                                (ind_prod_df['year'] <= 2070)].copy().reset_index(drop = True)
        if chart_df2.empty:
            pass

        else:
            fig, ax = plt.subplots()

            sns.set_theme(style = 'ticks')

            sns.lineplot(data = chart_df2,
                        x = 'year',
                        y = 'value',
                        hue = 'sub2sectors')

            ax.set(title = economy + ' ' + sector,
                   xlabel = 'Year',
                   ylabel = 'Production (2017 = 100)',
                   ylim = (0, chart_df2['value'].max() * 1.1))
            
            plt.legend(title = '')
                    
            plt.tight_layout()
            plt.savefig(save_data + economy + '_' + sector + '.png')
            plt.show()
            plt.close()
 

