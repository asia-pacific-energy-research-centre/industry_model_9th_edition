# Consolidate results ready for integration
import re

wanted_wd = 'industry_model_9th_edition'
os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

# execute config file
config_file = './config/config_apr2023.py'
with open(config_file) as infile:
    exec(infile.read())

# Energy industry subsectors
industry_sectors = pd.read_csv('./data/EGEDA/industry_egeda.csv', header = None)\
    .squeeze().to_dict()

ind1 = list(industry_sectors.values())[:3]
ind2 = list(industry_sectors.values())[3:]

# Only use 21 APEC economies (economy_list defined in config file)
economy_select = economy_list[:-7]
# economy_select = economy_select[0:1]

# Modelled years
proj_years = list(range(2022, 2101, 1))

# Read in steel data
for economy in list(economy_select):
    file_location = './results/industry/3_fuel_switch/{}/'.format(economy)

    adj_location = file_location + 'adjustment/'

    if not os.path.isdir(adj_location):
        os.makedirs(adj_location)

    steel_files = glob.glob(file_location + '*steel*.csv')
    chem_files = glob.glob(file_location + '*chemical*.csv')
    cement_files = glob.glob(file_location + '*nonmetallic*.csv')  

    for scenario in ['ref', 'tgt']:

        steel_file = [s for s in steel_files if scenario + '.csv' in s]
        chem_file = [s for s in chem_files if scenario + '.csv' in s]
        cem_file = [s for s in cement_files if scenario + '.csv' in s]

        if len(steel_file) == 1:
            steel_df = pd.read_csv(steel_file[0])

            adjust_df = steel_df[steel_df['subfuels'] == '16_x_hydrogen']
            adjust_df['subfuels'] = 'x'

            steel_df = steel_df.merge(adjust_df, how = 'outer',
                                            on = ['scenarios', 'economy', 'sectors', 'sub1sectors', 
                                                    'sub2sectors', 'fuels', 'subfuels', 'year']).reset_index(drop = True)
            
            steel_df['energy'] = steel_df['energy_x'].fillna(0) + steel_df['energy_y'].fillna(0)        
            steel_df = steel_df.drop(['energy_x', 'energy_y'], axis = 1).reset_index(drop = True)

            steel_df.to_csv(adj_location + economy + '_14_03_01_iron_and_steel_' + scenario + '.csv', index = False)

        else:
            pass

        if len(chem_file) == 1:    
            chem_df = pd.read_csv(chem_file[0])

            adjust_df = chem_df[chem_df['subfuels'] == '16_x_hydrogen']
            adjust_df['subfuels'] = 'x'

            chem_df = chem_df.merge(adjust_df, how = 'outer',
                                            on = ['scenarios', 'economy', 'sectors', 'sub1sectors', 
                                                  'sub2sectors', 'fuels', 'subfuels', 'year']).reset_index(drop = True)
            
            chem_df['energy'] = chem_df['energy_x'].fillna(0) + chem_df['energy_y'].fillna(0)        
            chem_df = chem_df.drop(['energy_x', 'energy_y'], axis = 1).reset_index(drop = True)

            chem_df.to_csv(adj_location + economy + '_14_03_02_chemical_incl_petrochemical_' + scenario + '.csv', index = False)
        else:
            pass

        if len(cem_file) == 1:    
            cement_df = pd.read_csv(cem_file[0])

            adjust_df = cement_df[cement_df['subfuels'] == '16_x_hydrogen']
            adjust_df['subfuels'] = 'x'

            cement_df = cement_df.merge(adjust_df, how = 'outer',
                                            on = ['scenarios', 'economy', 'sectors', 'sub1sectors', 
                                                  'sub2sectors', 'fuels', 'subfuels', 'year']).reset_index(drop = True)
            
            cement_df['energy'] = cement_df['energy_x'].fillna(0) + cement_df['energy_y'].fillna(0)        
            cement_df = cement_df.drop(['energy_x', 'energy_y'], axis = 1).reset_index(drop = True)

            cement_df.to_csv(adj_location + economy + '_14_03_04_nonmetallic_mineral_products_' + scenario + '.csv', index = False)
        else:
            pass

        # CCS files for adjutsment
        CCS_files = glob.glob(file_location + 'hydrogen_ccs/' + '*_ccs_*')

        ccs_steel = [s for s in CCS_files if 'steel_ccs_' + scenario in s]
        ccs_chem = [s for s in CCS_files if 'chemical_ccs_' + scenario in s]
        ccs_cem = [s for s in CCS_files if 'products_ccs_' + scenario in s]
        
        # Adjust for CCS
        # Steel 
        if len(ccs_steel) == 1:
            adj_df = pd.read_csv(ccs_steel[0])
            steel_df = steel_df.merge(adj_df, how = 'outer',
                                            on = ['scenarios', 'economy', 'sectors', 'sub1sectors', 
                                                    'sub2sectors', 'fuels', 'subfuels', 'year']).reset_index(drop = True)
            
            steel_df['energy'] = steel_df['energy_x'].fillna(0) - steel_df['energy_y'].fillna(0)        
            steel_df = steel_df.drop(['energy_x', 'energy_y'], axis = 1).reset_index(drop = True)

            steel_df['sub3sectors'] = '14_03_01_01_fs'

            steel_df = pd.concat([steel_df, adj_df]).copy().reset_index(drop = True)

            steel_df.to_csv(adj_location + economy + '_14_03_01_iron_and_steel_' + scenario + '.csv', index = False)

        else:
            pass

        # Chemicals 
        if len(ccs_chem) == 1:
            adj_df = pd.read_csv(ccs_chem[0])
            chem_df = chem_df.merge(adj_df, how = 'outer',
                                            on = ['scenarios', 'economy', 'sectors', 'sub1sectors', 
                                                    'sub2sectors', 'fuels', 'subfuels', 'year']).reset_index(drop = True)
            
            chem_df['energy'] = chem_df['energy_x'].fillna(0) - chem_df['energy_y'].fillna(0)        
            chem_df = chem_df.drop(['energy_x', 'energy_y'], axis = 1).reset_index(drop = True)

            chem_df['sub3sectors'] = '14_03_02_01_fs'

            chem_df = pd.concat([chem_df, adj_df]).copy().reset_index(drop = True)

            chem_df.to_csv(adj_location + economy + '_14_03_02_chemical_incl_petrochemical_' + scenario + '.csv', index = False)

        else:
            pass

        # Cement 
        if len(ccs_cem) == 1:
            adj_df = pd.read_csv(ccs_cem[0])
            cement_df = cement_df.merge(adj_df, how = 'outer',
                                            on = ['scenarios', 'economy', 'sectors', 'sub1sectors', 
                                                    'sub2sectors', 'fuels', 'subfuels', 'year']).reset_index(drop = True)
            
            cement_df['energy'] = cement_df['energy_x'].fillna(0) - cement_df['energy_y'].fillna(0)        
            cement_df = cement_df.drop(['energy_x', 'energy_y'], axis = 1).reset_index(drop = True)

            cement_df['sub3sectors'] = '14_03_04_02_nonccs'

            cement_df = pd.concat([cement_df, adj_df]).copy().reset_index(drop = True)

            cement_df.to_csv(adj_location + economy + '_14_03_04_nonmetallic_mineral_products_' + scenario + '.csv', index = False)

        else:
            pass
    
        # Identify the adjusted files to be used instead of the files in the higher folder location
        adjusted_files = glob.glob(adj_location + '*.csv')
        
        # Identify non-adjusted sector files (i.e. no hydrogen or CCS in these sectors)
        other_files = glob.glob(file_location + '*.csv') 
        other_files = [x for x in other_files if ('14_03_01' not in x) & ('14_03_02' not in x) & ('14_03_04' not in x)]
        
        all_files = adjusted_files + other_files

        relevant_files = [x for x in all_files if '_' + scenario in x]

        #######################################################
        industry_df = pd.DataFrame()

        for file in relevant_files:
            temp_df = pd.read_csv(file)
            industry_df = pd.concat([industry_df, temp_df]).copy().reset_index(drop = True)

        if 'sub3sectors' in industry_df.columns:
            pass

        else:
            industry_df['sub3sectors'] = np.nan

        industry_df['sub3sectors'] = np.where(industry_df['sub3sectors'].isna(), 'x', industry_df['sub3sectors'])

        industry_df['sub4sectors'] = 'x'

        if industry_df.empty:
            pass

        else:
            industry_df = industry_df[['scenarios', 'economy', 'sectors', 'sub1sectors', 
                                        'sub2sectors', 'sub3sectors', 'sub4sectors', 'fuels', 'subfuels', 'year', 'energy']].copy()\
                                            .sort_values(['sectors', 'sub1sectors', 'sub2sectors', 
                                                        'sub3sectors', 'fuels', 'year']).reset_index(drop = True)
            
            industry_df.to_csv(file_location + 'all_sectors/' + economy + '_industry_long_' + scenario + '.csv', index = False)

            industry_df_wide = industry_df.pivot_table(index = ['scenarios', 'economy', 'sectors', 'sub1sectors', 
                                                                'sub2sectors', 'sub3sectors', 'sub4sectors', 'fuels', 'subfuels'], 
                                                        values = 'energy', 
                                                        columns = 'year').reset_index()
            
            industry_df_wide.to_csv(file_location + 'all_sectors/' + economy + '_industry_wide_' + scenario + '.csv', index = False)

