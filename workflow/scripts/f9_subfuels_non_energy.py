# Non-energy subfuel disaggregation
import re

wanted_wd = 'industry_model_9th_edition'
os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

# execute config file
config_file = './config/config_apr2023.py'
with open(config_file) as infile:
    exec(infile.read())

# Only use 21 APEC economies (economy_list defined in config file)
economy_select = economy_list[:-7]

# Fuels
egeda_fuels = pd.read_csv('./data/config/EGEDA_fuels.csv', header = 0).squeeze().to_dict()
nonenergy_fuels = list(egeda_fuels.values())
nonenergy_fuels = [nonenergy_fuels[i] for i in [0, 1, 5, 6, 7, 15]]

# Modelled years
proj_years = list(range(2021, 2101, 1))
proj_years_str = [str(i) for i in proj_years]

# All years
all_years = list(range(1980, 2101, 1))
all_years_str = [str(i) for i in all_years]

# Read in EGEDA data to 2020 to provide disaggregation of fuels
EGEDA_hist = pd.read_csv(latest_EGEDA).loc[:, :'2020']

# Relevant subfuels
coal_sub = [i for i in EGEDA_hist['subfuels'].unique() if i.startswith('01_')]
crude_sub = [i for i in EGEDA_hist['subfuels'].unique() if i.startswith('06_')]
petrol_sub = [i for i in EGEDA_hist['subfuels'].unique() if i.startswith('07_')]
gas_sub = [i for i in EGEDA_hist['subfuels'].unique() if i.startswith('08_')]

EGEDA_coal = EGEDA_hist[(EGEDA_hist['sectors'] == '17_nonenergy_use') &
                        (EGEDA_hist['sub1sectors'] == 'x') &
                        (EGEDA_hist['subfuels'].isin(coal_sub))].copy().reset_index(drop = True)

EGEDA_crude = EGEDA_hist[(EGEDA_hist['sectors'] == '17_nonenergy_use') &
                         (EGEDA_hist['sub1sectors'] == 'x') &
                         (EGEDA_hist['subfuels'].isin(crude_sub))].copy().reset_index(drop = True)

EGEDA_petrol = EGEDA_hist[(EGEDA_hist['sectors'] == '17_nonenergy_use') &
                          (EGEDA_hist['sub1sectors'] == 'x') &
                          (EGEDA_hist['subfuels'].isin(petrol_sub))].copy().reset_index(drop = True)

EGEDA_gas = EGEDA_hist[(EGEDA_hist['sectors'] == '17_nonenergy_use') &
                       (EGEDA_hist['sub1sectors'] == 'x') &
                       (EGEDA_hist['subfuels'].isin(gas_sub))].copy().reset_index(drop = True)

