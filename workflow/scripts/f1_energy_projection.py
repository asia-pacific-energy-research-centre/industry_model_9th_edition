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

# Grab insudtrial production trajectories and also energy data
ind_energy_df = pd.read_csv(latest_inden)
EGEDA_df = pd.read_csv(latest_EGEDA)

# Energy industry subsectors
industry_sectors = pd.read_csv('./data/EGEDA/industry_egeda.csv', header = None)\
    .squeeze().to_dict()

ind1 = list(industry_sectors.values())[:3]
ind2 = list(industry_sectors.values())[3:]

# Only use 21 APEC economies (economy_list defined in config file)
economy_select = economy_list[:-7]

EGEDA_2020_df = EGEDA_df[list(EGEDA_df.iloc[:,:9].columns) + ['2020']]

EGEDA_ind_2020_df = EGEDA_2020_df[(EGEDA_2020_df['sub1sectors'].str.startswith('14_')) &
                                  (EGEDA_2020_df['sub3sectors'] == 'x') &
                                  (EGEDA_2020_df['subfuels'].isin(['x']))]\
                                    .copy().reset_index(drop = True)

EGEDA_ind_2020_df = EGEDA_ind_2020_df.melt(id_vars = ['economy', 'sub1sectors', 'sub2sectors', 'fuels', 'subfuels'],
                                           value_vars = '2020',
                                           var_name = 'year',
                                           value_name = 'energy')

EGEDA_ind_2020_df['year'] = EGEDA_ind_2020_df['year'].astype('int') 

for economy in economy_select:
    # Save location for charts and data
    save_location = './results/industry/2_energy_projctions/{}/'.format(economy)

    if not os.path.isdir(save_location):
        os.makedirs(save_location)
    for sector in ind1[:2]: 
        energy_df = EGEDA_ind_2020_df[(EGEDA_ind_2020_df['economy'] == economy) &
                                     (EGEDA_ind_2020_df['sub1sectors'] == sector)]\
                                        .copy().reset_index(drop = True)
        
        fuel_ratio_2020 = energy_df.loc[:, ['fuels', 'energy']]

        for i in range(len(energy_df)):
            fuel_ratio_2020.iloc[i, 1] = energy_df.iloc[i, -1] / \
                energy_df.loc[energy_df['fuels'] == '19_total', 'energy']
        
    for sector in ind2: 
        energy_df = EGEDA_ind_2020_df[(EGEDA_ind_2020_df['economy'] == economy) &
                                      (EGEDA_ind_2020_df['sub2sectors'] == sector)]\
                                        .copy().reset_index(drop = True)
        
        fuel_ratio_2020 = energy_df.loc[:, ['fuels', 'energy']]

        for i in range(len(energy_df)):
            fuel_ratio_2020.iloc[i, 1] = energy_df.iloc[i, -1] / \
                energy_df.loc[energy_df['fuels'] == '19_total', 'energy']
        
    


