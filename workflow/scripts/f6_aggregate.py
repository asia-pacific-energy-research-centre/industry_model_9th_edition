# Consolidate results ready for integration
import re

wanted_wd = 'industry_model_9th_edition'
os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

# execute config file
config_file = './config/config_apr2023.py'
with open(config_file) as infile:
    exec(infile.read())

# Only use 21 APEC economies (economy_list defined in config file)
economy_select = economy_list[:-7]

# Energy industry subsectors
industry_sectors = pd.read_csv('./data/EGEDA/industry_egeda.csv', header = None)\
    .squeeze().to_dict()

ind1 = list(industry_sectors.values())[:3]
ind2 = list(industry_sectors.values())[3:]

# Fuels
egeda_fuels = pd.read_csv('./data/config/EGEDA_fuels.csv', header = 0).squeeze().to_dict()
industry_fuels = list(egeda_fuels.values())
industry_fuels = [industry_fuels[i] for i in [0, 1, 5, 6, 7, 11, 14, 15, 16, 17]]

# Modelled years
proj_years = list(range(2021, 2101, 1))

proj_years_str = [str(i) for i in proj_years]

# Read in EGEDA data to 2020 to provide disaggregation of crudeoil and ngl and petroleum products
EGEDA_hist = pd.read_csv(latest_EGEDA).loc[:, :'2020']

EGEDA_coal = EGEDA_hist[(EGEDA_hist['sectors'] == '14_industry_sector') &
                        (EGEDA_hist['subfuels'].isin(['01_01_coking_coal', '01_x_thermal_coal', '01_05_lignite']))].copy().reset_index(drop = True)

EGEDA_crude = EGEDA_hist[(EGEDA_hist['sectors'] == '14_industry_sector') &
                          (EGEDA_hist['subfuels'].str.startswith('06_'))].copy().reset_index(drop = True)

EGEDA_petrol = EGEDA_hist[(EGEDA_hist['sectors'] == '14_industry_sector') &
                          (EGEDA_hist['subfuels'].str.startswith('07_'))].copy().reset_index(drop = True)

EGEDA_gas = EGEDA_hist[(EGEDA_hist['sectors'] == '14_industry_sector') &
                       (EGEDA_hist['subfuels'].isin(['08_01_natural_gas', '08_02_lng', '08_03_gas_works_gas']))].copy().reset_index(drop = True)

EGEDA_biomass = EGEDA_hist[(EGEDA_hist['sectors'] == '14_industry_sector') &
                           (EGEDA_hist['subfuels'].isin(['15_01_fuelwood_and_woodwaste', '15_02_bagasse', 
                                                         '15_03_charcoal', '15_04_black_liquor', '15_05_other_biomass']))].copy().reset_index(drop = True)

EGEDA_others = EGEDA_hist[(EGEDA_hist['sectors'] == '14_industry_sector') &
                           (EGEDA_hist['subfuels'].isin(['16_01_biogas', '16_02_industrial_waste',
                                                         '16_03_municipal_solid_waste_renewable',
                                                         '16_04_municipal_solid_waste_nonrenewable', '16_05_biogasoline',
                                                         '16_06_biodiesel', '16_07_bio_jet_kerosene',
                                                         '16_08_other_liquid_biofuels', '16_09_other_sources']))].copy().reset_index(drop = True)

