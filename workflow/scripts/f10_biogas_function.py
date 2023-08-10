# Biogas function to switch from gas to biogas
# Set working directory to be the project folder 
import os
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

# All years
all_years = list(range(1980, 2101, 1))
all_years_str = [str(i) for i in all_years]

id = ['scenarios', 'economy', 'sectors', 'sub1sectors',	'sub2sectors', 'sub3sectors', 'sub4sectors', 'fuels', 'subfuels']

def biogas_switch(economy = '01_AUS',
                  biogas_ref = False,
                  biogas_tgt = False,
                  biogas_start_ref = 2025,
                  biogas_start_tgt = 2025,
                  biogas_rate_ref = 0.002,
                  biogas_rate_tgt = 0.005):
    
    data_location = './results/industry/4_final/{}/'.format(economy)

    ref_prefix = economy + '_industry_ref_'
    tgt_prefix = economy + '_industry_tgt_'

    ref_files = glob.glob(data_location + ref_prefix + '*.csv')
    tgt_files = glob.glob(data_location + tgt_prefix + '*.csv')

    if len(ref_files) > 0:
        latest_ref = max(ref_files, key = os.path.getctime)
        ref_date = re.search(r'(\d{4})_(\d{2})_(\d{2})', latest_ref).group(0)

        ref_df = pd.read_csv(latest_ref)

        adjust_ref = pd.DataFrame(index = proj_years)
        adjust_ref['adjust'] = np.nan

        for year in range(biogas_start_ref, proj_years[-1] + 1, 1):
            adjust_ref.loc[year, 'adjust'] = (year - biogas_start_ref) * biogas_rate_ref
            adjust_ref = adjust_ref.fillna(0)

        relevant_sectors = np.delete(ref_df['sub3sectors'].unique(),
                                     np.where(ref_df['sub3sectors'].unique() == 'x'))

        new_sector_df = pd.DataFrame(columns = ref_df.columns)

        # Start at lowest sector level
        for sector in relevant_sectors:
            gas_data = ref_df[(ref_df['sub3sectors'] == sector) &
                              (ref_df['subfuels'] == '08_01_natural_gas')].copy().reset_index(drop = True)
            
            biogas_data = ref_df[(ref_df['sub3sectors'] == sector) &
                              (ref_df['subfuels'] == '16_01_biogas')].copy().reset_index(drop = True)
            
            gas_fuel = ref_df[(ref_df['sub3sectors'] == sector) &
                              (ref_df['fuels'] == '08_gas') &
                              (ref_df['subfuels'] == 'x')].copy().reset_index(drop = True)
            
            others_fuel = ref_df[(ref_df['sub3sectors'] == sector) &
                              (ref_df['fuels'] == '16_others') &
                              (ref_df['subfuels'] == 'x')].copy().reset_index(drop = True)
            
            subset_frames = [gas_data, biogas_data, gas_fuel, others_fuel]
            subset_data = pd.concat(subset_frames, ignore_index = True).copy().reset_index(drop = True)            

            filtered_data = ref_df.merge(subset_data, on = id + all_years_str, how = 'left', indicator = True)
            filtered_data = filtered_data[filtered_data['_merge'] == 'left_only']

            filtered_data = filtered_data.drop('_merge', axis = 1)

            adjust_ref['amount'] = np.nan
            
            new_gas = gas_data.copy()
            new_biogas = biogas_data.copy()
            new_gas_fuel = gas_fuel.copy()
            new_others_fuel = others_fuel.copy()

            for year in adjust_ref.index:
                adjust_ref.loc[year, 'amount'] = gas_data.loc[0, str(year)] * adjust_ref.loc[year, 'adjust']

                new_gas.loc[0, str(year)] = gas_data.loc[0, str(year)] - adjust_ref.loc[year, 'amount']
                new_biogas.loc[0, str(year)] = biogas_data.loc[0, str(year)] + adjust_ref.loc[year, 'amount']

                new_gas_fuel.loc[0, str(year)] = gas_fuel.loc[0, str(year)] - adjust_ref.loc[year, 'amount']
                if others_fuel.empty:
                    new_others_fuel = new_biogas.copy()
                    new_others_fuel['subfuels'] = 'x'
                else:
                    new_others_fuel.loc[0, str(year)] = others_fuel.loc[0, str(year)] + adjust_ref.loc[year, 'amount']
            
            new_sector_df = pd.concat([new_sector_df, filtered_data, new_gas, new_biogas, new_gas_fuel, new_others_fuel]).copy().reset_index(drop = True)

        new_sector_df.to_csv('test.csv', index = False)

    else:
        pass

    if len(tgt_files) > 0:
        latest_tgt = max(tgt_files, key = os.path.getctime)
        tgt_date = re.search(r'(\d{4})_(\d{2})_(\d{2})', latest_tgt).group(0)

        tgt_df = pd.read_csv(latest_tgt)


        # for year in range(biogas_start_tgt, proj_years[-1] + 1, 1):
        #     adjust_tgt.loc[year, 'adjust'] = (year - biogas_start_tgt) * biogas_rate_tgt
        #     adjust_tgt = adjust_tgt.fillna(0)

    else:
        pass



