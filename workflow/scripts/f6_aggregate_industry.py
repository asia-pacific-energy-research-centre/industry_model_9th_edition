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

# All years
all_years = list(range(1980, 2101, 1))
all_years_str = [str(i) for i in all_years]

# Read in steel data
for economy in list(economy_select):
    # Save location for charts and data
    save_location = './results/industry/4_final/{}/'.format(economy)

    if not os.path.isdir(save_location):
        os.makedirs(save_location)

    file_location = './results/industry/3_fuel_switch/{}/all_sectors/'.format(economy)

    files_to_agg = glob.glob(file_location + '*wide*.csv')

    ref_file = [item for item in files_to_agg if 'ref' in item]
    tgt_file = [item for item in files_to_agg if 'tgt' in item]

    if len(ref_file) + len(tgt_file) == 2:
        both_files = {'ref': ref_file[0],
                      'tgt': tgt_file[0]}
    
        # Begin aggregation process
        for file in both_files.keys(): 
            economy_df = pd.read_csv(both_files[file])
        
            # Define new empty dataframe to save results in 
            groundup_df = pd.DataFrame()

            # Start at lowest sector results (for industry: sub3sectors)
            for sector in economy_df['sub3sectors'].unique():
                if sector == 'x':
                    pass

                else:
                    temp1 = economy_df[(economy_df['sub3sectors'] == sector) &
                                    (economy_df['subfuels'] == 'x')].copy().reset_index(drop = True)
                    
                    total_row = temp1[temp1['fuels'].isin(industry_fuels)]\
                        .groupby(['scenarios', 'economy', 'sectors','sub1sectors', 'sub2sectors', 'sub3sectors',
                                'sub4sectors', 'subfuels']).sum()\
                        .assign(fuels = '19_total').reset_index()
                    
                    temp2 = pd.concat([temp1, total_row]).copy().reset_index(drop = True)

                    groundup_df = pd.concat([groundup_df, temp2]).copy().reset_index(drop = True)

            # Now one level higher
            for sector in economy_df['sub2sectors'].unique():
                if sector == 'x':
                    pass

                else:
                    temp3 = economy_df[(economy_df['sub2sectors'] == sector) &
                                        (economy_df['subfuels'] == 'x')].copy().reset_index(drop = True)
                    
                    # Now aggregate sub2sectors
                    agg_2sectors = temp3.groupby(['scenarios', 'economy', 'sectors','sub1sectors', 'sub2sectors', 
                                                    'sub4sectors', 'fuels', 'subfuels']).sum()\
                                                    .assign(sub3sectors = 'x').reset_index()
                
                    total_row = agg_2sectors[agg_2sectors['fuels'].isin(industry_fuels)]\
                        .groupby(['scenarios', 'economy', 'sectors','sub1sectors', 'sub2sectors', 'sub3sectors',
                                'sub4sectors', 'subfuels']).sum()\
                        .assign(fuels = '19_total').reset_index()
                    
                    temp4 = pd.concat([agg_2sectors, total_row]).copy().reset_index(drop = True)

                    groundup_df = pd.concat([groundup_df, temp4]).copy().reset_index(drop = True)

            # And one level higher
            for sector in economy_df['sub1sectors'].unique():
                if sector == 'x':
                    pass

                else:
                    temp5 = economy_df[(economy_df['sub1sectors'] == sector) &
                                        (economy_df['subfuels'] == 'x')].copy().reset_index(drop = True)
                    
                    # Now aggregate sub2sectors
                    agg_1sectors = temp5.groupby(['scenarios', 'economy', 'sectors', 'sub1sectors', 
                                                    'sub4sectors', 'fuels', 'subfuels']).sum()\
                                                    .assign(sub2sectors = 'x', sub3sectors = 'x').reset_index()
                
                    total_row = agg_1sectors[agg_1sectors['fuels'].isin(industry_fuels)]\
                        .groupby(['scenarios', 'economy', 'sectors', 'sub1sectors', 'sub2sectors', 'sub3sectors',
                                'sub4sectors', 'subfuels']).sum()\
                        .assign(fuels = '19_total').reset_index()
                    
                    temp6 = pd.concat([agg_1sectors, total_row]).copy().reset_index(drop = True)

                    groundup_df = pd.concat([groundup_df, temp6]).copy().reset_index(drop = True)

            # And final level
            for sector in economy_df['sectors'].unique():
                if sector == 'x':
                    pass

                else:
                    temp7 = economy_df[(economy_df['sectors'] == sector) &
                                        (economy_df['subfuels'] == 'x')].copy().reset_index(drop = True)
                    
                    # Now aggregate sub2sectors
                    agg_sectors = temp7.groupby(['scenarios', 'economy', 'sectors', 
                                                    'sub4sectors', 'fuels', 'subfuels']).sum()\
                                                    .assign(sub1sectors = 'x', sub2sectors = 'x', sub3sectors = 'x').reset_index()
                
                    total_row = agg_sectors[agg_sectors['fuels'].isin(industry_fuels)]\
                        .groupby(['scenarios', 'economy', 'sectors', 'sub1sectors', 'sub2sectors', 'sub3sectors',
                                'sub4sectors', 'subfuels']).sum()\
                        .assign(fuels = '19_total').reset_index()
                    
                    temp8 = pd.concat([agg_sectors, total_row]).copy().reset_index(drop = True)

                    groundup_df = pd.concat([groundup_df, temp8]).copy().reset_index(drop = True)

            # Now add in the one subfuel: hydrogen for relevant sector aggregations
            hydrogen_rows = economy_df[economy_df['subfuels'] == '16_x_hydrogen'].copy().reset_index(drop = True)

            hyd_sub3 = hydrogen_rows.copy()
            for i in hyd_sub3.index:       
                hyd_sub3.loc[i, 'sub3sectors'] = 'x'
            
            hyd_sub2 = hyd_sub3.copy()
            for j in hyd_sub2.index:
                hyd_sub2.loc[j, 'sub2sectors'] = 'x'

            hyd_sub1 = hyd_sub2.copy()
            for z in hyd_sub1.index:
                hyd_sub1.loc[z, 'sub1sectors'] = 'x'

            hyd_df = pd.concat([hydrogen_rows, hyd_sub3, hyd_sub2, hyd_sub1]).copy().drop_duplicates()

            groundup_df = pd.concat([groundup_df, hyd_df]).copy()\
                .sort_values(['sectors', 'sub1sectors', 'sub2sectors', 'sub3sectors', 'fuels']).reset_index(drop = True)
            
            groundup_df = groundup_df[['scenarios', 'economy', 'sectors', 'sub1sectors', 'sub2sectors', 'sub3sectors',
                                'sub4sectors', 'fuels', 'subfuels'] + all_years_str].copy()
            
            groundup_df.to_csv(save_location + economy + '_industry_interim_' + file + '.csv', index = False)
        
    else:
        pass
