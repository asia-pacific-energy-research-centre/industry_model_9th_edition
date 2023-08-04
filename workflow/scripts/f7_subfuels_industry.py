# Subfuel disaggregation
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
biomass_sub = [i for i in EGEDA_hist['subfuels'].unique() if i.startswith('15_')]
# Keep hydrogen and ammonia out of 16 subfuels
others_sub = [i for i in EGEDA_hist['subfuels'].unique() if i.startswith('16_')][:-2]

EGEDA_coal = EGEDA_hist[(EGEDA_hist['sectors'] == '14_industry_sector') &
                        (EGEDA_hist['subfuels'].isin(coal_sub))].copy().reset_index(drop = True)

EGEDA_crude = EGEDA_hist[(EGEDA_hist['sectors'] == '14_industry_sector') &
                          (EGEDA_hist['subfuels'].isin(crude_sub))].copy().reset_index(drop = True)

EGEDA_petrol = EGEDA_hist[(EGEDA_hist['sectors'] == '14_industry_sector') &
                          (EGEDA_hist['subfuels'].isin(petrol_sub))].copy().reset_index(drop = True)

EGEDA_gas = EGEDA_hist[(EGEDA_hist['sectors'] == '14_industry_sector') &
                       (EGEDA_hist['subfuels'].isin(gas_sub))].copy().reset_index(drop = True)

EGEDA_biomass = EGEDA_hist[(EGEDA_hist['sectors'] == '14_industry_sector') &
                           (EGEDA_hist['subfuels'].isin(biomass_sub))].copy().reset_index(drop = True)

EGEDA_others = EGEDA_hist[(EGEDA_hist['sectors'] == '14_industry_sector') &
                           (EGEDA_hist['subfuels'].isin(others_sub))].copy().reset_index(drop = True)


