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
# Just choose one economy
# economy_select = economy_select[17:18]

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
    save_location = './results/industry/4_consolidation/{}/'.format(economy)

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

###############################################################################################################################

# CCS charts
steel_sub3 = ['14_03_01_01_fs', '14_03_01_03_ccs']
chem_sub3 = ['14_03_02_01_fs', '14_03_02_02_ccs']
cement_sub3 = ['14_03_04_01_ccs', '14_03_04_02_nonccs']
id = ['scenarios', 'economy', 'sectors', 'sub1sectors',	'sub2sectors', 'sub3sectors', 'sub4sectors', 'fuels', 'subfuels']

# Now read in all data for each economy
for economy in list(economy_select):
    chart_save = './results/industry/3_fuel_switch/{}/ccs_charts/'.format(economy)

    if not os.path.isdir(chart_save):
        os.makedirs(chart_save)

    file_location = './results/industry/4_consolidation/{}/'.format(economy)

    interim_files = glob.glob(file_location + '*interim*.csv')

    ref_file = [item for item in interim_files if 'ref' in item]
    tgt_file = [item for item in interim_files if 'tgt' in item]

    if len(ref_file) + len(tgt_file) == 2:
        ccs_files = {'ref': ref_file[0],
                     'tgt': tgt_file[0]}
        
        ccs_ref = pd.read_csv(ccs_files['ref'])
        ccs_tgt = pd.read_csv(ccs_files['tgt'])

        # Steel
        if steel_sub3[1] in ccs_ref['sub3sectors'].unique():
            steel_ref = ccs_ref[(ccs_ref['sub3sectors'].isin(steel_sub3)) &
                                (ccs_ref['fuels'] == '19_total')].copy().reset_index(drop = True)
        
        else:
            steel_ref = ccs_ref[(ccs_ref['sub2sectors'] == '14_03_01_iron_and_steel') &
                                (ccs_ref['fuels'] == '19_total')].copy().reset_index(drop = True)

        if steel_sub3[1] in ccs_tgt['sub3sectors'].unique():
            steel_tgt = ccs_tgt[(ccs_tgt['sub3sectors'].isin(steel_sub3)) &
                                (ccs_tgt['fuels'] == '19_total')].copy().reset_index(drop = True)
        
        else:
            steel_tgt = ccs_tgt[(ccs_tgt['sub2sectors'] == '14_03_01_iron_and_steel') &
                                (ccs_tgt['fuels'] == '19_total')].copy().reset_index(drop = True)

        # Chemicals
        if chem_sub3[1] in ccs_ref['sub3sectors'].unique():
            chem_ref = ccs_ref[(ccs_ref['sub3sectors'].isin(chem_sub3)) &
                                (ccs_ref['fuels'] == '19_total')].copy().reset_index(drop = True)
        
        else:
            chem_ref = ccs_ref[(ccs_ref['sub2sectors'] == '14_03_02_chemical_incl_petrochemical') &
                               (ccs_ref['fuels'] == '19_total')].copy().reset_index(drop = True)

        if chem_sub3[1] in ccs_tgt['sub3sectors'].unique():
            chem_tgt = ccs_tgt[(ccs_tgt['sub3sectors'].isin(chem_sub3)) &
                                (ccs_tgt['fuels'] == '19_total')].copy().reset_index(drop = True)
        
        else:
            chem_tgt = ccs_tgt[(ccs_tgt['sub2sectors'] == '14_03_02_chemical_incl_petrochemical') &
                               (ccs_tgt['fuels'] == '19_total')].copy().reset_index(drop = True)

        # Cement
        if cement_sub3[0] in ccs_ref['sub3sectors'].unique():
            cement_ref = ccs_ref[(ccs_ref['sub3sectors'].isin(cement_sub3)) &
                                (ccs_ref['fuels'] == '19_total')].copy().reset_index(drop = True)
        
        else:
            cement_ref = ccs_ref[(ccs_ref['sub2sectors'] == '14_03_04_nonmetallic_mineral_products') &
                                 (ccs_ref['fuels'] == '19_total')].copy().reset_index(drop = True)

        if cement_sub3[0] in ccs_tgt['sub3sectors'].unique():
            cement_tgt = ccs_tgt[(ccs_tgt['sub3sectors'].isin(cement_sub3)) &
                                (ccs_tgt['fuels'] == '19_total')].copy().reset_index(drop = True)
        
        else:
            cement_tgt = ccs_tgt[(ccs_tgt['sub2sectors'] == '14_03_04_nonmetallic_mineral_products') &
                                 (ccs_tgt['fuels'] == '19_total')].copy().reset_index(drop = True)

        steel_ref = steel_ref.melt(id_vars = id, var_name = 'year')[['sub3sectors', 'year', 'value']].copy().reset_index(drop = True)
        steel_ref = steel_ref.astype({'year': 'int'})
        steel_ref = steel_ref[(steel_ref['year'] <= 2070) & (steel_ref['year'] >= 2020)]

        steel_tgt = steel_tgt.melt(id_vars = id, var_name = 'year')[['sub3sectors', 'year', 'value']].copy().reset_index(drop = True)
        steel_tgt = steel_tgt.astype({'year': 'int'})
        steel_tgt = steel_tgt[(steel_tgt['year'] <= 2070) & (steel_tgt['year'] >= 2020)]

        chem_ref = chem_ref.melt(id_vars = id, var_name = 'year')[['sub3sectors', 'year', 'value']].copy().reset_index(drop = True)
        chem_ref = chem_ref.astype({'year': 'int'})
        chem_ref = chem_ref[(chem_ref['year'] <= 2070) & (chem_ref['year'] >= 2020)]

        chem_tgt = chem_tgt.melt(id_vars = id, var_name = 'year')[['sub3sectors', 'year', 'value']].copy().reset_index(drop = True)
        chem_tgt = chem_tgt.astype({'year': 'int'})
        chem_tgt = chem_tgt[(chem_tgt['year'] <= 2070) & (chem_tgt['year'] >= 2020)]

        cement_ref = cement_ref.melt(id_vars = id, var_name = 'year')[['sub3sectors', 'year', 'value']].copy().reset_index(drop = True)
        cement_ref = cement_ref.astype({'year': 'int'})
        cement_ref = cement_ref[(cement_ref['year'] <= 2070) & (cement_ref['year'] >= 2020)] 

        cement_tgt = cement_tgt.melt(id_vars = id, var_name = 'year')[['sub3sectors', 'year', 'value']].copy().reset_index(drop = True)
        cement_tgt = cement_tgt.astype({'year': 'int'})
        cement_tgt = cement_tgt[(cement_tgt['year'] <= 2070) & (cement_tgt['year'] >= 2020)]    

        # Change steel variable names 
        steel_ref.replace({'14_03_01_01_fs': 'Non-CCS capacity',
                           '14_03_01_03_ccs': 'CCS capacity',
                           'x': 'Non-CCS capacity'}, inplace = True)
        steel_tgt.replace({'14_03_01_01_fs': 'Non-CCS capacity',
                           '14_03_01_03_ccs': 'CCS capacity',
                           'x': 'Non-CCS capacity'}, inplace = True)
        
        chem_ref.replace({'14_03_02_01_fs': 'Non-CCS capacity',
                           '14_03_02_02_ccs': 'CCS capacity',
                           'x': 'Non-CCS capacity'}, inplace = True)
        chem_tgt.replace({'14_03_02_01_fs': 'Non-CCS capacity',
                           '14_03_02_02_ccs': 'CCS capacity',
                           'x': 'Non-CCS capacity'}, inplace = True)
        
        cement_ref.replace({'14_03_04_02_nonccs': 'Non-CCS capacity',
                           '14_03_04_01_ccs': 'CCS capacity',
                           'x': 'Non-CCS capacity'}, inplace = True)
        cement_tgt.replace({'14_03_04_02_nonccs': 'Non-CCS capacity',
                           '14_03_04_01_ccs': 'CCS capacity',
                           'x': 'Non-CCS capacity'}, inplace = True)

        max_steel = 1.1 * np.nanmax([steel_ref.groupby('year')['value'].sum().max(), steel_tgt.groupby('year')['value'].sum().max()])
        max_chem = 1.1 * np.nanmax([chem_ref.groupby('year')['value'].sum().max(), chem_tgt.groupby('year')['value'].sum().max()])
        max_cement = 1.1 * np.nanmax([cement_ref.groupby('year')['value'].sum().max(), cement_tgt.groupby('year')['value'].sum().max()])

        steel_ref = steel_ref.pivot(columns = ['sub3sectors'], index = 'year', values = 'value').reset_index()
        steel_tgt = steel_tgt.pivot(columns = ['sub3sectors'], index = 'year', values = 'value').reset_index()

        chem_ref = chem_ref.pivot(columns = ['sub3sectors'], index = 'year', values = 'value').reset_index()
        chem_tgt = chem_tgt.pivot(columns = ['sub3sectors'], index = 'year', values = 'value').reset_index()

        cement_ref = cement_ref.pivot(columns = ['sub3sectors'], index = 'year', values = 'value').reset_index()
        cement_tgt = cement_tgt.pivot(columns = ['sub3sectors'], index = 'year', values = 'value').reset_index()

        fig, axs = plt.subplots(3, 2, figsize = (8, 8))

        sns.set_theme(style = 'ticks')

        steel_ref.plot(kind = 'bar', x = 'year', stacked = True, ax = axs[0, 0], color = fuel_palette_CCS, 
                       linewidth = 0, width = 0.7)

        axs[0, 0].set(title = economy + ' steel consumption REF',
            xlabel = 'Year',
            ylabel = 'Energy (PJ)',
            ylim = (0, max_steel))
        
        axs[0, 0].legend(title = '', fontsize = 8)

        steel_tgt.plot(kind = 'bar', x = 'year', stacked = True, ax = axs[0, 1], color = fuel_palette_CCS, 
                       linewidth = 0, width = 0.7)

        axs[0, 1].set(title = economy + ' steel consumption TGT',
            xlabel = 'Year',
            ylabel = 'Energy (PJ)',
            ylim = (0, max_steel))
        
        axs[0, 1].legend(title = '', fontsize = 8)

        chem_ref.plot(kind = 'bar', x = 'year', stacked = True, ax = axs[1, 0], color = fuel_palette_CCS, 
                      linewidth = 0, width = 0.7)

        axs[1, 0].set(title = economy + ' chemicals consumption REF',
            xlabel = 'Year',
            ylabel = 'Energy (PJ)',
            ylim = (0, max_chem))
        
        axs[1, 0].legend(title = '', fontsize = 8)
    
        chem_tgt.plot(kind = 'bar', x = 'year', stacked = True, ax = axs[1, 1], color = fuel_palette_CCS, 
                      linewidth = 0, width = 0.7)

        axs[1, 1].set(title = economy + ' chemicals consumption TGT',
            xlabel = 'Year',
            ylabel = 'Energy (PJ)',
            ylim = (0, max_chem))
        
        axs[1, 1].legend(title = '', fontsize = 8)

        cement_ref.plot(kind = 'bar', x = 'year', stacked = True, ax = axs[2, 0], color = fuel_palette_CCS, 
                        linewidth = 0, width = 0.7)

        axs[2, 0].set(title = economy + ' cement consumption REF',
            xlabel = 'Year',
            ylabel = 'Energy (PJ)',
            ylim = (0, max_cement))
        
        axs[2, 0].legend(title = '', fontsize = 8)
    

        cement_tgt.plot(kind = 'bar', x = 'year', stacked = True, ax = axs[2, 1], color = fuel_palette_CCS, 
                        linewidth = 0, width = 0.7)

        axs[2, 1].set(title = economy + ' cement consumption TGT',
            xlabel = 'Year',
            ylabel = 'Energy (PJ)',
            ylim = (0, max_cement))
        
        axs[2, 1].legend(title = '', fontsize = 8)

        for axis_to_change in [axs[0, 0], axs[0, 1], axs[1, 0], axs[1, 1], axs[2, 0], axs[2, 1]]:
            axis_to_change.xaxis.set_tick_params(rotation = 0)
            xticks = axis_to_change.xaxis.get_major_ticks()
            for i, tick in enumerate(xticks):
                if i % 10 != 0:
                    tick.label1.set_visible(False)
                
        plt.tight_layout()
        plt.savefig(chart_save + economy + '_ccs_results.png')
        plt.show()
        plt.close()