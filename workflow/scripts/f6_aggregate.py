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

        groundup_df.to_csv(save_location + economy + '_industry_ref_' + timestamp + '.csv', index = False)
    
    else:
        pass

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

        groundup_df.to_csv(save_location + economy + '_industry_tgt_' + timestamp + '.csv', index = False)

    else:
        pass
    