for economy in list(economy_select):
    # Save location for charts and data
    file_location = './results/industry/4_final/{}/'.format(economy)

    if not os.path.isdir(file_location):
        os.makedirs(file_location)

    # Interim files to disaggregate fuels
    files_to_disag = glob.glob(file_location + '*interim*.csv')

    ref_file = [item for item in files_to_disag if 'ref' in item]
    tgt_file = [item for item in files_to_disag if 'tgt' in item]    
    
    # Begin diaggregation process
    # REF
    if len(ref_file) == 1: 
        ref_df = pd.read_csv(ref_file[0])

        # subfuel historical grab
        coal_subfuels = EGEDA_coal[(EGEDA_coal['economy'] == economy) &
                                   (EGEDA_coal['sub3sectors'].isin(ref_df['sub3sectors'].unique()))]\
                                        .copy().reset_index(drop = True)

        petrol_subfuels = EGEDA_petrol[(EGEDA_petrol['economy'] == economy) &
                                       (EGEDA_petrol['sub3sectors'].isin(ref_df['sub3sectors'].unique()))]\
                                        .copy().reset_index(drop = True)
        
        crude_subfuels = EGEDA_crude[(EGEDA_crude['economy'] == economy) &
                                     (EGEDA_crude['sub3sectors'].isin(ref_df['sub3sectors'].unique()))]\
                                        .copy().reset_index(drop = True)
        
        gas_subfuels = EGEDA_gas[(EGEDA_gas['economy'] == economy) &
                                 (EGEDA_gas['sub3sectors'].isin(ref_df['sub3sectors'].unique()))]\
                                        .copy().reset_index(drop = True)
        
        biomass_subfuels = EGEDA_biomass[(EGEDA_biomass['economy'] == economy) &
                                         (EGEDA_biomass['sub3sectors'].isin(ref_df['sub3sectors'].unique()))]\
                                        .copy().reset_index(drop = True)
        
        other_subfuels = EGEDA_others[(EGEDA_others['economy'] == economy) &
                                         (EGEDA_others['sub3sectors'].isin(ref_df['sub3sectors'].unique()))]\
                                        .copy().reset_index(drop = True)

        ref_df = pd.concat([ref_df, coal_subfuels, petrol_subfuels, crude_subfuels, gas_subfuels, biomass_subfuels,
                                 other_subfuels]).copy().\
            sort_values(['sectors', 'sub1sectors', 'sub2sectors', 'sub3sectors', 'fuels']).reset_index(drop = True)

        ref_df = ref_df[['scenarios', 'economy', 'sectors', 'sub1sectors', 'sub2sectors', 
                                   'sub3sectors', 'sub4sectors', 'fuels', 'subfuels'] + all_years_str]\
                                   .copy().reset_index(drop = True)
        
        # New data frame to build in disaggregated results
        groundup_df_ref = pd.DataFrame()

        # # Now forward fill for each sector breakdown, starting with sub3sectors
        # Sub3sectors
        if len(ref_df['sub3sectors'].unique()) > 1:
            # Define array without 'x'
            relevant_sectors = np.delete(ref_df['sub3sectors'].unique(), 
                                         np.where(ref_df['sub3sectors'].unique() == 'x'))
            
            for sector in relevant_sectors:

                # Grab the 19_total and 16_x_hydrogen for later
                agg_totals = ref_df[(ref_df['sub3sectors'] == sector) &
                                         (ref_df['sub4sectors'] == 'x') &
                                            (ref_df['fuels'] == '19_total')].copy().reset_index(drop = True)
                
                hydrogen_grab = ref_df[(ref_df['sub3sectors'] == sector) &
                                            (ref_df['sub4sectors'] == 'x') &
                                            (ref_df['subfuels'] == '16_x_hydrogen')].copy().reset_index(drop = True)
                
                for fuel in ref_df['fuels'].unique()[:-1]:
                    if sector in ['14_03_01_01_fs', '14_03_02_01_fs', '14_03_04_02_nonccs']:
                        temp_sub3 = ref_df[(ref_df['sub3sectors'] == sector) &
                                                (ref_df['sub4sectors'] == 'x') &
                                                (ref_df['fuels'] == fuel)].copy().reset_index(drop = True)
                        
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
                    
                    # CCS adjustment
                    elif sector in ['14_03_01_03_ccs']:
                        temp_ccs = ref_df[(ref_df['sub2sectors'] == '14_03_01_iron_and_steel') &
                                          (ref_df['sub3sectors'] == 'x') &
                                          (ref_df['sub4sectors'] == 'x') &
                                          (ref_df['fuels'] == fuel)].copy().reset_index(drop = True)
                        
                        fuel_total_row_ccs = temp_ccs[temp_ccs['subfuels'] == 'x'].copy().reset_index(drop = True)
                        subfuels_ccs = temp_ccs[~temp_ccs['subfuels'].isin(['x', '16_x_hydrogen'])].copy().reset_index(drop = True)
                        
                    elif sector in ['14_03_02_02_ccs']:
                        temp_ccs = ref_df[(ref_df['sub2sectors'] == '14_03_02_chemical_incl_petrochemical') &
                                          (ref_df['sub3sectors'] == 'x') &
                                          (ref_df['sub4sectors'] == 'x') &
                                          (ref_df['fuels'] == fuel)].copy().reset_index(drop = True)
                        
                        fuel_total_row_ccs = temp_ccs[temp_ccs['subfuels'] == 'x'].copy().reset_index(drop = True)
                        subfuels_ccs = temp_ccs[~temp_ccs['subfuels'].isin(['x', '16_x_hydrogen'])].copy().reset_index(drop = True)

                    elif sector in ['14_03_04_01_ccs']:
                        temp_ccs = ref_df[(ref_df['sub2sectors'] == '14_03_04_nonmetallic_mineral_products') &
                                          (ref_df['sub3sectors'] == 'x') &
                                          (ref_df['sub4sectors'] == 'x') &
                                          (ref_df['fuels'] == fuel)].copy().reset_index(drop = True)
                        
                        fuel_total_row_ccs = temp_ccs[temp_ccs['subfuels'] == 'x'].copy().reset_index(drop = True)
                        subfuels_ccs = temp_ccs[~temp_ccs['subfuels'].isin(['x', '16_x_hydrogen'])].copy().reset_index(drop = True)

                    # Need the 2020 ratio
                    if sector in ['14_03_01_01_fs', '14_03_02_01_fs', '14_03_04_02_nonccs']:
                        fuel_ratio_ref = subfuels_df.loc[:, ['subfuels', '2020']].copy().reset_index(drop = True)

                        fuel_ratio_ref['ratio'] = np.nan
                        total_for_calc = fuel_total_row.loc[0, '2020']

                    else:
                        fuel_ratio_ref = subfuels_ccs.loc[:, ['subfuels', '2020']].copy().reset_index(drop = True)

                        fuel_ratio_ref['ratio'] = np.nan
                        total_for_calc = fuel_total_row_ccs.loc[0, '2020']

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
                            
                    groundup_df_ref = pd.concat([groundup_df_ref, fuel_total_row, subfuels_df]).copy().reset_index(drop = True)
                    
                groundup_df_ref = pd.concat([groundup_df_ref, agg_totals, hydrogen_grab]).copy().reset_index(drop = True)

        else:
            pass
        
        # Now sub2sectors
        if len(ref_df['sub2sectors'].unique()) > 1:
            # Define array without 'x'
            relevant_sectors = np.delete(ref_df['sub2sectors'].unique(), 
                                         np.where(ref_df['sub2sectors'].unique() == 'x'))
            
            for sector in relevant_sectors:

                # Grab the 19_total and 16_x_hydrogen for later
                agg_totals = ref_df[(ref_df['sub2sectors'] == sector) &
                                         (ref_df['sub3sectors'] == 'x') &
                                         (ref_df['sub4sectors'] == 'x') &
                                            (ref_df['fuels'] == '19_total')].copy().reset_index(drop = True)
                
                hydrogen_grab = ref_df[(ref_df['sub2sectors'] == sector) &
                                            (ref_df['sub3sectors'] == 'x') &
                                            (ref_df['sub4sectors'] == 'x') &
                                            (ref_df['subfuels'] == '16_x_hydrogen')].copy().reset_index(drop = True)
                
                for fuel in ref_df['fuels'].unique()[:-1]:
                    temp_sub2 = ref_df[(ref_df['sub2sectors'] == sector) &
                                            (ref_df['sub3sectors'] == 'x') &
                                            (ref_df['sub4sectors'] == 'x') &
                                            (ref_df['fuels'] == fuel)].copy().reset_index(drop = True)
                    
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
                            
                    groundup_df_ref = pd.concat([groundup_df_ref, fuel_total_row, subfuels_df]).copy().reset_index(drop = True)
                    
                groundup_df_ref = pd.concat([groundup_df_ref, agg_totals, hydrogen_grab]).copy().reset_index(drop = True)

        else:
            pass

        # Now sub1sectors
        if len(ref_df['sub1sectors'].unique()) > 1:
            # Define array without 'x'
            relevant_sectors = np.delete(ref_df['sub1sectors'].unique(), 
                                         np.where(ref_df['sub1sectors'].unique() == 'x'))
            
            for sector in relevant_sectors:

                # Grab the 19_total and 16_x_hydrogen for later
                agg_totals = ref_df[(ref_df['sub1sectors'] == sector) &
                                         (ref_df['sub2sectors'] == 'x') &
                                         (ref_df['sub3sectors'] == 'x') &
                                         (ref_df['sub4sectors'] == 'x') &
                                            (ref_df['fuels'] == '19_total')].copy().reset_index(drop = True)
                
                hydrogen_grab = ref_df[(ref_df['sub1sectors'] == sector) &
                                            (ref_df['sub2sectors'] == 'x') &
                                            (ref_df['sub3sectors'] == 'x') &
                                            (ref_df['sub4sectors'] == 'x') &
                                            (ref_df['subfuels'] == '16_x_hydrogen')].copy().reset_index(drop = True)
                
                for fuel in ref_df['fuels'].unique()[:-1]:
                    temp_sub1 = ref_df[(ref_df['sub1sectors'] == sector) &
                                            (ref_df['sub2sectors'] == 'x') &
                                            (ref_df['sub3sectors'] == 'x') &
                                            (ref_df['sub4sectors'] == 'x') &
                                            (ref_df['fuels'] == fuel)].copy().reset_index(drop = True)
                    
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
                            
                    groundup_df_ref = pd.concat([groundup_df_ref, fuel_total_row, subfuels_df]).copy().reset_index(drop = True)
                    
                groundup_df_ref = pd.concat([groundup_df_ref, agg_totals, hydrogen_grab]).copy().reset_index(drop = True)

        else:
            pass

        # Now sectors
        if len(ref_df['sectors'].unique()) == 1:
            # Define array without 'x'
            relevant_sectors = np.delete(ref_df['sectors'].unique(), 
                                         np.where(ref_df['sectors'].unique() == 'x'))
            
            for sector in relevant_sectors:

                # Grab the 19_total and 16_x_hydrogen for later
                agg_totals = ref_df[(ref_df['sectors'] == sector) &
                                         (ref_df['sub1sectors'] == 'x') &
                                         (ref_df['sub2sectors'] == 'x') &
                                         (ref_df['sub3sectors'] == 'x') &
                                         (ref_df['sub4sectors'] == 'x') &
                                            (ref_df['fuels'] == '19_total')].copy().reset_index(drop = True)
                
                hydrogen_grab = ref_df[(ref_df['sectors'] == sector) &
                                            (ref_df['sub1sectors'] == 'x') &
                                            (ref_df['sub2sectors'] == 'x') &
                                            (ref_df['sub3sectors'] == 'x') &
                                            (ref_df['sub4sectors'] == 'x') &
                                            (ref_df['subfuels'] == '16_x_hydrogen')].copy().reset_index(drop = True)
                
                for fuel in ref_df['fuels'].unique()[:-1]:
                    temp_sect = ref_df[(ref_df['sectors'] == sector) &
                                            (ref_df['sub1sectors'] == 'x') &
                                            (ref_df['sub2sectors'] == 'x') &
                                            (ref_df['sub3sectors'] == 'x') &
                                            (ref_df['sub4sectors'] == 'x') &
                                            (ref_df['fuels'] == fuel)].copy().reset_index(drop = True)
                    
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
                            
                    groundup_df_ref = pd.concat([groundup_df_ref, fuel_total_row, subfuels_df]).copy().reset_index(drop = True)
                    
                groundup_df_ref = pd.concat([groundup_df_ref, agg_totals, hydrogen_grab]).copy().reset_index(drop = True)

        else:
            pass
        
        groundup_df_ref = groundup_df_ref.sort_values(['sectors', 'sub1sectors', 'sub2sectors', 
                                                 'sub3sectors', 'fuels', 'subfuels']).reset_index(drop = True)

        groundup_df_ref.to_csv(file_location + economy + '_industry_ref_' + timestamp + '.csv', index = False)

    ############################################################################################################################
    # TGT
    if len(tgt_file) == 1: 
        tgt_df = pd.read_csv(tgt_file[0])

        # subfuel historical amendment (use gran from REF above and just change scenario column)
        coal_subfuels['scenarios'] = 'target'
        petrol_subfuels['scenarios'] = 'target' 
        crude_subfuels['scenarios'] = 'target'
        gas_subfuels['scenarios'] = 'target'
        biomass_subfuels['scenarios'] = 'target'
        other_subfuels['scenarios'] = 'target'

        tgt_df = pd.concat([tgt_df, coal_subfuels, petrol_subfuels, crude_subfuels, gas_subfuels, biomass_subfuels,
                                 other_subfuels]).copy().\
            sort_values(['sectors', 'sub1sectors', 'sub2sectors', 'sub3sectors', 'fuels']).reset_index(drop = True)

        tgt_df = tgt_df[['scenarios', 'economy', 'sectors', 'sub1sectors', 'sub2sectors', 
                                   'sub3sectors', 'sub4sectors', 'fuels', 'subfuels'] + all_years_str]\
                                   .copy().reset_index(drop = True)
        
        # New data frame to build in disaggregated results
        groundup_df_tgt = pd.DataFrame()

        # # Now forward fill for each sector breakdown, starting with sub3sectors
        # Sub3sectors
        if len(tgt_df['sub3sectors'].unique()) > 1:
            # Define array without 'x'
            relevant_sectors = np.delete(tgt_df['sub3sectors'].unique(), 
                                         np.where(tgt_df['sub3sectors'].unique() == 'x'))
            
            for sector in relevant_sectors:

                # Grab the 19_total and 16_x_hydrogen for later
                agg_totals = tgt_df[(tgt_df['sub3sectors'] == sector) &
                                         (tgt_df['sub4sectors'] == 'x') &
                                            (tgt_df['fuels'] == '19_total')].copy().reset_index(drop = True)
                
                hydrogen_grab = tgt_df[(tgt_df['sub3sectors'] == sector) &
                                            (tgt_df['sub4sectors'] == 'x') &
                                            (tgt_df['subfuels'] == '16_x_hydrogen')].copy().reset_index(drop = True)
                
                for fuel in tgt_df['fuels'].unique()[:-1]:
                    if sector in ['14_03_01_01_fs', '14_03_02_01_fs', '14_03_04_02_nonccs']:
                        temp_sub3 = tgt_df[(tgt_df['sub3sectors'] == sector) &
                                                (tgt_df['sub4sectors'] == 'x') &
                                                (tgt_df['fuels'] == fuel)].copy().reset_index(drop = True)
                        
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
                    
                    # CCS adjustment
                    elif sector in ['14_03_01_03_ccs']:
                        temp_ccs = tgt_df[(tgt_df['sub2sectors'] == '14_03_01_iron_and_steel') &
                                          (tgt_df['sub3sectors'] == 'x') &
                                          (tgt_df['sub4sectors'] == 'x') &
                                          (tgt_df['fuels'] == fuel)].copy().reset_index(drop = True)
                        
                        fuel_total_row_ccs = temp_ccs[temp_ccs['subfuels'] == 'x'].copy().reset_index(drop = True)
                        subfuels_ccs = temp_ccs[~temp_ccs['subfuels'].isin(['x', '16_x_hydrogen'])].copy().reset_index(drop = True)
                        
                    elif sector in ['14_03_02_02_ccs']:
                        temp_ccs = tgt_df[(tgt_df['sub2sectors'] == '14_03_02_chemical_incl_petrochemical') &
                                          (tgt_df['sub3sectors'] == 'x') &
                                          (tgt_df['sub4sectors'] == 'x') &
                                          (tgt_df['fuels'] == fuel)].copy().reset_index(drop = True)
                        
                        fuel_total_row_ccs = temp_ccs[temp_ccs['subfuels'] == 'x'].copy().reset_index(drop = True)
                        subfuels_ccs = temp_ccs[~temp_ccs['subfuels'].isin(['x', '16_x_hydrogen'])].copy().reset_index(drop = True)

                    elif sector in ['14_03_04_01_ccs']:
                        temp_ccs = tgt_df[(tgt_df['sub2sectors'] == '14_03_04_nonmetallic_mineral_products') &
                                          (tgt_df['sub3sectors'] == 'x') &
                                          (tgt_df['sub4sectors'] == 'x') &
                                          (tgt_df['fuels'] == fuel)].copy().reset_index(drop = True)
                        
                        fuel_total_row_ccs = temp_ccs[temp_ccs['subfuels'] == 'x'].copy().reset_index(drop = True)
                        subfuels_ccs = temp_ccs[~temp_ccs['subfuels'].isin(['x', '16_x_hydrogen'])].copy().reset_index(drop = True)

                    # Need the 2020 ratio
                    if sector in ['14_03_01_01_fs', '14_03_02_01_fs', '14_03_04_02_nonccs']:
                        fuel_ratio_tgt = subfuels_df.loc[:, ['subfuels', '2020']].copy().reset_index(drop = True)

                        fuel_ratio_tgt['ratio'] = np.nan
                        total_for_calc = fuel_total_row.loc[0, '2020']

                    else:
                        fuel_ratio_tgt = subfuels_ccs.loc[:, ['subfuels', '2020']].copy().reset_index(drop = True)

                        fuel_ratio_tgt['ratio'] = np.nan
                        total_for_calc = fuel_total_row_ccs.loc[0, '2020']

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
                            
                    groundup_df_tgt = pd.concat([groundup_df_tgt, fuel_total_row, subfuels_df]).copy().reset_index(drop = True)
                    
                groundup_df_tgt = pd.concat([groundup_df_tgt, agg_totals, hydrogen_grab]).copy().reset_index(drop = True)

        else:
            pass
        
        # Now sub2sectors
        if len(tgt_df['sub2sectors'].unique()) > 1:
            # Define array without 'x'
            relevant_sectors = np.delete(tgt_df['sub2sectors'].unique(), 
                                         np.where(tgt_df['sub2sectors'].unique() == 'x'))
            
            for sector in relevant_sectors:

                # Grab the 19_total and 16_x_hydrogen for later
                agg_totals = tgt_df[(tgt_df['sub2sectors'] == sector) &
                                         (tgt_df['sub3sectors'] == 'x') &
                                         (tgt_df['sub4sectors'] == 'x') &
                                            (tgt_df['fuels'] == '19_total')].copy().reset_index(drop = True)
                
                hydrogen_grab = tgt_df[(tgt_df['sub2sectors'] == sector) &
                                            (tgt_df['sub3sectors'] == 'x') &
                                            (tgt_df['sub4sectors'] == 'x') &
                                            (tgt_df['subfuels'] == '16_x_hydrogen')].copy().reset_index(drop = True)
                
                for fuel in tgt_df['fuels'].unique()[:-1]:
                    temp_sub2 = tgt_df[(tgt_df['sub2sectors'] == sector) &
                                            (tgt_df['sub3sectors'] == 'x') &
                                            (tgt_df['sub4sectors'] == 'x') &
                                            (tgt_df['fuels'] == fuel)].copy().reset_index(drop = True)
                    
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
                            
                    groundup_df_tgt = pd.concat([groundup_df_tgt, fuel_total_row, subfuels_df]).copy().reset_index(drop = True)
                    
                groundup_df_tgt = pd.concat([groundup_df_tgt, agg_totals, hydrogen_grab]).copy().reset_index(drop = True)

        else:
            pass

        # Now sub1sectors
        if len(tgt_df['sub1sectors'].unique()) > 1:
            # Define array without 'x'
            relevant_sectors = np.delete(tgt_df['sub1sectors'].unique(), 
                                         np.where(tgt_df['sub1sectors'].unique() == 'x'))
            
            for sector in relevant_sectors:

                # Grab the 19_total and 16_x_hydrogen for later
                agg_totals = tgt_df[(tgt_df['sub1sectors'] == sector) &
                                         (tgt_df['sub2sectors'] == 'x') &
                                         (tgt_df['sub3sectors'] == 'x') &
                                         (tgt_df['sub4sectors'] == 'x') &
                                            (tgt_df['fuels'] == '19_total')].copy().reset_index(drop = True)
                
                hydrogen_grab = tgt_df[(tgt_df['sub1sectors'] == sector) &
                                            (tgt_df['sub2sectors'] == 'x') &
                                            (tgt_df['sub3sectors'] == 'x') &
                                            (tgt_df['sub4sectors'] == 'x') &
                                            (tgt_df['subfuels'] == '16_x_hydrogen')].copy().reset_index(drop = True)
                
                for fuel in tgt_df['fuels'].unique()[:-1]:
                    temp_sub1 = tgt_df[(tgt_df['sub1sectors'] == sector) &
                                            (tgt_df['sub2sectors'] == 'x') &
                                            (tgt_df['sub3sectors'] == 'x') &
                                            (tgt_df['sub4sectors'] == 'x') &
                                            (tgt_df['fuels'] == fuel)].copy().reset_index(drop = True)
                    
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
                            
                    groundup_df_tgt = pd.concat([groundup_df_tgt, fuel_total_row, subfuels_df]).copy().reset_index(drop = True)
                    
                groundup_df_tgt = pd.concat([groundup_df_tgt, agg_totals, hydrogen_grab]).copy().reset_index(drop = True)

        else:
            pass

        # Now sectors
        if len(tgt_df['sectors'].unique()) == 1:
            # Define array without 'x'
            relevant_sectors = np.delete(tgt_df['sectors'].unique(), 
                                         np.where(tgt_df['sectors'].unique() == 'x'))
            
            for sector in relevant_sectors:

                # Grab the 19_total and 16_x_hydrogen for later
                agg_totals = tgt_df[(tgt_df['sectors'] == sector) &
                                         (tgt_df['sub1sectors'] == 'x') &
                                         (tgt_df['sub2sectors'] == 'x') &
                                         (tgt_df['sub3sectors'] == 'x') &
                                         (tgt_df['sub4sectors'] == 'x') &
                                            (tgt_df['fuels'] == '19_total')].copy().reset_index(drop = True)
                
                hydrogen_grab = tgt_df[(tgt_df['sectors'] == sector) &
                                            (tgt_df['sub1sectors'] == 'x') &
                                            (tgt_df['sub2sectors'] == 'x') &
                                            (tgt_df['sub3sectors'] == 'x') &
                                            (tgt_df['sub4sectors'] == 'x') &
                                            (tgt_df['subfuels'] == '16_x_hydrogen')].copy().reset_index(drop = True)
                
                for fuel in tgt_df['fuels'].unique()[:-1]:
                    temp_sect = tgt_df[(tgt_df['sectors'] == sector) &
                                            (tgt_df['sub1sectors'] == 'x') &
                                            (tgt_df['sub2sectors'] == 'x') &
                                            (tgt_df['sub3sectors'] == 'x') &
                                            (tgt_df['sub4sectors'] == 'x') &
                                            (tgt_df['fuels'] == fuel)].copy().reset_index(drop = True)
                    
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
                            
                    groundup_df_tgt = pd.concat([groundup_df_tgt, fuel_total_row, subfuels_df]).copy().reset_index(drop = True)
                    
                groundup_df_tgt = pd.concat([groundup_df_tgt, agg_totals, hydrogen_grab]).copy().reset_index(drop = True)

        else:
            pass
        
        groundup_df_tgt = groundup_df_tgt.sort_values(['sectors', 'sub1sectors', 'sub2sectors', 
                                                 'sub3sectors', 'fuels', 'subfuels']).reset_index(drop = True)

        groundup_df_tgt.to_csv(file_location + economy + '_industry_tgt_' + timestamp + '.csv', index = False)