for economy in list(economy_select):
    # Save location for charts and data
    file_location = './results/non_energy/4_final/{}/'.format(economy)

    if not os.path.isdir(file_location):
        os.makedirs(file_location)

    # Interim files to disaggregate fuels
    files_to_disag = glob.glob(file_location + '*interim*.csv')

    ref_file = [item for item in files_to_disag if 'ref' in item]
    tgt_file = [item for item in files_to_disag if 'tgt' in item]

    if len(ref_file) + len(tgt_file) == 2:
        both_files = {'ref': ref_file[0],
                      'tgt': tgt_file[0]}  

        for file in both_files.keys(): 
            economy_df = pd.read_csv(both_files[file])

            # subfuel historical grab
            coal_subfuels = EGEDA_coal[(EGEDA_coal['economy'] == economy) &
                                    (EGEDA_coal['sectors'].isin(economy_df['sectors'].unique()))]\
                                            .copy().reset_index(drop = True)

            petrol_subfuels = EGEDA_petrol[(EGEDA_petrol['economy'] == economy) &
                                        (EGEDA_petrol['sectors'].isin(economy_df['sectors'].unique()))]\
                                            .copy().reset_index(drop = True)
            
            crude_subfuels = EGEDA_crude[(EGEDA_crude['economy'] == economy) &
                                        (EGEDA_crude['sectors'].isin(economy_df['sectors'].unique()))]\
                                            .copy().reset_index(drop = True)
            
            gas_subfuels = EGEDA_gas[(EGEDA_gas['economy'] == economy) &
                                    (EGEDA_gas['sectors'].isin(economy_df['sectors'].unique()))]\
                                            .copy().reset_index(drop = True)

            economy_df = pd.concat([economy_df, coal_subfuels, petrol_subfuels, crude_subfuels, gas_subfuels]).copy().\
                sort_values(['sectors', 'sub1sectors', 'sub2sectors', 'sub3sectors', 'fuels']).reset_index(drop = True)
            
            if file == 'tgt':
                economy_df['scenarios'] = 'target'
            else:
                pass

            economy_df = economy_df[['scenarios', 'economy', 'sectors', 'sub1sectors', 'sub2sectors', 
                            'sub3sectors', 'sub4sectors', 'fuels', 'subfuels'] + all_years_str]\
                                    .copy().reset_index(drop = True)
            
            # New data frame to build in disaggregated results
            groundup_df = pd.DataFrame()

            # Now sectors
            if len(economy_df['sectors'].unique()) == 1:

                # Grab the 19_total and 16_x_hydrogen for later
                agg_totals = economy_df[economy_df['fuels'] == '19_total'].copy().reset_index(drop = True)
                
                hydrogen_grab = economy_df[economy_df['subfuels'] == '16_x_hydrogen'].copy().reset_index(drop = True)
                
                for fuel in economy_df['fuels'].unique()[:-1]:
                    temp_df = economy_df[economy_df['fuels'] == fuel].copy().reset_index(drop = True)
                    
                    fuel_total_row = temp_df[temp_df['subfuels'] == 'x'].copy().reset_index(drop = True)

                    hydrogen_adjust = temp_df[temp_df['subfuels'] == '16_x_hydrogen'].copy().reset_index(drop = True)
                    
                    if hydrogen_adjust.empty:
                        pass
                    else:
                        fuel_total_row_copy = fuel_total_row.copy()
                        hydrogen_adjust.fillna(0, inplace = True)
                        for year in proj_years_str:
                            fuel_total_row.loc[0, year] = fuel_total_row_copy.loc[0, year] - hydrogen_adjust.loc[0, year]

                    subfuels_df = temp_df[~temp_df['subfuels'].isin(['x', '16_x_hydrogen'])].copy().reset_index(drop = True)

                    # Need the 2020 ratio
                    fuel_ratio = subfuels_df.loc[:, ['subfuels', '2020']].copy().reset_index(drop = True)

                    fuel_ratio['ratio'] = np.nan
                    total_for_calc = fuel_total_row.loc[0, '2020']

                    for i in range(len(fuel_ratio['subfuels'].unique())):
                        # To avoid dividng by zero
                        if total_for_calc == 0:
                            fuel_ratio.iloc[i, 2] = total_for_calc
                        else: 
                            fuel_ratio.iloc[i, 2] = fuel_ratio.iloc[i, 1] / total_for_calc

                    for year in proj_years_str:
                        for fuel in fuel_ratio['subfuels'].unique():
                            subfuels_df.loc[subfuels_df['subfuels'] == fuel, year] = \
                                fuel_total_row.loc[0, year] * fuel_ratio.loc[fuel_ratio['subfuels'] == fuel, 'ratio']

                    # Now if hydrogen subtracted from 16_others, add the original 16_others total line in        
                    if hydrogen_adjust.empty:
                        pass
                    else:
                        fuel_total_row = fuel_total_row_copy.copy()
                            
                    groundup_df = pd.concat([groundup_df, fuel_total_row, subfuels_df]).copy().reset_index(drop = True)
                    
                groundup_df = pd.concat([groundup_df, agg_totals, hydrogen_grab]).copy().reset_index(drop = True)

            else:
                pass
            
            groundup_df = groundup_df.sort_values(['sectors', 'sub1sectors', 'sub2sectors', 
                                                    'sub3sectors', 'fuels', 'subfuels']).reset_index(drop = True)

            groundup_df.to_csv(file_location + economy + '_nonenergy_' + file + '_' + timestamp + '.csv', index = False)

        else:
            pass
