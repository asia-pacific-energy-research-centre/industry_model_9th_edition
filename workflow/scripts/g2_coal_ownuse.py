# Own use and losses
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
APEC_economies = list(APEC_economies.keys())[:-7]
APEC_economies = APEC_economies[17:18]

# 2022 and beyond
proj_years = list(range(2022, 2101, 1))
proj_years_str = [str(i) for i in proj_years]

# latest EGEDA data
EGEDA_df = pd.read_csv(latest_EGEDA)
EGEDA_df = EGEDA_df.drop(columns = ['is_subtotal'])

EGEDA_coalown_df = EGEDA_df[EGEDA_df['sub2sectors'].isin(['10_01_05_coke_ovens', '10_01_07_blast_furnaces'])]\
                        .copy().reset_index(drop = True)

for economy in APEC_economies:
    # Save location
    save_location = './results/coal_own_use/{}/'.format(economy)

    if not os.path.isdir(save_location):
        os.makedirs(save_location)

    modelled_result = './results/industry/5_final/{}/'.format(economy)

    ref_prefix = economy + '_industry_ref_'
    tgt_prefix = economy + '_industry_tgt_'

    ref_files = glob.glob(modelled_result + ref_prefix + '*.csv')
    tgt_files = glob.glob(modelled_result + tgt_prefix + '*.csv')

    # EGEDA coal ownuse
    EGEDA_coalown_ref = EGEDA_coalown_df[EGEDA_coalown_df['economy'] == economy].copy().reset_index(drop = True)
    EGEDA_coalown_tgt = EGEDA_coalown_df[EGEDA_coalown_df['economy'] == economy].copy().reset_index(drop = True)
    EGEDA_coalown_tgt['scenarios'] = 'target'

    scenario_dict = {'ref': [ref_files, EGEDA_coalown_ref],
                     'tgt': [tgt_files, EGEDA_coalown_tgt]}
    
    for scenario in scenario_dict.keys():
        files = scenario_dict[scenario][0]

        if len(files) > 0:
            latest_data = max(files, key = os.path.getctime)
            scenario_df = pd.read_csv(latest_data)

            steel_df = scenario_df[(scenario_df['sub2sectors'] == '14_03_01_iron_and_steel') &
                                   (scenario_df['sub3sectors'] == 'x') &
                                   (scenario_df['fuels'].isin(['01_coal', '02_coal_products', '07_petroleum_products', 
                                                               '08_gas', '15_solid_biomass'])) &
                                   (scenario_df['subfuels'] == 'x')].copy().reset_index(drop = True)
            
            if steel_df.empty:
                pass

            else:       
                total_steel = steel_df.groupby(['scenarios', 'economy', 'sectors', 'sub1sectors', 'sub2sectors', 
                                                'sub3sectors', 'sub4sectors', 'subfuels']).sum().reset_index()
                
                total_steel['fuels'] = 'Total of primary'
                total_steel = total_steel.fillna(0)

                own_df = scenario_dict[scenario][1]

                for year in proj_years_str:
                    if total_steel.loc[0, str(int(year) - 1)] == 0:
                        ratio = 0
                    else:
                        ratio = total_steel.loc[0, year] / total_steel.loc[0, str(int(year) - 1)]
                    for row in own_df.index:
                        own_df.loc[row, year] = own_df.loc[row, str(int(year) - 1)] * ratio

                own_df.to_csv(save_location + economy + '_coal_ownuse_' + scenario + '_' + timestamp + '.csv', index = False)