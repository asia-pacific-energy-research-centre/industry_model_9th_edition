# Aggregate and disaggregate non-energy
import re

wanted_wd = 'industry_model_9th_edition'
os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

# execute config file
config_file = './config/config_apr2023.py'
with open(config_file) as infile:
    exec(infile.read())

# Only use 21 APEC economies (economy_list defined in config file)
economy_select = economy_list[:-7]
economy_select = economy_select[4:5]

# Fuels
egeda_fuels = pd.read_csv('./data/config/EGEDA_fuels.csv', header = 0).squeeze().to_dict()
nonenergy_fuels = list(egeda_fuels.values())
nonenergy_fuels = [nonenergy_fuels[i] for i in [0, 1, 5, 6, 7, 15]]

# Modelled years
proj_years = list(range(2022, 2101, 1))
proj_years_str = [str(i) for i in proj_years]

# All years
all_years = list(range(1980, 2101, 1))
all_years_str = [str(i) for i in all_years]

# Read in steel data
for economy in list(economy_select):
    # Save location for charts and data
    save_location = './results/non_energy/4_final/{}/'.format(economy)

    if not os.path.isdir(save_location):
        os.makedirs(save_location)

    file_location = './results/non_energy/3_fuel_switch/{}/'.format(economy)

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

            fuel_level_df = economy_df[economy_df['subfuels'] == 'x'].copy().reset_index(drop = True)

            total_row = fuel_level_df[fuel_level_df['fuels'].isin(nonenergy_fuels)]\
                        .groupby(['scenarios', 'economy', 'sectors','sub1sectors', 'sub2sectors', 'sub3sectors',
                                'sub4sectors', 'subfuels']).sum()\
                        .assign(fuels = '19_total').reset_index()
            
            groundup_df = pd.concat([economy_df, total_row]).copy().reset_index(drop = True)

            groundup_df = groundup_df[['scenarios', 'economy', 'sectors', 'sub1sectors', 'sub2sectors', 'sub3sectors',
                                'sub4sectors', 'fuels', 'subfuels'] + all_years_str].copy()
            
            groundup_df.to_csv(save_location + economy + '_nonenergy_interim_' + file + '.csv', index = False)

    else:
        pass
