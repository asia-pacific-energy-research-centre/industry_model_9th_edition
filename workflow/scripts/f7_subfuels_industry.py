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
# Only run one economy option
# economy_select = economy_select[7:8]

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
    file_location = './results/industry/4_consolidation/{}/'.format(economy)

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
            # Begin diaggregation process 
            economy_df = pd.read_csv(both_files[file])

            # subfuel historical grab
            coal_subfuels = EGEDA_coal[(EGEDA_coal['economy'] == economy) &
                                    (EGEDA_coal['sub3sectors'].isin(economy_df['sub3sectors'].unique()))]\
                                            .copy().reset_index(drop = True)

            petrol_subfuels = EGEDA_petrol[(EGEDA_petrol['economy'] == economy) &
                                        (EGEDA_petrol['sub3sectors'].isin(economy_df['sub3sectors'].unique()))]\
                                            .copy().reset_index(drop = True)
            
            crude_subfuels = EGEDA_crude[(EGEDA_crude['economy'] == economy) &
                                        (EGEDA_crude['sub3sectors'].isin(economy_df['sub3sectors'].unique()))]\
                                            .copy().reset_index(drop = True)
            
            gas_subfuels = EGEDA_gas[(EGEDA_gas['economy'] == economy) &
                                    (EGEDA_gas['sub3sectors'].isin(economy_df['sub3sectors'].unique()))]\
                                            .copy().reset_index(drop = True)
            
            biomass_subfuels = EGEDA_biomass[(EGEDA_biomass['economy'] == economy) &
                                            (EGEDA_biomass['sub3sectors'].isin(economy_df['sub3sectors'].unique()))]\
                                            .copy().reset_index(drop = True)
            
            other_subfuels = EGEDA_others[(EGEDA_others['economy'] == economy) &
                                            (EGEDA_others['sub3sectors'].isin(economy_df['sub3sectors'].unique()))]\
                                            .copy().reset_index(drop = True)

            economy_df = pd.concat([economy_df, coal_subfuels, petrol_subfuels, crude_subfuels, gas_subfuels, biomass_subfuels,
                                    other_subfuels]).copy().\
                sort_values(['sectors', 'sub1sectors', 'sub2sectors', 'sub3sectors', 'fuels']).reset_index(drop = True)

            economy_df = economy_df[['scenarios', 'economy', 'sectors', 'sub1sectors', 'sub2sectors', 
                                    'sub3sectors', 'sub4sectors', 'fuels', 'subfuels'] + all_years_str]\
                                    .copy().reset_index(drop = True)
            
            if file == 'tgt':
                # Make scenarios variable target given that historical EGEDA reads in REF (hist is same REF and TGT)
                economy_df['scenarios'] = 'target'

                economy_df = economy_df[['scenarios', 'economy', 'sectors', 'sub1sectors', 'sub2sectors', 
                                        'sub3sectors', 'sub4sectors', 'fuels', 'subfuels'] + all_years_str]\
                                            .copy().reset_index(drop = True)
            
            # New data frame to build in disaggregated results
            groundup_df = pd.DataFrame()

            # Now forward fill for each sector breakdown, starting with sub3sectors
            # Sub3sectors
            if len(economy_df['sub3sectors'].unique()) > 1:
                # Define array without 'x'
                relevant_sectors = np.delete(economy_df['sub3sectors'].unique(), 
                                            np.where(economy_df['sub3sectors'].unique() == 'x'))

                for sector in relevant_sectors:

                    # Grab the 19_total and 16_x_hydrogen for later
                    agg_totals = economy_df[(economy_df['sub3sectors'] == sector) &
                                            (economy_df['sub4sectors'] == 'x') &
                                                (economy_df['fuels'] == '19_total')].copy().reset_index(drop = True)
                    
                    hydrogen_grab = economy_df[(economy_df['sub3sectors'] == sector) &
                                                (economy_df['sub4sectors'] == 'x') &
                                                (economy_df['subfuels'] == '16_x_hydrogen')].copy().reset_index(drop = True)
                    
                    for fuel in economy_df['fuels'].unique()[economy_df['fuels'].unique() != '19_total']:                    
                        temp_sub3 = economy_df[(economy_df['sub3sectors'] == sector) &
                                                (economy_df['sub4sectors'] == 'x') &
                                                (economy_df['fuels'] == fuel)].copy().reset_index(drop = True)
                        
                        if temp_sub3.empty:
                            pass

                        else:
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
                            
                            # Now if hydrogen subtracted from 16_others, add the original 16_others total line in
                            if hydrogen_adjust.empty:
                                pass
                            else:
                                fuel_total_row = fuel_total_row_copy.copy()
                                    
                            groundup_df = pd.concat([groundup_df, fuel_total_row, subfuels_df]).copy().reset_index(drop = True)
                        
                    groundup_df = pd.concat([groundup_df, agg_totals, hydrogen_grab]).copy().reset_index(drop = True)

            else:
                pass
            
            # Now sub2sectors
            if len(economy_df['sub2sectors'].unique()) > 1:
                # Define array without 'x'
                relevant_sectors = np.delete(economy_df['sub2sectors'].unique(), 
                                            np.where(economy_df['sub2sectors'].unique() == 'x'))
                
                for sector in relevant_sectors:

                    # Grab the 19_total and 16_x_hydrogen for later
                    agg_totals = economy_df[(economy_df['sub2sectors'] == sector) &
                                            (economy_df['sub3sectors'] == 'x') &
                                            (economy_df['sub4sectors'] == 'x') &
                                                (economy_df['fuels'] == '19_total')].copy().reset_index(drop = True)
                    
                    hydrogen_grab = economy_df[(economy_df['sub2sectors'] == sector) &
                                                (economy_df['sub3sectors'] == 'x') &
                                                (economy_df['sub4sectors'] == 'x') &
                                                (economy_df['subfuels'] == '16_x_hydrogen')].copy().reset_index(drop = True)
                    
                    for fuel in economy_df['fuels'].unique()[economy_df['fuels'].unique() != '19_total']:
                        temp_sub2 = economy_df[(economy_df['sub2sectors'] == sector) &
                                                (economy_df['sub3sectors'] == 'x') &
                                                (economy_df['sub4sectors'] == 'x') &
                                                (economy_df['fuels'] == fuel)].copy().reset_index(drop = True)
                        
                        if temp_sub2.empty:
                            pass

                        else:
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
                                for subfuel in fuel_ratio['subfuels'].unique():
                                    subfuels_df.loc[subfuels_df['subfuels'] == subfuel, year] = \
                                        fuel_total_row.loc[0, year] * fuel_ratio.loc[fuel_ratio['subfuels'] == subfuel, 'ratio']

                            # Now if hydrogen subtracted from 16_others, add the original 16_others total line in        
                            if hydrogen_adjust.empty:
                                pass
                            else:
                                fuel_total_row = fuel_total_row_copy.copy()
                                    
                            groundup_df = pd.concat([groundup_df, fuel_total_row, subfuels_df]).copy().reset_index(drop = True)
                        
                    groundup_df = pd.concat([groundup_df, agg_totals, hydrogen_grab]).copy().reset_index(drop = True)

            else:
                pass

            # Now sub1sectors
            if len(economy_df['sub1sectors'].unique()) > 1:
                # Define array without 'x'
                relevant_sectors = np.delete(economy_df['sub1sectors'].unique(), 
                                            np.where(economy_df['sub1sectors'].unique() == 'x'))
                
                for sector in relevant_sectors:

                    # Grab the 19_total and 16_x_hydrogen for later
                    agg_totals = economy_df[(economy_df['sub1sectors'] == sector) &
                                            (economy_df['sub2sectors'] == 'x') &
                                            (economy_df['sub3sectors'] == 'x') &
                                            (economy_df['sub4sectors'] == 'x') &
                                                (economy_df['fuels'] == '19_total')].copy().reset_index(drop = True)
                    
                    hydrogen_grab = economy_df[(economy_df['sub1sectors'] == sector) &
                                                (economy_df['sub2sectors'] == 'x') &
                                                (economy_df['sub3sectors'] == 'x') &
                                                (economy_df['sub4sectors'] == 'x') &
                                                (economy_df['subfuels'] == '16_x_hydrogen')].copy().reset_index(drop = True)
                    
                    for fuel in economy_df['fuels'].unique()[economy_df['fuels'].unique() != '19_total']:
                        temp_sub1 = economy_df[(economy_df['sub1sectors'] == sector) &
                                                (economy_df['sub2sectors'] == 'x') &
                                                (economy_df['sub3sectors'] == 'x') &
                                                (economy_df['sub4sectors'] == 'x') &
                                                (economy_df['fuels'] == fuel)].copy().reset_index(drop = True)
                        
                        if temp_sub1.empty:
                            pass

                        else:
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
                                for subfuel in fuel_ratio['subfuels'].unique():
                                    subfuels_df.loc[subfuels_df['subfuels'] == subfuel, year] = \
                                        fuel_total_row.loc[0, year] * fuel_ratio.loc[fuel_ratio['subfuels'] == subfuel, 'ratio']

                            # Now if hydrogen subtracted from 16_others, add the original 16_others total line in        
                            if hydrogen_adjust.empty:
                                pass
                            else:
                                fuel_total_row = fuel_total_row_copy.copy()
                                    
                            groundup_df = pd.concat([groundup_df, fuel_total_row, subfuels_df]).copy().reset_index(drop = True)
                        
                    groundup_df = pd.concat([groundup_df, agg_totals, hydrogen_grab]).copy().reset_index(drop = True)

            else:
                pass

            # Now sectors
            if len(economy_df['sectors'].unique()) == 1:
                # Define array without 'x'
                relevant_sectors = np.delete(economy_df['sectors'].unique(), 
                                            np.where(economy_df['sectors'].unique() == 'x'))
                
                for sector in relevant_sectors:

                    # Grab the 19_total and 16_x_hydrogen for later
                    agg_totals = economy_df[(economy_df['sectors'] == sector) &
                                            (economy_df['sub1sectors'] == 'x') &
                                            (economy_df['sub2sectors'] == 'x') &
                                            (economy_df['sub3sectors'] == 'x') &
                                            (economy_df['sub4sectors'] == 'x') &
                                                (economy_df['fuels'] == '19_total')].copy().reset_index(drop = True)
                    
                    hydrogen_grab = economy_df[(economy_df['sectors'] == sector) &
                                                (economy_df['sub1sectors'] == 'x') &
                                                (economy_df['sub2sectors'] == 'x') &
                                                (economy_df['sub3sectors'] == 'x') &
                                                (economy_df['sub4sectors'] == 'x') &
                                                (economy_df['subfuels'] == '16_x_hydrogen')].copy().reset_index(drop = True)
                    
                    for fuel in economy_df['fuels'].unique()[economy_df['fuels'].unique() != '19_total']:
                        temp_sect = economy_df[(economy_df['sectors'] == sector) &
                                                (economy_df['sub1sectors'] == 'x') &
                                                (economy_df['sub2sectors'] == 'x') &
                                                (economy_df['sub3sectors'] == 'x') &
                                                (economy_df['sub4sectors'] == 'x') &
                                                (economy_df['fuels'] == fuel)].copy().reset_index(drop = True)
                        
                        if temp_sect.empty:
                            pass

                        else:
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
                                for subfuel in fuel_ratio['subfuels'].unique():
                                    subfuels_df.loc[subfuels_df['subfuels'] == subfuel, year] = \
                                        fuel_total_row.loc[0, year] * fuel_ratio.loc[fuel_ratio['subfuels'] == subfuel, 'ratio']

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
            
            #############################################################################################################
            # Final edit for sub3sectors
            relevant_sectors = np.delete(groundup_df['sub3sectors'].unique(), 
                                                np.where(groundup_df['sub3sectors'].unique() == 'x'))
            
            if len(economy_df['sub3sectors'].unique()) > 0:
                # Subset data to amend:
                amend_df = groundup_df[groundup_df['sub3sectors'].isin(relevant_sectors)].copy()
                everything_else_df = groundup_df[~groundup_df['sub3sectors'].isin(relevant_sectors)].copy()

                post_amend_df = pd.DataFrame()

                for sector in relevant_sectors:
                    temp_df = amend_df[amend_df['sub3sectors'] == sector].copy()

                    totals_3sector = temp_df[temp_df['subfuels'] == 'x'].copy().reset_index(drop = True)
                    sub2sector_choice = totals_3sector.loc[0, 'sub2sectors']

                    totals_2sector = groundup_df[(groundup_df['sub2sectors'] == sub2sector_choice) &
                                            (groundup_df['sub3sectors'] == 'x') &
                                            (groundup_df['subfuels'] == 'x')].copy().reset_index(drop = True)
                    
                    subfuels_2sector = groundup_df[(groundup_df['sub2sectors'] == sub2sector_choice) &
                                            (groundup_df['sub3sectors'] == 'x') &
                                            (groundup_df['subfuels'] != 'x')].copy().reset_index(drop = True)
                    
                    totals_2sector.fillna(0, inplace = True)
                    totals_3sector.fillna(0, inplace = True)
                    subfuels_2sector.fillna(0, inplace = True)

                    share_df = totals_3sector.copy()

                    for year in all_years_str:
                        for fuel in share_df['fuels'].unique():
                            # Account for divide by zero issue
                            if totals_2sector.loc[totals_2sector['fuels'] == fuel, year].values[0] != 0:
                                share_df.loc[share_df['fuels'] == fuel, year] = totals_3sector.loc[totals_3sector['fuels'] == fuel, year].values[0]\
                                    / totals_2sector.loc[totals_2sector['fuels'] == fuel, year].values[0]
                            else:
                                share_df.loc[share_df['fuels'] == fuel, year] = 0

                    relevant_subfuels = np.delete(temp_df['subfuels'].unique(),
                                                    np.where(temp_df['subfuels'].unique() == 'x'))

                    for subfuel in relevant_subfuels:
                        for year in all_years_str:
                            fuel = temp_df.loc[(temp_df['subfuels'] == subfuel), 'fuels'].values[0]
                            if fuel in share_df['fuels'].unique():                
                                temp_df.loc[temp_df['subfuels'] == subfuel, year] = subfuels_2sector.loc[subfuels_2sector['subfuels'] == subfuel, year].values[0] \
                                    * share_df.loc[share_df['fuels'] == fuel, year].values[0]
                            else:
                                temp_df.loc[temp_df['subfuels'] == subfuel, year] = np.nan

                    post_amend_df = pd.concat([post_amend_df, temp_df]).copy().reset_index(drop = True)

                groundup_df = pd.concat([everything_else_df, post_amend_df]).copy().reset_index(drop = True)

                groundup_df = groundup_df.sort_values(['sectors', 'sub1sectors', 'sub2sectors', 
                                                        'sub3sectors', 'fuels', 'subfuels']).copy().reset_index(drop = True)
                
            else:
                pass

            groundup_df.to_csv(file_location + economy + '_industry_' + file + '_' + timestamp + '.csv', index = False)