# Read in steel data
for economy in [list(economy_select)[-3]]:
    # Save location for charts and data
    save_location = './results/industry/4_final/{}/'.format(economy)

    if not os.path.isdir(save_location):
        os.makedirs(save_location)

    file_location = './results/industry/3_fuel_switch/{}/all_sectors/'.format(economy)

    files_to_agg = glob.glob(file_location + '*wide*.csv')

    ref_file = [item for item in files_to_agg if 'ref' in item]
    tgt_file = [item for item in files_to_agg if 'tgt' in item]
    
    # Begin aggregation process
    # REF
    if len(ref_file) == 1: 
        ref_df = pd.read_csv(ref_file[0])
    
        # Define new empty dataframe to save results in 
        groundup_df = pd.DataFrame()

        # TGT
        # Start at lowest sector results (for industry: sub3sectors)
        for sector in ref_df['sub3sectors'].unique():
            if sector == 'x':
                pass

            else:
                ref_temp1 = ref_df[(ref_df['sub3sectors'] == sector) &
                                (ref_df['subfuels'] == 'x')].copy().reset_index(drop = True)
                
                total_row = ref_temp1[ref_temp1['fuels'].isin(industry_fuels)]\
                    .groupby(['scenarios', 'economy', 'sectors','sub1sectors', 'sub2sectors', 'sub3sectors',
                            'sub4sectors', 'subfuels']).sum()\
                    .assign(fuels = '19_total').reset_index()
                
                ref_temp2 = pd.concat([ref_temp1, total_row]).copy().reset_index(drop = True)

                groundup_df = pd.concat([groundup_df, ref_temp2]).copy().reset_index(drop = True)

        # Now one level higher
        for sector in ref_df['sub2sectors'].unique():
            if sector == 'x':
                pass

            else:
                ref_temp3 = ref_df[(ref_df['sub2sectors'] == sector) &
                                    (ref_df['subfuels'] == 'x')].copy().reset_index(drop = True)
                
                # Now aggregate sub2sectors
                agg_2sectors = ref_temp3.groupby(['scenarios', 'economy', 'sectors','sub1sectors', 'sub2sectors', 
                                                'sub4sectors', 'fuels', 'subfuels']).sum()\
                                                .assign(sub3sectors = 'x').reset_index()
            
                total_row = agg_2sectors[agg_2sectors['fuels'].isin(industry_fuels)]\
                    .groupby(['scenarios', 'economy', 'sectors','sub1sectors', 'sub2sectors', 'sub3sectors',
                            'sub4sectors', 'subfuels']).sum()\
                    .assign(fuels = '19_total').reset_index()
                
                ref_temp4 = pd.concat([agg_2sectors, total_row]).copy().reset_index(drop = True)

                groundup_df = pd.concat([groundup_df, ref_temp4]).copy().reset_index(drop = True)

        # And one level higher
        for sector in ref_df['sub1sectors'].unique():
            if sector == 'x':
                pass

            else:
                ref_temp5 = ref_df[(ref_df['sub1sectors'] == sector) &
                                    (ref_df['subfuels'] == 'x')].copy().reset_index(drop = True)
                
                # Now aggregate sub2sectors
                agg_1sectors = ref_temp5.groupby(['scenarios', 'economy', 'sectors', 'sub1sectors', 
                                                'sub4sectors', 'fuels', 'subfuels']).sum()\
                                                .assign(sub2sectors = 'x', sub3sectors = 'x').reset_index()
            
                total_row = agg_1sectors[agg_1sectors['fuels'].isin(industry_fuels)]\
                    .groupby(['scenarios', 'economy', 'sectors', 'sub1sectors', 'sub2sectors', 'sub3sectors',
                            'sub4sectors', 'subfuels']).sum()\
                    .assign(fuels = '19_total').reset_index()
                
                ref_temp6 = pd.concat([agg_1sectors, total_row]).copy().reset_index(drop = True)

                groundup_df = pd.concat([groundup_df, ref_temp6]).copy().reset_index(drop = True)

        # And final level
        for sector in ref_df['sectors'].unique():
            if sector == 'x':
                pass

            else:
                ref_temp7 = ref_df[(ref_df['sectors'] == sector) &
                                    (ref_df['subfuels'] == 'x')].copy().reset_index(drop = True)
                
                # Now aggregate sub2sectors
                agg_sectors = ref_temp7.groupby(['scenarios', 'economy', 'sectors', 
                                                'sub4sectors', 'fuels', 'subfuels']).sum()\
                                                .assign(sub1sectors = 'x', sub2sectors = 'x', sub3sectors = 'x').reset_index()
            
                total_row = agg_sectors[agg_sectors['fuels'].isin(industry_fuels)]\
                    .groupby(['scenarios', 'economy', 'sectors', 'sub1sectors', 'sub2sectors', 'sub3sectors',
                            'sub4sectors', 'subfuels']).sum()\
                    .assign(fuels = '19_total').reset_index()
                
                ref_temp8 = pd.concat([agg_sectors, total_row]).copy().reset_index(drop = True)

                groundup_df = pd.concat([groundup_df, ref_temp8]).copy().reset_index(drop = True)

        # Now add in the one subfuel: hydrogen for relevant sector aggregations
        hydrogen_rows_ref = ref_df[ref_df['subfuels'] == '16_x_hydrogen'].copy().reset_index(drop = True)

        hyd_sub3_ref = hydrogen_rows_ref.copy()
        for i in hyd_sub3_ref.index:       
            hyd_sub3_ref.loc[i, 'sub3sectors'] = 'x'
        
        hyd_sub2_ref = hyd_sub3_ref.copy()
        for j in hyd_sub2_ref.index:
            hyd_sub2_ref.loc[j, 'sub2sectors'] = 'x'

        hyd_sub1_ref = hyd_sub2_ref.copy()
        for z in hyd_sub1_ref.index:
            hyd_sub1_ref.loc[z, 'sub1sectors'] = 'x'

        hyd_ref = pd.concat([hydrogen_rows_ref, hyd_sub3_ref, hyd_sub2_ref, hyd_sub1_ref]).copy().drop_duplicates()

        groundup_df = pd.concat([groundup_df, hyd_ref]).copy()\
            .sort_values(['sectors', 'sub1sectors', 'sub2sectors', 'sub3sectors', 'fuels']).reset_index(drop = True)
        
        # Petroleum products and crude oil disaggregation grab
        coal_subfuels = EGEDA_coal[(EGEDA_coal['economy'] == economy) &
                                   (EGEDA_coal['sub3sectors'].isin(groundup_df['sub3sectors'].unique()))]\
                                        .copy().reset_index(drop = True)

        petrol_subfuels = EGEDA_petrol[(EGEDA_petrol['economy'] == economy) &
                                       (EGEDA_petrol['sub3sectors'].isin(groundup_df['sub3sectors'].unique()))]\
                                        .copy().reset_index(drop = True)
        
        crude_subfuels = EGEDA_crude[(EGEDA_crude['economy'] == economy) &
                                     (EGEDA_crude['sub3sectors'].isin(groundup_df['sub3sectors'].unique()))]\
                                        .copy().reset_index(drop = True)
        
        gas_subfuels = EGEDA_gas[(EGEDA_gas['economy'] == economy) &
                                 (EGEDA_gas['sub3sectors'].isin(groundup_df['sub3sectors'].unique()))]\
                                        .copy().reset_index(drop = True)
        
        biomass_subfuels = EGEDA_biomass[(EGEDA_biomass['economy'] == economy) &
                                         (EGEDA_biomass['sub3sectors'].isin(groundup_df['sub3sectors'].unique()))]\
                                        .copy().reset_index(drop = True)
        
        other_subfuels = EGEDA_others[(EGEDA_others['economy'] == economy) &
                                         (EGEDA_others['sub3sectors'].isin(groundup_df['sub3sectors'].unique()))]\
                                        .copy().reset_index(drop = True)

        groundup_df = pd.concat([groundup_df, coal_subfuels, petrol_subfuels, crude_subfuels, gas_subfuels, biomass_subfuels,
                                 other_subfuels]).copy().\
            sort_values(['sectors', 'sub1sectors', 'sub2sectors', 'sub3sectors', 'fuels']).reset_index(drop = True)

        groundup_df = groundup_df[['scenarios', 'economy', 'sectors', 'sub1sectors', 'sub2sectors', 
                                   'sub3sectors', 'sub4sectors', 'fuels', 'subfuels'] + [str(i) for i in range(1980, 2101, 1)]]\
                                   .copy().reset_index(drop = True)
        
        # New data frame to build in disaggregated results
        groundup_df2 = pd.DataFrame()

        # # Now forward fill for each sector breakdown, starting with sub3sectors
        # Sub3sectors
        if len(groundup_df['sub3sectors'].unique()) > 1:
            # Define array without 'x'
            relevant_sectors = np.delete(groundup_df['sub3sectors'].unique(), 
                                         np.where(groundup_df['sub3sectors'].unique() == 'x'))
            
            for sector in relevant_sectors:

                # Grab the 19_total and 16_x_hydrogen for later
                agg_totals = groundup_df[(groundup_df['sub3sectors'] == sector) &
                                         (groundup_df['sub4sectors'] == 'x') &
                                            (groundup_df['fuels'] == '19_total')].copy().reset_index(drop = True)
                
                hydrogen_grab = groundup_df[(groundup_df['sub3sectors'] == sector) &
                                            (groundup_df['sub4sectors'] == 'x') &
                                            (groundup_df['subfuels'] == '16_x_hydrogen')].copy().reset_index(drop = True)
                
                for fuel in groundup_df['fuels'].unique()[:-1]:
                    temp_sub3 = groundup_df[(groundup_df['sub3sectors'] == sector) &
                                            (groundup_df['sub4sectors'] == 'x') &
                                            (groundup_df['fuels'] == fuel)].copy().reset_index(drop = True)
                    
                    fuel_total_row = temp_sub3[temp_sub3['subfuels'] == 'x'].copy().reset_index(drop = True)

                    hydrogen_adjust = temp_sub3[temp_sub3['subfuels'] == '16_x_hydrogen'].copy().reset_index(drop = True)
                    
                    if hydrogen_adjust.empty:
                        pass
                    else:
                        fuel_total_row_copy = fuel_total_row.copy()
                        hydrogen_adjust.fillna(0, inplace = True)
                        for year in proj_years_str:
                            fuel_total_row.loc[0, year] = fuel_total_row_copy.loc[0, year] - hydrogen_adjust.loc[0, year]

                    subfuels_df = temp_sub3[~temp_sub3['subfuels'].isin(['x', '16_x_hydrogen'])].copy().reset_index(drop = True)

                    # Need the 2020 ratio
                    fuel_ratio_ref = subfuels_df.loc[:, ['subfuels', '2020']].copy().reset_index(drop = True)

                    fuel_ratio_ref['ratio'] = np.nan
                    total_for_calc = fuel_total_row.loc[0, '2020']

                    for i in range(len(fuel_ratio_ref['subfuels'].unique())):
                        # To avoid dividng by zero
                        if total_for_calc == 0:
                            fuel_ratio_ref.iloc[i, 2] = total_for_calc
                        else: 
                            fuel_ratio_ref.iloc[i, 2] = fuel_ratio_ref.iloc[i, 1] / total_for_calc

                    for year in proj_years_str:
                        for fuel in fuel_ratio_ref['subfuels'].unique():
                            subfuels_df.loc[subfuels_df['subfuels'] == fuel, year] = \
                                fuel_total_row.loc[0, year] * fuel_ratio_ref.loc[fuel_ratio_ref['subfuels'] == fuel, 'ratio']
                    
                    # Now if hydrogen subtracted from 16_others, add the original 16_others total line in
                    if hydrogen_adjust.empty:
                        pass
                    else:
                        fuel_total_row = fuel_total_row_copy.copy()
                            
                    groundup_df2 = pd.concat([groundup_df2, fuel_total_row, subfuels_df]).copy().reset_index(drop = True)
                    
                groundup_df2 = pd.concat([groundup_df2, agg_totals, hydrogen_grab]).copy().reset_index(drop = True)

        else:
            pass
        
        # Now sub2sectors
        if len(groundup_df['sub2sectors'].unique()) > 1:
            # Define array without 'x'
            relevant_sectors = np.delete(groundup_df['sub2sectors'].unique(), 
                                         np.where(groundup_df['sub2sectors'].unique() == 'x'))
            
            for sector in relevant_sectors:

                # Grab the 19_total and 16_x_hydrogen for later
                agg_totals = groundup_df[(groundup_df['sub2sectors'] == sector) &
                                         (groundup_df['sub3sectors'] == 'x') &
                                         (groundup_df['sub4sectors'] == 'x') &
                                            (groundup_df['fuels'] == '19_total')].copy().reset_index(drop = True)
                
                hydrogen_grab = groundup_df[(groundup_df['sub2sectors'] == sector) &
                                            (groundup_df['sub3sectors'] == 'x') &
                                            (groundup_df['sub4sectors'] == 'x') &
                                            (groundup_df['subfuels'] == '16_x_hydrogen')].copy().reset_index(drop = True)
                
                for fuel in groundup_df['fuels'].unique()[:-1]:
                    temp_sub2 = groundup_df[(groundup_df['sub2sectors'] == sector) &
                                            (groundup_df['sub3sectors'] == 'x') &
                                            (groundup_df['sub4sectors'] == 'x') &
                                            (groundup_df['fuels'] == fuel)].copy().reset_index(drop = True)
                    
                    fuel_total_row = temp_sub2[temp_sub2['subfuels'] == 'x'].copy().reset_index(drop = True)

                    hydrogen_adjust = temp_sub2[temp_sub2['subfuels'] == '16_x_hydrogen'].copy().reset_index(drop = True)
                    
                    if hydrogen_adjust.empty:
                        pass
                    else:
                        fuel_total_row_copy = fuel_total_row.copy()
                        hydrogen_adjust.fillna(0, inplace = True)
                        for year in proj_years_str:
                            fuel_total_row.loc[0, year] = fuel_total_row_copy.loc[0, year] - hydrogen_adjust.loc[0, year]

                    subfuels_df = temp_sub2[~temp_sub2['subfuels'].isin(['x', '16_x_hydrogen'])].copy().reset_index(drop = True)

                    # Need the 2020 ratio
                    fuel_ratio_ref = subfuels_df.loc[:, ['subfuels', '2020']].copy().reset_index(drop = True)

                    fuel_ratio_ref['ratio'] = np.nan
                    total_for_calc = fuel_total_row.loc[0, '2020']

                    for i in range(len(fuel_ratio_ref['subfuels'].unique())):
                        # To avoid dividng by zero
                        if total_for_calc == 0:
                            fuel_ratio_ref.iloc[i, 2] = total_for_calc
                        else: 
                            fuel_ratio_ref.iloc[i, 2] = fuel_ratio_ref.iloc[i, 1] / total_for_calc

                    for year in proj_years_str:
                        for fuel in fuel_ratio_ref['subfuels'].unique():
                            subfuels_df.loc[subfuels_df['subfuels'] == fuel, year] = \
                                fuel_total_row.loc[0, year] * fuel_ratio_ref.loc[fuel_ratio_ref['subfuels'] == fuel, 'ratio']

                    # Now if hydrogen subtracted from 16_others, add the original 16_others total line in        
                    if hydrogen_adjust.empty:
                        pass
                    else:
                        fuel_total_row = fuel_total_row_copy.copy()
                            
                    groundup_df2 = pd.concat([groundup_df2, fuel_total_row, subfuels_df]).copy().reset_index(drop = True)
                    
                groundup_df2 = pd.concat([groundup_df2, agg_totals, hydrogen_grab]).copy().reset_index(drop = True)

        else:
            pass

        # Now sub1sectors
        if len(groundup_df['sub1sectors'].unique()) > 1:
            # Define array without 'x'
            relevant_sectors = np.delete(groundup_df['sub1sectors'].unique(), 
                                         np.where(groundup_df['sub1sectors'].unique() == 'x'))
            
            for sector in relevant_sectors:

                # Grab the 19_total and 16_x_hydrogen for later
                agg_totals = groundup_df[(groundup_df['sub1sectors'] == sector) &
                                         (groundup_df['sub2sectors'] == 'x') &
                                         (groundup_df['sub3sectors'] == 'x') &
                                         (groundup_df['sub4sectors'] == 'x') &
                                            (groundup_df['fuels'] == '19_total')].copy().reset_index(drop = True)
                
                hydrogen_grab = groundup_df[(groundup_df['sub1sectors'] == sector) &
                                            (groundup_df['sub2sectors'] == 'x') &
                                            (groundup_df['sub3sectors'] == 'x') &
                                            (groundup_df['sub4sectors'] == 'x') &
                                            (groundup_df['subfuels'] == '16_x_hydrogen')].copy().reset_index(drop = True)
                
                for fuel in groundup_df['fuels'].unique()[:-1]:
                    temp_sub1 = groundup_df[(groundup_df['sub1sectors'] == sector) &
                                            (groundup_df['sub2sectors'] == 'x') &
                                            (groundup_df['sub3sectors'] == 'x') &
                                            (groundup_df['sub4sectors'] == 'x') &
                                            (groundup_df['fuels'] == fuel)].copy().reset_index(drop = True)
                    
                    fuel_total_row = temp_sub1[temp_sub1['subfuels'] == 'x'].copy().reset_index(drop = True)

                    hydrogen_adjust = temp_sub1[temp_sub1['subfuels'] == '16_x_hydrogen'].copy().reset_index(drop = True)
                    
                    if hydrogen_adjust.empty:
                        pass
                    else:
                        fuel_total_row_copy = fuel_total_row.copy()
                        hydrogen_adjust.fillna(0, inplace = True)
                        for year in proj_years_str:
                            fuel_total_row.loc[0, year] = fuel_total_row_copy.loc[0, year] - hydrogen_adjust.loc[0, year]

                    subfuels_df = temp_sub1[~temp_sub1['subfuels'].isin(['x', '16_x_hydrogen'])].copy().reset_index(drop = True)

                    # Need the 2020 ratio
                    fuel_ratio_ref = subfuels_df.loc[:, ['subfuels', '2020']].copy().reset_index(drop = True)

                    fuel_ratio_ref['ratio'] = np.nan
                    total_for_calc = fuel_total_row.loc[0, '2020']

                    for i in range(len(fuel_ratio_ref['subfuels'].unique())):
                        # To avoid dividng by zero
                        if total_for_calc == 0:
                            fuel_ratio_ref.iloc[i, 2] = total_for_calc
                        else: 
                            fuel_ratio_ref.iloc[i, 2] = fuel_ratio_ref.iloc[i, 1] / total_for_calc

                    for year in proj_years_str:
                        for fuel in fuel_ratio_ref['subfuels'].unique():
                            subfuels_df.loc[subfuels_df['subfuels'] == fuel, year] = \
                                fuel_total_row.loc[0, year] * fuel_ratio_ref.loc[fuel_ratio_ref['subfuels'] == fuel, 'ratio']

                    # Now if hydrogen subtracted from 16_others, add the original 16_others total line in        
                    if hydrogen_adjust.empty:
                        pass
                    else:
                        fuel_total_row = fuel_total_row_copy.copy()
                            
                    groundup_df2 = pd.concat([groundup_df2, fuel_total_row, subfuels_df]).copy().reset_index(drop = True)
                    
                groundup_df2 = pd.concat([groundup_df2, agg_totals, hydrogen_grab]).copy().reset_index(drop = True)

        else:
            pass

        # Now sectors
        if len(groundup_df['sectors'].unique()) == 1:
            # Define array without 'x'
            relevant_sectors = np.delete(groundup_df['sectors'].unique(), 
                                         np.where(groundup_df['sectors'].unique() == 'x'))
            
            for sector in relevant_sectors:

                # Grab the 19_total and 16_x_hydrogen for later
                agg_totals = groundup_df[(groundup_df['sectors'] == sector) &
                                         (groundup_df['sub1sectors'] == 'x') &
                                         (groundup_df['sub2sectors'] == 'x') &
                                         (groundup_df['sub3sectors'] == 'x') &
                                         (groundup_df['sub4sectors'] == 'x') &
                                            (groundup_df['fuels'] == '19_total')].copy().reset_index(drop = True)
                
                hydrogen_grab = groundup_df[(groundup_df['sectors'] == sector) &
                                            (groundup_df['sub1sectors'] == 'x') &
                                            (groundup_df['sub2sectors'] == 'x') &
                                            (groundup_df['sub3sectors'] == 'x') &
                                            (groundup_df['sub4sectors'] == 'x') &
                                            (groundup_df['subfuels'] == '16_x_hydrogen')].copy().reset_index(drop = True)
                
                for fuel in groundup_df['fuels'].unique()[:-1]:
                    temp_sect = groundup_df[(groundup_df['sectors'] == sector) &
                                            (groundup_df['sub1sectors'] == 'x') &
                                            (groundup_df['sub2sectors'] == 'x') &
                                            (groundup_df['sub3sectors'] == 'x') &
                                            (groundup_df['sub4sectors'] == 'x') &
                                            (groundup_df['fuels'] == fuel)].copy().reset_index(drop = True)
                    
                    fuel_total_row = temp_sect[temp_sect['subfuels'] == 'x'].copy().reset_index(drop = True)

                    hydrogen_adjust = temp_sect[temp_sect['subfuels'] == '16_x_hydrogen'].copy().reset_index(drop = True)
                    
                    if hydrogen_adjust.empty:
                        pass
                    else:
                        fuel_total_row_copy = fuel_total_row.copy()
                        hydrogen_adjust.fillna(0, inplace = True)
                        for year in proj_years_str:
                            fuel_total_row.loc[0, year] = fuel_total_row_copy.loc[0, year] - hydrogen_adjust.loc[0, year]

                    subfuels_df = temp_sect[~temp_sect['subfuels'].isin(['x', '16_x_hydrogen'])].copy().reset_index(drop = True)

                    # Need the 2020 ratio
                    fuel_ratio_ref = subfuels_df.loc[:, ['subfuels', '2020']].copy().reset_index(drop = True)

                    fuel_ratio_ref['ratio'] = np.nan
                    total_for_calc = fuel_total_row.loc[0, '2020']

                    for i in range(len(fuel_ratio_ref['subfuels'].unique())):
                        # To avoid dividng by zero
                        if total_for_calc == 0:
                            fuel_ratio_ref.iloc[i, 2] = total_for_calc
                        else: 
                            fuel_ratio_ref.iloc[i, 2] = fuel_ratio_ref.iloc[i, 1] / total_for_calc

                    for year in proj_years_str:
                        for fuel in fuel_ratio_ref['subfuels'].unique():
                            subfuels_df.loc[subfuels_df['subfuels'] == fuel, year] = \
                                fuel_total_row.loc[0, year] * fuel_ratio_ref.loc[fuel_ratio_ref['subfuels'] == fuel, 'ratio']

                    # Now if hydrogen subtracted from 16_others, add the original 16_others total line in        
                    if hydrogen_adjust.empty:
                        pass
                    else:
                        fuel_total_row = fuel_total_row_copy.copy()
                            
                    groundup_df2 = pd.concat([groundup_df2, fuel_total_row, subfuels_df]).copy().reset_index(drop = True)
                    
                groundup_df2 = pd.concat([groundup_df2, agg_totals, hydrogen_grab]).copy().reset_index(drop = True)

        else:
            pass
        
        groundup_df2 = groundup_df2.sort_values(['sectors', 'sub1sectors', 'sub2sectors', 
                                                 'sub3sectors', 'fuels', 'subfuels']).reset_index(drop = True)

        groundup_df2.to_csv(save_location + economy + '_industry_ref_' + timestamp + '.csv', index = False)
    
    else:
        pass
    
    ##################################################################################################################################
    # TGT
    if len(tgt_file) == 1:
        tgt_df = pd.read_csv(tgt_file[0])

        # Define new empty dataframe to save results in 
        groundup_df = pd.DataFrame()

        # TGT
        # Start at lowest sector results (for industry: sub3sectors)
        for sector in tgt_df['sub3sectors'].unique():
            if sector == 'x':
                pass

            else:
                tgt_temp1 = tgt_df[(tgt_df['sub3sectors'] == sector) &
                                (tgt_df['subfuels'] == 'x')].copy().reset_index(drop = True)
                
                total_row = tgt_temp1[tgt_temp1['fuels'].isin(industry_fuels)]\
                    .groupby(['scenarios', 'economy', 'sectors','sub1sectors', 'sub2sectors', 'sub3sectors',
                            'sub4sectors', 'subfuels']).sum()\
                    .assign(fuels = '19_total').reset_index()
                
                tgt_temp2 = pd.concat([tgt_temp1, total_row]).copy().reset_index(drop = True)

                groundup_df = pd.concat([groundup_df, tgt_temp2]).copy().reset_index(drop = True)

        # Now one level higher
        for sector in tgt_df['sub2sectors'].unique():
            if sector == 'x':
                pass

            else:
                tgt_temp3 = tgt_df[(tgt_df['sub2sectors'] == sector) &
                                    (tgt_df['subfuels'] == 'x')].copy().reset_index(drop = True)
                
                # Now aggregate sub2sectors
                agg_2sectors = tgt_temp3.groupby(['scenarios', 'economy', 'sectors','sub1sectors', 'sub2sectors', 
                                                'sub4sectors', 'fuels', 'subfuels']).sum()\
                                                .assign(sub3sectors = 'x').reset_index()
            
                total_row = agg_2sectors[agg_2sectors['fuels'].isin(industry_fuels)]\
                    .groupby(['scenarios', 'economy', 'sectors','sub1sectors', 'sub2sectors', 'sub3sectors',
                            'sub4sectors', 'subfuels']).sum()\
                    .assign(fuels = '19_total').reset_index()
                
                tgt_temp4 = pd.concat([agg_2sectors, total_row]).copy().reset_index(drop = True)

                groundup_df = pd.concat([groundup_df, tgt_temp4]).copy().reset_index(drop = True)

        # And one level higher
        for sector in tgt_df['sub1sectors'].unique():
            if sector == 'x':
                pass

            else:
                tgt_temp5 = tgt_df[(tgt_df['sub1sectors'] == sector) &
                                    (tgt_df['subfuels'] == 'x')].copy().reset_index(drop = True)
                
                # Now aggregate sub2sectors
                agg_1sectors = tgt_temp5.groupby(['scenarios', 'economy', 'sectors', 'sub1sectors', 
                                                'sub4sectors', 'fuels', 'subfuels']).sum()\
                                                .assign(sub2sectors = 'x', sub3sectors = 'x').reset_index()
            
                total_row = agg_1sectors[agg_1sectors['fuels'].isin(industry_fuels)]\
                    .groupby(['scenarios', 'economy', 'sectors', 'sub1sectors', 'sub2sectors', 'sub3sectors',
                            'sub4sectors', 'subfuels']).sum()\
                    .assign(fuels = '19_total').reset_index()
                
                tgt_temp6 = pd.concat([agg_1sectors, total_row]).copy().reset_index(drop = True)

                groundup_df = pd.concat([groundup_df, tgt_temp6]).copy().reset_index(drop = True)

        # And final level
        for sector in tgt_df['sectors'].unique():
            if sector == 'x':
                pass
            
            else:
                tgt_temp7 = tgt_df[(tgt_df['sectors'] == sector) &
                                    (tgt_df['subfuels'] == 'x')].copy().reset_index(drop = True)
                
                # Now aggregate sub2sectors
                agg_sectors = tgt_temp7.groupby(['scenarios', 'economy', 'sectors', 
                                                'sub4sectors', 'fuels', 'subfuels']).sum()\
                                                .assign(sub1sectors = 'x', sub2sectors = 'x', sub3sectors = 'x').reset_index()
            
                total_row = agg_sectors[agg_sectors['fuels'].isin(industry_fuels)]\
                    .groupby(['scenarios', 'economy', 'sectors', 'sub1sectors', 'sub2sectors', 'sub3sectors',
                            'sub4sectors', 'subfuels']).sum()\
                    .assign(fuels = '19_total').reset_index()
                
                tgt_temp8 = pd.concat([agg_sectors, total_row]).copy().reset_index(drop = True)

                groundup_df = pd.concat([groundup_df, tgt_temp8]).copy().reset_index(drop = True)

        # Now add in the one subfuel: hydrogen for relevant sector aggregations
        hydrogen_rows_tgt = tgt_df[tgt_df['subfuels'] == '16_x_hydrogen'].copy().reset_index(drop = True)
       
        hyd_sub3_tgt = hydrogen_rows_tgt.copy()
        for i in hyd_sub3_tgt.index:       
            hyd_sub3_tgt.loc[i, 'sub3sectors'] = 'x'
        
        hyd_sub2_tgt = hyd_sub3_tgt.copy()
        for j in hyd_sub2_tgt.index:
            hyd_sub2_tgt.loc[j, 'sub2sectors'] = 'x'

        hyd_sub1_tgt = hyd_sub2_tgt.copy()
        for z in hyd_sub1_tgt.index:
            hyd_sub1_tgt.loc[z, 'sub1sectors'] = 'x'

        hyd_tgt = pd.concat([hydrogen_rows_tgt, hyd_sub3_tgt, hyd_sub2_tgt, hyd_sub1_tgt]).copy().drop_duplicates()

        groundup_df = pd.concat([groundup_df, hyd_tgt]).copy()\
            .sort_values(['sectors', 'sub1sectors', 'sub2sectors', 'sub3sectors', 'fuels']).reset_index(drop = True)
        
        # Fuel disaggregation grab (taking reference grab from above)
        coal_subfuels['scenario'] = 'target'
        petrol_subfuels['scenario'] = 'target'
        crude_subfuels['scenario'] = 'target'
        gas_subfuels['scenario'] = 'target'
        biomass_subfuels['scenario'] = 'target'       
        other_subfuels['scenario'] = 'target'

        groundup_df = pd.concat([groundup_df, coal_subfuels, petrol_subfuels, crude_subfuels, gas_subfuels, biomass_subfuels,
                                 other_subfuels]).copy().\
            sort_values(['sectors', 'sub1sectors', 'sub2sectors', 'sub3sectors', 'fuels']).reset_index(drop = True)

        groundup_df = groundup_df[['scenarios', 'economy', 'sectors', 'sub1sectors', 'sub2sectors', 
                                   'sub3sectors', 'sub4sectors', 'fuels', 'subfuels'] + [str(i) for i in range(1980, 2101, 1)]]\
                                   .copy().reset_index(drop = True)
        
        # New data frame to build in disaggregated results
        groundup_df2 = pd.DataFrame()

        # # Now forward fill for each sector breakdown, starting with sub3sectors
        # Sub3sectors
        if len(groundup_df['sub3sectors'].unique()) > 1:
            # Define array without 'x'
            relevant_sectors = np.delete(groundup_df['sub3sectors'].unique(), 
                                         np.where(groundup_df['sub3sectors'].unique() == 'x'))
            
            for sector in relevant_sectors:

                # Grab the 19_total and 16_x_hydrogen for later
                agg_totals = groundup_df[(groundup_df['sub3sectors'] == sector) &
                                         (groundup_df['sub4sectors'] == 'x') &
                                            (groundup_df['fuels'] == '19_total')].copy().reset_index(drop = True)
                
                hydrogen_grab = groundup_df[(groundup_df['sub3sectors'] == sector) &
                                            (groundup_df['sub4sectors'] == 'x') &
                                            (groundup_df['subfuels'] == '16_x_hydrogen')].copy().reset_index(drop = True)
                
                for fuel in groundup_df['fuels'].unique()[:-1]:
                    temp_sub3 = groundup_df[(groundup_df['sub3sectors'] == sector) &
                                            (groundup_df['sub4sectors'] == 'x') &
                                            (groundup_df['fuels'] == fuel)].copy().reset_index(drop = True)
                    
                    fuel_total_row = temp_sub3[temp_sub3['subfuels'] == 'x'].copy().reset_index(drop = True)

                    hydrogen_adjust = temp_sub3[temp_sub3['subfuels'] == '16_x_hydrogen'].copy().reset_index(drop = True)
                    
                    if hydrogen_adjust.empty:
                        pass
                    else:
                        fuel_total_row_copy = fuel_total_row.copy()
                        hydrogen_adjust.fillna(0, inplace = True)
                        for year in proj_years_str:
                            fuel_total_row.loc[0, year] = fuel_total_row_copy.loc[0, year] - hydrogen_adjust.loc[0, year]

                    subfuels_df = temp_sub3[~temp_sub3['subfuels'].isin(['x', '16_x_hydrogen'])].copy().reset_index(drop = True)

                    # Need the 2020 ratio
                    fuel_ratio_tgt = subfuels_df.loc[:, ['subfuels', '2020']].copy().reset_index(drop = True)

                    fuel_ratio_tgt['ratio'] = np.nan
                    total_for_calc = fuel_total_row.loc[0, '2020']

                    for i in range(len(fuel_ratio_tgt['subfuels'].unique())):
                        # To avoid dividng by zero
                        if total_for_calc == 0:
                            fuel_ratio_tgt.iloc[i, 2] = total_for_calc
                        else: 
                            fuel_ratio_tgt.iloc[i, 2] = fuel_ratio_tgt.iloc[i, 1] / total_for_calc

                    for year in proj_years_str:
                        for fuel in fuel_ratio_tgt['subfuels'].unique():
                            subfuels_df.loc[subfuels_df['subfuels'] == fuel, year] = \
                                fuel_total_row.loc[0, year] * fuel_ratio_tgt.loc[fuel_ratio_tgt['subfuels'] == fuel, 'ratio']
                    
                    # Now if hydrogen subtracted from 16_others, add the original 16_others total line in
                    if hydrogen_adjust.empty:
                        pass
                    else:
                        fuel_total_row = fuel_total_row_copy.copy()
                            
                    groundup_df2 = pd.concat([groundup_df2, fuel_total_row, subfuels_df]).copy().reset_index(drop = True)
                    
                groundup_df2 = pd.concat([groundup_df2, agg_totals, hydrogen_grab]).copy().reset_index(drop = True)

        else:
            pass
        
        # Now sub2sectors
        if len(groundup_df['sub2sectors'].unique()) > 1:
            # Define array without 'x'
            relevant_sectors = np.delete(groundup_df['sub2sectors'].unique(), 
                                         np.where(groundup_df['sub2sectors'].unique() == 'x'))
            
            for sector in relevant_sectors:

                # Grab the 19_total and 16_x_hydrogen for later
                agg_totals = groundup_df[(groundup_df['sub2sectors'] == sector) &
                                         (groundup_df['sub3sectors'] == 'x') &
                                         (groundup_df['sub4sectors'] == 'x') &
                                            (groundup_df['fuels'] == '19_total')].copy().reset_index(drop = True)
                
                hydrogen_grab = groundup_df[(groundup_df['sub2sectors'] == sector) &
                                            (groundup_df['sub3sectors'] == 'x') &
                                            (groundup_df['sub4sectors'] == 'x') &
                                            (groundup_df['subfuels'] == '16_x_hydrogen')].copy().reset_index(drop = True)
                
                for fuel in groundup_df['fuels'].unique()[:-1]:
                    temp_sub2 = groundup_df[(groundup_df['sub2sectors'] == sector) &
                                            (groundup_df['sub3sectors'] == 'x') &
                                            (groundup_df['sub4sectors'] == 'x') &
                                            (groundup_df['fuels'] == fuel)].copy().reset_index(drop = True)
                    
                    fuel_total_row = temp_sub2[temp_sub2['subfuels'] == 'x'].copy().reset_index(drop = True)

                    hydrogen_adjust = temp_sub2[temp_sub2['subfuels'] == '16_x_hydrogen'].copy().reset_index(drop = True)
                    
                    if hydrogen_adjust.empty:
                        pass
                    else:
                        fuel_total_row_copy = fuel_total_row.copy()
                        hydrogen_adjust.fillna(0, inplace = True)
                        for year in proj_years_str:
                            fuel_total_row.loc[0, year] = fuel_total_row_copy.loc[0, year] - hydrogen_adjust.loc[0, year]

                    subfuels_df = temp_sub2[~temp_sub2['subfuels'].isin(['x', '16_x_hydrogen'])].copy().reset_index(drop = True)

                    # Need the 2020 ratio
                    fuel_ratio_tgt = subfuels_df.loc[:, ['subfuels', '2020']].copy().reset_index(drop = True)

                    fuel_ratio_tgt['ratio'] = np.nan
                    total_for_calc = fuel_total_row.loc[0, '2020']

                    for i in range(len(fuel_ratio_tgt['subfuels'].unique())):
                        # To avoid dividng by zero
                        if total_for_calc == 0:
                            fuel_ratio_tgt.iloc[i, 2] = total_for_calc
                        else: 
                            fuel_ratio_tgt.iloc[i, 2] = fuel_ratio_tgt.iloc[i, 1] / total_for_calc

                    for year in proj_years_str:
                        for fuel in fuel_ratio_tgt['subfuels'].unique():
                            subfuels_df.loc[subfuels_df['subfuels'] == fuel, year] = \
                                fuel_total_row.loc[0, year] * fuel_ratio_tgt.loc[fuel_ratio_tgt['subfuels'] == fuel, 'ratio']

                    # Now if hydrogen subtracted from 16_others, add the original 16_others total line in        
                    if hydrogen_adjust.empty:
                        pass
                    else:
                        fuel_total_row = fuel_total_row_copy.copy()
                            
                    groundup_df2 = pd.concat([groundup_df2, fuel_total_row, subfuels_df]).copy().reset_index(drop = True)
                    
                groundup_df2 = pd.concat([groundup_df2, agg_totals, hydrogen_grab]).copy().reset_index(drop = True)

        else:
            pass

        # Now sub1sectors
        if len(groundup_df['sub1sectors'].unique()) > 1:
            # Define array without 'x'
            relevant_sectors = np.delete(groundup_df['sub1sectors'].unique(), 
                                         np.where(groundup_df['sub1sectors'].unique() == 'x'))
            
            for sector in relevant_sectors:

                # Grab the 19_total and 16_x_hydrogen for later
                agg_totals = groundup_df[(groundup_df['sub1sectors'] == sector) &
                                         (groundup_df['sub2sectors'] == 'x') &
                                         (groundup_df['sub3sectors'] == 'x') &
                                         (groundup_df['sub4sectors'] == 'x') &
                                            (groundup_df['fuels'] == '19_total')].copy().reset_index(drop = True)
                
                hydrogen_grab = groundup_df[(groundup_df['sub1sectors'] == sector) &
                                            (groundup_df['sub2sectors'] == 'x') &
                                            (groundup_df['sub3sectors'] == 'x') &
                                            (groundup_df['sub4sectors'] == 'x') &
                                            (groundup_df['subfuels'] == '16_x_hydrogen')].copy().reset_index(drop = True)
                
                for fuel in groundup_df['fuels'].unique()[:-1]:
                    temp_sub1 = groundup_df[(groundup_df['sub1sectors'] == sector) &
                                            (groundup_df['sub2sectors'] == 'x') &
                                            (groundup_df['sub3sectors'] == 'x') &
                                            (groundup_df['sub4sectors'] == 'x') &
                                            (groundup_df['fuels'] == fuel)].copy().reset_index(drop = True)
                    
                    fuel_total_row = temp_sub1[temp_sub1['subfuels'] == 'x'].copy().reset_index(drop = True)

                    hydrogen_adjust = temp_sub1[temp_sub1['subfuels'] == '16_x_hydrogen'].copy().reset_index(drop = True)
                    
                    if hydrogen_adjust.empty:
                        pass
                    else:
                        fuel_total_row_copy = fuel_total_row.copy()
                        hydrogen_adjust.fillna(0, inplace = True)
                        for year in proj_years_str:
                            fuel_total_row.loc[0, year] = fuel_total_row_copy.loc[0, year] - hydrogen_adjust.loc[0, year]

                    subfuels_df = temp_sub1[~temp_sub1['subfuels'].isin(['x', '16_x_hydrogen'])].copy().reset_index(drop = True)

                    # Need the 2020 ratio
                    fuel_ratio_tgt = subfuels_df.loc[:, ['subfuels', '2020']].copy().reset_index(drop = True)

                    fuel_ratio_tgt['ratio'] = np.nan
                    total_for_calc = fuel_total_row.loc[0, '2020']

                    for i in range(len(fuel_ratio_tgt['subfuels'].unique())):
                        # To avoid dividng by zero
                        if total_for_calc == 0:
                            fuel_ratio_tgt.iloc[i, 2] = total_for_calc
                        else: 
                            fuel_ratio_tgt.iloc[i, 2] = fuel_ratio_tgt.iloc[i, 1] / total_for_calc

                    for year in proj_years_str:
                        for fuel in fuel_ratio_tgt['subfuels'].unique():
                            subfuels_df.loc[subfuels_df['subfuels'] == fuel, year] = \
                                fuel_total_row.loc[0, year] * fuel_ratio_tgt.loc[fuel_ratio_tgt['subfuels'] == fuel, 'ratio']

                    # Now if hydrogen subtracted from 16_others, add the original 16_others total line in        
                    if hydrogen_adjust.empty:
                        pass
                    else:
                        fuel_total_row = fuel_total_row_copy.copy()
                            
                    groundup_df2 = pd.concat([groundup_df2, fuel_total_row, subfuels_df]).copy().reset_index(drop = True)
                    
                groundup_df2 = pd.concat([groundup_df2, agg_totals, hydrogen_grab]).copy().reset_index(drop = True)

        else:
            pass

        # Now sectors
        if len(groundup_df['sectors'].unique()) == 1:
            # Define array without 'x'
            relevant_sectors = np.delete(groundup_df['sectors'].unique(), 
                                         np.where(groundup_df['sectors'].unique() == 'x'))
            
            for sector in relevant_sectors:

                # Grab the 19_total and 16_x_hydrogen for later
                agg_totals = groundup_df[(groundup_df['sectors'] == sector) &
                                         (groundup_df['sub1sectors'] == 'x') &
                                         (groundup_df['sub2sectors'] == 'x') &
                                         (groundup_df['sub3sectors'] == 'x') &
                                         (groundup_df['sub4sectors'] == 'x') &
                                            (groundup_df['fuels'] == '19_total')].copy().reset_index(drop = True)
                
                hydrogen_grab = groundup_df[(groundup_df['sectors'] == sector) &
                                            (groundup_df['sub1sectors'] == 'x') &
                                            (groundup_df['sub2sectors'] == 'x') &
                                            (groundup_df['sub3sectors'] == 'x') &
                                            (groundup_df['sub4sectors'] == 'x') &
                                            (groundup_df['subfuels'] == '16_x_hydrogen')].copy().reset_index(drop = True)
                
                for fuel in groundup_df['fuels'].unique()[:-1]:
                    temp_sect = groundup_df[(groundup_df['sectors'] == sector) &
                                            (groundup_df['sub1sectors'] == 'x') &
                                            (groundup_df['sub2sectors'] == 'x') &
                                            (groundup_df['sub3sectors'] == 'x') &
                                            (groundup_df['sub4sectors'] == 'x') &
                                            (groundup_df['fuels'] == fuel)].copy().reset_index(drop = True)
                    
                    fuel_total_row = temp_sect[temp_sect['subfuels'] == 'x'].copy().reset_index(drop = True)

                    hydrogen_adjust = temp_sect[temp_sect['subfuels'] == '16_x_hydrogen'].copy().reset_index(drop = True)
                    
                    if hydrogen_adjust.empty:
                        pass
                    else:
                        fuel_total_row_copy = fuel_total_row.copy()
                        hydrogen_adjust.fillna(0, inplace = True)
                        for year in proj_years_str:
                            fuel_total_row.loc[0, year] = fuel_total_row_copy.loc[0, year] - hydrogen_adjust.loc[0, year]

                    subfuels_df = temp_sect[~temp_sect['subfuels'].isin(['x', '16_x_hydrogen'])].copy().reset_index(drop = True)

                    # Need the 2020 ratio
                    fuel_ratio_tgt = subfuels_df.loc[:, ['subfuels', '2020']].copy().reset_index(drop = True)

                    fuel_ratio_tgt['ratio'] = np.nan
                    total_for_calc = fuel_total_row.loc[0, '2020']

                    for i in range(len(fuel_ratio_tgt['subfuels'].unique())):
                        # To avoid dividng by zero
                        if total_for_calc == 0:
                            fuel_ratio_tgt.iloc[i, 2] = total_for_calc
                        else: 
                            fuel_ratio_tgt.iloc[i, 2] = fuel_ratio_tgt.iloc[i, 1] / total_for_calc

                    for year in proj_years_str:
                        for fuel in fuel_ratio_tgt['subfuels'].unique():
                            subfuels_df.loc[subfuels_df['subfuels'] == fuel, year] = \
                                fuel_total_row.loc[0, year] * fuel_ratio_tgt.loc[fuel_ratio_tgt['subfuels'] == fuel, 'ratio']

                    # Now if hydrogen subtracted from 16_others, add the original 16_others total line in        
                    if hydrogen_adjust.empty:
                        pass
                    else:
                        fuel_total_row = fuel_total_row_copy.copy()
                            
                    groundup_df2 = pd.concat([groundup_df2, fuel_total_row, subfuels_df]).copy().reset_index(drop = True)
                    
                groundup_df2 = pd.concat([groundup_df2, agg_totals, hydrogen_grab]).copy().reset_index(drop = True)

        else:
            pass
        
        groundup_df2 = groundup_df2.sort_values(['sectors', 'sub1sectors', 'sub2sectors', 
                                                 'sub3sectors', 'fuels', 'subfuels']).reset_index(drop = True)

        groundup_df2.to_csv(save_location + economy + '_industry_tgt_' + timestamp + '.csv', index = False)
    
    else:
        pass
    