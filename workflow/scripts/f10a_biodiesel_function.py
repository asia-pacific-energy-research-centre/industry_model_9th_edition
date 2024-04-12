# Biogasoline
# Set working directory to be the project folder 
import os
import re

wanted_wd = 'industry_model_9th_edition'
os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

# execute config file
config_file = './config/config_apr2023.py'
with open(config_file) as infile:
    exec(infile.read())

# Modelled years 
proj_years = list(range(2022, 2101, 1))

# All years
all_years = list(range(1980, 2101, 1))
all_years_str = [str(i) for i in all_years]

id = ['scenarios', 'economy', 'sectors', 'sub1sectors',	'sub2sectors', 'sub3sectors', 'sub4sectors', 'fuels', 'subfuels']

def biodiesel_switch(economy = '01_AUS',
                     biogas_ref = False,
                     biogas_tgt = False,
                     biogas_start_ref = 2025,
                     biogas_start_tgt = 2025,
                     biogas_rate_ref = 0.002,
                     biogas_rate_tgt = 0.005):
    
    data_location = './results/industry/4_consolidation/{}/'.format(economy)

    save_location = './results/industry/5_final/{}/'.format(economy)

    if not os.path.isdir(save_location):
        os.makedirs(save_location)

    ref_prefix = economy + '_industry_ref_'
    tgt_prefix = economy + '_industry_tgt_'

    ref_files = glob.glob(data_location + ref_prefix + '*.csv')
    tgt_files = glob.glob(data_location + tgt_prefix + '*.csv')

    scenario_dict = {'ref': [biogas_ref, biogas_start_ref, biogas_rate_ref, ref_files],
                     'tgt': [biogas_tgt, biogas_start_tgt, biogas_rate_tgt, tgt_files]}

    for scenario in scenario_dict.keys():
        
        files = scenario_dict[scenario][3]
        start_year = scenario_dict[scenario][1]
        rate = scenario_dict[scenario][2]
        switch_flag = scenario_dict[scenario][0]

        latest_data = max(files, key = os.path.getctime)
        file_date = re.search(r'(\d{4})_(\d{2})_(\d{2})', latest_data).group(0)

        # Print file data info
        print(economy, scenario, 'file date:', file_date)

        scenario_df = pd.read_csv(latest_data)

        numeric_df = scenario_df.iloc[:,9:].clip(lower = 0)
        scenario_df.iloc[:, 9:] = numeric_df

        if (len(files) > 0) & (switch_flag):

            adjust_ref = pd.DataFrame(index = proj_years)
            adjust_ref['adjust'] = np.nan

            for year in range(start_year, proj_years[-1] + 1, 1):
                adjust_ref.loc[year, 'adjust'] = (year - start_year) * rate
                adjust_ref = adjust_ref.fillna(0)

            relevant_3sectors = np.delete(scenario_df['sub3sectors'].unique(),
                                          np.where(scenario_df['sub3sectors'].unique() == 'x'))

            new_sector_df = pd.DataFrame(columns = scenario_df.columns)

            # Start at lowest sector level
            for sector in relevant_3sectors:
                sector_df = scenario_df[scenario_df['sub3sectors'] == sector].copy().reset_index(drop = True)     

                # Subfuels level
                gas_sub = scenario_df[(scenario_df['sub3sectors'] == sector) &
                                       (scenario_df['subfuels'] == '07_07_gas_diesel_oil')].copy().reset_index(drop = True)
                
                biogas_sub = scenario_df[(scenario_df['sub3sectors'] == sector) &
                                          (scenario_df['subfuels'] == '16_06_biodiesel')].copy().reset_index(drop = True)
                
                # Fuels level
                gas_fuel = scenario_df[(scenario_df['sub3sectors'] == sector) &
                                       (scenario_df['fuels'] == '07_petroleum_products') &
                                       (scenario_df['subfuels'] == 'x')].copy().reset_index(drop = True)
                
                others_fuel = scenario_df[(scenario_df['sub3sectors'] == sector) &
                                          (scenario_df['fuels'] == '16_others') &
                                          (scenario_df['subfuels'] == 'x')].copy().reset_index(drop = True)
                
                subset_frames = [gas_sub, biogas_sub, gas_fuel, others_fuel]
                subset_data = pd.concat(subset_frames, ignore_index = True).copy().reset_index(drop = True)            

                # Now set aside data that won't change (to add the new changed data to at the end)
                filtered_data = sector_df.merge(subset_data, on = id + all_years_str, how = 'left', indicator = True)
                filtered_data = filtered_data[filtered_data['_merge'] == 'left_only']

                filtered_data = filtered_data.drop('_merge', axis = 1)

                # Now ensure calculations work by making the filling na's in subset data with zeroes
                gas_sub = gas_sub.copy().fillna(0)
                biogas_sub = biogas_sub.copy().fillna(0)
                gas_fuel = gas_fuel.copy().fillna(0)
                others_fuel = others_fuel.copy().fillna(0)

                adjust_ref['amount'] = np.nan
                
                # subfuels
                new_gas = gas_sub.copy()
                new_biogas = biogas_sub.copy()
                # fuels
                new_gas_fuel = gas_fuel.copy()
                new_others_fuel = others_fuel.copy()

                if gas_fuel.empty:
                    pass
                else:
                    for year in adjust_ref.index:
                        adjust_ref.loc[year, 'amount'] = gas_sub.loc[0, str(year)] * adjust_ref.loc[year, 'adjust']

                        # Subfuels level
                        new_gas.loc[0, str(year)] = gas_sub.loc[0, str(year)] - adjust_ref.loc[year, 'amount']
                        new_biogas.loc[0, str(year)] = biogas_sub.loc[0, str(year)] + adjust_ref.loc[year, 'amount']

                        # Fuels level
                        new_gas_fuel.loc[0, str(year)] = gas_fuel.loc[0, str(year)] - adjust_ref.loc[year, 'amount']
                        if others_fuel.empty:
                            new_others_fuel = new_biogas.copy()
                            new_others_fuel['subfuels'] = 'x'
                        else:
                            new_others_fuel.loc[0, str(year)] = others_fuel.loc[0, str(year)] + adjust_ref.loc[year, 'amount']
                    
                    new_sector_df = pd.concat([new_sector_df, filtered_data, new_gas, new_biogas, new_gas_fuel, new_others_fuel]).copy().reset_index(drop = True)

            # Now move to the next level up
            relevant_2sectors = np.delete(scenario_df['sub2sectors'].unique(),
                                        np.where(scenario_df['sub2sectors'].unique() == 'x'))
            
            for sector in relevant_2sectors:
                sector_df = scenario_df[(scenario_df['sub2sectors'] == sector) &
                                        (scenario_df['sub3sectors'] == 'x')].copy().reset_index(drop = True)     

                # Subfuels level
                gas_sub = scenario_df[(scenario_df['sub2sectors'] == sector) &
                                      (scenario_df['sub3sectors'] == 'x') &
                                      (scenario_df['subfuels'] == '07_07_gas_diesel_oil')].copy().reset_index(drop = True)
                
                biogas_sub = scenario_df[(scenario_df['sub2sectors'] == sector) &
                                         (scenario_df['sub3sectors'] == 'x') &
                                         (scenario_df['subfuels'] == '16_06_biodiesel')].copy().reset_index(drop = True)
                
                # Fuels level
                gas_fuel = scenario_df[(scenario_df['sub2sectors'] == sector) &
                                       (scenario_df['sub3sectors'] == 'x') &
                                       (scenario_df['fuels'] == '07_petroleum_products') &
                                       (scenario_df['subfuels'] == 'x')].copy().reset_index(drop = True)
                
                others_fuel = scenario_df[(scenario_df['sub2sectors'] == sector) &
                                          (scenario_df['sub3sectors'] == 'x') &
                                          (scenario_df['fuels'] == '16_others') &
                                          (scenario_df['subfuels'] == 'x')].copy().reset_index(drop = True)
                
                subset_frames = [gas_sub, biogas_sub, gas_fuel, others_fuel]
                subset_data = pd.concat(subset_frames, ignore_index = True).copy().reset_index(drop = True)            

                # Now set aside data that won't change (to add the new changed data to at the end)
                filtered_data = sector_df.merge(subset_data, on = id + all_years_str, how = 'left', indicator = True)
                filtered_data = filtered_data[filtered_data['_merge'] == 'left_only']

                filtered_data = filtered_data.drop('_merge', axis = 1)

                # Now ensure calculations work by making the filling na's in subset data with zeroes
                gas_sub = gas_sub.copy().fillna(0)
                biogas_sub = biogas_sub.copy().fillna(0)
                gas_fuel = gas_fuel.copy().fillna(0)
                others_fuel = others_fuel.copy().fillna(0)

                adjust_ref['amount'] = np.nan
                
                # subfuels
                new_gas = gas_sub.copy()
                new_biogas = biogas_sub.copy()
                # fuels
                new_gas_fuel = gas_fuel.copy()
                new_others_fuel = others_fuel.copy()

                if gas_fuel.empty:
                    pass
                
                else:
                    for year in adjust_ref.index:
                        adjust_ref.loc[year, 'amount'] = gas_sub.loc[0, str(year)] * adjust_ref.loc[year, 'adjust']

                        # Subfuels level
                        new_gas.loc[0, str(year)] = gas_sub.loc[0, str(year)] - adjust_ref.loc[year, 'amount']
                        new_biogas.loc[0, str(year)] = biogas_sub.loc[0, str(year)] + adjust_ref.loc[year, 'amount']

                        # Fuels level
                        new_gas_fuel.loc[0, str(year)] = gas_fuel.loc[0, str(year)] - adjust_ref.loc[year, 'amount']
                        if others_fuel.empty:
                            new_others_fuel = new_biogas.copy()
                            new_others_fuel['subfuels'] = 'x'
                        else:
                            new_others_fuel.loc[0, str(year)] = others_fuel.loc[0, str(year)] + adjust_ref.loc[year, 'amount']
                    
                    new_sector_df = pd.concat([new_sector_df, filtered_data, new_gas, new_biogas, new_gas_fuel, new_others_fuel]).copy().reset_index(drop = True)

            # Now move to the next level up
            # Can do this for all sub1sectors including 'x' because there is nothing higher than sub1sectors in industry results            
            relevant_1sectors = scenario_df['sub1sectors'].unique()
            
            for sector in relevant_1sectors:
                sector_df = scenario_df[(scenario_df['sub1sectors'] == sector) &
                                        (scenario_df['sub2sectors'] == 'x')].copy().reset_index(drop = True)     

                # Subfuels level
                gas_sub = scenario_df[(scenario_df['sub1sectors'] == sector) &
                                      (scenario_df['sub2sectors'] == 'x') &
                                      (scenario_df['subfuels'] == '07_07_gas_diesel_oil')].copy().reset_index(drop = True)
                
                biogas_sub = scenario_df[(scenario_df['sub1sectors'] == sector) &
                                         (scenario_df['sub2sectors'] == 'x') &
                                         (scenario_df['subfuels'] == '16_06_biodiesel')].copy().reset_index(drop = True)
                
                # Fuels level
                gas_fuel = scenario_df[(scenario_df['sub1sectors'] == sector) &
                                       (scenario_df['sub2sectors'] == 'x') &
                                       (scenario_df['fuels'] == '07_petroleum_products') &
                                       (scenario_df['subfuels'] == 'x')].copy().reset_index(drop = True)
                
                others_fuel = scenario_df[(scenario_df['sub1sectors'] == sector) &
                                          (scenario_df['sub2sectors'] == 'x') &
                                          (scenario_df['fuels'] == '16_others') &
                                          (scenario_df['subfuels'] == 'x')].copy().reset_index(drop = True)
                
                subset_frames = [gas_sub, biogas_sub, gas_fuel, others_fuel]
                subset_data = pd.concat(subset_frames, ignore_index = True).copy().reset_index(drop = True)            

                # Now set aside data that won't change (to add the new changed data to at the end)
                filtered_data = sector_df.merge(subset_data, on = id + all_years_str, how = 'left', indicator = True)
                filtered_data = filtered_data[filtered_data['_merge'] == 'left_only']

                filtered_data = filtered_data.drop('_merge', axis = 1)

                # Now ensure calculations work by making the filling na's in subset data with zeroes
                gas_sub = gas_sub.copy().fillna(0)
                biogas_sub = biogas_sub.copy().fillna(0)
                gas_fuel = gas_fuel.copy().fillna(0)
                others_fuel = others_fuel.copy().fillna(0)

                adjust_ref['amount'] = np.nan
                
                # subfuels
                new_gas = gas_sub.copy()
                new_biogas = biogas_sub.copy()
                # fuels
                new_gas_fuel = gas_fuel.copy()
                new_others_fuel = others_fuel.copy()

                for year in adjust_ref.index:
                    adjust_ref.loc[year, 'amount'] = gas_sub.loc[0, str(year)] * adjust_ref.loc[year, 'adjust']

                    # Subfuels level
                    new_gas.loc[0, str(year)] = gas_sub.loc[0, str(year)] - adjust_ref.loc[year, 'amount']
                    new_biogas.loc[0, str(year)] = biogas_sub.loc[0, str(year)] + adjust_ref.loc[year, 'amount']

                    # Fuels level
                    new_gas_fuel.loc[0, str(year)] = gas_fuel.loc[0, str(year)] - adjust_ref.loc[year, 'amount']
                    if others_fuel.empty:
                        new_others_fuel = new_biogas.copy()
                        new_others_fuel['subfuels'] = 'x'
                    else:
                        new_others_fuel.loc[0, str(year)] = others_fuel.loc[0, str(year)] + adjust_ref.loc[year, 'amount']
                
                new_sector_df = pd.concat([new_sector_df, filtered_data, new_gas, new_biogas, new_gas_fuel, new_others_fuel]).copy().reset_index(drop = True)

            new_sector_df = new_sector_df.sort_values(['sectors', 'sub1sectors', 'sub2sectors', 'sub3sectors', 'fuels', 'subfuels']).reset_index(drop = True)

            new_sector_df.to_csv(save_location + economy + '_industry_' + scenario + '_' + timestamp + '.csv', index = False)

        else:
            scenario_df.to_csv(save_location + economy + '_industry_' + scenario + '_' + timestamp + '.csv', index = False)