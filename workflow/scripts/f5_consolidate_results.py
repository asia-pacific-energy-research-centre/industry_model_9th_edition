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

# Modelled years
proj_years = list(range(2021, 2101, 1))

# Read in steel data
for economy in [list(economy_select)[-3]]:
    file_location = './results/industry/3_fuel_switch/{}/'.format(economy)

    adj_location = file_location + 'adjustment/'

    if not os.path.isdir(adj_location):
        os.makedirs(adj_location)

    steel_files = glob.glob(file_location + '*steel*.csv')

    ref_steel = [s for s in steel_files if 'ref.csv' in s]
    tgt_steel = [s for s in steel_files if 'tgt.csv' in s]

    if len(ref_steel) == 1:
        steel_df_ref = pd.read_csv(ref_steel[0])

        adjust_df = steel_df_ref[steel_df_ref['subfuels'] == '16_x_hydrogen']
        adjust_df['subfuels'] = 'x'

        steel_df_ref = steel_df_ref.merge(adjust_df, how = 'outer',
                                          on = ['scenarios', 'economy', 'sectors', 'sub1sectors', 
                                                'sub2sectors', 'fuels', 'subfuels', 'year']).reset_index(drop = True)
        
        steel_df_ref['energy'] = steel_df_ref['energy_x'].fillna(0) + steel_df_ref['energy_y'].fillna(0)        
        steel_df_ref = steel_df_ref.drop(['energy_x', 'energy_y'], axis = 1).reset_index(drop = True)

        steel_df_ref.to_csv(adj_location + economy + '_14_03_01_iron_and_steel_ref.csv', index = False)

    else:
        pass

    if len(tgt_steel) == 1:
        steel_df_tgt = pd.read_csv(tgt_steel[0])

        adjust_df = steel_df_tgt[steel_df_tgt['subfuels'] == '16_x_hydrogen']
        adjust_df['subfuels'] = 'x'

        steel_df_tgt = steel_df_tgt.merge(adjust_df, how = 'outer',
                                          on = ['scenarios', 'economy', 'sectors', 'sub1sectors', 
                                                'sub2sectors', 'fuels', 'subfuels', 'year']).reset_index(drop = True)
        
        steel_df_tgt['energy'] = steel_df_tgt['energy_x'].fillna(0) + steel_df_tgt['energy_y'].fillna(0)        
        steel_df_tgt = steel_df_tgt.drop(['energy_x', 'energy_y'], axis = 1).reset_index(drop = True)

        steel_df_tgt.to_csv(adj_location + economy + '_14_03_01_iron_and_steel_tgt.csv', index = False)

    else:
        pass

    # CCS adjustment
    chem_files_ref = glob.glob(file_location + '*chemical*ref.csv')
    cement_files_ref = glob.glob(file_location + '*nonmetallic*ref.csv')
    chem_files_tgt = glob.glob(file_location + '*chemical*tgt.csv')
    cement_files_tgt = glob.glob(file_location + '*nonmetallic*tgt.csv')

    for file in chem_files_ref:
        chem_ref = pd.read_csv(file)
        chem_ref.to_csv(adj_location + economy + '_14_03_02_chemical_incl_petrochemical_ref.csv', index = False)

    for file in cement_files_ref:
        cem_ref = pd.read_csv(file)
        cem_ref.to_csv(adj_location + economy + '_14_03_04_nonmetallic_mineral_products_ref.csv', index = False)

    for file in chem_files_tgt:
        chem_tgt = pd.read_csv(file)
        chem_tgt.to_csv(adj_location + economy + '_14_03_02_chemical_incl_petrochemical_tgt.csv', index = False)

    for file in cement_files_tgt:
        cem_tgt = pd.read_csv(file)
        cem_tgt.to_csv(adj_location + economy + '_14_03_04_nonmetallic_mineral_products_tgt.csv', index = False)

    # CCS files for adjutsment
    CCS_files = glob.glob(file_location + 'hydrogen_ccs/' + '*_ccs_*')

    ccs_steel_ref = [s for s in CCS_files if 'steel_ccs_ref' in s]
    ccs_steel_tgt = [s for s in CCS_files if 'steel_ccs_tgt' in s]
    ccs_chem_ref = [s for s in CCS_files if 'chemical_ccs_ref' in s]
    ccs_chem_tgt = [s for s in CCS_files if 'chemical_ccs_tgt' in s]
    ccs_cem_ref = [s for s in CCS_files if 'products_ccs_ref' in s]
    ccs_cem_tgt = [s for s in CCS_files if 'products_ccs_tgt' in s]

    # Adjust for CCS
    # Steel REF
    if len(ccs_steel_ref) == 1:
        adj_df = pd.read_csv(ccs_steel_ref[0])
        steel_df_ref = steel_df_ref.merge(adj_df, how = 'outer',
                                          on = ['scenarios', 'economy', 'sectors', 'sub1sectors', 
                                                'sub2sectors', 'fuels', 'subfuels', 'year']).reset_index(drop = True)
        
        steel_df_ref['energy'] = steel_df_ref['energy_x'].fillna(0) - steel_df_ref['energy_y'].fillna(0)        
        steel_df_ref = steel_df_ref.drop(['energy_x', 'energy_y'], axis = 1).reset_index(drop = True)

        steel_df_ref['sub3sectors'] = '14_03_01_01_fs'

        steel_df_ref = pd.concat([steel_df_ref, adj_df]).copy().reset_index(drop = True)

        steel_df_ref.to_csv(adj_location + economy + '_14_03_01_iron_and_steel_ref.csv', index = False)

    else:
        pass

    # Steel TGT
    if len(ccs_steel_tgt) == 1:
        adj_df = pd.read_csv(ccs_steel_tgt[0])
        steel_df_tgt = steel_df_tgt.merge(adj_df, how = 'outer',
                                          on = ['scenarios', 'economy', 'sectors', 'sub1sectors', 
                                                'sub2sectors', 'fuels', 'subfuels', 'year']).reset_index(drop = True)
        
        steel_df_tgt['energy'] = steel_df_tgt['energy_x'].fillna(0) - steel_df_tgt['energy_y'].fillna(0)        
        steel_df_tgt = steel_df_tgt.drop(['energy_x', 'energy_y'], axis = 1).reset_index(drop = True)

        steel_df_tgt['sub3sectors'] = '14_03_01_01_fs'

        steel_df_tgt = pd.concat([steel_df_tgt, adj_df]).copy().reset_index(drop = True)

        steel_df_tgt.to_csv(adj_location + economy + '_14_03_01_iron_and_steel_tgt.csv', index = False)

    else:
        pass

    # Chemicals REF
    if len(ccs_chem_ref) == 1:
        adj_df = pd.read_csv(ccs_chem_ref[0])
        chem_ref = chem_ref.merge(adj_df, how = 'outer',
                                          on = ['scenarios', 'economy', 'sectors', 'sub1sectors', 
                                                'sub2sectors', 'fuels', 'subfuels', 'year']).reset_index(drop = True)
        
        chem_ref['energy'] = chem_ref['energy_x'].fillna(0) - chem_ref['energy_y'].fillna(0)        
        chem_ref = chem_ref.drop(['energy_x', 'energy_y'], axis = 1).reset_index(drop = True)

        chem_ref['sub3sectors'] = '14_03_02_01_fs'

        chem_ref = pd.concat([chem_ref, adj_df]).copy().reset_index(drop = True)

        chem_ref.to_csv(adj_location + economy + '_14_03_02_chemical_incl_petrochemical_ref.csv', index = False)

    else:
        pass

    # Chemicals TGT
    if len(ccs_chem_tgt) == 1:
        adj_df = pd.read_csv(ccs_chem_tgt[0])
        chem_tgt = chem_tgt.merge(adj_df, how = 'outer',
                                          on = ['scenarios', 'economy', 'sectors', 'sub1sectors', 
                                                'sub2sectors', 'fuels', 'subfuels', 'year']).reset_index(drop = True)
        
        chem_tgt['energy'] = chem_tgt['energy_x'].fillna(0) - chem_tgt['energy_y'].fillna(0)        
        chem_tgt = chem_tgt.drop(['energy_x', 'energy_y'], axis = 1).reset_index(drop = True)

        chem_tgt['sub3sectors'] = '14_03_02_01_fs'

        chem_tgt = pd.concat([chem_tgt, adj_df]).copy().reset_index(drop = True)

        chem_tgt.to_csv(adj_location + economy + '_14_03_02_chemical_incl_petrochemical_tgt.csv', index = False)

    else:
        pass

    # Cement REF
    if len(ccs_cem_ref) == 1:
        adj_df = pd.read_csv(ccs_cem_ref[0])
        cem_ref = cem_ref.merge(adj_df, how = 'outer',
                                          on = ['scenarios', 'economy', 'sectors', 'sub1sectors', 
                                                'sub2sectors', 'fuels', 'subfuels', 'year']).reset_index(drop = True)
        
        cem_ref['energy'] = cem_ref['energy_x'].fillna(0) - cem_ref['energy_y'].fillna(0)        
        cem_ref = cem_ref.drop(['energy_x', 'energy_y'], axis = 1).reset_index(drop = True)

        cem_ref['sub3sectors'] = '14_03_02_01_fs'

        cem_ref = pd.concat([cem_ref, adj_df]).copy().reset_index(drop = True)

        cem_ref.to_csv(adj_location + economy + '_14_03_04_nonmetallic_mineral_products_ref.csv', index = False)

    else:
        pass

    # Cement TGT
    if len(ccs_cem_tgt) == 1:
        adj_df = pd.read_csv(ccs_cem_tgt[0])
        cem_tgt = cem_tgt.merge(adj_df, how = 'outer',
                                          on = ['scenarios', 'economy', 'sectors', 'sub1sectors', 
                                                'sub2sectors', 'fuels', 'subfuels', 'year']).reset_index(drop = True)
        
        cem_tgt['energy'] = cem_tgt['energy_x'].fillna(0) - cem_tgt['energy_y'].fillna(0)        
        cem_tgt = cem_tgt.drop(['energy_x', 'energy_y'], axis = 1).reset_index(drop = True)

        cem_tgt['sub3sectors'] = '14_03_04_02_nonccs'

        cem_tgt = pd.concat([cem_tgt, adj_df]).copy().reset_index(drop = True)

        cem_tgt.to_csv(adj_location + economy + '_14_03_04_nonmetallic_mineral_products_tgt.csv', index = False)

    else:
        pass
    
    adjusted_files = glob.glob(adj_location + '*.csv')

    other_files = glob.glob(file_location + '*.csv') 
    other_files = [x for x in other_files if ('14_03_01' not in x) & ('14_03_02' not in x) & ('14_03_04' not in x)]
    
    all_files = adjusted_files + other_files

    files_ref = [x for x in all_files if '_ref' in x]
    files_tgt = [x for x in all_files if '_tgt' in x]

    #######################################################
    # REF
    industry_ref = pd.DataFrame()

    for file in files_ref:
        temp_df = pd.read_csv(file)
        industry_ref = pd.concat([industry_ref, temp_df]).copy().reset_index(drop = True)

    if 'sub3sectors' in industry_ref.columns:
        pass

    else:
        industry_ref['sub3sectors'] = np.nan

    industry_ref['sub3sectors'] = np.where(industry_ref['sub3sectors'].isna(), 'x', industry_ref['sub3sectors'])

    industry_ref = industry_ref[['scenarios', 'economy', 'sectors', 'sub1sectors', 
                                 'sub2sectors', 'sub3sectors', 'fuels', 'subfuels', 'year', 'energy']].copy()\
                                    .sort_values(['sectors', 'sub1sectors', 'sub2sectors', 
                                                  'sub3sectors', 'fuels', 'year']).reset_index(drop = True)
    
    industry_ref.to_csv(file_location + 'all_sectors/' + economy + '_industry_long_ref.csv', index = False)

    industry_ref_wide = industry_ref.pivot_table(index = ['scenarios', 'economy', 'sectors', 'sub1sectors', 
                                                         'sub2sectors', 'sub3sectors', 'fuels', 'subfuels'], 
                                                values = 'energy', 
                                                columns = 'year').reset_index()
    
    industry_ref_wide.to_csv(file_location + 'all_sectors/' + economy + '_industry_wide_ref.csv', index = False)
    
    #########################################################
    # TGT
    industry_tgt = pd.DataFrame()

    for file in files_tgt:
        temp_df = pd.read_csv(file)
        industry_tgt = pd.concat([industry_tgt, temp_df]).copy().reset_index(drop = True)

    if 'sub3sectors' in industry_tgt.columns:
        pass

    else:
        industry_tgt['sub3sectors'] = np.nan
        
    industry_tgt['sub3sectors'] = np.where(industry_tgt['sub3sectors'].isna(), 'x', industry_tgt['sub3sectors'])

    industry_tgt = industry_tgt[['scenarios', 'economy', 'sectors', 'sub1sectors', 
                                 'sub2sectors', 'sub3sectors', 'fuels', 'subfuels', 'year', 'energy']].copy()\
                                    .sort_values(['sectors', 'sub1sectors', 'sub2sectors', 
                                                  'sub3sectors', 'fuels', 'year']).reset_index(drop = True)
    
    industry_tgt.to_csv(file_location + 'all_sectors/' + economy + '_industry_long_tgt.csv', index = False)

    industry_tgt_wide = industry_tgt.pivot_table(index = ['scenarios', 'economy', 'sectors', 'sub1sectors', 
                                                         'sub2sectors', 'sub3sectors', 'fuels', 'subfuels'], 
                                                values = 'energy', 
                                                columns = 'year').reset_index()
    
    industry_tgt_wide.to_csv(file_location + 'all_sectors/' + economy + '_industry_wide_tgt.csv', index = False)