#################################################################################################

# Non-energy

# Read in non-energy data
for economy in list(economy_select):
    file_location = './results/non_energy/3_fuel_switch/{}/'.format(economy)

    ne_files = glob.glob(file_location + '*.csv')

    ref_ne = [s for s in ne_files if 'switched_ref.csv' in s]
    tgt_ne = [s for s in ne_files if 'switched_tgt.csv' in s]

    if len(ref_ne) + len(tgt_ne) == 2:
        both_files = {'ref': ref_ne[0],
                      'tgt': tgt_ne[0]}
        
        # Consolidate
        for file in both_files.keys():
            non_energy_df = pd.read_csv(both_files[file])

            non_energy_df['sub2sectors'] = 'x'
            non_energy_df['sub3sectors'] = 'x'
            non_energy_df['sub4sectors'] = 'x'

            non_energy_df = non_energy_df[['scenarios', 'economy', 'sectors', 'sub1sectors', 
                                            'sub2sectors', 'sub3sectors', 'sub4sectors', 'fuels', 'subfuels', 'year', 'energy']].copy()\
                                                .reset_index(drop = True)
            
            non_energy_df.to_csv(file_location + economy + '_non_energy_long_' + file + '.csv', index = False)

            non_energy_wide = non_energy_df.pivot_table(index = ['scenarios', 'economy', 'sectors', 'sub1sectors', 
                                                                'sub2sectors', 'sub3sectors', 'sub4sectors', 'fuels', 'subfuels'], 
                                                            values = 'energy', 
                                                            columns = 'year').reset_index()
            
            non_energy_wide.to_csv(file_location + economy + '_non_energy_wide_' + file + '.csv', index = False)

    else:
        pass